# SSbD Project Tracker

A community-maintained, sortable reference table of EU Horizon-funded **Safe and Sustainable by Design (SSbD)** research projects — built for LCA practitioners, consortium partners, and EC project officers who need one map of who is doing what, where.

**Live site:** `https://JonciH.github.io/ssbd-table/` (after you complete setup below)

## What's in this repo

```
data/projects.json         <- single source of truth: all project data
docs/                       <- the GitHub Pages site (reads docs/data/projects.json)
docs/index.html              the sortable/filterable table itself
scripts/fill_cordis_data.py <- script to bulk-fill CORDIS fields for new/blank projects
.github/workflows/deploy.yml        <- auto-deploys docs/ to GitHub Pages on every push
.github/ISSUE_TEMPLATE/             <- the "propose an edit" / "add a project" forms
```

### Why two copies of `projects.json`?

`data/projects.json` is the file you and the CORDIS script edit. The deploy workflow automatically copies it into `docs/data/projects.json` on every push to `main`, which is what the live site actually fetches. You never need to touch `docs/data/projects.json` by hand — just edit `data/projects.json` and push.

## One-time setup (do this first)

1. **Create the repo on GitHub** and push this folder's contents to it (see "Pushing this to GitHub" below).
2. **Enable GitHub Pages**: repo → Settings → Pages → under "Build and deployment", set Source to **GitHub Actions**. The included workflow (`.github/workflows/deploy.yml`) handles the rest.
3. **Replace placeholders**: search this repo for `JonciH` (in `docs/index.html`, this README, and `.github/ISSUE_TEMPLATE/config.yml`) and swap in your actual GitHub username/org and repo name.
4. **Push to `main`.** The first push triggers the Action, which validates the data, syncs it into `docs/`, and deploys. Check the *Actions* tab for progress; the site URL appears under Settings → Pages once it succeeds.

## Pushing this to GitHub for the first time

If you don't already have a repo:

```bash
cd ssbd-table
git init
git add .
git commit -m "Initial SSbD project tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ssbd-table.git
git push -u origin main
```

Then do steps 2–3 above.

## Filling in the rest of the CORDIS data

Five projects currently have full CORDIS data (topic ID, dates, coordinator country, budget) filled in as a pilot batch; the remaining ones have placeholders. Rather than scraping CORDIS project-by-project, use the official bulk datasets:

1. Download the relevant bulk export(s) — most SSbD projects are Horizon Europe, a few older ones are H2020:
   - Horizon Europe: https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027
   - Horizon 2020: https://data.europa.eu/88u/dataset/cordisH2020projects
   - Unzip and locate the `...projects.csv` file inside each download.

2. Run the fill script against each one:
   ```bash
   pip install pandas --break-system-packages
   python3 scripts/fill_cordis_data.py --projects-csv /path/to/horizon_projects.csv
   python3 scripts/fill_cordis_data.py --projects-csv /path/to/h2020_projects.csv
   ```
   The script only fills in *blank* fields — it won't overwrite anything already there (including your own manual corrections) unless you pass `--overwrite`.

3. Check `data/projects_unmatched.txt` afterwards for any acronyms that didn't match (typically projects too new for the latest monthly CORDIS dump, or with a slightly different acronym spelling in the dataset). Look these up manually on https://cordis.europa.eu/search.

4. Commit and push — the site updates automatically.

## How "edit by request" works

This is intentionally **not** a live database anyone can write to directly — edits go through review so the table stays trustworthy:

1. Someone notices an error or gap and clicks **"Propose an edit"** on the site (or opens an Issue directly using the *Propose an edit* or *Add a new SSbD project* template).
2. You get notified, review the suggested change and its source against `data/projects.json`.
3. If it checks out, edit `data/projects.json` directly (or ask a trusted collaborator to open a Pull Request) and push to `main`. The site updates within a minute or two via the Actions workflow.
4. Close the Issue, ideally with a one-line note on what changed.

If you'd rather let trusted contributors edit the file directly via Pull Request instead of you applying every change yourself, just enable that by adding them as collaborators — no extra setup needed since `data/projects.json` is a plain JSON file.

## Data provenance

- **Acronym, full title, project website, coordinator (initial name)** — compiled manually from public SSbD project communications.
- **Funding call / topic ID, start/end date, coordinator country, total cost, EU contribution, CORDIS ID** — sourced from [CORDIS](https://cordis.europa.eu), the European Commission's R&I results database, either fetched directly or via the bulk-data script above.
- **Focus category, SSbD assessment scope, use cases, solutions, and all partner-role columns** (technology development, scoping, risk assessment, environmental LCA, social LCA, AI, MCDA/SSbD scoring, industrial use cases, dissemination, exploitation) — **not available from CORDIS**, since CORDIS does not tag participants by project role. These are filled in through manual review of project websites, deliverables, and consortium knowledge, and are the columns most likely to need community correction.

## Updating column structure

The table's columns are defined in the `columns` array at the top of `data/projects.json`, not hardcoded in `docs/index.html` — so adding, renaming, or reordering a column only requires editing the JSON, not the page code.

## License

Add a `LICENSE` file appropriate to your use (e.g. CC-BY-4.0 is common for open reference datasets like this). Project data itself is drawn from public sources (CORDIS, project websites); please retain that attribution if you redistribute.
