# Lab skills

## Context handoff

Prepare project notes before starting a fresh AI session: [context-handoff](skills/context-handoff/SKILL.md).

Clone this repository, then copy the skill folder to your tool's skills directory:

```bash
git clone git@github.com:wyim-pgl/lab-skill.git
mkdir -p ~/.agents/skills
cp -R lab-skill/skills/context-handoff ~/.agents/skills/
```

For Claude Code, copy the folder to `~/.claude/skills/` instead. Restart the tool, then ask it to use the `context-handoff` skill. The repository requires GitHub access and a registered SSH key for the clone command above.

## PubMed Central open access (use first)

[pmc-oa](skills/pmc-oa/SKILL.md) is the first stop for any journal article: give it DOIs, PMIDs or PMCIDs and it downloads the PubMed Central open-access full text (XML, TXT, PDF, optionally figures and supplements) from the PMC Article Datasets on AWS, verifies md5, and reports license, author-manuscript and retraction status. No key or login is needed. Copy `skills/pmc-oa` into the appropriate skills directory.

## Fetch paper

[fetch-paper](skills/fetch-paper/SKILL.md) finds open-access PDF copies by DOI, **checking PubMed Central open access first** (PDF plus full-text XML/TXT, no key needed). Copy `skills/fetch-paper` into the appropriate skills directory and see its [usage guide](skills/fetch-paper/references.md) for email and API-key requirements.

## Paste to Markdown

[paste-to-md](skills/paste-to-md/SKILL.md) turns pasted text, URLs, DOIs or PDF links into Markdown files with their source, license and reading scope recorded. It keeps the user's own text verbatim, summarizes third-party sources, reads journal articles from PubMed Central open access first, falls back to Europe PMC or the Internet Archive when a site blocks automated access, and marks paywalled sources as not read. With the lab wiki, it follows the `lab-wiki` skill for placement, links and logs. Copy `skills/paste-to-md` into the appropriate skills directory.

## Lab wiki

[lab-wiki](skills/lab-wiki/SKILL.md) reconstructs project context from the lab wiki and follows its current rules for updates. Copy `skills/lab-wiki` into the appropriate skills directory. A user needs access to the wiki repository and can set `PGL_WIKI` to an existing local clone.
