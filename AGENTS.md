# AGENTS.md

Rules for editing the **ask-questions** skill. User-facing guidance lives in `SKILL.md`. `README.md` is the human skim layer.

## File roles

| File | Role |
| --- | --- |
| `SKILL.md` | When to ask, context with the question, the question tool, question shapes, structured question rules, the per-prompt limit, blocker rule |
| `README.md` | Short human summary |

## Editing

- Bump `metadata.version` by the release-versioning skill's rules for skills.
- Quote every frontmatter string value. Keys stay unquoted.
- No em dashes, and no semicolons used to join what should be separate sentences. Use commas, periods, parentheses, or "to".
- Capitalized bullets and parallel list voice.
- The one-question default and two-question cap are stated once, in How Many Questions. Other sections point there instead of restating them. Do not loosen the cap without a major version bump.

## Design notes

A dedicated question tool is preferred because:

- The user can answer inline without waiting for a whole new turn
- The decision stays attached to the current flow
- Structured answers can be faster and clearer when the options are real
- The agent can continue immediately after the blocker is resolved

Context goes inside the prompt because users read the prompt and skip the text before it.

## Before finishing

- `metadata.version` bumped as the release-versioning skill requires.
- `README.md` matches the actual file layout.
