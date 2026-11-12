# A: Cloudflare Worker + Access + GitHub Actions trigger (research notes)

Access note: WebFetch failed with DNS errors (ENOTFOUND) for developers.cloudflare.com and docs.github.com. The official pages were downloaded with curl through the proxy and converted to text. Labels: [D] official doc (fetched via curl), [B] full text read, [O] search summary, NOT FOUND = not found in the sources checked.

Known gaps: the Cloudflare Workers rate-limiting binding page returned unrelated content (CORS example), so it is NOT FOUND. The Access service-token header names are NOT FOUND in the fetched copy. The GitHub App installation-token TTL is NOT FOUND in the fetched copy.

## 1. Cloudflare Worker (free plan)

- Requests: 100,000 requests/day on Workers Free, reset at midnight UTC. Over the limit returns Error 1027. [D] https://developers.cloudflare.com/workers/platform/limits/
- CPU time: 10 ms per HTTP request on Free. Paid default is 30 s, max 5 min. Waiting on fetch() does not count as CPU time. [D] same page
- CPU overrun returns Error 1102 "Worker exceeded resource limits". [D] same page
- Subrequests: 50 per invocation on Free (1,000 to internal services). [D] same page
- Variables and secrets combined: 64 per Worker on Free; 5 KB per value. [D] same page
- Worker size: 64 MiB uncompressed. Memory: 128 MB per isolate. [D] same page
- Secrets: "encrypted text values" for keys and tokens. `wrangler secret put` adds one and deploys a new version immediately. Value is hidden in Wrangler and the dashboard. [D] https://developers.cloudflare.com/workers/configuration/secrets/
- Local dev uses `.dev.vars` (or `.env`) next to the Wrangler config file, not committed. [D] same page
- `wrangler versions secret put` creates a version without deploying it (for gradual deployments). [D] same page
- CORS: a Worker reverses the CORS problem by setting `Access-Control-Allow-Origin` to the caller's origin, adding `Vary: Origin`, and answering OPTIONS preflight with Allow-Methods/Allow-Headers. Example uses `*` for preflight. [D] Cloudflare CORS proxy example (Workers examples page)

## 2. Cloudflare Access (Zero Trust)

- Free plan user limit: 50 users. [O] Cloudflare pricing page (via search summary; the fetched plans page had no numbers). Community thread reports a possible billing caveat above free limits, unofficial, verify in dashboard.
- Login methods: One-time PIN (email), and third-party identity providers such as GitHub (listed as a provider type). OTP PIN expires 10 minutes after request. [D] https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/ ; GitHub as IdP [O]
- Passing the request: Access adds `Cf-Access-Jwt-Assertion` header to requests to the origin; browsers also get a `CF_Authorization` cookie. Cloudflare recommends validating the header, not the cookie. [D] https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/
- JWT validation: public keys at `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs` (current and previous key, during rotation). Check signature, `iss` = `https://<team>.cloudflareaccess.com`, and `aud` = the application AUD tag (fixed unless the Access app is deleted or recreated). Sample uses the jose npm package. [D] same page
- Expiry (`exp`) check: not explicitly stated on the page; the jose library's default validation covers it (verify in code). [B]
- Service tokens: exist for automated callers (Client ID and Client Secret). Secrets can be rotated, with a grace period from 1 hour to 30 days, or revoked immediately. [D] https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/ . Exact request header names NOT FOUND in the fetched copy.

## 3. Triggering GitHub Actions

- workflow_dispatch: `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches`; `workflow_id` may be the file name (e.g. `deploy.yml`). [D] https://docs.github.com/en/rest/actions/workflows
- Body: `ref` (required, branch or tag), optional `inputs`. The workflow file must have `on: workflow_dispatch`. [D] same page
- Success: 204 No Content, no body (run ID is not returned). [D] same page
- Permissions: fine-grained PAT needs Actions repository permission = write (read for listing workflows). [D] same page
- repository_dispatch: `POST /repos/{owner}/{repo}/dispatches` with `event_type` and optional `client_payload` (JSON, max size not checked). Success 204. [D] https://docs.github.com/en/rest/repos/repos (curl copy)
- Finding the run after dispatch: `GET /repos/{owner}/{repo}/actions/runs` (filter by `event`, `status`, `branch`, per_page up to 100). Single run: `GET /repos/{owner}/{repo}/actions/runs/{run_id}`; it includes `status`, `conclusion`, `logs_url`, `artifacts_url`. [D] https://docs.github.com/en/rest/actions/workflow-runs
- Jobs and logs: `logs_url` returns 302 with a Location header to a zip download. [D] same page
- Artifacts: list at `artifacts_url`; each has `archive_download_url` (`.../artifacts/{id}/zip`) and `expired` flag. Download needs a token. [D] https://docs.github.com/en/rest/actions/artifacts
- Token lifetime: fine-grained PAT expiry 1 to 366 days (default 30 days when using the creation URL with no expiry given); no-expiry allowed unless org policy blocks it. Tokens unused for a year are removed. [D] https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- GitHub App installation token lifetime: NOT FOUND in fetched copy (commonly 1 hour; verify). Fetched file was not the right page.
- Rate limits: PAT 5,000 req/hour. GitHub App installation token: at least 5,000 req/hour, scales up to 12,500/hour with repos/users. GITHUB_TOKEN 1,000 req/hour per repo. [D] https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- Secondary limits: 900 points/min on REST endpoints; 80 content-creating requests/minute and 500/hour. Whether a dispatch counts as content creation is NOT FOUND. [D] same page

## 4. Security and cost control (design notes, from the sources above)

- Key stays on the Worker: store the GitHub token with `wrangler secret put`; the browser never receives it. [D] secrets page
- Owner check: validate `Cf-Access-Jwt-Assertion` (sig, iss, aud, exp) before any GitHub call. [D] JWT page
- Free limits for abuse control: 100k Worker requests/day and 10 ms CPU per request bound total cost. Dispatch budget per day: no source found; implement own counter with a KV or Durable Object (Durable Objects on free plan: NOT verified). Rate-limiting binding: NOT FOUND.
- GitHub side: fine-grained PAT restricted to one repository with Actions write only; short expiry.

## 5. Pages Functions vs Worker, deployment

- Pages Functions run on Cloudflare Workers; they are part of Pages projects and handle `functions/` routes. [D] https://developers.cloudflare.com/pages/functions/ (short description only)
- Wrangler is the Workers CLI; commands use the authenticated member's or API token's permissions. [D] https://developers.cloudflare.com/workers/wrangler/ (short intro only)
- Deploy from GitHub Actions with `wrangler deploy` (CI deploy using an API token stored as a GitHub secret): NOT verified in fetched pages.

## Recommended direction (short)

- Simple owner-only trigger: one Worker, Access app in front of it (OTP or GitHub IdP, 1 user), Worker checks the JWT, then calls workflow_dispatch with a fine-grained PAT stored as a Worker secret. Status: `GET .../actions/runs` and `logs_url`.
- Limits to design around: 10 ms CPU per request, 50 subrequests per request, 64 secrets/vars, and the GitHub REST rate limit.

## Remaining gaps

- Access free-plan user cap: confirmed only by search summary, not on an official page.
- Access service token header names: NOT FOUND.
- Workers rate-limiting binding and Durable Objects free-plan availability: NOT FOUND.
- GitHub App installation token TTL: NOT FOUND.
- Whether workflow_dispatch counts toward content-creation secondary limit: NOT FOUND.
