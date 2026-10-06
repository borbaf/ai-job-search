import { parseArgs } from 'util';

interface JobItem {
  id: string;
  title: string;
  company: string;
  location: string;
  type: string;
  category: string;
  seniority?: string;
  salary?: string;
  date: string;
  expires_at?: string;
  url: string;
  external_url?: string;
  description_snippet?: string;
  description?: string;
  tags?: string[];
  requirements?: string[];
}

const API_BASE = 'https://api.remotar.com.br';
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

function formatSalary(jobSalary: any): string | undefined {
  if (!jobSalary || jobSalary.type === 'uninformed') return undefined;
  if (jobSalary.from && jobSalary.to) {
    return `${jobSalary.currency || 'BRL'} ${jobSalary.from} - ${jobSalary.to}`;
  }
  if (jobSalary.from) {
    return `A partir de ${jobSalary.currency || 'BRL'} ${jobSalary.from}`;
  }
  if (jobSalary.to) {
    return `Até ${jobSalary.currency || 'BRL'} ${jobSalary.to}`;
  }
  return undefined;
}

function mapApiJob(raw: any): JobItem {
  const id = String(raw.id);
  const title = (raw.title || '').trim();
  const company = raw.company?.name || raw.companyDisplayName || 'Empresa Confidencial';
  
  const tags: string[] = [];
  let seniority: string | undefined;
  if (Array.isArray(raw.jobTags)) {
    for (const jt of raw.jobTags) {
      if (jt.tag?.name) {
        tags.push(jt.tag.name);
        if (jt.tag.name.includes('Júnior') || jt.tag.name.includes('Pleno') || jt.tag.name.includes('Sênior') || jt.tag.name.includes('Especialista') || jt.tag.name.includes('Estágio')) {
          seniority = jt.tag.name.replace(/^[^\w]+/, '').trim();
        }
      }
    }
  }

  const categories: string[] = [];
  if (Array.isArray(raw.jobCategories)) {
    for (const jc of raw.jobCategories) {
      if (jc.category?.name) categories.push(jc.category.name);
    }
  }

  const requirements: string[] = [];
  if (Array.isArray(raw.jobRequirements)) {
    for (const req of raw.jobRequirements) {
      if (req.description) {
        requirements.push(`${req.mandatory ? '[Obrigatório] ' : ''}${req.description}`);
      }
    }
  }

  const descText = stripHtml(raw.description || raw.moreInfos || '');
  const url = `https://remotar.com.br/job/${id}`;
  const external_url = raw.externalLink || undefined;

  let date = '';
  if (raw.createdAt) {
    date = raw.createdAt.slice(0, 10);
  }

  return {
    id,
    title,
    company,
    location: raw.type === 'remote' ? '100% Remoto' : (raw.city ? `${raw.city}, ${raw.state || ''}` : 'Remoto / Brasil'),
    type: raw.type || 'remote',
    category: categories.join(', ') || 'Geral',
    seniority,
    salary: formatSalary(raw.jobSalary),
    date,
    expires_at: raw.expiresAt ? raw.expiresAt.slice(0, 10) : undefined,
    url,
    external_url,
    description_snippet: descText.slice(0, 300) + (descText.length > 300 ? '...' : ''),
    description: descText,
    tags,
    requirements
  };
}

