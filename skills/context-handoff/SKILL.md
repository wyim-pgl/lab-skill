---
name: context-handoff
description: Use when preparing a project handoff before clearing context, starting a fresh session, or transferring work between Codex and Claude Code.
---

# Context handoff

Leave a verified, navigable record that lets a person or another session understand the project and continue. In an identified writable project, create or update all six required files: `INTENTION.md`, `README.md`, `TODO.md`, `ISSUE.md`, `QUARANTINE.md`, and `AGENTS.md`. Also maintain `resume.md` for current state. Read applicable project instructions and existing notes first; preserve user work, existing content, and established naming or location conventions. On case-sensitive filesystems, check for lowercase equivalents before creating anything; do not silently replace or discard them. If exact uppercase names are missing but equivalent files exist, create concise uppercase pointers to the existing authoritative files so both the required names and prior history remain usable. Do not invent a repository for a remote document; use the user's chosen handoff directory and link the source.

## Each file and how to use it

| File | Purpose and handling |
| --- | --- |
| `INTENTION.md` | Durable purpose and direction: the user's goal, intended outcome, constraints, decisions and unresolved choices. Record why the work exists so later sessions preserve the user's intent. Update only when intent or decisions change. |
| `README.md` | Entry point for people and agents: project purpose, actual working location or canonical remote document, navigation to the other records, and verified prerequisites. Update or add a small navigation section without replacing an existing project README. |
| `TODO.md` | Future work: specific next actions and dependencies, linked to relevant open issues. Mark completed tasks with date and commit when known. |
| `ISSUE.md` | Issue register organized by status: **Blocker** (what cannot proceed, evidence and required unblock), **To Go** (open items ready for action and next step), **In Progress**, **Waiting** (dependency or decision), and **Resolved** (date and evidence). Record impact, status and owner or source when known; use explicit unknowns. Link related tasks in `TODO.md` and external issues when available. Use only categories relevant to the project, with empty categories explicitly marked none when initially created. Do not invent issues. |
| `QUARANTINE.md` | Closed historical findings: invalidated assumptions, superseded claims and rejected approaches, with dates, reasons and pointers to current evidence. Prevents repeating settled mistakes. Preserve existing historical content; if nothing has been invalidated, state that explicitly rather than inventing items. |
| `AGENTS.md` | Durable instructions automatically discovered by Codex for this project and its scope: concise project-specific rules and pointers to the handoff notes. Preserve higher-priority rules and existing instructions; avoid duplicating volatile status. For Claude Code, inspect and preserve `CLAUDE.md` as well, and update it when appropriate or requested; it does not replace the required `AGENTS.md`. |
| `resume.md` | Current verified snapshot: progress, changed files, checks and results, running jobs if checked, blockers and the concrete next step. Link the five files. This is a handoff record, not proof the original source is unchanged. |

`INTENTION.md`, `TODO.md`, `ISSUE.md`, `QUARANTINE.md`, and `resume.md` are project conventions, not files automatically loaded by default. Point to them from `AGENTS.md` and tell the next session to read them. `README.md` is the human-facing entry point.

## Workflow

1. Review the user's goal, conversation, project instructions and existing records. Inspect Git status and recent commit when the project is a Git repository, without changing either. Verify running jobs, file paths and test results only where relevant and observable. Keep verified facts, previous reports, assumptions, uncertainty and open questions distinct; exclude secrets and credentials.
2. Create or update all required records and `resume.md` using the purposes above. Use the user's language. Identify the canonical source and timestamp time-sensitive state. Link related notes; preserve existing conventions and unrelated edits. Do not fabricate findings or change `AGENTS.md` into a transcript.
3. For an invalidated claim, preserve historical context and identify the current source of truth. Where the project uses the lab wiki's marker convention, apply dated `SUPERSEDED`, `CAUTION`, `PARTIAL` or `ARCHIVED BELOW` markers and links; record unresolved issues in `ISSUE.md` and link actionable work from `TODO.md`.
4. Codex `/init` can generate `AGENTS.md`; Claude Code `/init` can generate `CLAUDE.md`. Review generated guidance if initialization is requested. Do not invoke `/init` merely for a handoff or overwrite existing instructions.
5. Re-read the records and reconcile with observed state. Report every file path, unresolved uncertainty, and a short restart prompt. Do not clear the conversation, commit, push, stop jobs, change sharing or send messages unless explicitly requested.
