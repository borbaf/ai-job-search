import { parseArgs } from 'util';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

interface JobItem {
  id: string;
  title: string;
  company: string;
  tenant: string;
  location: string;
  workplace_type: string;
  url: string;
  status: string;
  description?: string;
}

const API_BASE = 'https://api.inhire.app';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

function normalizeText(text: string): string {
  if (!text) return '';
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function stripHtml(html: string): string {
  if (!html) return '';
  return html
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&quot;/gi, '"')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/\s+/g, ' ')
    .trim();
}

function loadTenants(): Record<string, { name: string; count: number }> {
  try {
    const p = join(__dirname, 'tenants.json');
    return JSON.parse(readFileSync(p, 'utf-8'));
  } catch {
    return {
      nstech: { name: 'NSTECH', count: 100 },
      mottu: { name: 'Mottu', count: 50 },
      wilsonsonsoffshore: { name: 'Wilson Sons', count: 10 },
      autoglass: { name: 'Autoglass', count: 10 },
      agrosearch: { name: 'AgroSearch', count: 15 },
      nuvemshop: { name: 'Nuvemshop', count: 20 },
    };
  }
}

async function fetchTenantJobs(tenant: string, tenantName: string): Promise<JobItem[]> {
  try {
    const res = await fetch(`${API_BASE}/job-posts/public/pages`, {
      headers: {
        'User-Agent': USER_AGENT,
        'X-Tenant': tenant,
      },
      signal: AbortSignal.timeout(6000),
    });
    if (!res.ok) return [];
    const data: any = await res.json();
    const list = data.jobsPage || [];
    const company = data.tenantName || tenantName || tenant;

    return list.map((j: any) => {
      const jobId = j.jobId;
      const title = (j.displayName || '').trim();
      return {
        id: `${tenant}:${jobId}`,
        title,
        company,
        tenant,
        location: j.location || 'Brasil',
        workplace_type: j.workplaceType || 'Unspecified',
        url: `https://${tenant}.inhire.app/vagas/${jobId}`,
        status: j.status || 'published',
      };
    });
  } catch {
    return [];
  }
}

async function fetchJobDetail(tenant: string, jobId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/job-posts/public/pages/${jobId}`, {
    headers: {
      'User-Agent': USER_AGENT,
      'X-Tenant': tenant,
    },
    signal: AbortSignal.timeout(8000),
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch job detail (${res.status})`);
  }
  return res.json();
}

async function handleSearch(args: string[]) {
  const { values } = parseArgs({
    args,
    options: {
      query: { type: 'string', short: 'q' },
      tenant: { type: 'string', short: 't' },
      remote: { type: 'boolean' },
      limit: { type: 'string', short: 'n', default: '30' },
      format: { type: 'string', default: 'json' },
    },
    allowPositionals: true,
  });

  const queryTerms = (values.query || '')
    .split(/\s+/)
    .map(t => normalizeText(t.trim()))
    .filter(Boolean);

  const limit = parseInt(values.limit || '30', 10);
  const tenantsMap = loadTenants();
  let tenantsToScan: Array<[string, string]> = [];

  if (values.tenant) {
    const t = values.tenant.toLowerCase();
    tenantsToScan = [[t, tenantsMap[t]?.name || t]];
  } else {
    tenantsToScan = Object.entries(tenantsMap).map(([k, v]) => [k, v.name]);
  }

  // Scan tenants concurrently with a concurrency limit
  const batchSize = 12;
  const allJobs: JobItem[] = [];

  for (let i = 0; i < tenantsToScan.length; i += batchSize) {
    const batch = tenantsToScan.slice(i, i + batchSize);
    const results = await Promise.all(
      batch.map(([t, name]) => fetchTenantJobs(t, name))
    );
    for (const jobList of results) {
      for (const job of jobList) {
        if (values.remote && !job.workplace_type.toLowerCase().includes('remote')) {
          continue;
        }

        if (queryTerms.length > 0) {
          const text = normalizeText(`${job.title} ${job.company} ${job.location}`);
          const matches = queryTerms.every(term => text.includes(term));
          if (!matches) continue;
        }

        allJobs.push(job);
      }
    }
  }

  const output = allJobs.slice(0, limit);

  if (values.format === 'json') {
    console.log(JSON.stringify(output, null, 2));
  } else if (values.format === 'table') {
    console.table(
      output.map(j => ({
        Company: j.company,
        Title: j.title,
        Location: j.location,
        Workplace: j.workplace_type,
        URL: j.url,
      }))
    );
  } else {
    for (const j of output) {
      console.log(`[${j.company}] ${j.title} (${j.workplace_type} - ${j.location})`);
      console.log(`  URL: ${j.url}\n`);
    }
  }
}

