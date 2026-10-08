---
name: "ask-questions"
description: "Use before writing the final message of any turn in which you are waiting on the user: for a decision, an approval, something only they can supply, or their pick among things you found. Not for a turn that finished the job with nothing left to decide. Also use when requirements are unclear or several real paths remain, and load it in that turn when the user mentions this skill, asks for questions, or asked for them earlier in the thread. Asks through the harness's question tool, with everything to read inside the question."
metadata:
  author: "Leeor Nahum"
  version: "2.1.0"
---

# Ask Questions

Ask questions earlier and more often than most agents do. Ask as many questions as the work genuinely needs, and make each one count. Questions are for meaningful uncertainty, not for avoiding responsibility, and never for the sake of asking.

Once the user mentions this skill, asks for questions, or asks for a more questioning style, that is a standing request for the rest of the thread. The user should not have to restate it.

## Ask Through The Tool Before The Turn Ends

Before writing the final message of a turn, check what still waits on the user. If a decision that changes what you do next is waiting, do not end the turn on a report, a summary, or a question written as plain text. Ask through the question tool. When the answer comes back, act on it or note it, then ask the next thing, and end the turn only when nothing more needs the user or the user says to stop.

- A tool that asks the user and waits for the answer is the question tool whatever its name. It is called AskUserQuestion in Claude Code and request_user_input in Codex, which offers it only in some modes, and differently elsewhere
- Before concluding there is no question tool, check the whole tool list, including tools that must be loaded or searched for first
- A blocker the user could clear is asked the moment it appears: what blocked you, what they can do, and what happens once they answer. When the blocker is a secret, ask the user to put it where the project reads it, never in the answer
- An optional follow-up the user did not ask for is mentioned in a line, not asked
- When no user can answer, as in a headless run, a scheduled task, or an agent working for another agent, do not call the question tool. Where a safe assumption exists, state it in a line, continue, and repeat it in what you hand back. Where none exists, or you cannot continue, stop and hand back the question with what you found
- If the harness has no question tool, or the tool rejects the question, ask conversationally, with the same content in the message

## Everything Goes Inside The Question

The question text is what the user reads. Text written before the tool call is often collapsed or skipped, and the user then answers a question they cannot see the reason for.

Scale the question to the decision. A choice the user can make from one sentence gets that sentence and its options. When the user must read material to decide, such as a draft, a list, numbers, or a comparison, that material goes in the question text in full. Never shorten it, and never swap the thing itself for a sentence describing it.

Where they apply, in this order:

1. The answer to the user's last message, as Reading The Answer describes
2. The current state, only as far as it bears on the answer
3. The material itself: the items, the facts with their numbers, the exact text of any draft, message, or command
4. What is still unclear, what would change, and why the answer matters
5. Your recommendation, if you have one. Do not hide behind neutrality when a recommendation would help the user answer faster
6. The one question, last

Use plain words the user already uses. A label you invented during the work, a file the user has not seen, or a name for something only you have looked at means nothing to them, so say what the thing is. Blank lines, short labels, and hyphen bullets keep long text readable where formatting does not render.

### The Visible Limit

A question tool may show only the start of a long question and cut the rest without telling you. Claude Code's AskUserQuestion shows the first 2,000 characters of the question text and replaces everything after with an ellipsis. Where a tool's limit is not known, treat 2,000 characters as the limit. The question itself comes last, so it is the first thing a cut removes.

You cannot count characters while writing, so judge by words. In plain prose 300 words is about 1,700 characters, which leaves a margin, so split at 300 words and not before. Commands, paths, code, logs, and tables run far more characters per word. For those, or whenever the size is in doubt and you can run code, measure the text before sending.

Material that does not fit is split, not shortened:

- Break it at natural parts and send one part per prompt, in order
- Each part ends with a question about that part, so the user reacts to it while it is in front of them. The last part ends with the decision on the whole when it fits there. When it does not, the decision is its own prompt after a short recap
- Say what comes next, such as "next: the pricing section", so the user knows what to expect. Do not number the parts against a total, because the list grows and shrinks as answers arrive

## Options

Options are for choosing, not for reading. Some interfaces collapse or truncate option descriptions, side previews, and checkbox lists, so anything the user must read before choosing stays in the question text.

- Offer options when the answer space is genuinely constrained, and ask an open question through the same tool when it is not. When the tool demands options for an open question, offer the two most likely answers and say a typed answer is welcome. Never add an option that only says to type something
- Make the options distinct in consequence, not just wording, in user-facing terms, and say what each one does
- Put your recommended option first and mark it
- Offer few options, and leave room for the user's own answer, adding that option when the tool does not provide one
- Avoid forcing a binary if a hybrid or defer path is more honest
- Do not make the user choose a standard or implementation shape when the real question is about outcome or priority

Good options reduce cognitive load. Bad options expose unfinished reasoning.

## When To Ask

Ask when the answer will materially change the plan, the scope, the correctness of the output, the safety of the action, whether to proceed at all, or which tradeoff the user prefers. Ask when you are unsure enough that guessing would likely waste time, when several real paths remain, and when you want confirmation before an important step.

Do not make the user answer a question that you have not framed well enough to ask yet, and do not ask what you can settle yourself:

- Check the conversation and the files first. Never ask what the user already answered
- An obvious next step is taken, not offered for permission
- When a reasonable assumption is safe, state it in a line, continue, and invite correction
- Never fill a gap with a guess presented as fact. Ask instead

## How Many Questions

A prompt is one ask: one question-tool call, or one message that asks. Default to a single question per prompt. That is the strong preference.

Ask a second question in the same prompt only when both belong to the same decision, both are cheap to answer, and the pair does not become a form to decipher. Never ask more than two at once, whether in a tool call or in prose, unless the user asks for more, such as one question per item on a list they want to confirm. People answer one question with context better than several at once, and a later question often changes with the first answer, so asking it early wastes it.

Separate decisions get separate prompts, never one multi-select. Multi-select fits only a single decision whose answer is a set.

A list of open items is walked one item per prompt, each prompt naming what comes after it. Show the whole list first only when all of it fits the visible limit.

Asking many questions over the course of the work is good and encouraged. The cap is only on how many land in one prompt. Sequence them: ask the one whose answer most reshapes the rest, listen, then dig deeper with the next. A real interview asks, hears the answer, and follows the thread, rather than handing over a fixed list of ten to fill out all at once.

## Reading The Answer

The user often types a full reply into the answer box: a correction, a new request, a question of their own. Treat it as a message.

- Do what it asks before anything else
- Answer every question in it at the top of the next prompt
- If it changes the decision you asked about, ask that decision again in its new form
- If it says the user could not see or follow something, or that a question was cut off, show that thing in full inside the next question
