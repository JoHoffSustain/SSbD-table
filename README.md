# SSbD Project Tracker

A community-maintained, open reference database of EU Horizon-funded research projects working within the **Safe and Sustainable by Design (SSbD)** framework — built to give SSbD practitioners, consortium partners, policy officers, and researchers a single, transparent map of who is doing what across the European SSbD landscape.

**Live site:** [johoffsustain.github.io/SSbD-table](https://JoHoffSustain.github.io/SSbD-table/)

---

## Why does this exist?

The European Commission's SSbD framework has generated a rapidly growing portfolio of Horizon Europe and H2020 projects — covering nanomaterials, coatings, textiles, surfactants, flame retardants, plasticizers, lubricants, pharmaceuticals, bio-based materials, and more. As of mid-2026, over 55 projects are active or completed across these areas.

Despite this activity, there was no single place to answer basic questions like:
- Which projects are working on PFAS alternatives in coatings?
- Who is doing social LCA in the SSbD context?
- Which projects share a funding call and might be natural collaboration partners?
- Which consortia include risk assessment, LCA, and industrial validation together?

This tracker was built to fill that gap. It is **not** an official European Commission resource — it is a practitioner-maintained dataset, built openly so that project coordinators, researchers, and policy stakeholders can contribute corrections and additions.

---

## What's in the database?

Each project entry covers:

| Field | Source |
|---|---|
| Acronym, full title, project website | CORDIS |
| Funding call / topic ID | CORDIS |
| Start and end dates | CORDIS |
| Coordinator and country | CORDIS |
| Total cost and EU contribution | CORDIS |
| CORDIS Grant ID and link | CORDIS |
| Focus category (product group) | Manual classification |
| SSbD assessment scope | Manual review |
| Use cases | Manual review |
| Substitutable Material (SoC) | Manual review |
| Innovation / solutions | Manual review |
| Partner roles (tech dev, hazard, risk & exposure, env LCA, social LCA/LCC/TEA, AI, MCDA, industrial, dissemination, exploitation, social acceptance & policy) | Manual review from project presentations and deliverables |
| SSbD relevant publications | Manual curation |
| SSbD core project flag | Analysis of call text |

**Partner role columns** (hazard assessment, risk and exposure, environmental LCA, socioeconomics, AI, MCDA/scoring, industrial, dissemination, social acceptance) are **not available from CORDIS** — CORDIS does not tag participants by role. These columns are filled through manual review of project websites, consortium presentations, and deliverables, and are the fields most likely to need community input.

---

## How the data was built

### Step 1 — Project list
The initial list of 46 projects was derived from Peter Fantke's published chart of EU-funded SSbD projects, who analyzed the CORDIS database for SSbD keywords. Additional projects were identified from the EC SSbD Networking Event (Brussels, March 2026) and from newer Horizon calls.

### Step 2 — CORDIS data
Factual fields (dates, coordinator, budget, grant ID, topic ID) were sourced project-by-project from [cordis.europa.eu](https://cordis.europa.eu). For bulk backfill, the [CORDIS open datasets](https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027) on data.europa.eu can be used (see `scripts/fill_cordis_data.py`).

### Step 3 — SSbD classification
Each project was classified by:
- **Focus category** — product group cluster (Coatings, Nanomaterials, Flame Retardants, Surfactants, Lubricants, Textiles, Bio-based Materials, Assessment Methods & Digital Tools, etc.)
- **SSbD core project** flag — whether SSbD was explicitly named in the funding call topic title, or whether the project is part of the established SSbD ecosystem (e.g. PARC, NANORIGO) even if the call predates the exact terminology. Projects marked *No* apply SSbD methodology but were funded under broader calls (bio-based innovation, circular bioeconomy, hydrogen, batteries) where SSbD was not the primary rationale.
- **Active/completed** — based on the project end date compared to today

### Step 4 — Partner roles
Partner role columns were filled manually from project consortium presentations, slides from the EC SSbD Networking Event (March 2026), project websites, and publicly available deliverables. Only explicitly stated roles were entered — no inference from diagram positions or assumed roles.

---

## How to propose a correction or addition

This tracker is transparent by design. Changes are proposed through GitHub Issues and reviewed before being applied to the dataset.

1. Click **"Propose an edit"** on the live site, or open an Issue directly using one of the templates:
   - **Propose an edit** — correct or add data for an existing project
   - **Add a new SSbD project** — suggest a project that is missing entirely
2. Include a source (CORDIS link, project website, deliverable, or first-hand knowledge as a consortium member)
3. The maintainer reviews and applies the change to `data/projects.json`
4. On the next push to `main`, the site updates automatically within minutes

---

## Repository structure

```
data/projects.json              ← single source of truth — edit this file
docs/index.html                 ← the interactive table (GitHub Pages)
docs/data/projects.json         ← auto-synced copy served by the site (do not edit manually)
scripts/fill_cordis_data.py     ← bulk-fill CORDIS fields from official open datasets
.github/workflows/deploy.yml   ← validates data, syncs docs/, deploys to GitHub Pages
.github/ISSUE_TEMPLATE/        ← propose-edit and new-project issue forms
```

The workflow on every push to `main`:
1. Validates `data/projects.json` (checks for JSON errors and duplicate acronyms)
2. Copies it to `docs/data/projects.json`
3. Deploys `docs/` to GitHub Pages

You never need to touch `docs/data/projects.json` manually.

---

## Data provenance and licence

All CORDIS-sourced fields (acronym, title, coordinator, dates, budget, grant ID, topic) are drawn from the European Commission's [CORDIS database](https://cordis.europa.eu), which is published as open data under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Partner role data, focus categories, SSbD assessment scopes, and use case classifications are editorial contributions based on publicly available project materials and are released under the same licence.

**Cite as:** J. Hoffmann, *SSbD Project Tracker*, [johoffsustain.github.io/SSbD-table](https://johoffsustain.github.io/SSbD-table/), 2026.

[![CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Transparency

This project is mostly done with the support of AI.

