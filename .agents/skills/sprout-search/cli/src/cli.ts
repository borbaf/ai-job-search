import { parseArgs } from 'util';

interface JobItem {
  id: string;
  title: string;
  company: string;
  location: string;
  url: string;
  date?: string;
  salary?: string;
  description_snippet?: string;
}

interface SearchResponse {
  meta: {
    portal: string;
    count: number;
    total: number;
    query?: string;
    location?: string;
    search_url?: string;
    note?: string;
  };
  results: JobItem[];
}

function buildSearchUrl(query: string, location: string = 'Remote'): string {
  const encQuery = encodeURIComponent(query);
  const encLoc = encodeURIComponent(location);
  return `https://usesprout.com/jobs?q=${encQuery}&location=${encLoc}`;
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      query: { type: 'string', short: 'q' },
      location: { type: 'string', short: 'l', default: 'Remote' },
      limit: { type: 'string', short: 'n', default: '20' },
      format: { type: 'string', default: 'json' },
      help: { type: 'boolean', short: 'h' },
    },
    strict: false,
    allowPositionals: true,
  });

  const command = positionals[0] || 'search';

  if (values.help || command === 'help') {
    console.log(`
Sprout Search CLI

Usage:
  bun run cli.ts search [options]
  bun run cli.ts url [options]

Options:
  -q, --query <text>       Search query (keywords, title)
  -l, --location <text>    Target location (default: Remote)
  -n, --limit <number>     Max number of jobs to return (default: 20)
  --format <format>        Output format: json (default), table, plain
  -h, --help               Show help
    `);
    process.exit(0);
  }

  const query = (values.query as string) || '';
  const location = (values.location as string) || 'Remote';
  const format = values.format as string;
  const searchUrl = buildSearchUrl(query, location);

  if (command === 'url') {
    console.log(searchUrl);
    process.exit(0);
  }

  if (command === 'search') {
    const results: JobItem[] = [];

    const output: SearchResponse = {
      meta: {
        portal: 'Sprout',
        count: results.length,
        total: results.length,
        query: query || undefined,
        location: location || undefined,
        search_url: searchUrl,
        note: `Sprout (sprout.ph / usesprout.com) operates as an HR platform and AI application portal. Automated direct querying uses web search fallback or direct exploration via ${searchUrl}.`,
      },
      results,
    };

    if (format === 'json') {
      console.log(JSON.stringify(output, null, 2));
    } else if (format === 'table') {
      console.table([
        {
          Portal: output.meta.portal,
          Query: output.meta.query || 'All',
          Location: output.meta.location,
          SearchURL: output.meta.search_url,
          Count: output.meta.count,
        },
      ]);
      if (output.meta.note) {
        console.log(`\nNote: ${output.meta.note}`);
      }
    } else {
      console.log(`=== Sprout Search ===`);
      console.log(`Query: ${output.meta.query || 'All'}`);
      console.log(`Location: ${output.meta.location}`);
      console.log(`Search URL: ${output.meta.search_url}`);
      if (output.meta.note) {
        console.log(`Note: ${output.meta.note}`);
      }
    }

    process.exit(0);
  }

  console.error(JSON.stringify({ error: `Unknown command "${command}". Use "search" or "url".`, code: 'INVALID_COMMAND' }));
  process.exit(1);
}

main();
