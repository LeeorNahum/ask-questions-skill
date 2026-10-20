# Results

Raw run output stays in `EVAL_ROOT`, outside this repository. Only this summary is committed.

## Smoke Test

Opus in `claude -p`, one session per run, no scored round yet.

| Run | Result |
| --- | --- |
| `settled-earlier-in-thread`, before the load sentence | Both turns completed in one resumed session, and the second turn kept the first turn's draft rule without asking. The skill never loaded, so the run measured nothing about it. |
| A turn that invites questions, or names the skill, with nothing unclear | The skill never loaded. |
| `obvious-next-step`, opening with the load sentence | The skill loaded, the rename finished, and no question was asked. |
