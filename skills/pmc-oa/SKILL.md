---
name: pmc-oa
description: Use FIRST whenever a paper must be found, downloaded, read or summarized by DOI, PMID or PMCID (or a pubmed / pmc link), before publisher pages or other sources — gets the PubMed Central open-access full text (XML, TXT, PDF, supplements) with license and retraction status.
---

# PubMed Central open access first

**Most important — summary:** for any journal article, look in **PubMed Central (PMC) open access first**. Resolve the DOI / PMID to a PMCID with the PMC ID converter, then take the full text from the PMC Article Datasets bucket on AWS (`pmc-oa-opendata`): `.xml` and `.txt` for reading and summarizing, `.pdf` for the paper itself, plus figures and supplementary files. It is legal, needs no key or login, is not blocked like publisher sites, and its metadata states the license and whether the article is retracted. Use other sources only after this says the article is not in PMC open access.

## Run

```bash
python3 <skill-directory>/scripts/pmc_oa.py <DOI|PMID|PMCID|pmc URL> [more ...] \
    [--files xml,txt,pdf|media|all] [--output-dir ~/papers/pmc] [--email you@example.edu]
```

- Default files: `xml,txt,pdf`; `media` adds figures and supplementary files (can be large); `all` = both.
- Saves to `~/papers/pmc/<PMCID>.<version>/`, verifies each file against the md5 in PMC's metadata, never overwrites.
- Prints for each article: PMCID and version, PMID, DOI, title, citation, **license** (e.g. CC BY), open-access and author-manuscript flags, and a **RETRACTED** warning when PMC marks it.
- Exit code 3 means at least one article is not in PMC open access; the output says whether it has no PMCID at all or is in PMC but outside the open-access dataset.

## Then

1. **Report the status line first** — in PMC OA or not, license, retracted or not, author manuscript or version of record.
2. **To summarize or quote, read the `.xml`** (sections, boxes, figure captions, tables and references are tagged; extract boxed-text, fig and table-wrap explicitly) or the `.txt`; do not summarize from the abstract alone. Copy numbers and names exactly.
3. Respect the license: CC BY / CC0 allow reuse with attribution; other licenses (e.g. CC BY-NC-ND, "author manuscript") mean summary plus short quotes only.
4. If the article is **not** in PMC open access: say so, then use the `fetch-paper` skill (Unpaywall, OpenAlex, Semantic Scholar). If a PMCID exists but the text is not in the open-access dataset, give the reader link `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/` rather than scraping it.
5. Never bypass a paywall or login. When writing a Markdown page from the result, follow the `paste-to-md` skill and record "full text from PMC open access, <PMCID>.<version>" in the header.

## Endpoints (checked 2026-11-11)

- ID converter: `https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=<id>&idtype=doi|pmid&format=json` — one ID type per request. Docs: <https://pmc.ncbi.nlm.nih.gov/tools/idconv/>
- Article Datasets: `https://pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix=<PMCID>.` lists versions/files; `<PMCID>.<v>/<PMCID>.<v>.json` holds the metadata. Docs: <https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/>
- Not usable for automation as of that date: the old `www.ncbi.nlm.nih.gov/pmc/utils/` endpoints (404), the PMC website PDF link (bot check page) and Europe PMC `?pdf=render` (403). Europe PMC REST `fullTextXML` still works as a second route for the XML.
