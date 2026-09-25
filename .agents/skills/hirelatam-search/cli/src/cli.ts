#!/usr/bin/env bun
// Self-contained CLI for searching jobs on HireLATAM (hirelatam.com).
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
  date: string | null
  url: string
  work_mode: string | null
  department?: string | null
  description: string | null
}

export interface JobDetailResult extends JobResult {
  employment_type?: string | null
}

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
const WIDGET_URL = "https://recruiterflow.com/hirelatam/jobs-page-widget"

async function fetchWidgetHtml(): Promise<string> {
  const res = await fetch(WIDGET_URL, {
    headers: {
      "User-Agent": UA,
      Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.9",
    },
    signal: AbortSignal.timeout(15000),
  })
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
    { header: "ID", width: 8, cell: (r: JobResult) => r.id },
    { header: "TITLE", width: 44, cell: (r: JobResult) => r.title },
    { header: "DEPARTMENT", width: 18, cell: (r: JobResult) => r.department ?? "General" },
    { header: "LOCATION", width: 16, cell: (r: JobResult) => r.location ?? "Latin America" },
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
      `  HireLATAM · ${r.department ?? "General"} · ${r.location ?? "Latin America"} (Remote) · ${shortDate(r.date)}`,
      `  id: ${r.id}`,
      `  ${r.url}`,
    ].join("\n")
  return rows.map(block).join("\n\n")
}

const KNOWN_FLAGS: Record<string, Set<string>> = {
  search: new Set(["query", "location", "page", "limit", "format", "help", "h"]),
  detail: new Set(["format", "help", "h"]),
}

const HELP = `hirelatam-cli — search remote US/global roles on HireLATAM (hirelatam.com)

USAGE
  bun run src/cli.ts search [-q "<keywords>"] [-l "<location>"] [flags]
  bun run src/cli.ts detail <id|url> [--format json|plain]

SEARCH FLAGS
  --query, -q <text>      Keywords (title, department, skill, e.g. "finance", "analyst", "sales").
  --location, -l <text>   Location / country filter (e.g. "Brazil", "Mexico", "Latin America").
  --page <n>              1-indexed page. Default 1.
  --limit, -n <n>         Cap results emitted. Default 20.
  --format <fmt>          json (default) | table | plain.
`

async function runSearch(flags: Flags): Promise<number> {
  const query = typeof flags.query === "string" ? flags.query.trim().toLowerCase() : ""
  const location = typeof flags.location === "string" ? flags.location.trim().toLowerCase() : ""
  const page = Math.max(1, parseInt(String(flags.page || "1"), 10) || 1)
  const limit = Math.max(1, parseInt(String(flags.limit || "20"), 10) || 20)
  const format = (flags.format as string) || "json"

  try {
    const html = await fetchWidgetHtml()
    const match = html.match(/window\.jobsList\s*=\s*(\{[\s\S]*?\});/)
    if (!match) {
      writeError("could not extract jobs list from HireLATAM widget", "PARSE_ERROR")
      return 1
    }

    const data = JSON.parse(match[1])
    let allJobs: JobResult[] = []

    for (const [dept, jobs] of data.department || []) {
      for (const j of jobs) {
        allJobs.push({
          id: String(j.job_id),
          title: j.job_name || "(untitled)",
          company: "HireLATAM",
          location: j.details || "Latin America",
          date: j.last_opened || null,
          url: `https://recruiterflow.com/${(j.apply_link || "").replace(/\?widget=1/, "")}`,
          work_mode: "remote",
          department: dept,
          description: null,
        })
      }
    }

    // Apply filtering
    if (query) {
      allJobs = allJobs.filter(
        (j) =>
          j.title.toLowerCase().includes(query) ||
          (j.department && j.department.toLowerCase().includes(query)),
      )
    }
    if (location) {
      allJobs = allJobs.filter(
        (j) => j.location && j.location.toLowerCase().includes(location),
      )
    }

    const total = allJobs.length
    const offset = (page - 1) * limit
    const paged = allJobs.slice(offset, offset + limit)

    if (format === "table") {
      process.stdout.write(renderTable(paged) + "\n")
    } else if (format === "plain") {
      process.stdout.write(renderPlain(paged) + "\n")
    } else {
      process.stdout.write(
        JSON.stringify(
          {
            meta: { count: paged.length, page, total },
            results: paged,
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
    fetchUrl = `https://recruiterflow.com/hirelatam/jobs/${encodeURIComponent(target)}`
  }

  try {
    const res = await fetch(fetchUrl, {
      headers: {
        "User-Agent": UA,
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      },
      signal: AbortSignal.timeout(15000),
    })
    if (!res.ok) {
      writeError(`HTTP ${res.status}: ${res.statusText}`, "NOT_FOUND")
      return 1
    }
    const html = await res.text()

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

    const idMatch = fetchUrl.match(/\/jobs\/(\d+)/)
    const id = idMatch ? idMatch[1] : target

    const result: JobDetailResult = {
      id,
      title: posting.title || "(untitled)",
      company: posting.hiringOrganization?.name || "HireLATAM",
      location: posting.jobLocation?.address?.addressCountry || "Latin America",
      date: posting.datePosted || null,
      url: fetchUrl,
      work_mode: "remote",
      employment_type: posting.employmentType || null,
      description: cleanHtml(posting.description || ""),
    }

    if (format === "plain") {
      const lines = [
        result.title,
        `${result.company || "HireLATAM"} · ${result.location} (Remote)`,
        result.date ? `Posted: ${shortDate(result.date)}` : "",
        result.employment_type ? `Employment: ${result.employment_type}` : "",
        "",
        "Description:",
        result.description || "(no description)",
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
