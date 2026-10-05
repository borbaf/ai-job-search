#!/usr/bin/env bun
// Self-contained CLI for searching jobs on Get on Board (getonbrd.com).
// Uses the official public REST API v0.
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
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/\n{3,}/g, "\n\n")
    .trim()
}

interface JobItem {
  id: string
  title: string
  company: string
  location: string
  country: string
  remote: boolean
  remote_modality?: string
  salary?: string
  date_posted?: string
  url: string
  description?: string
  functions?: string
  requirements?: string
  benefits?: string
}

async function fetchWithRetry(url: string, retries = 3): Promise<Response> {
  let attempt = 0
  while (attempt < retries) {
    try {
      const res = await fetch(url, {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ai-job-search/getonbrd-search",
          Accept: "application/json, text/html, */*",
        },
        redirect: "follow",
      })
      if (res.status === 429) {
        attempt++
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)))
        continue
      }
      return res
    } catch (e) {
      attempt++
      if (attempt >= retries) throw e
      await new Promise((r) => setTimeout(r, 1000 * attempt))
    }
  }
  throw new Error(`Failed to fetch ${url} after ${retries} attempts`)
}

function parseJobApiItem(raw: any): JobItem {
  const attrs = raw.attributes || {}
  const companyAttrs = attrs.company?.data?.attributes || {}
  const companyName = companyAttrs.name || "Unknown Company"

  const countries = Array.isArray(attrs.countries) ? attrs.countries : []
  const countryStr = countries.join(", ")

  let locationStr = countryStr || "Not specified"
  if (attrs.remote) {
    locationStr = attrs.remote_modality ? `Remote (${attrs.remote_modality})` : "Remote"
    if (attrs.remote_zone) locationStr += ` [${attrs.remote_zone}]`
  }

  let salaryStr: string | undefined
  if (attrs.min_salary || attrs.max_salary) {
    salaryStr = `$${attrs.min_salary ?? "?"} - $${attrs.max_salary ?? "?"} USD/month`
  }

  let datePosted: string | undefined
  if (attrs.published_at) {
    try {
      datePosted = new Date(attrs.published_at * 1000).toISOString()
    } catch {
      // ignore
    }
  }

  const publicUrl = raw.links?.public_url || `https://www.getonbrd.com/jobs/${raw.id}`

  return {
    id: raw.id,
    title: attrs.title || "",
    company: companyName,
    location: locationStr,
    country: countryStr,
    remote: Boolean(attrs.remote),
    remote_modality: attrs.remote_modality,
    salary: salaryStr,
    date_posted: datePosted,
    url: publicUrl,
    description: cleanHtml(attrs.description || ""),
    functions: cleanHtml(attrs.functions || ""),
    requirements: cleanHtml(attrs.desirable || ""),
    benefits: cleanHtml(attrs.benefits || ""),
  }
}

