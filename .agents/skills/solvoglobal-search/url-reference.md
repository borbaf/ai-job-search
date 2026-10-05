# Solvo Global URL & Endpoint Reference

## Base URLs
- Public Portal: `https://careers.solvoglobal.com/job-listing/`
- AJAX Endpoint: `https://careers.solvoglobal.com/wp-admin/admin-ajax.php`

## Search Endpoint (`fetch_jobs`)
- **Method:** `POST`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Payload Parameters:**
  - `action`: `fetch_jobs`
  - `page`: `1` (1-indexed page integer)
  - `title`: String keyword filter (e.g. `logistics`, `analyst`, `developer`)
  - `country`: String country filter (e.g. `Colombia`, `Mexico`)

## Response Structure
The endpoint returns JSON:
```json
{
  "html": "<article class=\"job-card\" data-id=\"...\" data-job=\"{...}\">...",
  "pagination": "<button class=\"job-page active\" data-page=\"1\">1</button>..."
}
```

Each job card in `html` contains a `data-job` JSON attribute with full job details:
- `id`: Unique base64-like hash or identifier.
- `job_code`: Job code identifier (e.g. `JPC - 7863`).
- `job_title` / `public_job_title`: Job position title.
- `country`: Country of posting.
- `city`: City location.
- `remote_job`: Remote indicator (`Yes`, `No`, or specific notes).
- `job_type`: Employment type (e.g. `Full Time`).
- `job_description`: HTML-formatted job description including responsibilities and requirements.
- `languages`: Language requirements (e.g. bilingual English/Spanish).
- `time_of_experience`: Years / level of required experience.
- `vertical`: Business area or domain (e.g. Logistics, IT, Accounting).
- `apply_job_without_registration`: Direct link to Ceipal candidate portal job detail.
- `apply_job`: Direct Ceipal application link.

## Access & Robots.txt
- `robots.txt` explicitly allows `/wp-admin/admin-ajax.php`.
- No authentication or API keys required.
