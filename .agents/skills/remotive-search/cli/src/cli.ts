import { parseArgs } from 'util';

interface JobItem {
  id: string;
  title: string;
  company: string;
  location: string;
  categories: string[];
  tags: string[];
  job_type?: string;
  salary?: string;
  date: string;
  url: string;
  description_snippet?: string;
}

const API_BASE = 'https://remotive.com/api/remote-jobs';
const CATEGORIES_API = 'https://remotive.com/api/remote-jobs/categories';
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

function mapApiJob(raw: any): JobItem {
  const id = String(raw.id || '');
  const title = (raw.title || '').trim();
  const company = raw.company_name || 'Unknown';
  const location = raw.candidate_required_location || 'Worldwide';
  
  const categories: string[] = [];
  if (raw.category) categories.push(raw.category);

  const tags: string[] = Array.isArray(raw.tags) ? raw.tags : [];

  let date = '';
  if (raw.publication_date) {
    try {
      const d = new Date(raw.publication_date);
      if (!isNaN(d.getTime())) date = d.toISOString().slice(0, 10);
    } catch {}
  }

  const descClean = stripHtml(raw.description || '');
  const url = raw.url || `https://remotive.com`;

  return {
    id,
    title,
    company,
    location,
    categories,
    tags,
    job_type: raw.job_type || undefined,
    salary: raw.salary || undefined,
    date,
    url,
    description_snippet: descClean.slice(0, 300) + (descClean.length > 300 ? '...' : ''),
  };
}

async function fetchJobs(category?: string, searchParam?: string): Promise<any[]> {
  const url = new URL(API_BASE);
  if (category) url.searchParams.set('category', category);
  if (searchParam) url.searchParams.set('search', searchParam);

  const res = await fetch(url.toString(), {
    headers: {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json',
    },
  });

  if (!res.ok) {
    throw new Error(`Remotive API responded with status ${res.status}: ${res.statusText}`);
  }

  const data = (await res.json()) as any;
  return Array.isArray(data.jobs) ? data.jobs : [];
}

async function fetchCategories(): Promise<any[]> {
  const res = await fetch(CATEGORIES_API, {
    headers: {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json',
    },
  });

  if (!res.ok) {
    throw new Error(`Remotive API categories responded with status ${res.status}: ${res.statusText}`);
  }

  const data = (await res.json()) as any;
  return Array.isArray(data.jobs) ? data.jobs : [];
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      query: { type: 'string', short: 'q' },
      category: { type: 'string', short: 'c' },
      limit: { type: 'string', short: 'n', default: '20' },
      jobage: { type: 'string' },
      format: { type: 'string', default: 'json' },
      help: { type: 'boolean', short: 'h' },
    },
    strict: false,
    allowPositionals: true,
  });

  const command = positionals[0] || 'search';

  if (values.help || command === 'help') {
    console.log(`
Remotive Search CLI

Usage:
  bun run cli.ts search [options]
  bun run cli.ts categories

Options:
  -q, --query <text>       Search query (title, company, description, tags)
  -c, --category <slug>    Filter by category slug
  -n, --limit <number>     Max number of jobs to return (default: 20)
  --jobage <days>          Filter jobs published in the last N days
  --format <format>        Output format: json (default), table, plain
  -h, --help               Show help
    `);
    process.exit(0);
  }

  if (command === 'categories') {
    try {
      const categories = await fetchCategories();
      if (values.format === 'json') {
        console.log(JSON.stringify(categories, null, 2));
      } else {
        for (const cat of categories) {
          console.log(`- ${cat.name} (slug: ${cat.slug})`);
        }
      }
      process.exit(0);
    } catch (err: any) {
      console.error(JSON.stringify({ error: err.message, code: 'FETCH_CATEGORIES_ERROR' }));
      process.exit(1);
    }
  }

  if (command === 'search') {
    try {
      const query = (values.query as string) || '';
      const category = (values.category as string) || '';
      const limit = parseInt(values.limit as string, 10) || 20;
      const jobage = values.jobage ? parseInt(values.jobage as string, 10) : undefined;
      const format = values.format as string;

      const rawJobs = await fetchJobs(category, query);
      let jobs = rawJobs.map(mapApiJob);

      // Client-side text filtering across title, company, tags, description if query provided
      if (query) {
        const qLower = query.toLowerCase();
        const terms = qLower.split(/\s+/).filter(Boolean);
        jobs = jobs.filter(j => {
          const haystack = `${j.title} ${j.company} ${j.categories.join(' ')} ${j.tags.join(' ')} ${j.location} ${j.description_snippet || ''}`.toLowerCase();
          return terms.every(t => haystack.includes(t));
        });
      }

      // Filter by jobage in days if requested
      if (jobage !== undefined && !isNaN(jobage) && jobage > 0) {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - jobage);
        const cutoffStr = cutoff.toISOString().slice(0, 10);
        jobs = jobs.filter(j => j.date && j.date >= cutoffStr);
      }

      // Limit results
      const total = jobs.length;
      jobs = jobs.slice(0, limit);

      if (format === 'json') {
        console.log(JSON.stringify({
          meta: {
            count: jobs.length,
            total,
            query: query || undefined,
            category: category || undefined,
          },
          results: jobs,
        }, null, 2));
      } else if (format === 'table') {
        if (jobs.length === 0) {
          console.log('No jobs found matching criteria.');
        } else {
          console.table(jobs.map(j => ({
            Title: j.title.length > 35 ? j.title.slice(0, 32) + '...' : j.title,
            Company: j.company.length > 20 ? j.company.slice(0, 17) + '...' : j.company,
            Location: j.location.length > 20 ? j.location.slice(0, 17) + '...' : j.location,
            Date: j.date,
            Salary: j.salary || 'N/A',
          })));
        }
      } else {
        // Plain text format
        if (jobs.length === 0) {
          console.log('No jobs found matching criteria.');
        } else {
          for (const j of jobs) {
            console.log(`[${j.date || 'N/D'}] ${j.title} | ${j.company} (${j.location})`);
            if (j.salary) console.log(`  Salary: ${j.salary}`);
            console.log(`  URL: ${j.url}`);
            if (j.description_snippet) console.log(`  Snippet: ${j.description_snippet.slice(0, 150)}...`);
            console.log('');
          }
        }
      }

      process.exit(0);
    } catch (err: any) {
      console.error(JSON.stringify({ error: err.message, code: 'SEARCH_ERROR' }));
      process.exit(1);
    }
  }

  console.error(JSON.stringify({ error: `Unknown command "${command}". Use "search" or "categories".`, code: 'INVALID_COMMAND' }));
  process.exit(1);
}

main();