async function runSearch(flags: Flags): Promise<void> {
  const query = (flags.query as string) || (flags._[1] as string) || ""
  const country = (flags.country as string) || (flags.location as string) || ""
  const onlyRemote = Boolean(flags.remote)
  const page = parseInt((flags.page as string) || "1", 10) || 1
  const limit = parseInt((flags.limit as string) || "20", 10) || 20
  const format = (flags.format as string) || "json"

  const perPage = Math.min(Math.max(limit, 20), 100)
  const apiUrl = new URL("https://www.getonbrd.com/api/v0/search/jobs")
  if (query) apiUrl.searchParams.set("query", query)
  apiUrl.searchParams.set("page", String(page))
  apiUrl.searchParams.set("per_page", String(perPage))
  apiUrl.searchParams.append("expand[]", "company")

  let data: any
  try {
    const res = await fetchWithRetry(apiUrl.toString())
    if (!res.ok) {
      writeError(`HTTP ${res.status}: ${res.statusText}`, "FETCH_ERROR")
      process.exit(1)
    }
    data = await res.json()
  } catch (err: any) {
    writeError(err.message, "NETWORK_ERROR")
    process.exit(1)
  }

  const rawList: any[] = Array.isArray(data.data) ? data.data : []
  let items = rawList.map(parseJobApiItem)

  if (country) {
    const cLower = country.toLowerCase()
    items = items.filter(
      (it) =>
        it.country.toLowerCase().includes(cLower) ||
        it.location.toLowerCase().includes(cLower)
    )
  }

  if (onlyRemote) {
    items = items.filter((it) => it.remote)
  }

  if (items.length > limit) {
    items = items.slice(0, limit)
  }

  if (format === "table") {
    if (items.length === 0) {
      console.log("No jobs found matching criteria.")
      return
    }
    console.log(
      "ID".padEnd(35) +
        " | " +
        "TITLE".padEnd(32) +
        " | " +
        "COMPANY".padEnd(20) +
        " | " +
        "LOCATION".padEnd(20) +
        " | " +
        "POSTED"
    )
    console.log("-".repeat(125))
    for (const it of items) {
      const idStr = it.id.length > 33 ? it.id.slice(0, 32) + "…" : it.id
      const titleStr = it.title.length > 30 ? it.title.slice(0, 29) + "…" : it.title
      const compStr = it.company.length > 18 ? it.company.slice(0, 17) + "…" : it.company
      const locStr = it.location.length > 18 ? it.location.slice(0, 17) + "…" : it.location
      const dateStr = it.date_posted ? it.date_posted.split("T")[0] : ""
      console.log(
        idStr.padEnd(35) +
          " | " +
          titleStr.padEnd(32) +
          " | " +
          compStr.padEnd(20) +
          " | " +
          locStr.padEnd(20) +
          " | " +
          dateStr
      )
    }
    return
  }

  if (format === "plain") {
    if (items.length === 0) {
      console.log("No jobs found matching criteria.")
      return
    }
    for (const it of items) {
      console.log(`[${it.id}] ${it.title}`)
      console.log(`Company: ${it.company}`)
      console.log(`Location: ${it.location}`)
      if (it.salary) console.log(`Salary: ${it.salary}`)
      if (it.date_posted) console.log(`Posted: ${it.date_posted}`)
      console.log(`URL: ${it.url}`)
      console.log("-".repeat(40))
    }
    return
  }

  // default json
  console.log(JSON.stringify(items, null, 2))
}

