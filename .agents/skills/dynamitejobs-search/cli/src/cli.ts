#!/usr/bin/env bun
// Self-contained CLI for searching jobs on Dynamite Jobs (dynamitejobs.com).
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
}

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async function fetchDJ(url: string): Promise<string> {
  const res = await fetch(url, {
    headers: {
      "User-Agent": UA,
      Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.9",
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
    { header: "SLUG", width: 28, cell: (r: JobResult) => r.id },
    { header: "TITLE", width: 38, cell: (r: JobResult) => r.title },
    { header: "COMPANY", width: 20, cell: (r: JobResult) => r.company ?? "—" },
    { header: "LOCATION", width: 14, cell: (r: JobResult) => r.location ?? "Remote" },
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
      `  ${r.company ?? "—"} · ${r.location ?? "Remote"} · ${shortDate(r.date)}`,
      `  slug: ${r.id}`,
      `  ${r.url}`,
    ].join("\n")
  return rows.map(block).join("\n\n")
}

const KNOWN_FLAGS: Record<string, Set<string>> = {
  search: new Set(["query", "location", "page", "limit", "format", "help", "h"]),
  detail: new Set(["format", "help", "h"]),
}

const HELP = `dynamitejobs-cli — search remote jobs on Dynamite Jobs (dynamitejobs.com)

USAGE
  bun run src/cli.ts search [-q "<keywords>"] [flags]
  bun run src/cli.ts detail <slug|url> [--format json|plain]

SEARCH FLAGS
  --query, -q <text>      Keywords (skill, role, e.g. "python", "data-analyst", "product").
  --location, -l <text>   Location filter (Dynamite Jobs is 100% remote-first).
  --page <n>              1-indexed page. Default 1.
  --limit, -n <n>         Cap results emitted. Default 20.
  --format <fmt>          json (default) | table | plain.
`

function extractJobCardsFromHtml(html: string): JobResult[] {
  const results: JobResult[] = []
  // Regex to match job link: <a href="/company/<comp>/remote-job/<slug>" ...>Title</a>
  const regex = /<a\s+href="(\/company\/([^\/]+)\/remote-job\/([^\/"]+))"[^>]*>([\s\S]*?)<\/a>/gi
  let match: RegExpExecArray | null

  while ((match = regex.exec(html)) !== null) {
    const rawPath = match[1]
    const companySlug = match[2]
    const jobSlug = match[3]
    const rawTitle = cleanHtml(match[4])
    if (!rawTitle || rawTitle.includes("<img")) continue

    // Find company name nearby if possible
    let companyName = companySlug
    const compRegex = new RegExp(`<a\\s+href="\\/company\\/${companySlug}"[^>]*>([\\s\\S]*?)<\\/a>`, "i")
    const compMatch = compRegex.exec(html.slice(match.index, match.index + 800))
    if (compMatch) {
      const parsedComp = cleanHtml(compMatch[1])
      if (parsedComp) companyName = parsedComp
    }

    results.push({
      id: `${companySlug}/${jobSlug}`,
      title: rawTitle,
      company: companyName,
      location: "Remote",
      date: null,
      url: `https://dynamitejobs.com${rawPath}`,
      work_mode: "remote",
      description: null,
    })
  }

  // Deduplicate by URL
  const seen = new Set<string>()
  return results.filter((r) => {
    if (seen.has(r.url)) return false
    seen.add(r.url)
    return true
  })
}

async function runSearch(flags: Flags): Promise<number> {
  const query = typeof flags.query === "string" ? flags.query.trim().toLowerCase() : ""
  const limit = Math.max(1, parseInt(String(flags.limit || "20"), 10) || 20)
  const format = (flags.format as string) || "json"

  let html = ""
  if (query) {
    const cleanTerm = query.replace(/\s+/g, "-")
    // Try skill endpoint first, then category
    html = await fetchDJ(`https://dynamitejobs.com/skill/remote-${cleanTerm}-jobs`)
    if (!html || !html.includes("/remote-job/")) {
      html = await fetchDJ(`https://dynamitejobs.com/category/remote-${cleanTerm}-jobs`)
    }
    if (!html || !html.includes("/remote-job/")) {
      html = await fetchDJ(`https://dynamitejobs.com/skill/remote-${cleanTerm.split("-")[0]}-jobs`)
    }
    if (!html || !html.includes("/remote-job/")) {
      html = await fetchDJ(`https://dynamitejobs.com/category/remote-${cleanTerm.split("-")[0]}-jobs`)
    }
  } else {
    // Default to software / data / product categories
    html = await fetchDJ("https://dynamitejobs.com/category/remote-development-jobs")
  }

  try {
    let rows = extractJobCardsFromHtml(html)
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
            meta: { count: rows.length, page: 1, total: rows.length },
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
    writeError("missing required slug or URL for detail command", "BAD_ARGS")
    return 1
  }
  const format = (flags.format as string) || "json"

  let fetchUrl = target
  if (!target.startsWith("http")) {
    const cleanSlug = target.replace(/^\/+/, "")
    fetchUrl = cleanSlug.includes("company/")
      ? `https://dynamitejobs.com/${cleanSlug}`
      : `https://dynamitejobs.com/company/${cleanSlug.replace("remote-job/", "")}`
    if (!fetchUrl.includes("/remote-job/")) {
      const parts = cleanSlug.split("/")
      if (parts.length >= 2) {
        fetchUrl = `https://dynamitejobs.com/company/${parts[0]}/remote-job/${parts[1]}`
      }
    }
  }

  try {
    const html = await fetchDJ(fetchUrl)
    if (!html) {
      writeError(`job not found at ${fetchUrl}`, "NOT_FOUND")
      return 1
    }

    // Extract Schema.org JobPosting LD+JSON
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

    const result: JobDetailResult = {
      id: fetchUrl.replace(/^https?:\/\/[^\/]+\/company\//, "").replace("/remote-job/", "/"),
      title: posting.title || "(untitled)",
      company: posting.hiringOrganization?.name || null,
      location: "Remote",
      date: posting.datePosted || null,
      url: fetchUrl,
      work_mode: "remote",
      employment_type: posting.employmentType || null,
      salary: posting.baseSalary?.value ? `${posting.baseSalary.value.minValue ?? ""} - ${posting.baseSalary.value.maxValue ?? ""}` : null,
      description: cleanHtml(posting.description || ""),
    }

    if (format === "plain") {
      const lines = [
        result.title,
        `${result.company || "—"} · ${result.location} (remote)`,
        result.date ? `Posted: ${shortDate(result.date)}` : "",
        result.employment_type ? `Employment: ${result.employment_type}` : "",
        result.salary ? `Salary: ${result.salary}` : "",
        "",
        "Description:",
        result.description || "(no description)",
        "",
        `URL: ${result.url}`,
        `slug: ${result.id}`,
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
