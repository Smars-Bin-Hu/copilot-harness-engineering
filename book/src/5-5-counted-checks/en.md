This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html), which explains why a checker with a separate context is worth having. Here the question is a different one: how do you know a check really happened and really passed?

## In one sentence {#in-one-sentence}

For a check to count, the passes have to be counted by code. Do not take the agent's word that it checked.

## For leaders {#for-leaders}

- **The decision:** decide that "checked" means a record that code counts, not the agent's word. The person sets how many passes in a row are needed, and only the person can waive the rule.
- **The risk:** "I had it checked and it passed" cannot be tested, because the agent may have skipped the check, checked an older version, or read a FAIL as a pass. Waivers can also become a habit, and then the limit is only decoration.
- **The cost of doing it right:** extra checks cost usage every time, and the counter needs a fingerprint of the work that includes the right things. In my setup the limit is n checks plus two extra, an example rather than a tuned value. Without any machinery, you can still ask for the command and its result.
- **Ask the team:** "For the last change that shipped, show me the record that a check ran on that exact version."

## Why "I had it checked" proves nothing {#problem}

Say you want every piece of work to pass an independent check before it is written back to a repository (see [Two gates](5-3-two-approvals.html) for the write-back, the step that copies finished work into the real repository). You write that in the rules. The agent finishes and tells you: "I had it checked, and it passed."

What can you do with that sentence? Nothing. It may be true, but the agent may also have skipped the check, or checked an older version of the work, or read a FAIL as a pass because it wanted to be done. A sentence in a chat is the cheapest thing an agent produces. It is also the one thing you cannot test.

Underneath that sentence are three questions: did the check happen, was it on this version, and what was the verdict? Answering them gives you a guarantee about the process, not about the quality of the work. Getting that guarantee takes the same idea as in [Requests and rules](4-1-requests-and-rules.html): instead of asking the agent whether it did the thing, make the thing leave a trace that code can read, then let code decide. So what would that trace be, and what would code do with it?

## Let code keep the record and count the passes {#how-it-works}

### The checker's answer is saved by code, not by the agent

The first trace is the checker's answer itself. When the checker replies, a hook writes the answer, exactly as it was written, to a file the agent cannot edit. Because the first line of the answer is fixed as PASS or FAIL ([Use subagents sparingly](2-3-subagents.html)), the question "did a check happen, and what was the verdict?" becomes a question about files that a small program can answer.

### Count passes in a row, on the exact work

One recorded pass is still weak evidence, because a checker is a model and can be lucky or wrong. Asking for several passes in a row lowers the chance that the work got through on one lucky verdict. It cannot remove a blind spot that every run shares, though, because the checkers are all the same kind of model ([Can a model check a model?](5-6-model-checks-model.html)). How many are enough is therefore a judgment, and the person makes it: **n passes in a row**. In my setup the person writes the number in a prompt, for example "two passes in a row". The agent cannot write it for itself.

Code does the counting. Starting from the latest check, it walks back and counts the PASSes in a row until it reaches the first FAIL. It stops there because a FAIL is usually followed by an edit that changes the work, so the passes before it no longer count. In other words, the n passes must all be on one version, and not just any version: a PASS counts only if it checked **exactly the work as it is now**.

::: figure 5-5-pass-counter

But what does "exactly" mean here? The code takes a **fingerprint** of the work, which is a hash (a short code that changes when the content changes) of the result files, the requirement and the plan. Each check records the fingerprint it saw, so if the fingerprint now is different, that check was about older work and does not count.

What goes into the fingerprint decides whether the count stays honest. Only things that change the result belong there, so progress notes, logs and the checker's own records are left out. If they were in, ticking off a to-do item would cancel a pass and reset the counter for nothing. The requirement and the plan, on the other hand, are in, so a change to either one resets the count too. A pass against an old plan says little about the new one.

The count then gates the next move. The step that writes the work back to the repository is refused until the passes reach n. The agent has no path around that, because the only way to raise the count is to get the work checked again.

### A limit on the number of checks

What if the passes never reach n? That can happen when a checker keeps finding something. If every round brings new findings, the loop never ends. So there is a **limit** of n checks plus a small margin (in my setup two extra, an example rather than a tuned value). When the checks are used up without enough passes, the agent stops and tells the person where the last findings are. The person then chooses, by typing a code in a terminal, whether to allow more checks or to waive the rule for this version. The first option simply gives the checker more rounds. The second needs a closer look.

### Waivers

