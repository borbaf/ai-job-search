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
    search_url: string;
    note?: string;
  };
  results: JobItem[];
}

function buildSearchUrl(query: string): string {
  const encQuery = encodeURIComponent(query);
  return `https://jobnagringa.com.br/?search=${encQuery}`;
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      query: { type: 'string', short: 'q' },
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
Job na Gringa Search CLI

Usage:
  bun run cli.ts search [options]
  bun run cli.ts url [options]

Options:
  -q, --query <text>       Search query (keywords, title)
  -n, --limit <number>     Max number of jobs to return (default: 20)
  --format <format>        Output format: json (default), table, plain
  -h, --help               Show help
    `);
    process.exit(0);
  }

  const query = (values.query as string) || '';
  const format = values.format as string;
  const searchUrl = buildSearchUrl(query);

  if (command === 'url') {
    console.log(searchUrl);
    process.exit(0);
  }

  if (command === 'search') {
    const results: JobItem[] = [];

    const output: SearchResponse = {
      meta: {
        portal: 'Job na Gringa',
        count: results.length,
        total: results.length,
        query: query || undefined,
        search_url: searchUrl,
        note: `Job na Gringa (jobnagringa.com.br) é uma comunidade privada e plataforma de curadoria de vagas remotas internacionais para brasileiros. O mural de vagas e canais de recrutadores estão disponíveis diretamente no portal e nos canais de membros (Discord).`,
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
          SearchURL: output.meta.search_url,
          Count: output.meta.count,
        },
      ]);
      if (output.meta.note) {
        console.log(`\nNota: ${output.meta.note}`);
      }
    } else {
      console.log(`=== Job na Gringa Search ===`);
      console.log(`Query: ${output.meta.query || 'All'}`);
      console.log(`URL do Portal: ${output.meta.search_url}`);
      if (output.meta.note) {
        console.log(`Nota: ${output.meta.note}`);
      }
    }

    process.exit(0);
  }

  console.error(JSON.stringify({ error: `Unknown command "${command}". Use "search" or "url".`, code: 'INVALID_COMMAND' }));
  process.exit(1);
}

main();
