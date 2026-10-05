#!/usr/bin/env bun
// Self-contained CLI for searching jobs on Solvo Global (careers.solvoglobal.com).
// No external CLI framework and zero runtime dependencies beyond Bun.

interface Flags {
  _: string[]
  [k: string]: string | boolean | string[]
}

const ALIAS: Record<string, string> = {
  q: "query",
  l: "location",
  c: "country",
  n: "limit",
}

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
    .replace(/&bull;/gi, "• ")
    .replace(/&ndash;/gi, "–")
    .replace(/&mdash;/gi, "—")
    .replace(/&hellip;/gi, "…")
    .replace(/&rsquo;/gi, "'")
    .replace(/&lsquo;/gi, "'")
    .replace(/&rdquo;/gi, '"')
    .replace(/&ldquo;/gi, '"')
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
    .replace(/&#([0-9]+);/g, (_, dec) => String.fromCharCode(parseInt(dec, 10)))
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

export interface JobResult {
  id: string
  job_code: string | null
  title: string
  company: string
  location: string | null
  country: string | null
  city: string | null
  date: string | null
  url: string
  apply_url: string | null
  work_mode: string | null
  vertical: string | null
  job_type: string | null
  languages: string | null
  time_of_experience: string | null
  description: string | null
}

const UA = "Mozilla/5.0 (compatible; solvoglobal-cli/1.0)"
const AJAX_URL = "https://careers.solvoglobal.com/wp-admin/admin-ajax.php"

function decodeHtmlEntities(str: string): string {
  return str
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&#039;/g, "'")
    .replace(/&#39;/g, "'")
}

async function fetchJobsPage(page: number, title: string = "", country: string = ""): Promise<{ html: string; pagination: string }> {
  const body = new URLSearchParams({
    action: "fetch_jobs",
    page: String(page),
    title,
    country,
  })

  let attempt = 0
  const maxAttempts = 5
  while (attempt < maxAttempts) {
    try {
      const res = await fetch(AJAX_URL, {
        method: "POST",
        headers: {
          "User-Agent": UA,
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json, text/javascript, */*; q=0.01",
        },
        body,
        signal: AbortSignal.timeout(15000),
      })

      if (res.status === 429 || res.status >= 500) {
        attempt++
        const delay = Math.pow(2, attempt) * 500 + Math.random() * 200
        await new Promise((resolve) => setTimeout(resolve, delay))
        continue
      }

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      }

      return await res.json()
    } catch (err) {
      attempt++
      if (attempt >= maxAttempts) {
        throw err
      }
      const delay = Math.pow(2, attempt) * 500 + Math.random() * 200
      await new Promise((resolve) => setTimeout(resolve, delay))
    }
  }
  throw new Error("Failed to fetch jobs from Solvo Global after retries")
}

function parseJobCards(html: string): JobResult[] {
  const results: JobResult[] = []
  const regex = /<article[^>]*class=["'][^"']*job-card[^"']*["'][^>]*data-job='([^']+)'[^>]*>/g
  let match: RegExpExecArray | null

  while ((match = regex.exec(html)) !== null) {
    const raw = decodeHtmlEntities(match[1])
    try {
      const data = JSON.parse(raw)
      const cleanTitle = (data.job_title || data.public_job_title || "").replace(/^[^-]+-\s*/, "").trim()
      const locationParts = [data.city, data.country].filter(Boolean)
      const location = locationParts.length > 0 ? locationParts.join(", ") : null
      const isRemote = data.remote_job === "Yes" ? "remote" : data.remote_job === "No" ? "on-site" : data.remote_job || null

      results.push({
        id: data.id || data.job_code || "",
        job_code: data.job_code || null,
        title: cleanTitle || data.job_title || "(untitled)",
        company: "Solvo Global",
        location,
        country: data.country || null,
        city: data.city || null,
        date: data.created || null,
        url: data.apply_job_without_registration || data.apply_job || "https://careers.solvoglobal.com/job-listing/",
        apply_url: data.apply_job || data.apply_job_without_registration || null,
        work_mode: isRemote,
        vertical: data.vertical || null,
        job_type: data.job_type || null,
        languages: data.languages || null,
        time_of_experience: data.time_of_experience || null,
        description: cleanHtml(data.job_description || ""),
      })
    } catch (e) {
      // Individual card parse failure should not break the rest
    }
  }
  return results
}

function renderTable(rows: JobResult[]): string {
  if (rows.length === 0) return "No results."
  const columns = [
    { header: "CODE", width: 12, cell: (r: JobResult) => r.job_code || r.id.slice(0, 10) },
    { header: "TITLE", width: 38, cell: (r: JobResult) => r.title },
    { header: "COUNTRY", width: 12, cell: (r: JobResult) => r.country || "—" },
    { header: "CITY", width: 14, cell: (r: JobResult) => r.city || "—" },
    { header: "MODE", width: 8, cell: (r: JobResult) => r.work_mode || "—" },
    { header: "VERTICAL", width: 16, cell: (r: JobResult) => r.vertical || "—" },
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
      `  Solvo Global · ${r.job_code || "N/A"} · ${r.location || "Latin America"} (${r.work_mode || "N/A"})`,
      `  Vertical: ${r.vertical || "N/A"} · Type: ${r.job_type || "N/A"} · Exp: ${r.time_of_experience || "N/A"}`,
      `  Languages: ${r.languages || "N/A"}`,
      `  id: ${r.id}`,
      `  ${r.url}`,
    ].join("\n")
  return rows.map(block).join("\n\n")
}

const KNOWN_FLAGS: Record<string, Set<string>> = {
  search: new Set(["query", "q", "country", "c", "location", "l", "page", "limit", "n", "format", "help", "h"]),
  detail: new Set(["format", "help", "h"]),
}

const HELP = `solvoglobal-cli — search nearshore/remote jobs on Solvo Global (careers.solvoglobal.com)

USAGE
  bun run src/cli.ts search [-q "<keywords>"] [-c "<country>"] [flags]
  bun run src/cli.ts detail <id|code|url> [--format json|plain]

SEARCH FLAGS
  --query, -q <text>      Keywords (title, role, skill, e.g. "logistics", "analyst", "supply chain").
  --country, -c <text>    Country filter (e.g. "Colombia", "Mexico", "Argentina").
  --location, -l <text>   Location / country filter (alias for country/city).
  --page <n>              1-indexed page. Default 1.
  --limit, -n <n>         Cap results emitted. Default 20.
  --format <fmt>          json (default) | table | plain.
`

async function runSearch(flags: Flags): Promise<number> {
  const query = typeof flags.query === "string" ? flags.query.trim() : ""
  const country = typeof flags.country === "string"
    ? flags.country.trim()
    : typeof flags.location === "string"
    ? flags.location.trim()
    : ""
  const page = Math.max(1, parseInt(String(flags.page || "1"), 10) || 1)
  const limit = Math.max(1, parseInt(String(flags.limit || "20"), 10) || 20)
  const format = (flags.format as string) || "json"

  try {
    const data = await fetchJobsPage(page, query, country)
    let jobs = parseJobCards(data.html)

    // Additional client-side filtering if user specified location or keywords not caught by backend
    if (query) {
      const qLower = query.toLowerCase()
      jobs = jobs.filter(
        (j) =>
          j.title.toLowerCase().includes(qLower) ||
          (j.vertical && j.vertical.toLowerCase().includes(qLower)) ||
          (j.description && j.description.toLowerCase().includes(qLower)) ||
          (j.job_code && j.job_code.toLowerCase().includes(qLower))
      )
    }

    if (country) {
      const cLower = country.toLowerCase()
      jobs = jobs.filter(
        (j) =>
          (j.country && j.country.toLowerCase().includes(cLower)) ||
          (j.city && j.city.toLowerCase().includes(cLower)) ||
          (j.location && j.location.toLowerCase().includes(cLower))
      )
    }

    const paged = jobs.slice(0, limit)

    if (format === "table") {
      process.stdout.write(renderTable(paged) + "\n")
    } else if (format === "plain") {
      process.stdout.write(renderPlain(paged) + "\n")
    } else {
      process.stdout.write(
        JSON.stringify(
          {
            meta: { count: paged.length, page, total: jobs.length },
            results: paged,
          },
          null,
          2
        ) + "\n"
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
    writeError("missing required job ID, code, or URL for detail command", "BAD_ARGS")
    return 1
  }
  const format = (flags.format as string) || "json"

  try {
    // Solvo Global embeds full job details in the search endpoint cards.
    // We scan page 1 through page 5 if needed to find the matching job.
    let found: JobResult | null = null
    const targetClean = target.trim().toLowerCase()

    for (let p = 1; p <= 5; p++) {
      const data = await fetchJobsPage(p)
      const jobs = parseJobCards(data.html)
      if (jobs.length === 0) break

      for (const j of jobs) {
        if (
          j.id.toLowerCase() === targetClean ||
          (j.job_code && j.job_code.toLowerCase().replace(/\s+/g, "").includes(targetClean.replace(/\s+/g, ""))) ||
          j.url.toLowerCase() === targetClean ||
          (j.apply_url && j.apply_url.toLowerCase() === targetClean)
        ) {
          found = j
          break
        }
      }
      if (found) break
    }

    if (!found) {
      writeError(`job not found for '${target}' in Solvo Global listings`, "NOT_FOUND")
      return 1
    }

    if (format === "plain") {
      const lines = [
        found.title,
        `Solvo Global · ${found.job_code || "N/A"} · ${found.location || "Latin America"} (${found.work_mode || "N/A"})`,
        found.date ? `Date: ${found.date}` : "",
        found.job_type ? `Type: ${found.job_type}` : "",
        found.vertical ? `Vertical: ${found.vertical}` : "",
        found.languages ? `Languages: ${found.languages}` : "",
        found.time_of_experience ? `Experience: ${found.time_of_experience}` : "",
        "",
        "Description:",
        found.description || "(no description)",
        "",
        `URL: ${found.url}`,
        `ID: ${found.id}`,
      ]
      process.stdout.write(lines.filter((l) => l !== "").join("\n") + "\n")
    } else {
      process.stdout.write(JSON.stringify(found, null, 2) + "\n")
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
        "UNKNOWN_FLAG"
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
