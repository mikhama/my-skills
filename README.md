# my-skills
My skills for AI agents

## Available skills
| Skill                 | Description                                                                                                                                                                    |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| gather-pkup-artifacts | To collect PKUP artifacts for submission from a specific repository, open the repository where you want to gather the artifacts, start the assistant shell, and run the skill. |
| explain-current-flow  | Useful helper to check the current implementation flow and find any misalignments with the spec so you can fix bugs.                                                           |

## Setup

User-level setup:

| Assistant      | User-level location  |
|----------------|----------------------|
| Codex          | `~.codex/skills/`    |
| GitHub Copilot | `~/.copilot/skills/` |
| Claude Code    | `~/.claude/skills/`  |
| Cursor         | `~/.cursor/skills/`  |

Install:

```bash
cp -R skills/<skill-name> <assistant-user-level-location>
```
