---
name: fetch-paper
description: Use when asked to retrieve an open-access research paper PDF by DOI or identify available copies.
---

# Fetch a paper by DOI

Run `python3 <skill-directory>/scripts/fetch_paper.py DOI --email EMAIL` with the user's real contact email for Unpaywall, or omit the email to skip Unpaywall. The script checks Unpaywall, OpenAlex (when `OPENALEX_API_KEY` is set), and Semantic Scholar in order. It saves verified PDF bytes under `~/papers` by default and reports the source, URL, and available version metadata. Optional `--output-dir` selects a destination; existing files are never overwritten.

Report which source succeeded and whether it identifies a preprint, accepted manuscript, or published version. If all sources fail, distinguish provider errors and missing credentials from an actual absence of results; suggest an institution's library or requesting a copy from the author. Do not assert that author email addresses or an institution subscription have been verified without evidence. Verify that a retrieved version is suitable for the user's purpose.

See [usage and provider requirements](references.md).