async function runDetail(flags: Flags): Promise<void> {
  const target = (flags._[1] as string) || (flags.id as string) || ""
  const format = (flags.format as string) || "json"

  if (!target) {
    writeError("Missing job ID or URL for detail command", "INVALID_ARGUMENT")
    process.exit(1)
  }

  let slug = target
  let fullUrl = ""
  if (target.startsWith("http")) {
    fullUrl = target
    const u = new URL(target)
    const parts = u.pathname.split("/").filter(Boolean)
    slug = parts[parts.length - 1]
  } else {
    fullUrl = `https://www.getonbrd.com/jobs/${slug}`
  }

  // First check API by extracting search keywords from the slug (first 3-4 words)
  const slugWords = slug.split("-").filter(Boolean)
  const searchKeywords = slugWords.slice(0, 3).join(" ")

  let foundItem: JobItem | null = null
  if (searchKeywords) {
    try {
      const searchUrl = `https://www.getonbrd.com/api/v0/search/jobs?query=${encodeURIComponent(
        searchKeywords
      )}&per_page=50&expand[]=company`
      const res = await fetchWithRetry(searchUrl)
      if (res.ok) {
        const data = await res.json()
        if (Array.isArray(data.data)) {
          const exact = data.data.find((j: any) => j.id === slug)
          if (exact) {
            foundItem = parseJobApiItem(exact)
          }
        }
      }
    } catch {
      // ignore
    }
  }

  // If not found via search API, fetch and parse the public web page directly
  if (!foundItem) {
    try {
      const res = await fetchWithRetry(fullUrl)
      if (!res.ok) {
        writeError(`Job not found: ${target}`, "NOT_FOUND")
        process.exit(1)
      }
      const html = await res.text()
      const titleMatch =
        html.match(/itemprop=["']title["'][^>]*>([\s\S]*?)<\//i) ||
        html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)

      let companyName = "Unknown Company"
      const ogTitle = html.match(/<meta content="([^"]+)" property="og:title">/i)
      if (ogTitle && ogTitle[1].includes(" at ")) {
        // e.g. "Actuario Senior at BNP Paribas Cardif - Chile"
        const afterAt = ogTitle[1].split(" at ")[1]
        companyName = afterAt.split(" - ")[0].trim()
      } else {
        const compMatch =
          html.match(/<strong itemprop="name">([\s\S]*?)<\/strong>/i) ||
          html.match(/itemprop="name"[^>]*>([\s\S]*?)<\//i)
        if (compMatch) companyName = cleanHtml(compMatch[1])
      }

      const descMatch = html.match(/itemprop=["']description["'][\s\S]*?>([\s\S]*?)<\/div>/i)

      foundItem = {
        id: slug,
        title: titleMatch ? cleanHtml(titleMatch[1]) : slug,
        company: companyName,
        location: html.includes("Hybrid")
          ? "Hybrid"
          : html.includes("Remote")
          ? "Remote"
          : "Not specified",
        country: "",
        remote: html.includes("Remote"),
        url: res.url || fullUrl,
        description: descMatch ? cleanHtml(descMatch[1]) : "",
      }
    } catch (err: any) {
      writeError(`Failed to fetch job detail: ${err.message}`, "FETCH_ERROR")
      process.exit(1)
    }
  }

  if (format === "plain") {
    console.log(`TITLE: ${foundItem.title}`)
    console.log(`COMPANY: ${foundItem.company}`)
    console.log(`LOCATION: ${foundItem.location}`)
    if (foundItem.salary) console.log(`SALARY: ${foundItem.salary}`)
    if (foundItem.date_posted) console.log(`POSTED: ${foundItem.date_posted}`)
    console.log(`URL: ${foundItem.url}`)
    console.log(`\nDESCRIPTION:\n${foundItem.description || "No description available."}`)
    if (foundItem.functions) {
      console.log(`\nFUNCTIONS:\n${foundItem.functions}`)
    }
    if (foundItem.requirements) {
      console.log(`\nREQUIREMENTS:\n${foundItem.requirements}`)
    }
    if (foundItem.benefits) {
      console.log(`\nBENEFITS:\n${foundItem.benefits}`)
    }
    return
  }

  // default json
  console.log(JSON.stringify(foundItem, null, 2))
}

function showHelp(): void {
  console.log(`Get on Board (getonbrd.com) Job Search CLI

Usage:
  bun run cli.ts search [options]
  bun run cli.ts detail <id|url> [options]

Commands:
  search                 Search active job listings on Get on Board
  detail <id|url>        Fetch full description and details for a job

Options for 'search':
  -q, --query <text>     Keyword search (role, skill, tech stack)
  -c, --country <text>   Filter by country (e.g. Chile, Brazil, Colombia, Mexico)
  -l, --location <text>  Alias for --country
      --remote           Filter for remote positions only
      --page <n>         Page number (default: 1)
  -n, --limit <n>        Limit results count (default: 20)
      --format <fmt>     Output format: json (default), table, plain

Options for 'detail':
      --format <fmt>     Output format: json (default), plain
  -h, --help             Show this help message
`)
}

async function main(): Promise<void> {
  const flags = parseFlags(process.argv.slice(2))
  const cmd = flags._[0]

  if (flags.help || flags.h || !cmd) {
    showHelp()
    return
  }

  switch (cmd) {
    case "search":
      await runSearch(flags)
      break
    case "detail":
      await runDetail(flags)
      break
    default:
      writeError(`Unknown command: ${cmd}`, "UNKNOWN_COMMAND")
      showHelp()
      process.exit(1)
  }
}

main().catch((err) => {
  writeError(err.message, "UNEXPECTED_ERROR")
  process.exit(1)
})
