import { parseArgs } from 'util';

interface JobItem {
  id: string;
  title: string;
  company: string;
  location: string;
  region: string;
  category: string;
  type: string;
  date: string;
  expires_at: string;
  url: string;
  description_snippet?: string;
  description?: string;
}

const RSS_FEEDS = [
  'https://weworkremotely.com/remote-jobs.rss',
  'https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss',
  'https://weworkremotely.com/categories/remote-product-jobs.rss',
  'https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss'
];

const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

function decodeHtmlEntities(str: string): string {
  return str
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&');
}

function stripHtml(html: string): string {
  const decoded = decodeHtmlEntities(html);
  return decoded
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function parseTag(item: string, tag: string): string {
  const open = `<${tag}>`;
  const close = `</${tag}>`;
  const i = item.indexOf(open);
  if (i === -1) return '';
  const j = item.indexOf(close, i + open.length);
  if (j === -1) return '';
  return item.slice(i + open.length, j).trim();
}

function parsePubDate(rawDate: string): string {
  try {
    const d = new Date(rawDate);
    if (!isNaN(d.getTime())) {
      return d.toISOString().split('T')[0];
    }
  } catch {}
  return rawDate;
}

async function fetchFeed(url: string): Promise<string> {
  const res = await fetch(url, {
    headers: {
      'User-Agent': USER_AGENT,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
    },
    signal: AbortSignal.timeout(15000),
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch RSS from ${url}: HTTP ${res.status}`);
  }

  return await res.text();
}

function parseItemsFromXml(xml: string): JobItem[] {
  const rawItems = xml.split('<item>').slice(1);
  const jobs: JobItem[] = [];

  for (const raw of rawItems) {
    const itemContent = raw.split('</item>')[0];
    const rawTitle = decodeHtmlEntities(parseTag(itemContent, 'title'));
    let company = '';
    let title = rawTitle;

    const colonIdx = rawTitle.indexOf(': ');
    if (colonIdx !== -1) {
      company = rawTitle.slice(0, colonIdx).trim();
      title = rawTitle.slice(colonIdx + 2).trim();
    }

    const region = decodeHtmlEntities(parseTag(itemContent, 'region')) || 'Remote';
    const country = decodeHtmlEntities(parseTag(itemContent, 'country'));
    const category = decodeHtmlEntities(parseTag(itemContent, 'category'));
    const type = decodeHtmlEntities(parseTag(itemContent, 'type')) || 'Full-Time';
    const pubDate = parsePubDate(parseTag(itemContent, 'pubDate'));
    const expiresAt = parsePubDate(parseTag(itemContent, 'expires_at'));
    const link = parseTag(itemContent, 'link') || parseTag(itemContent, 'guid');
    const rawDesc = parseTag(itemContent, 'description');

    const cleanDesc = stripHtml(rawDesc);
    const snippet = cleanDesc.slice(0, 300) + (cleanDesc.length > 300 ? '...' : '');

    const idMatch = link.match(/remote-jobs\/([^/?#]+)/);
    const id = idMatch ? idMatch[1] : link;

    let location = 'Remote';
    if (region && region.toLowerCase() !== 'anywhere in the world') {
      location = country ? `${region}, ${country}` : region;
    }

    jobs.push({
      id,
      title,
      company,
      location,
      region,
      category,
      type,
      date: pubDate,
      expires_at: expiresAt,
      url: link,
      description_snippet: snippet,
      description: cleanDesc,
    });
  }

  return jobs;
}

async function searchJobs(options: {
  query?: string;
  category?: string;
  limit?: number;
  format?: string;
}) {
  const query = options.query?.toLowerCase().trim() || '';
  const limit = options.limit || 20;
  const format = options.format || 'json';

  const seenIds = new Set<string>();
  const allJobs: JobItem[] = [];

  for (const feedUrl of RSS_FEEDS) {
    try {
      const xml = await fetchFeed(feedUrl);
      const parsed = parseItemsFromXml(xml);
      for (const j of parsed) {
        if (!seenIds.has(j.id)) {
          seenIds.add(j.id);
          allJobs.push(j);
        }
      }
    } catch (err: any) {
      // Continue with other feeds if one fails
    }
  }

  let filtered = allJobs;
  if (query) {
    const terms = query.split(/\s+/).filter(Boolean);
    filtered = filtered.filter(j => {
      const target = `${j.title} ${j.company} ${j.category} ${j.description || ''}`.toLowerCase();
      return terms.every(t => target.includes(t));
    });
  }

  if (options.category) {
    const cat = options.category.toLowerCase();
    filtered = filtered.filter(j => j.category.toLowerCase().includes(cat));
  }

  const results = filtered.slice(0, limit);

  if (format === 'json') {
    console.log(JSON.stringify(results.map(j => ({
      id: j.id,
      title: j.title,
      company: j.company,
      location: j.location,
      region: j.region,
      category: j.category,
      type: j.type,
      date: j.date,
      expires_at: j.expires_at,
      url: j.url,
      description_snippet: j.description_snippet,
    })), null, 2));
  } else if (format === 'table') {
    if (results.length === 0) {
      console.log('No jobs found.');
      return;
    }
    console.table(results.map(j => ({
      Title: j.title.slice(0, 35),
      Company: j.company.slice(0, 20),
      Category: j.category.slice(0, 18),
      Location: j.location.slice(0, 20),
      Date: j.date,
    })));
  } else {
    for (const j of results) {
      console.log(`[${j.date}] ${j.title} - ${j.company}`);
      console.log(`Location: ${j.location} | Category: ${j.category}`);
      console.log(`URL: ${j.url}`);
      console.log(`Snippet: ${j.description_snippet}\n`);
    }
  }
}

async function getJobDetail(idOrUrl: string, format = 'json') {
  let targetId = idOrUrl;
  if (idOrUrl.includes('weworkremotely.com/remote-jobs/')) {
    const m = idOrUrl.match(/remote-jobs\/([^/?#]+)/);
    if (m) targetId = m[1];
  }

  // Look in the RSS feeds
  for (const feedUrl of RSS_FEEDS) {
    try {
      const xml = await fetchFeed(feedUrl);
      const parsed = parseItemsFromXml(xml);
      const match = parsed.find(j => j.id === targetId || j.url.includes(targetId));
      if (match) {
        if (format === 'plain') {
          console.log(`Title: ${match.title}`);
          console.log(`Company: ${match.company}`);
          console.log(`Location: ${match.location}`);
          console.log(`Category: ${match.category}`);
          console.log(`Type: ${match.type}`);
          console.log(`Posted: ${match.date}`);
          console.log(`Expires: ${match.expires_at}`);
          console.log(`URL: ${match.url}\n`);
          console.log(`--- DESCRIPTION ---`);
          console.log(match.description);
        } else {
          console.log(JSON.stringify(match, null, 2));
        }
        return;
      }
    } catch {}
  }

  console.error(JSON.stringify({ error: `Job not found: ${idOrUrl}`, code: 'NOT_FOUND' }));
  process.exit(1);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    console.log(`
We Work Remotely Search CLI (weworkremotely-search)

Usage:
  bun run cli.ts search [flags]
  bun run cli.ts detail <id|url> [flags]

Search Flags:
  -q, --query <text>     Keyword search across title, company, category, description
  -c, --category <text>  Filter by category (Product, Management, etc.)
  -n, --limit <number>   Max results (default: 20)
  --format <format>      Output format: json (default), table, plain

Detail Flags:
  --format <format>      Output format: json (default), plain
`);
    return;
  }

  if (command === 'search') {
    const { values } = parseArgs({
      args: args.slice(1),
      options: {
        query: { type: 'string', short: 'q' },
        category: { type: 'string', short: 'c' },
        limit: { type: 'string', short: 'n' },
        format: { type: 'string' },
      },
      strict: false,
    });

    await searchJobs({
      query: values.query as string | undefined,
      category: values.category as string | undefined,
      limit: values.limit ? parseInt(values.limit as string, 10) : 20,
      format: (values.format as string) || 'json',
    });
  } else if (command === 'detail') {
    const idOrUrl = args[1];
    if (!idOrUrl) {
      console.error(JSON.stringify({ error: 'Missing job ID or URL', code: 'INVALID_ARGS' }));
      process.exit(1);
    }

    const { values } = parseArgs({
      args: args.slice(2),
      options: {
        format: { type: 'string' },
      },
      strict: false,
    });

    await getJobDetail(idOrUrl, (values.format as string) || 'json');
  } else {
    console.error(JSON.stringify({ error: `Unknown command: ${command}`, code: 'UNKNOWN_COMMAND' }));
    process.exit(1);
  }
}

main().catch(err => {
  console.error(JSON.stringify({ error: err.message, code: 'UNEXPECTED_ERROR' }));
  process.exit(1);
});
