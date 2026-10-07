# ask-questions-skill

`ask-questions` helps an agent ask earlier, better, and more useful clarifying questions.

It is for ambiguous or collaborative tasks where the agent should ask more often when unsure, unclear, or wanting confirmation, and should strongly prefer a dedicated question tool when one exists so the user can answer inline during the same flow.

It pushes the agent toward useful questions, real options, brief framing, and explicit recommendations instead of passive guessing or empty multiple choice.

The skill asks one decision at a time and keeps going as each answer arrives. Each question carries what the user needs to decide: the current state, what would change, the exact text when the decision is about wording, and a recommendation when there is one.

## Files

- `SKILL.md` contains the question-asking rules.
- `AGENTS.md` is the maintenance contract for editing this skill.
