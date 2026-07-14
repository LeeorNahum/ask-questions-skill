# AGENTS.md

Rules for editing the **ask-questions** skill. User-facing guidance lives in `SKILL.md`. `README.md` is the human skim layer.

## File roles

| File | Role |
| --- | --- |
| `SKILL.md` | When to ask, question shapes, structured question rules, response pattern, blocker rule |
| `README.md` | Short human summary |

## Editing

- Bump `metadata.version` with semver in the same change whenever behavior changes: patch for wording, minor for new guidance or a new question shape, major for a changed turn-limit or scope.
- Quote every frontmatter string value. Keys stay unquoted.
- No em dashes, and no semicolons used to join what should be separate sentences. Use commas, periods, parentheses, or "to".
- Capitalized bullets and parallel list voice.
- Keep the one-question default and two-question hard cap intact in every place that states it (description and body). Do not loosen it without updating both.

## Before finishing

- `metadata.version` bumped if and only if behavior changed.
- `README.md` matches the actual file layout.
