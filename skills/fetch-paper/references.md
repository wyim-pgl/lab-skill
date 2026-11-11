# Fetch paper usage

```bash
python3 skills/fetch-paper/scripts/fetch_paper.py '10.7717/peerj.4375' --email you@example.edu
```

PubMed Central open access is tried first and needs no key: the [PMC ID converter API](https://pmc.ncbi.nlm.nih.gov/tools/idconv/) maps the DOI to a PMCID and the [PMC Article Datasets on AWS](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) (`pmc-oa-opendata`) provide the PDF, XML and TXT. The old `www.ncbi.nlm.nih.gov/pmc/utils/` endpoints return 404, and the PMC website PDF link and Europe PMC `?pdf=render` refused automated requests when tested on 2026-11-11.

Use your own contact email. Unpaywall requires it; no fabricated email is sent. OpenAlex requires an API key (`OPENALEX_API_KEY`). Semantic Scholar may rate-limit unauthenticated calls; set `S2_API_KEY` if available. No key is printed or written to the output. DOI slashes are encoded safely in output filenames. The tool does not bypass authentication or automate institutional logins.

Metadata and retrieval errors are reported separately. An accessible PDF may be a different manuscript version from the version of record; check version and license at its source. The PDF signature check is not a full PDF integrity check.

Sources: [Unpaywall API](https://unpaywall.org/api), [Unpaywall data format](https://unpaywall.org/data-format), [OpenAlex authentication](https://help.openalex.org/api/authentication/), [OpenAlex locations](https://help.openalex.org/data/locations/), [Semantic Scholar API](https://api.semanticscholar.org/api-docs).
