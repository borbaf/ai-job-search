# We Work Remotely - URL & Endpoint Reference

## Base URLs
- Public Portal: `https://weworkremotely.com/`
- Job Detail URL: `https://weworkremotely.com/remote-jobs/<slug>`

## Endpoints
We Work Remotely enforces Cloudflare anti-bot challenges on raw search HTML endpoints (`/remote-jobs/search?term=...`), but maintains public, high-volume RSS XML feeds syndicated directly by the platform.

### Syndicated Feeds Used:
1. `https://weworkremotely.com/remote-jobs.rss` (All latest jobs)
2. `https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss` (Operations, Management, Strategy)
3. `https://weworkremotely.com/categories/remote-product-jobs.rss` (Product Management, PO, Product Operations)
4. `https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss` (GTM, Business Development)

## Data Structure
Each `<item>` in the RSS XML feed contains:
- `<title>`: Formatted as `Company Name: Job Title`
- `<region>`: Geographic scope (e.g. `Anywhere in the World`, `USA Only`, `LATAM Only`)
- `<country>`, `<state>`: Specific local qualifiers if applicable
- `<category>`: Portal category (e.g. `Product`, `Management and Finance`, `Customer Support`)
- `<type>`: Employment type (`Full-Time`, `Contract`)
- `<pubDate>`: Publication RFC 822 date
- `<expires_at>`: Expiration date
- `<guid>` / `<link>`: Full canonical URL to the posting
- `<description>`: HTML-encoded full job description including requirements, company overview, and direct application links
