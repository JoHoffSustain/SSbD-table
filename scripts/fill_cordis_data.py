#!/usr/bin/env python3
"""
fill_cordis_data.py

Fills in CORDIS-derivable fields (topic ID, start/end date, coordinator,
coordinator country, total cost, EU contribution, CORDIS ID/URL) for every
project in data/projects.json, by matching project acronyms against the
official CORDIS bulk open-data exports.

Why this approach instead of scraping cordis.europa.eu page by page:
  - CORDIS publishes the full Horizon Europe and Horizon 2020 project
    catalogues as downloadable CSV/XML/JSON datasets on data.europa.eu.
  - These bulk files already contain: acronym, title, topic, call ID,
    start/end date, total cost, EC contribution, coordinator, coordinator
    country, and the full participant list with countries.
  - Downloading two files once and matching locally is far more reliable
    and far faster than fetching ~40 individual project pages.

Usage:
    1. Download the two zip files manually (links below) and unzip them
       into a folder, e.g. ./cordis_raw/
         Horizon Europe: https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027
         Horizon 2020:   https://data.europa.eu/88u/dataset/cordisH2020projects
       Each download contains a "...projects.csv" (or .xlsx) file -- that's
       the one this script needs. Point --projects-csv at it (run once per
       framework programme, since SSbD projects span both H2020 and HORIZON).

    2. Run:
         pip install pandas --break-system-packages
         python3 fill_cordis_data.py --projects-csv /path/to/horizon_projects.csv
         python3 fill_cordis_data.py --projects-csv /path/to/h2020_projects.csv

    Each run only fills in projects that are still missing CORDIS data
    (i.e. it won't overwrite the 8 already filled), and matches are made
    on normalised acronym, so re-running is always safe.

    3. Review data/projects_unmatched.txt for any acronyms that didn't
       find a match (these need a manual CORDIS search -- e.g. because the
       acronym in the dataset has different casing/punctuation, or the
       project is too new to be in the latest monthly dump yet).
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "projects.json"
UNMATCHED_FILE = Path(__file__).resolve().parent.parent / "data" / "projects_unmatched.txt"


def normalise(acronym: str) -> str:
    """Normalise an acronym for matching: lowercase, strip non-alphanumerics."""
    return re.sub(r"[^a-z0-9]", "", acronym.lower())


def load_projects():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_projects(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_cordis_csv(path: str):
    """
    Load a CORDIS bulk projects CSV into a dict keyed by normalised acronym.
    CORDIS CSV column names have varied slightly across dataset versions,
    so we match flexibly on common header variants.
    """
    candidates_acronym = ["acronym", "title_acronym", "project_acronym"]
    candidates_topic = ["topics", "topic", "topicCode", "topic_id"]
    candidates_call = ["call", "callIdentifier", "call_id"]
    candidates_start = ["startDate", "start_date"]
    candidates_end = ["endDate", "end_date"]
    candidates_coord = ["coordinator", "coordinatorName"]
    candidates_coord_country = ["coordinatorCountry", "coordinator_country"]
    candidates_cost = ["totalCost", "total_cost"]
    candidates_ec = ["ecMaxContribution", "ec_max_contribution", "eu_contribution"]
    candidates_id = ["id", "rcn", "projectID", "grantDoi"]

    def pick(row, candidates):
        for c in candidates:
            if c in row and row[c] not in (None, ""):
                return row[c]
        return ""

    index = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        # CORDIS bulk exports are typically semicolon-delimited
        sample = f.read(4096)
        f.seek(0)
        delimiter = ";" if sample.count(";") > sample.count(",") else ","
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            acr = pick(row, candidates_acronym)
            if not acr:
                continue
            key = normalise(acr)
            index[key] = {
                "topic_id": pick(row, candidates_topic),
                "call_id": pick(row, candidates_call),
                "start_date": pick(row, candidates_start),
                "end_date": pick(row, candidates_end),
                "coordinator": pick(row, candidates_coord),
                "coordinator_country": pick(row, candidates_coord_country),
                "total_cost_eur": pick(row, candidates_cost),
                "eu_contribution_eur": pick(row, candidates_ec),
                "cordis_id": pick(row, candidates_id),
            }
    return index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--projects-csv",
        required=True,
        help="Path to a CORDIS bulk 'projects.csv' file (Horizon Europe or H2020 export)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite fields that are already filled in (default: only fill blanks)",
    )
    args = parser.parse_args()

    data = load_projects()
    cordis_index = load_cordis_csv(args.projects_csv)
    print(f"Loaded {len(cordis_index)} projects from CORDIS export.")

    matched, unmatched = 0, []

    for project in data["projects"]:
        key = normalise(project["acronym"])
        record = cordis_index.get(key)
        if not record:
            unmatched.append(project["acronym"])
            continue

        fields_to_fill = [
            "topic_id",
            "start_date",
            "end_date",
            "coordinator",
            "coordinator_country",
            "total_cost_eur",
            "eu_contribution_eur",
            "cordis_id",
        ]
        for field in fields_to_fill:
            current = project.get(field)
            is_blank = current in (None, "", 0)
            if is_blank or args.overwrite:
                value = record.get(field, "")
                if field in ("total_cost_eur", "eu_contribution_eur") and value:
                    try:
                        value = float(str(value).replace(",", "."))
                    except ValueError:
                        pass
                if value not in (None, ""):
                    project[field] = value

        if record.get("cordis_id"):
            project["cordis_url"] = f"https://cordis.europa.eu/project/id/{record['cordis_id']}"

        matched += 1

    save_projects(data)

    with open(UNMATCHED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(unmatched))

    print(f"Matched and updated: {matched}")
    print(f"Unmatched (need manual lookup): {len(unmatched)}")
    if unmatched:
        print("  -> see", UNMATCHED_FILE)
    print(f"Saved: {DATA_FILE}")


if __name__ == "__main__":
    sys.exit(main())