async function searchJobs(options: {
  query?: string;
  category?: string;
  limit?: number;
}): Promise<JobItem[]> {
  const limit = options.limit || 20;
  const searchParam = options.query ? encodeURIComponent(options.query) : '';
  const url = `${API_BASE}/jobs?search=${searchParam}&per_page=${Math.min(limit, 50)}`;

  const res = await fetch(url, {
    headers: {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(15000)
  });

  if (!res.ok) {
    throw new Error(`Remotar API returned HTTP ${res.status}`);
  }

  const data = await res.json();
  const jobs: JobItem[] = [];

  if (Array.isArray(data.data)) {
    for (const raw of data.data) {
      const item = mapApiJob(raw);
      if (options.category) {
        const catLower = options.category.toLowerCase();
        if (!item.category.toLowerCase().includes(catLower)) {
          continue;
        }
      }
      jobs.push(item);
      if (jobs.length >= limit) break;
    }
  }

  return jobs;
}

async function getJobDetail(idOrUrl: string): Promise<JobItem> {
  let id = idOrUrl.trim();
  const match = id.match(/\/job\/(\d+)/);
  if (match) {
    id = match[1];
  }

  const url = `${API_BASE}/jobs/${id}`;
  const res = await fetch(url, {
    headers: {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json'
    },
    signal: AbortSignal.timeout(15000)
  });

  if (!res.ok) {
    throw new Error(`Remotar API detail returned HTTP ${res.status} for job ${id}`);
  }

  const raw = await res.json();
  return mapApiJob(raw);
}

function printHelp(): void {
  console.log(`remotar-search - Search live remote jobs on Remotar (remotar.com.br)

USAGE:
  bun run cli.ts search [options]
  bun run cli.ts detail <id|url> [options]

COMMANDS:
  search                  Search remote jobs
  detail <id|url>         Get full details of a single posting

OPTIONS:
  -q, --query <text>      Search keyword (e.g. "supply chain", "logistica", "dados")
  -c, --category <name>   Filter by category
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
            ID: r.id,
            Title: r.title.slice(0, 35),
            Company: r.company.slice(0, 20),
            Date: r.date,
            Seniority: r.seniority || 'N/I',
            Category: r.category.slice(0, 20)
          }))
        );
      } else if (values.format === 'plain') {
        for (const r of results) {
          console.log(`\n[${r.id}] ${r.title} - ${r.company}`);
          console.log(`Local: ${r.location} | Data: ${r.date} | Senioridade: ${r.seniority || 'N/I'}`);
          if (r.salary) console.log(`Salário: ${r.salary}`);
          console.log(`URL Remotar: ${r.url}`);
          if (r.external_url) console.log(`Candidatura Direta: ${r.external_url}`);
          if (r.description_snippet) console.log(`Resumo: ${r.description_snippet}`);
        }
      } else {
        console.log(JSON.stringify(results, null, 2));
      }
    } catch (err: any) {
      console.error(JSON.stringify({ error: err.message, code: 'SEARCH_FAILED' }));
      process.exit(1);
    }
  } else if (command === 'detail') {
    const target = args[1];
    if (!target) {
      console.error(JSON.stringify({ error: 'Missing job ID or URL', code: 'MISSING_TARGET' }));
      process.exit(1);
    }

    const { values } = parseArgs({
      args: args.slice(2),
      options: {
        format: { type: 'string', short: 'f', default: 'json' },
        help: { type: 'boolean', short: 'h' }
      },
      allowPositionals: true
    });

    try {
      const detail = await getJobDetail(target);
      if (values.format === 'plain') {
        console.log(`\n========================================`);
        console.log(`${detail.title}`);
        console.log(`Empresa: ${detail.company}`);
        console.log(`Localização: ${detail.location}`);
        console.log(`Data: ${detail.date} | Senioridade: ${detail.seniority || 'N/I'}`);
        if (detail.salary) console.log(`Salário: ${detail.salary}`);
        console.log(`URL Remotar: ${detail.url}`);
        if (detail.external_url) console.log(`Candidatura Direta: ${detail.external_url}`);
        console.log(`========================================\n`);
        if (detail.requirements && detail.requirements.length > 0) {
          console.log('Requisitos:');
          detail.requirements.forEach(req => console.log(` - ${req}`));
          console.log();
        }
        console.log('Descrição:');
        console.log(detail.description);
      } else {
        console.log(JSON.stringify(detail, null, 2));
      }
    } catch (err: any) {
      console.error(JSON.stringify({ error: err.message, code: 'DETAIL_FAILED' }));
      process.exit(1);
    }
  } else {
    console.error(JSON.stringify({ error: `Unknown command "${command}"`, code: 'UNKNOWN_COMMAND' }));
    printHelp();
    process.exit(1);
  }
}

main();
