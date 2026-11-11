#!/usr/bin/env python3
"""Get a paper's full text from PubMed Central (PMC) open access.

Accepts DOIs, PMIDs or PMCIDs. Resolves each to a PMCID with the PMC ID
converter, reads the article's metadata from the PMC Article Datasets bucket
(pmc-oa-opendata on AWS), prints title, citation, license and status flags,
and downloads the requested files (default: xml, txt, pdf), verifying each
against the md5 published in the metadata. Existing files are not overwritten.

Exit codes: 0 all found, 1 error, 3 at least one article not available in PMC
open access (use the fetch-paper skill for other legal open-access sources).
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

IDCONV = "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/"
BUCKET = "https://pmc-oa-opendata.s3.amazonaws.com/"
LIMIT = 200 * 1024 * 1024
KINDS = ("xml", "txt", "pdf", "media")


def get(url):
    req = Request(url, headers={"User-Agent": "lab-skill-pmc-oa/1.0"})
    with urlopen(req, timeout=60) as r:
        data = r.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("response exceeds 200 MiB")
    return data


def normalize(raw):
    s = raw.strip()
    s = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", s, flags=re.I)
    m = re.search(r"PMC\d+", s, flags=re.I)
    if m:
        return "pmcid", m.group(0).upper()
    if re.fullmatch(r"\d{1,9}", s):
        return "pmid", s
    if re.fullmatch(r"10\.\d{4,9}/\S+", s):
        return "doi", s
    raise ValueError(f"not a DOI, PMID or PMCID: {raw}")


def to_pmcid(kind, value, email):
    if kind == "pmcid":
        return value
    q = {"ids": value, "idtype": kind, "format": "json", "tool": "lab-skill-pmc-oa"}
    if email:
        q["email"] = email
    rec = (json.loads(get(IDCONV + "?" + urlencode(q))).get("records") or [{}])[0]
    return rec.get("pmcid")


def s3_key(url):
    # s3://pmc-oa-opendata/PMC123.1/file.pdf?md5=... -> (PMC123.1/file.pdf, md5)
    m = re.match(r"s3://pmc-oa-opendata/([^?]+)(?:\?md5=([0-9a-f]{32}))?", url or "")
    return (m.group(1), m.group(2)) if m else (None, None)


def fetch_one(raw, kinds, outdir, email):
    kind, value = normalize(raw)
    pmcid = to_pmcid(kind, value, email)
    if not pmcid:
        print(f"[{raw}] NOT IN PMC: no PMCID for this {kind}. Try the fetch-paper skill.")
        return 3
    listing = get(BUCKET + "?" + urlencode({"list-type": "2", "prefix": pmcid + "."})).decode()
    versions = sorted({k.split("/")[0] for k in re.findall(r"<Key>([^<]+)</Key>", listing)},
                      key=lambda v: int(v.rsplit(".", 1)[1]))
    if not versions:
        print(f"[{raw}] {pmcid} is in PMC but NOT in the open-access dataset "
              f"(read it at https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/ or try fetch-paper).")
        return 3
    ver = versions[-1]
    meta = json.loads(get(f"{BUCKET}{ver}/{ver}.json"))
    print(f"[{raw}] {ver}  PMID {meta.get('pmid')}  DOI {meta.get('doi')}")
    print(f"  Title:    {meta.get('title')}")
    print(f"  Citation: {meta.get('citation')}")
    print(f"  License:  {meta.get('license_code') or 'not stated'}"
          f"  | open access: {meta.get('is_pmc_openaccess')}"
          f"  | author manuscript: {meta.get('is_manuscript')}")
    if meta.get("is_retracted"):
        print("  WARNING: PMC marks this article as RETRACTED.")
    if meta.get("is_historical_ocr"):
        print("  NOTE: historical OCR text; check against the PDF.")
    if len(versions) > 1:
        print(f"  Versions available: {', '.join(versions)} (using latest)")
    wanted = []
    for k in kinds:
        if k == "media":
            wanted += meta.get("media_urls") or []
        elif meta.get(f"{k}_url" if k != "txt" else "text_url"):
            wanted.append(meta[f"{k}_url" if k != "txt" else "text_url"])
    dest = outdir / ver
    status = 0
    for url in wanted:
        key, md5 = s3_key(url)
        if not key:
            continue
        target = dest / key.split("/", 1)[1]
        if target.exists():
            print(f"  exists, not overwritten: {target}")
            continue
        data = get(BUCKET + key)
        if md5 and hashlib.md5(data).hexdigest() != md5:
            print(f"  MD5 MISMATCH, not saved: {key}", file=sys.stderr)
            status = 1
            continue
        dest.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as f:
            f.write(data)
        print(f"  saved {target} ({len(data):,} bytes, md5 ok)")
    return status


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ids", nargs="+", help="DOI, PMID or PMCID (any mix)")
    p.add_argument("--files", default="xml,txt,pdf",
                   help="comma list from: xml, txt, pdf, media, all (default: xml,txt,pdf)")
    p.add_argument("--output-dir", type=Path, default=Path.home() / "papers" / "pmc")
    p.add_argument("--email", help="your contact email for the NCBI ID converter (optional)")
    a = p.parse_args()
    kinds = KINDS if a.files.strip() == "all" else tuple(x.strip() for x in a.files.split(",") if x.strip())
    bad = [k for k in kinds if k not in KINDS]
    if bad:
        p.error(f"unknown --files value(s): {', '.join(bad)}")
    worst = 0
    for raw in a.ids:
        try:
            rc = fetch_one(raw, kinds, a.output_dir, a.email)
        except Exception as exc:
            print(f"[{raw}] ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
            rc = 1
        worst = 1 if 1 in (worst, rc) else max(worst, rc)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
