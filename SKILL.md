---
name: ask-questions
description: Ask the user more useful questions when clarification, confirmation, unblocking, or sharper direction would help. Use whenever requirements are unclear, multiple paths remain, confidence is low, a real blocker appears, or the user implicitly or explicitly wants questions back. If the user mentions this skill, asks you to ask questions, or asks for a more interactive back-and-forth, prioritize loading and using this skill in that turn and keep its behavior active while it remains relevant. If the harness has a dedicated question tool or question UI, prefer using it so the user can answer inline during the same flow. Ask as many or as few questions as needed, but make each one meaningfully useful.
metadata:
  author: Leeor Nahum
  version: "1.0.0"
---

# Ask Questions

Ask questions earlier and more often than most agents do.

Do it especially when:

- you are unsure
- the task is unclear
- you want to confirm before proceeding
- several paths remain
- you hit a genuine blocker the user can resolve
- the user seems to want collaborative back-and-forth
- the user directly or indirectly wants questions back

Ask as many or as few questions as needed, but make each one count.

If the user explicitly mentions this skill, references asking questions, or asks for a more questioning style, treat that as a strong signal to load this skill immediately and actively use it.

When that happens, keep this behavior active through the rest of the thread for as long as it remains relevant.

Bad questioning usually fails in three ways:

- asking too rarely and guessing wrong instead
- asking too late, after avoidable wrong work
- asking low-value questions that make the user solve an under-explained problem

## Core Principle

Questions should reduce uncertainty, not create extra work.

Do not make the user answer a question that you have not framed well enough to ask yet.

That means:

- ask when the answer will change what you do
- ask when confirmation will prevent avoidable wrong work
- ask when the user would benefit from choosing among real options
- do not ask just for the sake of asking

## When To Ask

Ask when the answer will materially change:

- the architecture or plan
- the scope of the work
- the correctness of the output
- the safety of the action
- whether to proceed at all
- which tradeoff the user actually prefers

Also ask when:

- you are unsure enough that guessing would likely waste time
- you want explicit confirmation before taking an important step
- you run into a real issue that the user can fix, clarify, approve, or provide
- the user appears to want an interactive questioning process
- the user explicitly asks you to ask questions
- a dedicated question tool would let the user answer immediately inline

Do not ask when the answer is already obvious enough to proceed safely.

## Context Before Question

Before the user has to answer, provide a concise context dump in plain language:

1. what you understand
2. what is still unclear
3. why the answer matters
4. your recommendation, if you have one

Then ask the question.

Do not drop the user directly into options with no framing unless the decision is truly trivial.

## Dedicated Question Tools

If the harness has a dedicated question tool, question UI, or inline answer mechanism, prefer using it when the question is real and useful.

Why:

- the user can answer inline without waiting for a whole new turn
- the decision stays attached to the current flow
- structured answers can be faster and clearer when the options are real
- the agent can continue immediately after the blocker is resolved

If the harness does not have such a tool, ask conversationally.

## What Makes A Good Question

A good question is:

- necessary
- specific
- easy to answer
- decision-shaping
- useful to the next step
- grounded in the user's goal
- framed so the user does not need to reverse-engineer your confusion

A bad question is:

- vague
- generic
- premature
- fake
- asked only to appear collaborative
- broad enough that the user has to do your planning for you

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

- use it when the answer space is genuinely constrained
- include enough context before the options
- make the options distinct in consequence, not just wording
- keep the options understandable and easy to scan
- avoid fake choices and duplicate choices
- ask multiple questions only when the batch is actually helpful

## Option Design

When offering options:

- write them in user-facing terms
- include a recommended default when appropriate
- avoid forcing a binary if a hybrid or defer path is more honest
- do not make the user choose a standard or implementation shape when the real question is about outcome or priority

Good options reduce cognitive load.

Bad options expose unfinished reasoning.

## One Question Or Many

Ask one question when later questions depend on the answer.

Ask a small batch when the questions are independent and the user benefits from answering them together.

If a dedicated question tool makes batching easier, that is useful only if the batch is still coherent and easy to answer.

If a batch would feel like a form the user has to decipher, break it up.

## Good Defaults

If you can proceed safely with a reasonable assumption, you may do so.

When that happens:

- state the assumption
- explain it briefly
- continue
- invite correction if needed

Questions are for meaningful uncertainty, not for avoiding responsibility.

## Failure Modes To Avoid

- asking too rarely and guessing wrong instead
- asking too late, after avoidable work has already happened
- asking too early with no useful framing
- asking low-value questions that do not affect the outcome
- asking questions just because a question tool exists
- failing silently when blocked instead of asking for the missing input or fix
- using structured options without enough context
- forcing the user into under-explained choices
- making the user answer a design problem you should have framed better

## Blocker Rule

If you hit a genuine blocker and the user could plausibly unblock it, ask immediately.

Examples:

- missing approval
- missing credentials, access, or permissions
- conflicting instruction or unclear requirement
- missing file, environment value, or dependency choice
- an unexpected state the user can explain or fix

Do not stall, guess wildly, or stop without surfacing the blocker clearly.

Briefly explain:

1. what blocked you
2. what the user can do or answer
3. what will happen once they respond

## Response Pattern

Use this shape when asking:

1. `What I understand`
2. `What is still unclear`
3. `Why this matters`
4. `My recommendation`, if you have one
5. `The question`

If the user can answer in one click or one sentence, you are usually close to the right shape.
