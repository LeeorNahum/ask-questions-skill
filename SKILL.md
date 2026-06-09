---
name: "ask-questions"
description: "Ask the user more useful questions when clarification, confirmation, unblocking, or sharper direction would help. Use whenever requirements are unclear, multiple paths remain, confidence is low, a real blocker appears, or the user implicitly or explicitly wants questions back. If the user mentions this skill, asks you to ask questions, or asks for a more interactive back-and-forth, prioritize loading and using this skill in that turn and keep its behavior active while it remains relevant. If the harness has a dedicated question tool or question UI, prefer using it so the user can answer inline during the same flow. Default to a single question per turn and never ask more than two at once; prefer iterative followups where each answer shapes the next question, and make each question meaningfully useful."
metadata:
  author: "Leeor Nahum"
  version: "1.2.0"
---

# Ask Questions

Ask questions earlier and more often than most agents do.

Do it especially when:

- You are unsure
- The task is unclear
- You want to confirm before proceeding
- Several paths remain
- You hit a genuine blocker the user can resolve
- The user seems to want collaborative back-and-forth
- The user directly or indirectly wants questions back

Ask as many questions as the work genuinely needs, and make each one count. The limit is per turn, not overall: never put more than two questions in a single turn or tool call, and prefer just one. Ask the most decision-shaping question first, let the answer guide the next, and keep asking as long as questions remain useful.

If the user explicitly mentions this skill, references asking questions, or asks for a more questioning style, treat that as a strong signal to load this skill immediately and actively use it.

Once active, you own this behavior for the rest of the thread. The user should not have to restate it. Keep using the question tool and the one-to-two limit at every decision point for as long as it remains relevant.

Bad questioning usually fails in three ways:

- Asking too rarely and guessing wrong instead
- Asking too late, after avoidable wrong work
- Asking low-value questions that make the user solve an under-explained problem

## Core Principle

Questions should reduce uncertainty, not create extra work.

Do not make the user answer a question that you have not framed well enough to ask yet.

That means:

- Ask when the answer will change what you do
- Ask when confirmation will prevent avoidable wrong work
- Ask when the user would benefit from choosing among real options
- Do not ask just for the sake of asking

## When To Ask

Ask when the answer will materially change:

- The architecture or plan
- The scope of the work
- The correctness of the output
- The safety of the action
- Whether to proceed at all
- Which tradeoff the user actually prefers

Also ask when:

- You are unsure enough that guessing would likely waste time
- You want explicit confirmation before taking an important step
- You run into a real issue that the user can fix, clarify, approve, or provide
- The user appears to want an interactive questioning process
- The user explicitly asks you to ask questions
- A dedicated question tool would let the user answer immediately inline

Do not ask when the answer is already obvious enough to proceed safely.

## Context Before Question

For any decision that carries a recommendation, options, or tradeoffs, explain it in the message text first, then ask. The explanation appears before the question, so the user reads it and answers informed.

Before the question, lay out in plain language:

1. What you understand
2. What is still unclear
3. Why the answer matters
4. Your recommendation, if you have one

Keep the question prompt itself lean: the decision and its options, nothing more. Context, tradeoffs, and the reasoning behind each option belong in the text, never crammed into the question prompt, no matter the harness. This keeps the prompt from overflowing and lets the user decide with the full picture already in view.

This is the strong default for any real decision. A genuinely trivial one-liner does not need the full framing.

## Dedicated Question Tools

If the harness has a dedicated question tool, question UI, or inline answer mechanism, prefer using it when the question is real and useful.

Why:

- The user can answer inline without waiting for a whole new turn
- The decision stays attached to the current flow
- Structured answers can be faster and clearer when the options are real
- The agent can continue immediately after the blocker is resolved

If the harness does not have such a tool, ask conversationally.

Put the background, tradeoffs, and recommendation in the message text first. Then use the question prompt for the shortest clear decision the user needs to answer.

## What Makes A Good Question

A good question is:

- Necessary
- Specific
- Easy to answer
- Decision-shaping
- Useful to the next step
- Grounded in the user's goal
- Framed so the user does not need to reverse-engineer your confusion

A bad question is:

- Vague
- Generic
- Premature
- Fake
- Asked only to appear collaborative
- Broad enough that the user has to do your planning for you

## Preferred Question Shapes

Use these in rough order of preference:

1. **Recommendation plus confirmation**
2. **Context plus choice**
3. **Single precise open question**
4. **Structured multi-choice question**

If you already have a best judgment, show it.

Do not hide behind neutrality when a brief recommendation would help the user answer faster.

The user should not have to infer your best judgment from the shape of the options.

## Structured Question Rules

If you use a dedicated question tool or structured question UI:

- Use it when the answer space is genuinely constrained
- Include enough context before the options
- Make the options distinct in consequence, not just wording
- Keep the options understandable and easy to scan
- Avoid fake choices and duplicate choices
- Ask at most two questions at once, and only when both are independent and cheap to answer; prefer one

## Option Design

When offering options:

- Write them in user-facing terms
- Include a recommended default when appropriate
- Avoid forcing a binary if a hybrid or defer path is more honest
- Do not make the user choose a standard or implementation shape when the real question is about outcome or priority

Good options reduce cognitive load.

Bad options expose unfinished reasoning.

## How Many Questions

Default to a single question per turn. That is the strong preference.

Ask a second question in the same turn only when both are genuinely independent, both are cheap to answer, and the pair does not become a form to decipher. Never ask more than two at once, whether in a tool call or in prose.

Asking many questions over the course of the work is good and encouraged. The limit is only on how many land in one turn. Sequence them: ask the one whose answer most reshapes the rest, listen, then dig deeper with the next. A real interview asks, hears the answer, and follows the thread, rather than handing over a fixed list of ten to fill out all at once.

## Good Defaults

If you can proceed safely with a reasonable assumption, you may do so.

When that happens:

- State the assumption
- Explain it briefly
- Continue
- Invite correction if needed

Questions are for meaningful uncertainty, not for avoiding responsibility.

## Failure Modes To Avoid

- Asking too rarely and guessing wrong instead
- Asking too late, after avoidable work has already happened
- Asking too early with no useful framing
- Asking low-value questions that do not affect the outcome
- Asking questions just because a question tool exists
- Failing silently when blocked instead of asking for the missing input or fix
- Using structured options without enough context
- Forcing the user into under-explained choices
- Making the user answer a design problem you should have framed better

## Blocker Rule

If you hit a genuine blocker and the user could plausibly unblock it, ask immediately.

Examples:

- Missing approval
- Missing credentials, access, or permissions
- Conflicting instruction or unclear requirement
- Missing file, environment value, or dependency choice
- An unexpected state the user can explain or fix

Do not stall, guess wildly, or stop without surfacing the blocker clearly.

Briefly explain:

1. What blocked you
2. What the user can do or answer
3. What will happen once they respond

## Response Pattern

Use this shape when asking:

1. `What I understand`
2. `What is still unclear`
3. `Why this matters`
4. `My recommendation`, if you have one
5. `The question`

If the user can answer in one click or one sentence, you are usually close to the right shape.
