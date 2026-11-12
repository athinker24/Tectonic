# B: GitHub Actions runners and storage options (2026 notes)

Status: DONE (research pass). Accessed 2026-11-12.
Access note: docs.github.com failed in WebFetch with DNS error (ENOTFOUND). Pages were downloaded with curl through the agent proxy (HTTP 200) and converted to text with the local oku.py helper. No TLS or bot protection was bypassed. Cloudflare, PyPI, anaconda.org and raw.githubusercontent.com were reachable the same way.

Labels: [D] official documentation or official registry metadata / [B] full text of a page (converted) / [O] search summary (none used) / BULUNAMADI = not found in the fetched text.

## 1. GitHub-hosted runners (2026)

### Hardware (ubuntu-latest and related labels)
- Public repo, `ubuntu-latest` (Linux x64, 4 vCPU, 16 GB RAM, 14 GB SSD). Matches the premise. [D] https://docs.github.com/en/actions/reference/runners/github-hosted-runners : "Use of the standard GitHub-hosted runners is free and unlimited on public repositories."
- Private repo, `ubuntu-latest` (Linux x64, 2 vCPU, **8 GB** RAM, 14 GB SSD). NOTE: the premise said 7 GB; the 2026 table says 8 GB. [D] same URL, private table.
- Private repo, arm64 Linux (`ubuntu-24.04-arm`, etc.): 2 vCPU, 8 GB, 14 GB SSD. [D] same URL.
- Single-CPU `ubuntu-slim`: 1 vCPU, 5 GB, 14 GB SSD, 15 min job timeout. [D] same URL.
- Larger runners: available for Team and Enterprise Cloud orgs; billed also on public repos; more RAM/CPU/disk, static IPs, GPU. Exact larger-runner prices: BULUNAMADI in fetched text (only "billed for public repositories"). [B] same URL.

### Limits
- Job execution time: 6 hours per job. [D] https://docs.github.com/en/actions/reference/limits : "Each job in a workflow can run for up to 6 hours of execution time."
- Workflow run time: 35 days per workflow run (includes waiting and approvals). [D] same URL.
- Concurrent standard jobs: Free 20; Pro 40; Team 60; Enterprise 500. Larger runners: Team 1000, Enterprise 1000. [D] same URL ("Total concurrent jobs"). These are the same values as the premise (Free: 20).
- Re-runs: 50 per workflow run. Matrix: 256 jobs per run. [D] same URL.

### Minutes and money (the premise's "2000 min/month" is outdated)
- Free plan private-repo quota is now a dollar amount, not minutes: "The included compute usage is expressed as a monetary amount, not a fixed number of minutes." GitHub Free = $12 USD per month included compute. [D] https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions
- Per-minute rates: Linux 1-core $0.002; Linux 2-core x64 $0.006; Linux 2-core arm64 $0.005; Windows 2-core $0.010; macOS $0.062. [D] same URL.
- Derived: $12 / $0.006 = 2000 min of Linux 2-core x64 per month on Free. This is a calculation from the official numbers, not a stated quota. [D-derived]
- Public repo standard runners: free and unlimited, do not draw from included compute. [D] same URL.
- Plans: Pro $18, Team $18 (org), Enterprise Cloud $300 included compute (per the plan table on the same page). [D]

### Storage allowances (Actions, separate lines)
- Artifact storage (shared with GitHub Packages): Free 500 MB; Pro 1 GB; Team 2 GB; Enterprise Cloud 50 GB. [D] https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions
- Artifact storage beyond quota: $0.25 per GB-month. [D] same URL.
- Actions cache: 10 GB per repository included on all plans; $0.07 per GB-month beyond. Entries not accessed for over 7 days are evicted. Cache rate limits: 200 uploads/min, 1500 downloads/min per repo. [D] same URL + https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- Artifact default and maximum retention (90 days per the premise): BULUNAMADI in the fetched text. The page only shows the `retention-days` option (example: 5 days), which "cannot exceed the retention limit set by the repository, organization, or enterprise." [B] https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
- Artifact per-file size limit: BULUNAMADI in fetched text.
- Storage limits for hosted runners: "GitHub Support cannot increase storage limits for GitHub Actions." [D] limits page.

## 2. Where to store frame-animation output (30-100 frames x 2-6 MB)
Total size estimate: 30 x 2 MB = 60 MB up to 100 x 6 MB = 600 MB per run (arithmetic, not a source).

- Actions artifact: Free quota is 500 MB total shared with Packages. A single 600 MB run would exceed the whole Free quota. Not suitable for Free accounts; retention and per-file limits unverified. [D] storage quota above.
- GitHub Releases: "Each file included in a release must be under 2 GiB. There is no limit on the total size of a release, nor bandwidth usage." Up to 1000 assets per release. [B] https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases . Good fit for a zipped/tarred frame set (600 MB fits in one file) or individual frames (up to 1000 assets). Releases are public for public repos.
- GitHub Pages: site size no larger than 1 GB; source repo recommended 1 GB; soft bandwidth 100 GB/month; soft 10 builds per hour unless a custom Actions workflow deploys. [B] https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits . A 600 MB set fits but leaves little room; not a storage area for many runs.
- Git LFS: Free quota 10 GiB storage and 10 GiB bandwidth per month; per-file max 2 GB on Free (5 GB Enterprise). If quota exceeded with no payment method, usage is blocked. [B] https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage and https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage ("Git LFS support is disabled on your account until the next month" when bandwidth is exceeded). Note the page says "GitHub Free 10 GiB" for both bandwidth and storage.
- actions/cache: 10 GB per repo, evicted after 7 days of no access. Not a deliverable store: it is for dependency caches, not outputs. [D]

