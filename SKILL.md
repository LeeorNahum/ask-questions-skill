---
name: "ask-questions"
description: "Use whenever requirements are unclear, multiple paths remain, confidence is low, a real blocker appears, several decisions or open items need the user's answer, or the user implicitly or explicitly wants questions back, and load it in that turn when the user mentions this skill, asks you to ask questions, or asks for a more interactive back-and-forth. Asks the user more useful questions when clarification, confirmation, unblocking, or sharper direction would help."
metadata:
  author: "Leeor Nahum"
  version: "2.0.0"
---

# Ask Questions

Ask questions earlier and more often than most agents do. Ask as many questions as the work genuinely needs, and make each one count. Keep asking as long as questions remain useful.

If the user explicitly mentions this skill, references asking questions, or asks for a more questioning style, treat that as a strong signal to load this skill immediately and actively use it.

Once active, you own this behavior for the rest of the thread. The user should not have to restate it. At every decision point that warrants a question, keep using the question tool and the limit in How Many Questions for as long as it remains relevant.

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

- You are unsure enough that guessing would likely waste time, or the task itself is unclear
- Several real paths remain
- You want explicit confirmation before taking an important step
- You run into a real issue that the user can fix, clarify, approve, or provide
- The user wants questions back or a collaborative back-and-forth, whether they ask directly or indirectly
- A dedicated question tool would let the user answer immediately inline

Do not ask when the answer is already obvious enough to proceed safely.

## Context With The Question

Everything the user needs in order to decide travels inside the prompt, where a prompt is one ask: a single question-tool call, or a single message that asks. With a question tool, the prompt is what the user reads, and text written before the tool call is easily missed.

In plain language, the prompt carries:

1. What you understand, including the current state
2. What is still unclear, and what would change
3. Why the answer matters
4. The exact text, when the decision is about a draft, a message, a command, or any other wording. Show the thing itself, never a description of it
5. Your recommendation, if you have one

Make it complete but short: a few sentences plus any exact text, and nothing that would not change the answer. Options say what each choice does. What the user must read before choosing stays in the question text, not anywhere they have to open or look aside to see. Only when the tool cannot hold the material, such as a full document, keep the framing and the passage being decided in the prompt, put the rest in the text just before the tool call, and say so in the prompt.

This is the strong default for any real decision. A genuinely trivial one-liner does not need the full framing.

If the user can answer in one click or one sentence, you are usually close to the right shape.

## Dedicated Question Tools

If the harness has a dedicated question tool, question UI, or inline answer mechanism available, ask through it whenever the question is real and useful.

When its answer comes back inside the same turn, chain: ask, read the answer, act on it or note it, then ask the next, and do not end the turn while decisions that need the user remain. Ending the turn on a question written as plain text, or on a report followed by a question about what to do next, is a failure when such a tool is available and can carry the question.

If the harness has no such tool, or the tool cannot carry the question, ask conversationally.

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

- Offer options when the answer space is genuinely constrained, and ask an open question through the same tool when it is not
- Include the context in the prompt, ahead of the options
- Make the options distinct in consequence, not just wording
- Keep the options understandable and easy to scan
- Avoid fake choices and duplicate choices

## Option Design

When offering options:

- Write them in user-facing terms
- Include a recommended default when appropriate
- Offer few options
- Leave room for the user's own answer, and add that option when the tool does not provide one
- Avoid forcing a binary if a hybrid or defer path is more honest
- Do not make the user choose a standard or implementation shape when the real question is about outcome or priority

Good options reduce cognitive load.

Bad options expose unfinished reasoning.

## How Many Questions

Default to a single question per prompt. That is the strong preference.

Ask a second question in the same prompt only when both belong to the same decision, both are cheap to answer, and the pair does not become a form to decipher. Never ask more than two at once, whether in a tool call or in prose, unless the user asks for more, such as one question per item on a list they want to confirm. People answer one question with context better than several at once, and a later question often changes with the first answer, so asking it early wastes it.

Separate decisions get separate prompts, never one multi-select. Multi-select fits only a single decision whose answer is a set.

Asking many questions over the course of the work is good and encouraged. The limit is only on how many land in one prompt. Sequence them: ask the one whose answer most reshapes the rest, listen, then dig deeper with the next. A real interview asks, hears the answer, and follows the thread, rather than handing over a fixed list of ten to fill out all at once.

Walk a list of open items the same way, one item per prompt, instead of reporting them all and asking once at the end.

When the user's answer is itself a question or a correction, open the next prompt by answering it in a sentence or two, then ask what is still needed, which may be the same decision again.

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
- Asking questions just because a question tool exists

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
