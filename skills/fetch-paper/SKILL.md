---
name: fetch-paper
description: Use when asked to retrieve an open-access research paper PDF by DOI or identify available copies.
---

# Fetch a paper by DOI

**Most important: look in PubMed Central (PMC) open access first.** For biomedical and life-science papers, PMC is the most reliable legal source of the full text: the PMC ID converter (`https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=<DOI or PMID>&format=json`) gives the PMCID, and the PMC Article Datasets bucket (`https://pmc-oa-opendata.s3.amazonaws.com/<PMCID>.<version>/`) holds the PDF plus full-text `.xml` and `.txt` and the supplementary files. Prefer this over publisher pages, which often block automated access, and over other aggregators. The script below does this first. If a paper is in PMC but not in the open-access dataset, or not in PMC at all, say so explicitly before using other sources.

Run `python3 <skill-directory>/scripts/fetch_paper.py DOI --email EMAIL` with the user's real contact email for Unpaywall, or omit the email to skip Unpaywall. The script checks PubMed Central open access first (no key needed), then Unpaywall, OpenAlex (when `OPENALEX_API_KEY` is set), and Semantic Scholar. For PMC hits it also prints the full-text XML/TXT URLs, which are better than PDF text for summarizing. It saves verified PDF bytes under `~/papers` by default and reports the source, URL, and available version metadata. Optional `--output-dir` selects a destination; existing files are never overwritten.

Report which source succeeded and whether it identifies a preprint, accepted manuscript, or published version. If all sources fail, distinguish provider errors and missing credentials from an actual absence of results; suggest an institution's library or requesting a copy from the author. Do not assert that author email addresses or an institution subscription have been verified without evidence. Verify that a retrieved version is suitable for the user's purpose.

See [usage and provider requirements](references.md).
