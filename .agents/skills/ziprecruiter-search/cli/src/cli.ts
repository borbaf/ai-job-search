import { parseArgs } from 'util';

interface SearchResult {
  portal: string;
  query: string;
  location: string;
  search_url: string;
  results: any[];
  note?: string;
}

function buildSearchUrl(query: string, location: string = 'Remote', days?: number): string {
  const url = new URL('https://www.ziprecruiter.com/jobs/search');
  if (query) url.searchParams.set('q', query);
  if (location) url.searchParams.set('l', location);
  if (days && days > 0) url.searchParams.set('days', String(days));
  return url.toString();
}

async function tryFetchZipRecruiter(query: string, location: string, days?: number): Promise<{ success: boolean; data?: any[]; error?: string }> {
  const targetUrl = buildSearchUrl(query, location, days);
  try {
    const res = await fetch(targetUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
      },
      signal: AbortSignal.timeout(6000),
    });

    if (res.status === 403 || res.status === 429) {
      return {
        success: false,
        error: `ZipRecruiter requires interactive browser verification (Cloudflare/PerimeterX WAF HTTP ${res.status}).`,
      };
    }

    if (!res.ok) {
      return {
        success: false,
        error: `HTTP ${res.status}: ${res.statusText}`,
      };
    }

    // In the unlikely case HTML returns directly without challenge:
    return { success: true, data: [] };
  } catch (err: any) {
    return {
      success: false,
      error: err.message || 'Fetch failed',
    };
  }
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      query: { type: 'string', short: 'q' },
      location: { type: 'string', short: 'l', default: 'Remote' },
      days: { type: 'string', short: 'd' },
      format: { type: 'string', default: 'json' },
      help: { type: 'boolean', short: 'h' },
    },
    strict: false,
    allowPositionals: true,
  });

  const command = positionals[0] || 'search';

  if (values.help || command === 'help') {
    console.log(`
ZipRecruiter Search CLI

Usage:
  bun run cli.ts search [options]
  bun run cli.ts url [options]

Options:
  -q, --query <text>       Search query (keywords, title)
  -l, --location <text>    Target location (default: Remote)
  -d, --days <number>      Max job age in days (e.g. 7, 14)
  --format <format>        Output format: json (default), table, plain
  -h, --help               Show help
    `);
    process.exit(0);
  }

  const query = (values.query as string) || '';
  const location = (values.location as string) || 'Remote';
  const days = values.days ? parseInt(values.days as string, 10) : undefined;
  const format = values.format as string;
  const searchUrl = buildSearchUrl(query, location, days);

  if (command === 'url') {
    console.log(searchUrl);
    process.exit(0);
  }

  if (command === 'search') {
    const fetchAttempt = await tryFetchZipRecruiter(query, location, days);

    const output: SearchResult = {
      portal: 'ZipRecruiter',
      query,
      location,
      search_url: searchUrl,
      results: fetchAttempt.data || [],
      note: fetchAttempt.success
        ? undefined
        : `ZipRecruiter blocks automated HTTP scraping (${fetchAttempt.error}). Use the generated direct search URL with browser tool or WebSearch fallback (site:ziprecruiter.com/jobs/ "${query}" ${location}).`,
    };

    if (format === 'json') {
      console.log(JSON.stringify(output, null, 2));
    } else if (format === 'table') {
      console.table([
        {
          Portal: output.portal,
          Query: output.query,
          Location: output.location,
          SearchURL: output.search_url,
        },
      ]);
      if (output.note) {
        console.log(`\nNote: ${output.note}`);
      }
    } else {
      console.log(`=== ZipRecruiter Search ===`);
      console.log(`Query: ${output.query}`);
      console.log(`Location: ${output.location}`);
      console.log(`Direct Search URL: ${output.search_url}`);
      if (output.note) {
        console.log(`Status / Note: ${output.note}`);
      }
    }

    process.exit(0);
  }

  console.error(JSON.stringify({ error: `Unknown command "${command}". Use "search" or "url".`, code: 'INVALID_COMMAND' }));
  process.exit(1);
}

main();