A **waiver** lets the current version through without enough passes. People need it, because sometimes the last findings are only about wording, or the checker is wrong, and the person has read the work and is satisfied. Three rules keep a waiver safe. Only the person can grant it, through a channel the agent cannot reach ([Two gates](5-3-two-approvals.html) says how). A waiver also covers one version only, so when the work changes again the waiver ends and the count starts over. And it leaves a record, so later you can see that this version went through on a person's decision rather than on passes.

A second tool works the other way round. Instead of letting a version through without enough passes, it takes away one check that the person judges was wrong. Once the person sets that check aside, it no longer counts, neither as a check used nor as a FAIL.

### Without the machinery

All of this assumes a checker agent and code that counts its passes. If you have no checker agent, the idea still holds: do not accept "I checked". Ask the agent to paste the command it ran and its result, then read the verdict yourself. After any later edit, ask again.

### Checks on, but nothing checked

Back in the setup with a checker, everything counted so far assumes that the agent actually calls it. The sneakiest failure is silence, where checks are on and the agent simply never calls the checker. No FAIL is ever recorded, because nothing ran. A rule in the prompt will not catch this either, because the agent is the one who forgot.

So the check goes where the agent has to pass through, which is the moment it tries to stop. A hook ([Hooks](2-2-hooks.html)) at that moment compares the state with the facts. If checks are on and there has been no check, or the work changed after the last one, it blocks once and tells the agent to catch up. Whatever the agent does with that reminder, the write-back gate ([Two gates](5-3-two-approvals.html)) stays closed, because the count is still below n.

### What the checker hands in

A count is only as good as what is counted, so the checker's answer has a fixed shape, as in [Use subagents sparingly](2-3-subagents.html). After the answer comes in, a script checks that shape and drops any finding whose file or line does not exist. A FAIL with nothing left is **invalid**: the check is given back, so a vague checker does not eat the budget.

The script checks the shape, though, not the judgment. Whether the checker is right is still a model's opinion, and that is the subject of [Can a model check a model?](5-6-model-checks-model.html).

## What counting costs, and what it cannot prove {#costs-and-traps}

The first thing to get right is the fingerprint. If it includes too much, every small edit cancels the passes and you pay for the checks again. If it includes too little, a change slips past a pass. I have not found a perfect list, so I decide by asking "does this file change what the work is?".

Even with the right fingerprint, a counted pass is only as strong as the checker. The counter proves that a check happened on this exact version, but it does not prove the checker was right. Two checkers can give different verdicts on the same work ([Can a model check a model?](5-6-model-checks-model.html)). That is one reason to allow more than one pass in a row for important changes. How often a checker is wrong, I have not measured.

Nor does a counted pass replace running things. A pass from a read-only checker is a pass about reading. For checks the agent can run, such as tests and linters, see [Let the agent check its own work](5-4-self-checks.html), where the same warning applies: a test that "passed" means little unless you can see the command and its output. Anthropic's guide says it directly: "'All tests pass' on its own tells you very little" ([Best practices](https://code.claude.com/docs/en/best-practices)).

The last trap sits with the person, not the agent: waivers can become a habit. If a person waives every time the limit is hit, the limit is only decoration. The record of waivers is how you notice.

## When to delete the counter {#when-to-delete-it}

A counter like this exists because the platform has no built-in notion of "this work was independently checked, n times, on this version". If a platform adds that, with a record the agent cannot change, use it and drop the counter. The idea behind it does not retire, though: the person, not the agent, decides what counts as checked.

## Try it on your own setup {#try-it}

::: prompt
Look at how this project shows that a check really happened: CI configuration, required reviews, status checks, review comments, and any file the agent writes to say it checked something. For each kind of record, tell me whether it is tied to the exact commit, who or what can edit or fake it (including the agent), and what happens to it if the code changes afterwards. Point out any place where the only evidence is someone's sentence. Do not change any files.
:::

## Go deeper {#go-deeper}

- Claude Code docs: [Best practices](https://code.claude.com/docs/en/best-practices) (ask for evidence, not a claim)

## Explore it in the harness {#explore}

The counting, the limit, the waiver and the catch-up at stop all run in Copilot Harness, so the harness can teach them to you from the inside, with a real record of checks.

::: prompt
/harness-rookie-wondering I have read the chapter "Make a pass count". Teach me how this harness counts independent checks (topic 11): how the passes in a row are worked out, what the limit is, what allowing more checks, waiving and setting a check aside do, and what happens when checks are on but nothing was checked. Open a real task's record of checks with me and draw how the pieces fit together.
:::
