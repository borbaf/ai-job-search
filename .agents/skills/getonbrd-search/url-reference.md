# Get on Board (getonbrd.com) URL and API Reference

**Portal:** Get on Board (`https://www.getonbrd.com/`)
**Target market:** Latin America and international remote tech jobs (Chile, Colombia, Mexico, Argentina, Peru, Brazil, Global Remote).
**Authentication:** None required for public job search (`/api/v0/search/jobs` and `/api/v0/categories/<category>/jobs`).

---

## 1. Official Public REST API (`v0`)

Get on Board exposes an official public JSON REST API with zero authentication requirements for published listings.

- **Base URL:** `https://www.getonbrd.com/api/v0`
- **User-Agent:** Honest UA or standard browser header (e.g. `Mozilla/5.0...` or `ai-job-search/getonbrd-search`).

### Endpoints

#### 1. Search Jobs
- **Method:** `GET`
- **URL:** `https://www.getonbrd.com/api/v0/search/jobs`
- **Query Parameters:**
  - `query` (string): Search terms, e.g. `python`, `data`, `operations`, `supply chain`, `product manager`.
  - `page` (integer): Page number (1-indexed). Default: 1.
  - `per_page` (integer): Items per page. Max: 100 or default ~20.
  - `expand[]` (string): Relationship expansion, e.g. `expand[]=company` or `expand=["company"]` (expands company details and attributes directly into the response payload).

#### 2. Category Jobs
- **Method:** `GET`
- **URL:** `https://www.getonbrd.com/api/v0/categories/<category-slug>/jobs`
- **Slugs:** `programming`, `data-science-analytics`, `operations-management`, `machine-learning-ai`, `sysadmin-devops-qa`, `product-commercial`, etc.
- **Query Parameters:**
  - `page` (integer)
  - `per_page` (integer)
  - `expand[]` (string)

#### 3. Categories List
- **Method:** `GET`
- **URL:** `https://www.getonbrd.com/api/v0/categories`

---

## 2. Detail Endpoint & HTML Fallback

### Direct API Search Payload
The search response contains rich detailed attributes for every job directly:
- `id`: Unique slug identifier (e.g. `software-developer-full-stack-react-ror-rankmi-remote`).
- `attributes.title`: Job title.
- `attributes.description`: Full HTML description.
- `attributes.description_headline`: Section headline.
- `attributes.functions`: Responsibilities HTML.
- `attributes.functions_headline`: Section headline.
- `attributes.desirable`: Requirements/qualifications HTML.
- `attributes.desirable_headline`: Section headline.
- `attributes.benefits`: Benefits HTML.
- `attributes.remote`: Boolean (`true` / `false`).
- `attributes.remote_modality`: Modality string (`remote_local`, `fully_remote`, `hybrid`, `no_remote`).
- `attributes.remote_zone`: Allowed timezone or geo-fencing (e.g. `UTC-5 to UTC-3`, `Latin America`).
- `attributes.countries`: Array of country names or `["Remote"]`.
- `attributes.min_salary` & `attributes.max_salary`: Numerical bounds (when public).
- `attributes.published_at`: Epoch timestamp (seconds).
- `attributes.company.data.attributes.name`: Company name.
- `links.public_url`: Web link to posting on Get on Board.

### Web Detail Page
- **URL:** `https://www.getonbrd.com/jobs/<slug>` or `https://www.getonbrd.com/jobs/<category>/<slug>`.
- The direct web page issues a 301 redirect to canonical category URL and renders semantic HTML (`itemprop="title"`, `itemprop="name"`, `itemprop="description"`).
- In the CLI, `detail <id|url>` first queries the search API for the exact slug to pull the full structured attributes, and falls back to fetching and parsing the public HTML page if needed.

---

## 3. Rate Limiting and Etiquette
- Backoff gracefully on HTTP 429.
- Use modest page sizes (`per_page=20` to `50`).
- No credentials or API keys needed.
