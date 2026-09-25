#!/usr/bin/env bun
// Self-contained CLI for searching jobs on Gupy (portal.gupy.io).
// No external CLI framework and zero runtime dependencies beyond Bun.

interface Flags {
  _: string[]
  [k: string]: string | boolean | string[]
}

const ALIAS: Record<string, string> = { q: "query", l: "location", n: "limit" }

function parseFlags(argv: string[]): Flags {
  const flags: Flags = { _: [] }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (!a.startsWith("-")) {
      ;(flags._ as string[]).push(a)
      continue
    }
    const name = a.replace(/^-+/, "")
    const key = ALIAS[name] ?? name
    const next = argv[i + 1]
    let value: string | boolean = true
    if (next !== undefined && !next.startsWith("-")) {
      value = next
      i++
    }
    flags[key] = value
  }
  return flags
}

function writeError(error: string, code: string): void {
  process.stderr.write(JSON.stringify({ error, code }) + "\n")
}

function cleanHtml(html: string): string {
  if (!html) return ""
  return html
    .replace(/<br\s*[\/]?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<\/li>/gi, "\n")
    .replace(/<li>/gi, "• ")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

export interface JobResult {
  id: string
  title: string
  company: string | null
  location: string | null
  date: string | null
  url: string
  work_mode: string | null
  description: string | null
}

export interface JobDetailResult extends JobResult {
  employment_type?: string | null
  salary?: string | null
  prerequisites?: string | null
  responsibilities?: string | null
}

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async function fetchGupyHtml(url: string): Promise<string> {
  const res = await fetch(url, {
    headers: {
      "User-Agent": UA,
      Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    },
    redirect: "follow",
    signal: AbortSignal.timeout(15000),
  })
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`)
  }
  return res.text()
}

function extractNextData(html: string): any {
  const match = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/)
  if (!match) return null
  try {
    return JSON.parse(match[1])
  } catch {
    return null
  }
}

function shortDate(date: string | null): string {
  return date ? date.slice(0, 10) : "—"
}

function renderTable(rows: JobResult[]): string {
  if (rows.length === 0) return "No results."
  const columns = [
    { header: "ID", width: 12, cell: (r: JobResult) => r.id },
    { header: "TITLE", width: 40, cell: (r: JobResult) => r.title },
    { header: "COMPANY", width: 22, cell: (r: JobResult) => r.company ?? "—" },
    { header: "LOCATION", width: 20, cell: (r: JobResult) => r.location ?? "—" },
    { header: "MODE", width: 10, cell: (r: JobResult) => r.work_mode ?? "—" },
    { header: "DATE", width: 10, cell: (r: JobResult) => shortDate(r.date) },
  ]
  const formatRow = (cells: string[]) =>
    cells.map((c, i) => c.slice(0, columns[i].width).padEnd(columns[i].width)).join("  ")

  const header = formatRow(columns.map((c) => c.header))
  const body = rows.map((r) => formatRow(columns.map((c) => c.cell(r))))
  return [header, "-".repeat(header.length), ...body].join("\n")
}

function renderPlain(rows: JobResult[]): string {
  if (rows.length === 0) return "No results."
  const block = (r: JobResult) =>
    [
      r.title,
      `  ${r.company ?? "—"} · ${r.location ?? "—"} (${r.work_mode ?? "—"}) · ${shortDate(r.date)}`,
      `  id: ${r.id}`,
      `  ${r.url}`,
    ].join("\n")
  return rows.map(block).join("\n\n")
}

const KNOWN_FLAGS: Record<string, Set<string>> = {
  search: new Set(["query", "location", "page", "limit", "format", "remote", "help", "h"]),
  detail: new Set(["format", "help", "h"]),
}

const HELP = `gupy-cli — search jobs on Gupy (portal.gupy.io)

USAGE
  bun run src/cli.ts search [-q "<termo>"] [-l "<cidade/estado>"] [--remote] [flags]
  bun run src/cli.ts detail <id|url> [--format json|plain]

SEARCH FLAGS
  --query, -q <text>      Keywords (title, skill, role). Optional.
  --location, -l <text>   Location filter (e.g. "São Paulo", "Fortaleza", "Remoto").
  --remote                Shortcut for remote-only positions.
  --page <n>              1-indexed page. Default 1.
  --limit, -n <n>         Cap results emitted. Default 12.
  --format <fmt>          json (default) | table | plain.
`

async function runSearch(flags: Flags): Promise<number> {
  const query = typeof flags.query === "string" ? flags.query.trim() : ""
  const location = typeof flags.location === "string" ? flags.location.trim() : ""
  const isRemote = flags.remote === true || location.toLowerCase() === "remoto" || location.toLowerCase() === "remote"
  const page = Math.max(1, parseInt(String(flags.page || "1"), 10) || 1)
  const limit = Math.max(1, parseInt(String(flags.limit || "12"), 10) || 12)
  const format = (flags.format as string) || "json"

  // Build target URL on portal.gupy.io
  const encodedTerm = encodeURIComponent(query || "vagas")
  let targetUrl = `https://portal.gupy.io/job-search/term=${encodedTerm}`
  const params = new URLSearchParams()
  if (isRemote) {
    params.set("workplaceType", "remote")
  }
  if (location && !isRemote) {
    params.set("city", location)
  }
  const offset = (page - 1) * limit
  if (offset > 0) {
    params.set("offset", String(offset))
  }
  const qs = params.toString()
  if (qs) {
    targetUrl += `?${qs}`
  }

  try {
    const html = await fetchGupyHtml(targetUrl)
    const nextData = extractNextData(html)
    if (!nextData) {
      writeError("could not extract job data from Gupy portal response", "PARSE_ERROR")
      return 1
    }

    const jobList = nextData.props?.pageProps?.initialJobList
    const rawJobs: any[] = jobList?.data ?? []
    let rows: JobResult[] = rawJobs.map((j) => ({
      id: String(j.id),
      title: j.name || "(sem título)",
      company: j.careerPageName || null,
      location: [j.city, j.state].filter(Boolean).join(", ") || (j.workplaceType === "remote" ? "Remoto" : null),
      date: j.publishedDate || null,
      url: j.jobUrl || `https://portal.gupy.io/job/${j.id}`,
      work_mode: j.workplaceType || null,
      description: cleanHtml(j.description || ""),
    }))

    if (flags.limit !== undefined) {
      rows = rows.slice(0, limit)
    }

    const total = jobList?.pagination?.total ?? rows.length

    if (format === "table") {
      process.stdout.write(renderTable(rows) + "\n")
    } else if (format === "plain") {
      process.stdout.write(renderPlain(rows) + "\n")
    } else {
      process.stdout.write(
        JSON.stringify(
          {
            meta: { count: rows.length, page, total },
            results: rows,
          },
          null,
          2,
        ) + "\n",
      )
    }
    return 0
  } catch (e) {
    writeError(e instanceof Error ? e.message : String(e), "SEARCH_FAILED")
    return 1
  }
}

async function runDetail(flags: Flags): Promise<number> {
  const target = (flags._ as string[])[1]
  if (!target) {
    writeError("missing required job ID or URL for detail command", "BAD_ARGS")
    return 1
  }
  const format = (flags.format as string) || "json"

  let fetchUrl = target
  if (!target.startsWith("http")) {
    fetchUrl = `https://portal.gupy.io/job/${encodeURIComponent(target)}`
  }

  try {
    const html = await fetchGupyHtml(fetchUrl)
    const nextData = extractNextData(html)
    if (!nextData) {
      writeError("could not extract job detail from Gupy response", "PARSE_ERROR")
      return 1
    }

    const j = nextData.props?.pageProps?.job
    if (!j) {
      writeError(`job not found at ${fetchUrl}`, "NOT_FOUND")
      return 1
    }

    const result: JobDetailResult = {
      id: String(j.id),
      title: j.name || "(sem título)",
      company: j.careerPageName || nextData.props?.pageProps?.subdomain || null,
      location: [j.city, j.state].filter(Boolean).join(", ") || (j.workplaceType === "remote" ? "Remoto" : null),
      date: j.publishedDate || null,
      url: j.jobUrl || fetchUrl,
      work_mode: j.workplaceType || null,
      employment_type: j.type || null,
      salary: j.salary || null,
      description: cleanHtml(j.description || ""),
      prerequisites: cleanHtml(j.prerequisites || ""),
      responsibilities: cleanHtml(j.responsibilities || ""),
    }

    if (format === "plain") {
      const lines = [
        result.title,
        `${result.company || "—"} · ${result.location || "—"} (${result.work_mode || "—"})`,
        result.date ? `Data: ${shortDate(result.date)}` : "",
        result.employment_type ? `Tipo: ${result.employment_type}` : "",
        result.salary ? `Salário: ${result.salary}` : "",
        "",
        "Descrição:",
        result.description || "(sem descrição)",
      ]
      if (result.responsibilities) {
        lines.push("", "Responsabilidades:", result.responsibilities)
      }
      if (result.prerequisites) {
        lines.push("", "Requisitos:", result.prerequisites)
      }
      lines.push("", `URL: ${result.url}`, `ID: ${result.id}`)
      process.stdout.write(lines.filter((l) => l !== "").join("\n") + "\n")
    } else {
      process.stdout.write(JSON.stringify(result, null, 2) + "\n")
    }
    return 0
  } catch (e) {
    writeError(e instanceof Error ? e.message : String(e), "DETAIL_FAILED")
    return 1
  }
}

async function main(): Promise<number> {
  const argv = process.argv.slice(2)
  const flags = parseFlags(argv)
  const cmd = (flags._ as string[])[0]

  if (!cmd || flags.help || flags.h) {
    process.stdout.write(HELP)
    return cmd ? 0 : 1
  }

  const known = KNOWN_FLAGS[cmd]
  if (known) {
    for (const key of Object.keys(flags)) {
      if (key === "_" || known.has(key)) continue
      writeError(
        `unknown flag --${key} for '${cmd}' - flags are never silently ignored; see --help for supported flags`,
        "UNKNOWN_FLAG",
      )
      return 1
    }
  }

  if (cmd === "search") {
    return runSearch(flags)
  }
  if (cmd === "detail") {
    return runDetail(flags)
  }

  writeError(`unknown command '${cmd}' - supported commands: search, detail`, "UNKNOWN_COMMAND")
  return 1
}

main().then((code) => {
  if (code !== 0) process.exit(code)
})
