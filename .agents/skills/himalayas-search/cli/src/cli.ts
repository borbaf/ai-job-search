import { parseArgs } from 'util';

interface JobItem {
  id: string;
  title: string;
  company: string;
  company_slug?: string;
  location: string;
  location_restrictions: string[];
  seniority?: string;
  employment_type?: string;
  categories: string[];
  salary?: string;
  date: string;
  expires_at?: string;
  url: string;
  application_link?: string;
  description_snippet?: string;
  description?: string;
}

const API_BASE = 'https://himalayas.app/jobs/api';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

function stripHtml(html: string): string {
  if (!html) return '';
  return html
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function formatSalary(raw: any): string | undefined {
  if (!raw.minSalary && !raw.maxSalary) return undefined;
  const currency = raw.currency || 'USD';
  const period = raw.salaryPeriod ? `/${raw.salaryPeriod}` : '';
  if (raw.minSalary && raw.maxSalary) {
    return `${currency} ${raw.minSalary.toLocaleString()} - ${raw.maxSalary.toLocaleString()}${period}`;
  }
  if (raw.minSalary) {
    return `From ${currency} ${raw.minSalary.toLocaleString()}${period}`;
  }
  if (raw.maxSalary) {
    return `Up to ${currency} ${raw.maxSalary.toLocaleString()}${period}`;
  }
  return undefined;
}

function mapApiJob(raw: any): JobItem {
  const id = raw.guid || String(raw.pubDate) + '-' + (raw.companySlug || 'job');
  const title = (raw.title || '').trim();
  const company = raw.companyName || 'Unknown';
  const location_restrictions: string[] = Array.isArray(raw.locationRestrictions) ? raw.locationRestrictions : [];
  
  let location = 'Worldwide Remote';
  if (location_restrictions.length > 0) {
    location = location_restrictions.join(', ');
  }

  const categories: string[] = [];
  if (Array.isArray(raw.categories)) categories.push(...raw.categories);
  if (Array.isArray(raw.parentCategories)) categories.push(...raw.parentCategories);

  let date = '';
  if (raw.pubDate) {
    try {
      const d = typeof raw.pubDate === 'number' ? new Date(raw.pubDate * 1000) : new Date(raw.pubDate);
      if (!isNaN(d.getTime())) date = d.toISOString().slice(0, 10);
    } catch {}
  }

  let expires_at = undefined;
  if (raw.expiryDate) {
    try {
      const d = typeof raw.expiryDate === 'number' ? new Date(raw.expiryDate * 1000) : new Date(raw.expiryDate);
      if (!isNaN(d.getTime())) expires_at = d.toISOString().slice(0, 10);
    } catch {}
  }

  const descClean = stripHtml(raw.description || raw.excerpt || '');
  const url = raw.guid && raw.guid.startsWith('http') ? raw.guid : (raw.applicationLink || `https://himalayas.app`);

  return {
    id,
    title,
    company,
    company_slug: raw.companySlug,
    location,
    location_restrictions,
    seniority: raw.seniority || undefined,
    employment_type: raw.employmentType || undefined,
    categories: [...new Set(categories)],
    salary: formatSalary(raw),
    date,
    expires_at,
    url,
    application_link: raw.applicationLink,
    description_snippet: descClean.slice(0, 300) + (descClean.length > 300 ? '...' : ''),
    description: descClean
  };
}

async function searchJobs(options: {
  query?: string;
  category?: string;
  limit?: number;
}): Promise<JobItem[]> {
  const limit = options.limit || 20;
  const qTerms = (options.query || '').toLowerCase().split(/\s+/).filter(Boolean);
  const catFilter = (options.category || '').toLowerCase();

  const matchedJobs: JobItem[] = [];
  let cursor: string | null = null;
  let pagesFetched = 0;
  const maxPages = 5; // Scan up to 500 recent postings

  while (matchedJobs.length < limit && pagesFetched < maxPages) {
    const url = new URL(API_BASE);
    url.searchParams.set('limit', '100');
    if (cursor) url.searchParams.set('cursor', cursor);

    const res = await fetch(url.toString(), {
      headers: {
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
      },
      signal: AbortSignal.timeout(15000)
    });

    if (!res.ok) {
      throw new Error(`Himalayas API returned HTTP ${res.status}`);
    }

    const data = await res.json();
    pagesFetched++;

    if (!Array.isArray(data.jobs) || data.jobs.length === 0) break;

    for (const raw of data.jobs) {
      const item = mapApiJob(raw);

      // Check category
      if (catFilter) {
        const matchesCategory = item.categories.some(c => c.toLowerCase().includes(catFilter));
        if (!matchesCategory) continue;
      }

      // Check query match across title, company, description, categories
      if (qTerms.length > 0) {
        const searchBlob = `${item.title} ${item.company} ${item.categories.join(' ')} ${item.description_snippet}`.toLowerCase();
        const matchesAll = qTerms.every(term => searchBlob.includes(term));
        if (!matchesAll) continue;
      }

      matchedJobs.push(item);
      if (matchedJobs.length >= limit) break;
    }

    cursor = data.nextCursor;
    if (!cursor) break;
  }

  return matchedJobs;
}

function printHelp(): void {
  console.log(`himalayas-search - Search live remote jobs on Himalayas (himalayas.app)

USAGE:
  bun run cli.ts search [options]

COMMANDS:
  search                  Search remote jobs

OPTIONS:
  -q, --query <text>      Search keywords (e.g. "supply chain", "product manager", "operations")
  -c, --category <name>   Filter by category (e.g. "Operations", "Product", "Data")
  -n, --limit <number>    Maximum results to return (default: 20)
  -f, --format <format>   Output format: json, table, or plain (default: json)
  -h, --help              Show this help message
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h' || command === 'help') {
    printHelp();
    process.exit(0);
  }

  if (command === 'search') {
    const { values } = parseArgs({
      args: args.slice(1),
      options: {
        query: { type: 'string', short: 'q' },
        category: { type: 'string', short: 'c' },
        limit: { type: 'string', short: 'n' },
        format: { type: 'string', short: 'f', default: 'json' },
        help: { type: 'boolean', short: 'h' }
      },
      allowPositionals: true
    });

    if (values.help) {
      printHelp();
      process.exit(0);
    }

    try {
      const results = await searchJobs({
        query: values.query,
        category: values.category,
        limit: values.limit ? parseInt(values.limit, 10) : 20
      });

      if (values.format === 'table') {
        console.table(
          results.map(r => ({
            Title: r.title.slice(0, 35),
            Company: r.company.slice(0, 20),
            Location: r.location.slice(0, 25),
            Salary: r.salary || 'N/I',
            Date: r.date
          }))
        );
      } else if (values.format === 'plain') {
        for (const r of results) {
          console.log(`\n${r.title} - ${r.company}`);
          console.log(`Location: ${r.location} | Date: ${r.date}`);
          if (r.salary) console.log(`Salary: ${r.salary}`);
          console.log(`URL: ${r.url}`);
          if (r.application_link && r.application_link !== r.url) console.log(`Apply: ${r.application_link}`);
          if (r.description_snippet) console.log(`Summary: ${r.description_snippet}`);
        }
      } else {
        console.log(JSON.stringify(results, null, 2));
      }
    } catch (err: any) {
      console.error(JSON.stringify({ error: err.message, code: 'SEARCH_FAILED' }));
      process.exit(1);
    }
  } else {
    console.error(JSON.stringify({ error: `Unknown command "${command}"`, code: 'UNKNOWN_COMMAND' }));
    printHelp();
    process.exit(1);
  }
}

main();
