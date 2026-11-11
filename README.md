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

## Fetch paper

[fetch-paper](skills/fetch-paper/SKILL.md) finds open-access PDF copies by DOI. Copy `skills/fetch-paper` into the appropriate skills directory and see its [usage guide](skills/fetch-paper/references.md) for email and API-key requirements.

## Lab wiki

[lab-wiki](skills/lab-wiki/SKILL.md) reconstructs project context from the lab wiki and follows its current rules for updates. Copy `skills/lab-wiki` into the appropriate skills directory. A user needs access to the wiki repository and can set `PGL_WIKI` to an existing local clone.
