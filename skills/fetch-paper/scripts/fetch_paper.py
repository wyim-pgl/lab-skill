#!/usr/bin/env python3
"""Retrieve an open-access PDF associated with a DOI."""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

LIMIT = 100 * 1024 * 1024


def request(url, headers=None):
    h = {"User-Agent": "lab-skill-fetch-paper/1.0"}
    h.update(headers or {})
    with urlopen(Request(url, headers=h), timeout=30) as response:
        data = response.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("response exceeds 100 MiB")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doi")
    parser.add_argument("--email", default=os.environ.get("UNPAYWALL_EMAIL"))
    parser.add_argument("--output-dir", type=Path, default=Path.home() / "papers")
    args = parser.parse_args()
    doi = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", args.doi.strip(), flags=re.I)
    if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
        parser.error("provide a valid DOI or doi.org URL")
    encoded = quote(doi, safe="")
    candidates = []
    sources = []
    if args.email:
        sources.append(("Unpaywall", "https://api.unpaywall.org/v2/" + encoded + "?" + urlencode({"email": args.email}), {}))
    else:
        print("Unpaywall: skipped (provide --email)", file=sys.stderr)
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        sources.append(("OpenAlex", "https://api.openalex.org/works/https://doi.org/" + encoded, {"Authorization": "Bearer " + key}))
    else:
        print("OpenAlex: skipped (OPENALEX_API_KEY not set)", file=sys.stderr)
    headers = {"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else {}
    sources.append(("Semantic Scholar", "https://api.semanticscholar.org/graph/v1/paper/DOI:" + encoded + "?fields=title,openAccessPdf", headers))
    for name, url, headers in sources:
        try:
            obj = json.loads(request(url, headers))
            if name == "Unpaywall":
                locations = [obj.get("best_oa_location") or {}] + (obj.get("oa_locations") or [])
                candidates = [(x.get("url_for_pdf"), x.get("version")) for x in locations]
            elif name == "OpenAlex":
                locations = [obj.get("best_oa_location") or {}]
                candidates = [(x.get("pdf_url"), x.get("version")) for x in locations]
            else:
                item = obj.get("openAccessPdf") or {}
                candidates = [(item.get("url"), item.get("status"))]
            for pdf, version in candidates:
                if not isinstance(pdf, str) or not pdf.startswith("https://"):
                    continue
                try:
                    data = request(pdf)
                    if not data.startswith(b"%PDF-"):
                        raise ValueError("response is not a PDF")
                    args.output_dir.mkdir(parents=True, exist_ok=True)
                    target = args.output_dir / (quote(doi, safe="") + ".pdf")
                    with target.open("xb") as f:
                        f.write(data)
                    print(f"Saved: {target}\nSource: {name}\nURL: {pdf}\nVersion/status: {version or 'unknown'}")
                    return 0
                except FileExistsError:
                    print(f"File already exists: {target}; not overwritten", file=sys.stderr)
                    return 2
                except Exception as exc:
                    print(f"{name}: PDF download failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            print(f"{name}: no downloadable PDF found", file=sys.stderr)
        except Exception as exc:
            print(f"{name}: lookup failed: {type(exc).__name__}: {exc}", file=sys.stderr)
    print("No PDF obtained. Check provider errors, library access, or contact the author.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
