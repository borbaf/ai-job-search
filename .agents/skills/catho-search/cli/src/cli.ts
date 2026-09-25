#!/usr/bin/env bun
// Self-contained CLI for searching jobs on Catho (catho.com.br).
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
    .replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
    .replace(/&#([0-9]+);/g, (_, dec) => String.fromCharCode(parseInt(dec, 10)))
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

export interface JobResult {
  id: string
  title: string
  company: string | null
  location: string | null
  salary?: string | null
  date: string | null
  url: string
  work_mode: string | null
  description: string | null
}

export interface JobDetailResult extends JobResult {
  employment_type?: string | null
}

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async function fetchCatho(url: string): Promise<string> {
  const res = await fetch(url, {
    headers: {
      "User-Agent": UA,
      Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    },
    redirect: "follow",
    signal: AbortSignal.timeout(15000),
  })
  if (res.status === 404) return ""
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`)
  }
  return res.text()
}

function shortDate(date: string | null): string {
  return date ? date.slice(0, 10) : "—"
}

function renderTable(rows: JobResult[]): string {
  if (rows.length === 0) return "No results."
  const columns = [
    { header: "ID", width: 10, cell: (r: JobResult) => r.id },
    { header: "TITLE", width: 40, cell: (r: JobResult) => r.title },
    { header: "COMPANY", width: 20, cell: (r: JobResult) => r.company ?? "—" },
    { header: "LOCATION", width: 18, cell: (r: JobResult) => r.location ?? "—" },
    { header: "SALARY", width: 16, cell: (r: JobResult) => r.salary ?? "A Combinar" },
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
      `  ${r.company ?? "—"} · ${r.location ?? "—"} · ${r.salary ?? "A Combinar"}`,
      `  id: ${r.id}`,
      `  ${r.url}`,
    ].join("\n")
  return rows.map(block).join("\n\n")
}

const KNOWN_FLAGS: Record<string, Set<string>> = {
  search: new Set(["query", "location", "page", "limit", "format", "help", "h"]),
  detail: new Set(["format", "help", "h"]),
}

const HELP = `catho-cli — search jobs on Catho (catho.com.br)

USAGE
  bun run src/cli.ts search [-q "<termo>"] [-l "<cidade/estado>"] [flags]
  bun run src/cli.ts detail <id|url> [--format json|plain]

SEARCH FLAGS
  --query, -q <text>      Keywords (title, skill, role). Optional.
  --location, -l <text>   Location filter (city/state).
  --page <n>              1-indexed page. Default 1.
  --limit, -n <n>         Cap results emitted. Default 20.
  --format <fmt>          json (default) | table | plain.
`

function extractJobCards(html: string): JobResult[] {
  const results: JobResult[] = []
  const articles = [...html.matchAll(/<article\b[^>]*>([\s\S]*?)<\/article>/gi)]

  for (const artMatch of articles) {
    const artHtml = artMatch[1]

    // Link and title: <h2 class="title_offer">\s*<a href="(/vagas/[^"]+)"[^>]*>([^<]+)</a>
    const titleMatch = artHtml.match(/<h2[^>]*class="[^"]*title_offer[^"]*"[^>]*>[\s\S]*?<a\s+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/i)
    if (!titleMatch) continue

    const path = titleMatch[1]
    const title = cleanHtml(titleMatch[2])

    // ID is the trailing digits in /vagas/.../(\d+)
    const idMatch = path.match(/\/(\d+)(?:\?|$)/)
    const id = idMatch ? idMatch[1] : path

    // Company: <span class="text-12">([^<]+)</span>
    const compMatch = artHtml.match(/<span[^>]*class="[^"]*text-12[^"]*"[^>]*>([\s\S]*?)<\/span>/i)
    const company = compMatch ? cleanHtml(compMatch[1]) : null

    // Location: <span class="icon i_job_location"></span> ...
    const locMatch = artHtml.match(/<span[^>]*class="[^"]*i_job_location[^"]*"[^>]*><\/span>[\s\S]*?(?:<strong>[^<]*<\/strong>\s*-\s*)?([^<]+)/i)
    const location = locMatch ? cleanHtml(locMatch[1]) : null

    // Salary: <span class="icon i_salary"></span> ... <strong>([^<]+)</strong>
    const salMatch = artHtml.match(/<span[^>]*class="[^"]*i_salary[^"]*"[^>]*><\/span>[\s\S]*?<strong>([^<]+)<\/strong>/i)
    const salary = salMatch ? cleanHtml(salMatch[1]) : null

    const fullUrl = path.startsWith("http") ? path : `https://www.catho.com.br${path}`

    results.push({
      id,
      title,
      company,
      location,
      salary,
      date: null,
      url: fullUrl,
      work_mode: location?.toLowerCase().includes("home office") || title.toLowerCase().includes("home office") ? "remote" : null,
      description: null,
    })
  }

  return results
}

