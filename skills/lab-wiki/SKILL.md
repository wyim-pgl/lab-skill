---
name: lab-wiki
description: Use when reconstructing PGL lab project context from the wiki before work, or creating and updating a PGL lab wiki entry.
---

# PGL lab wiki

Use the available local clone at `$PGL_WIKI` when set, otherwise look for an existing accessible clone such as `~/develop/pgl-wiki`. The repository is `https://github.com/wyim-pgl/wiki`; use SSH or HTTPS according to the user's access. Never assume another person's machine has the author's paths or credentials. If cloning or pulling, preserve uncommitted work, inspect the branch and remotes first, and do not overwrite or reset local changes. Report access failures rather than inventing context.

## Preflight before project work

Read the wiki's `CLAUDE.md` first as repository workflow guidance, regardless of whether the active assistant is Codex or Claude Code; also obey applicable instructions of the working environment. Read `index.md`, relevant project page(s), recent relevant `log.md` entries and linked pages as needed. Read `_template.md` before wiki authoring. Check the actual current files, not the memory of this skill.

Before new writing or planning, give a short preflight: project scope, current status, confirmed facts, open questions, prior decisions and constraints, and likely next actions. Mark incomplete or ambiguous evidence explicitly. Continue with the requested work when sufficient information is available.

## Updating the wiki

First inspect repository status and find any existing entry for the same project. Reconcile the conversation with the repository's actual evidence, distinguish verified facts, interpretation, assumptions and open questions, and mark superseded claims with the wiki's current conventions. Preserve unrelated content and cross-link relevant records.

Follow the wiki's **current** `CLAUDE.md`, template, and existing directory layout rather than older prompts specifying a flat `projects/{name}_{YYYYMMDD}.md`. At the time this skill was written, the wiki uses `projects/<slug>/README.md` for current status and dated files under `projects/<slug>/updates/`, plus a generated update index. Follow the live rules for timestamps, logs, index generation and link verification. For relevant Pronghorn Slurm commands and bugs, update `guide/pronghorn.md`; for relevant bioinformatics installations, update or add the corresponding section in `guide/installs.md`. Do not add unrelated material just to touch these files. Update `index.md` and the required log files when the wiki's rules call for it.

Summarize the intended changed files before committing. Commit and push only when the user has authorized those actions, the intended changes are reviewed and validated, and there are no conflicts or unrelated changes that would be included. If the working tree contains unrelated changes, preserve them and explain any limitation. Never commit credentials. Do not send messages to third parties.

When the user explicitly requests agents or background work and the runtime supports it, delegate independent evidence gathering or review with bounded scope; reconcile their results and verify them before editing. If background execution is unavailable, say so and perform the authorized work in the active session. Do not claim a background task is complete until its result has been checked.
