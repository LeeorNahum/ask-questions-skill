# AGENTS.md

Rules for editing the **ask-questions** skill. User-facing guidance lives in `SKILL.md`. `README.md` is the human skim layer.

## File roles

| File | Role |
| --- | --- |
| `SKILL.md` | Asking through the tool before a turn ends, what goes inside the question, the visible limit, options, when to ask, the per-prompt limit, reading the answer |
| `README.md` | Short human summary |

## Editing

- Bump `metadata.version` by the release-versioning skill's rules for skills.
- Quote every frontmatter string value. Keys stay unquoted.
- No em dashes, and no semicolons used to join what should be separate sentences. Use commas, periods, parentheses, or "to".
- Capitalized bullets and parallel list voice.
- The one-question default and two-question cap are stated once, in How Many Questions. Do not restate them in other sections. Do not loosen the cap without a major version bump.

## Design notes

A dedicated question tool is preferred because:

- The user can answer inline without waiting for a whole new turn
- The decision stays attached to the current flow
- Structured answers can be faster and clearer when the options are real
- The agent can continue immediately after the blocker is resolved

Context goes inside the prompt because users read the prompt and skip the text before it.

The failures this skill exists to stop:

- The agent ends its turn on a report or a plain-text question instead of asking through the tool
- What the user had to read was placed where the tool hides or shortens it: before the call, in a side preview, in an option description, or behind a checkbox label
- The question used the agent's own labels, or asked about something the user had never seen
- The agent asked what it could have decided or what was already answered
- Several decisions were bundled into one prompt
- A question the user typed into the answer box went unanswered

The description leads with the end-of-turn trigger because the first failure happens when the skill is not loaded at that moment. Tools are named in two places, because an agent that does not connect "question tool" to the tool it holds writes the question as text: the bullet that says what a question tool is, and The Visible Limit, which carries each measured figure. Keep everything else tool-agnostic.

Do not add a word such as "short" or "brief" to the rules for the question text. Agents shorten the material until the user can no longer decide from it. The visible limit is a reason to split, never to trim.

The 2,000-character figure for Claude Code's AskUserQuestion was measured in the terminal client, version 2.1.295 (Claude Code), by sending a question with a running character count on each line and asking the user where it ended. A count of lines made no difference. Measure a tool the same way before adding its figure, and remeasure when a harness changes its question interface.

The section on asking through the tool states the end-of-turn rule and the chaining rule once each. Do not restate them in other sections.

Long material is split across prompts, not across the questions of one call. In a call that carries several questions, a spoken or typed number can select an option and move the user to the next question before they have finished answering, which loses the answer.

## Before finishing

- `metadata.version` bumped as the release-versioning skill requires.
- `README.md` matches the actual file layout.
