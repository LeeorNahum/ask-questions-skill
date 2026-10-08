# ask-questions-skill

`ask-questions` makes an agent ask through the harness's question tool instead of ending its turn on a report or a question written as plain text.

Before a turn ends, the agent checks what still waits on the user and asks it. Everything the user needs to read goes inside the question itself, as long as it needs to be: the state that bears on the answer, the full material, the exact text when the decision is about wording, and a recommendation when there is one. Options are only for choosing. Where a tool shows only the start of a long question, the material is split across several questions, one after another, and never trimmed.

It asks one decision at a time, keeps going as each answer arrives, and answers whatever the user typed back before asking the next thing. It does not ask what it can settle itself.

## Files

- `SKILL.md` contains the question-asking rules.
- `AGENTS.md` is the maintenance contract for editing this skill.
