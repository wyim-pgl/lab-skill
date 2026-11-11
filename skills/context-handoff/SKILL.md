---
name: context-handoff
description: Use when preparing a project handoff before clearing context, starting a fresh session, or transferring work between Codex and Claude Code.
---

# Context handoff

Preserve the user's goal and enough verified project state for another session or person to continue. Inspect existing project instructions and handoff files first; follow their naming and structure when they already serve the same purpose. Use the user's language.

1. Review the conversation and project state. For a Git project, inspect the working tree and recent commit without changing either. Check running jobs and test results only where relevant and observable. Distinguish verified facts, prior reports, uncertainty, and unfinished work. Keep secrets and credentials out of handoff notes.
2. Record durable purpose, intended outcome, constraints and decisions in `intention.md`. Preserve the user's intent and identify open decisions. This is a project convention, not a file automatically loaded by either tool.
3. Update `resume.md` with the current state, relevant paths, changes, validation and results, running work, blockers, and concrete next action. Include a session identifier if known and useful. Do not invent identifiers or claim a process is running without checking.
4. Update `todo.md` with outstanding work and dependencies; mark completed tasks with dates and commit references when known. Keep rejected approaches and superseded facts out of current tasks. Where the project uses `quarantine.md` or a similar archive, link to it and retain historical context.
5. Check the project instruction file for the active tool: Codex uses `AGENTS.md`; Claude Code uses `CLAUDE.md`. These files hold durable project guidance, not a dump of the current session. If requested to initialize a project, explain that the tool's `/init` can generate its corresponding file; review the result, preserve existing instructions, and do not run `/init` merely because a handoff is requested. If appropriate, add concise pointers to the handoff files so future sessions know when to read them.
6. Read back the changed notes and reconcile them with observed state. Provide the user the paths, outstanding uncertainty, and a short restart prompt asking the next session to read the handoff files and inspect current state. Do not clear the conversation, commit, push, stop jobs, or change external systems as part of the handoff unless explicitly requested.

If the current work is a remote document or there is no project directory, do not fabricate a repository or imply local notes capture inaccessible state. Provide a portable handoff in the requested destination, including links or identifiers and the same purpose, status, and next-step information.
