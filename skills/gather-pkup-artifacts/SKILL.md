---
name: gather-pkup-artifacts
description: Gather PKUP submission artifacts from a GitHub or GitLab repository by listing the current git user's commits in the PKUP reporting window, deriving valid commit URLs from the origin remote, and using commit messages to write a Markdown table with Date, Location, Item title, and Description. Use when Codex is asked to prepare PKUP, IP box, copyright transfer, work artifact, or monthly commit evidence from any local git repository.
---

# Gather PKUP Artifacts

## Overview

Prepare PKUP artifact evidence from the current git repository. Always base the reporting window on the current date unless the user provides an explicit anchor date or date range.

## Quick Start

Run the helper script from the target repository to collect source commit data:

```bash
python3 /path/to/gather-pkup-artifacts/scripts/gather_pkup_artifacts.py
```

The script prints a source table with `Date`, `Location`, `Commit subject`, and `Commit body`. If the repository path is different from the current working directory, pass it explicitly:

```bash
python3 /path/to/gather-pkup-artifacts/scripts/gather_pkup_artifacts.py --repo /path/to/repo
```

## Workflow

1. Identify the target git repository.
2. Invoke `git config --get user.email` in that repository and use that email to filter commits for the current user.
3. Invoke `git remote get-url origin` in that repository.
4. Compute the default PKUP window as the 19th day of the previous calendar month at 00:00 through the 18th day of the current calendar month at 23:59:59, using the current date as the anchor.
5. List commits for that user in chronological order with commit hash, refs, commit datetime, subject, and body.
6. Convert the origin URL into a commit URL. If the host has a suffix such as `github.com-work`, use the canonical host `github.com`; apply the same rule for `gitlab.com-*`.
   - GitHub: `https://github.com/OWNER/REPO/commit/<sha>`
   - GitLab: `https://gitlab.example.com/GROUP/PROJECT/-/commit/<sha>`
7. Use the source commit subject/body as evidence and write `Item title` and `Description` with LLM judgment. Do not rely on deterministic string rewriting for these fields.
8. Return the final result as a Markdown table with exactly this header:

```markdown
| Date | Location | Item title | Description |
| --- | --- | --- | --- |
```

## Table Rules

- Put one commit per row, ordered from oldest to newest.
- Copy `Date` and `Location` from the source table without changing them.
- Use the source `Commit subject` and `Commit body` to write `Item title` and `Description`.
- Write `Item title` as a short human-readable title with no conventional prefixes such as `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`, `build:`, `ci:`, and optional scopes such as `feat(api):`.
- Write `Description` as a natural work statement based on what the commit created or changed. Prefer the commit body when it has useful detail; otherwise infer from the subject.
- Start every description with a factual creation phrase such as `I've implemented`, `I've created`, `I've added`, `I've updated`, `I've extended`, or `I've integrated`.
- Do not form descriptions by blindly prepending `I've implemented` to the title. Convert the commit message into a natural sentence.
- Do not start descriptions with weak process verbs such as `I've fixed`, `I've investigated`, `I've analyzed`, or `I've reviewed`; rephrase to the concrete created or changed artifact.
- Keep descriptions concise and specific enough for a PKUP submission.
- Do not include `Commit subject` or `Commit body` in the final table.

## Helper Script

Use `scripts/gather_pkup_artifacts.py` for source data collection only. The script accepts `--repo`, `--anchor-date YYYY-MM-DD`, `--since YYYY-MM-DD`, and `--until YYYY-MM-DD`. Use explicit `--since` and `--until` only when the user asks for a non-default range.