async function runSearch(flags: Flags): Promise<number> {
  const query = typeof flags.query === "string" ? flags.query.trim() : ""
  const location = typeof flags.location === "string" ? flags.location.trim() : ""
  const page = Math.max(1, parseInt(String(flags.page || "1"), 10) || 1)
  const limit = Math.max(1, parseInt(String(flags.limit || "20"), 10) || 20)
  const format = (flags.format as string) || "json"

  const term = query || location || "vagas"
  const cleanTerm = encodeURIComponent(term.toLowerCase().replace(/\s+/g, "-"))
  let url = `https://www.catho.com.br/vagas/${cleanTerm}/?q=${encodeURIComponent(query || term)}`
  if (page > 1) {
    url += `&page=${page}`
  }

  try {
    const html = await fetchCatho(url)
    if (!html) {
      writeError(`search returned empty response from ${url}`, "EMPTY_RESPONSE")
      return 1
    }

    let rows = extractJobCards(html)
    if (flags.limit !== undefined) {
      rows = rows.slice(0, limit)
    }

    if (format === "table") {
      process.stdout.write(renderTable(rows) + "\n")
    } else if (format === "plain") {
      process.stdout.write(renderPlain(rows) + "\n")
    } else {
      process.stdout.write(
        JSON.stringify(
          {
            meta: { count: rows.length, page, total: rows.length },
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
    fetchUrl = `https://www.catho.com.br/vagas/vaga/${encodeURIComponent(target)}`
  }

  try {
    const html = await fetchCatho(fetchUrl)
    if (!html) {
      writeError(`job not found at ${fetchUrl}`, "NOT_FOUND")
      return 1
    }

    let posting: any = null
    const lds = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)].map((m) => m[1])
    for (const ld of lds) {
      try {
        const data = JSON.parse(ld)
        if (data["@type"] === "JobPosting") {
          posting = data
          break
        }
      } catch {}
    }

    if (!posting) {
      writeError(`could not parse JobPosting LD+JSON from ${fetchUrl}`, "PARSE_ERROR")
      return 1
    }

    const idMatch = fetchUrl.match(/\/(\d+)(?:\?|$)/)
    const id = idMatch ? idMatch[1] : target

    const result: JobDetailResult = {
      id,
      title: posting.title || "(sem título)",
      company: posting.hiringOrganization?.name || null,
      location: posting.jobLocation?.address?.addressLocality || null,
      date: posting.datePosted || null,
      url: fetchUrl,
      work_mode: posting.jobLocationType === "TELECOMMUTE" ? "remote" : null,
      employment_type: posting.employmentType || null,
      salary: posting.baseSalary?.value?.value ? `${posting.baseSalary.value.value}` : null,
      description: cleanHtml(posting.description || ""),
    }

    if (format === "plain") {
      const lines = [
        result.title,
        `${result.company || "—"} · ${result.location || "—"}`,
        result.date ? `Data: ${shortDate(result.date)}` : "",
        result.employment_type ? `Tipo: ${result.employment_type}` : "",
        result.salary ? `Salário: ${result.salary}` : "",
        "",
        "Descrição:",
        result.description || "(sem descrição)",
        "",
        `URL: ${result.url}`,
        `ID: ${result.id}`,
      ]
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