async function handleDetail(args: string[]) {
  const { values, positionals } = parseArgs({
    args,
    options: {
      format: { type: 'string', default: 'json' },
    },
    allowPositionals: true,
  });

  const target = positionals[0];
  if (!target) {
    console.error(JSON.stringify({ error: 'Missing target jobId or URL', code: 'INVALID_INPUT' }));
    process.exit(1);
  }

  let tenant = '';
  let jobId = '';

  if (target.includes('inhire.app/vagas/')) {
    const urlMatch = target.match(/https?:\/\/([a-zA-Z0-9_-]+)\.inhire\.app\/vagas\/([a-zA-Z0-9_-]+)/);
    if (urlMatch) {
      tenant = urlMatch[1];
      jobId = urlMatch[2];
    }
  } else if (target.includes(':')) {
    const parts = target.split(':');
    tenant = parts[0];
    jobId = parts[1];
  }

  if (!tenant || !jobId) {
    console.error(JSON.stringify({ error: 'Invalid identifier. Use "<tenant>:<jobId>" or "https://<tenant>.inhire.app/vagas/<jobId>"', code: 'INVALID_ID' }));
    process.exit(1);
  }

  try {
    const data = await fetchJobDetail(tenant, jobId);
    const item: JobItem = {
      id: `${tenant}:${jobId}`,
      title: (data.displayName || '').trim(),
      company: data.tenantName || tenant,
      tenant,
      location: data.location || 'Brasil',
      workplace_type: data.workplaceType || 'Unspecified',
      url: `https://${tenant}.inhire.app/vagas/${jobId}`,
      status: data.status || 'published',
      description: stripHtml(data.description || ''),
    };

    if (values.format === 'plain') {
      console.log(`Title: ${item.title}`);
      console.log(`Company: ${item.company}`);
      console.log(`Location: ${item.location} (${item.workplace_type})`);
      console.log(`URL: ${item.url}\n`);
      console.log(`Description:\n${item.description}`);
    } else {
      console.log(JSON.stringify(item, null, 2));
    }
  } catch (err: any) {
    console.error(JSON.stringify({ error: err.message, code: 'FETCH_ERROR' }));
    process.exit(1);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help') {
    console.log(`InHire Search CLI
Usage:
  bun run cli.ts search [options]
  bun run cli.ts detail <tenant:jobId|URL> [options]

Search Options:
  -q, --query <text>     Search keywords across title and company
  -t, --tenant <name>    Scan specific tenant (e.g. nstech, mottu)
  --remote               Filter only remote positions
  -n, --limit <n>        Limit results (default: 30)
  --format <fmt>         Output format: json (default), table, plain
`);
    return;
  }

  if (command === 'search') {
    await handleSearch(args.slice(1));
  } else if (command === 'detail') {
    await handleDetail(args.slice(1));
  } else {
    console.error(JSON.stringify({ error: `Unknown command: ${command}`, code: 'UNKNOWN_COMMAND' }));
    process.exit(1);
  }
}

main().catch(err => {
  console.error(JSON.stringify({ error: err.message, code: 'INTERNAL_ERROR' }));
  process.exit(1);
});