## 3. Cloudflare Pages / R2 / Workers KV (free tier)
- Pages: per-file max 25 MiB; up to 20,000 files per site on Free; 500 builds/month on Free; 1 concurrent build; build timeout 20 min; 100 projects per account; 100 custom domains per project (Free). [D] https://developers.cloudflare.com/pages/platform/limits/ . Implication: a 25 MiB cap per file means one 6 MB frame fits, but a single large zip (600 MB) does not; frames must be stored as separate files.
- R2 (Standard storage): free 10 GB-month storage per month; 1 million Class A ops/month; 10 million Class B ops/month; egress to the internet free. Standard $0.015 / GB-month beyond free. Max single object 5 TiB; single-part upload 5 GiB. [D] https://developers.cloudflare.com/r2/pricing/ and https://developers.cloudflare.com/r2/platform/limits/ . Best fit for 600 MB per run if the total stays under 10 GB; cost is then zero within the free tier.
- Workers KV: storage 1 GB per account (Free); value size max 25 MiB; reads 100,000/day; writes to different keys 1,000/day; writes to same key 1 per second. [D] https://developers.cloudflare.com/kv/platform/limits/ . Not suitable for multi-hundred-MB frame sets (1 GB total, 1000 writes/day).

## 4. Python environment setup speed
- actions/setup-python: built-in `cache: pip` (also pipenv, poetry). Cache key uses the dependency file hash (requirements.txt or pyproject.toml). For pip it caches the global pip cache directory. [B] https://raw.githubusercontent.com/actions/setup-python/main/README.md (line ~85-91). The README is in the repo, not a timing claim.
- fastscapelib on PyPI: version 0.3.0 (latest in the registry metadata). Wheels exist for CPython 3.10, 3.11, 3.12, 3.13 on manylinux_2_27/2_28 x86_64, plus macOS (x86_64 and arm64) and Windows amd64, plus an sdist (tar.gz). No cp314 wheel listed. So `pip install fastscapelib` on Linux x64 with Python 3.10-3.13 installs a prebuilt wheel, no compile. [D] https://pypi.org/pypi/fastscapelib/json
- Conda: conda-forge has fastscapelib, latest 0.3.0 (anaconda.org API). [D] https://api.anaconda.org/package/conda-forge/fastscapelib . conda-forge introduction page: install via miniforge recommended; create a new env rather than base. [B] https://conda-forge.org/docs/user/introduction/
- goSPL on PyPI: latest 2026.7.14, sdist only (gospl-2026.7.14.tar.gz), requires Python >=3.11. Declared runtime dependencies include petsc4py, mpi4py, vtk, pyshtools, h5py, numpy, scipy, pandas, numpy-indexed, ruamel.yaml. No wheel is published, so pip will build from source, and petsc4py/mpi4py/vtk are heavy native dependencies. Conda-forge route is likely faster for these, but a build time was not measured in this pass. [D] https://pypi.org/pypi/goSPL/json
- Measured install times for fastscapelib or goSPL in CI: BULUNAMADI (not measured; no CI run performed).

## 5. Public vs private repository (consequences)
- Public repo: code, workflows, logs, artifacts, releases and Pages output are publicly visible. Standard runners free and unlimited; 4 vCPU / 16 GB runner for `ubuntu-latest`. Anyone with read access can download public artifacts and release assets. [D] runner page and billing page.
- Private repo: 2 vCPU / 8 GB runner; minutes and storage draw from included compute (Free $12/month) and artifact quota (500 MB). Extra usage billed at $0.006/min (Linux 2-core x64). [D] same URLs.
- Larger runners are billed even for public repos. [D] billing page.
- Visibility is a repo-level setting; a private repo with Pages publishing may still have public Pages on some plans (not verified in this pass: BULUNAMADI).

## Key takeaways for the frame-storage question
1. If the repo is public, `ubuntu-latest` gives 4 vCPU / 16 GB at no minute cost. Storage is the bottleneck, not compute.
2. Avoid Actions artifacts for 600 MB output on Free (500 MB shared quota).
3. Best candidates: R2 (10 GB free, egress free, no per-file size issue below 5 GiB) or a GitHub Release (2 GiB per file, no total cap) for public repos. Pages is OK only if the set is <1 GB and public.
4. Workers KV is not suitable for this size.

## Sources (URLs used)
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners [D]
- https://docs.github.com/en/actions/reference/limits [D]
- https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions [D]
- https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-packages/about-billing-for-github-packages [D]
- https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts [B]
- https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching [B]
- https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases [B]
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits [B]
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage [B]
- https://developers.cloudflare.com/pages/platform/limits/ [D]
- https://developers.cloudflare.com/r2/pricing/ [D]
- https://developers.cloudflare.com/r2/platform/limits/ [D]
- https://developers.cloudflare.com/kv/platform/limits/ [D]
- https://pypi.org/pypi/fastscapelib/json [D]
- https://pypi.org/pypi/goSPL/json [D]
- https://api.anaconda.org/package/conda-forge/fastscapelib [D]
- https://raw.githubusercontent.com/actions/setup-python/main/README.md [B]
- https://conda-forge.org/docs/user/introduction/ [B]
