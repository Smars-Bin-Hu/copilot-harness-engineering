This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html), which explains why a checker with a separate context is worth having. Here the question is a different one: how do you know a check really happened and really passed?

## In one sentence {#in-one-sentence}

For a check to count, code counts the passes. Do not accept the agent's word that it checked.

## For leaders {#for-leaders}

- **The decision:** decide that "checked" means a record that code counts, not the agent's word. The person sets how many passes in a row are needed, and only the person can waive the rule.
- **The risk:** "I had it checked and it passed" cannot be tested. The agent may have skipped the check, checked an older version, or read a FAIL as a pass. Waivers can also become a habit, and then the limit is decoration.
- **The cost of doing it right:** extra checks cost usage each time, and a counter needs a fingerprint of the work that includes the right things. In my setup the limit is n checks plus two extra, which is an example and not a tuned value. Without any machinery, ask for the command and its result.
- **Ask the team:** "For the last change that shipped, show me the record that a check ran on that exact version."

## The problem {#problem}

Say you want every piece of work to pass an independent check before it is written back to a repository (the write-back: copying finished work into the real repository, see [Two gates](5-3-two-approvals.html)). You write that in the rules. The agent finishes, and says: "I had it checked, and it passed."

What can you do with that sentence? Nothing. It may be true. The agent may also have skipped the check, or checked an older version of the work, or read a FAIL as a pass because it wanted to be done. A sentence in a chat is the cheapest thing an agent produces. It is also the one thing you cannot test.

This chapter is about whether the check happened, on this version, with this verdict. It is a guarantee about the process, not about the quality of the work. The fix is the same idea as in [Requests and rules](4-1-requests-and-rules.html): do not ask the agent whether it did the thing. Make the thing leave a trace that code can read, and let code decide.

## How it works {#how-it-works}

### The checker's answer is saved by code, not by the agent

When the checker answers, its answer is written to a file by a hook, as it was written. The agent cannot edit that file. The first line of the answer is fixed: PASS or FAIL ([Use subagents sparingly](2-3-subagents.html)). So "did a check happen, and what was the verdict?" becomes a question about files, and a small program can answer it.

### Count passes in a row, on the exact work

A single pass is weak. A checker is a model, so it can be lucky or wrong. Passing several times in a row lowers the chance of one lucky verdict. It does not remove a blind spot that every run shares, because the checkers are the same kind of model ([Can a model check a model?](5-6-model-checks-model.html)). So the person says how many passes are needed: **n passes in a row**. In my setup the person writes it in a prompt, for example "two passes in a row". The agent cannot write it for itself.

Counting is done by code, and it works like this: start from the latest check and walk back. Count the PASSes in a row. Stop at the first FAIL. A FAIL is usually followed by an edit, and the edit changes the work, so the earlier passes stop counting: the n passes must all be on one version. And count a PASS only if the version it checked is **exactly the work as it is now**.

::: figure 5-5-pass-counter

"Exactly" needs a definition. The code takes a **fingerprint** of the work: a hash (a short code that changes when the content changes) of the result files, the requirement and the plan. A check records the fingerprint it saw. If the fingerprint now is different, that check is about older work, so it does not count.

Two details keep this honest:

- **Only things that change the result are in the fingerprint.** Progress notes, logs and the checker's own records are left out. Otherwise ticking a to-do item would cancel a pass, and the counter would reset for nothing.
- **A change to the requirement or the plan resets the count too.** A pass against an old plan says little about the new one.

The count then gates the next move. The step that writes the work back to the repository is refused until the passes reach n. The agent has no path around it: the only way to raise the count is to get the work checked again.

### A limit on the number of checks

A checker may keep finding something. If every round brings new findings, the loop never ends. So there is a **limit**: n checks plus a small margin (in my setup, two extra; an example, not a tuned value). When they are used up without enough passes, the agent stops and tells the person where the last findings are.

The person then chooses, in a terminal, with a typed code: allow more checks, or waive the rule for this version.

### Waivers

A **waiver** lets the current version through without enough passes. People need it: sometimes the last findings are wording, or the checker is wrong, and the person has read the work and is satisfied. Three rules make a waiver safe:

- **Only the person can grant it**, through a channel the agent cannot reach ([Two approvals](5-3-two-approvals.html) says how).
- **It covers one version.** When the work changes again, the waiver ends and the count starts over.
- **It leaves a record.** Later you can see that this version went through on a person's decision, not on passes.

There is a second tool for the opposite case. If the person judges that one check was wrong, they can set it aside. It no longer counts, neither as a check used nor as a FAIL.

### Without the machinery

If you have no checker agent, keep the idea: do not accept "I checked". Ask the agent to paste the command it ran and its result, and read the verdict yourself. After any later edit, ask again.

### Checks on, but nothing checked

The sneakiest failure is silence: checks are on, and the agent simply never calls the checker. No FAIL is ever recorded, because nothing ran. A rule in the prompt will not catch this, because the agent is the one who forgot.

So the check goes where the agent has to pass through: the moment it tries to stop. A hook ([Hooks](2-2-hooks.html)) at that moment compares the state with the facts. If checks are on and there is no check, or the work changed after the last check, it blocks once and tells the agent to catch up. Then the write-back gate ([Two gates](5-3-two-approvals.html)) stays closed anyway, because the count is still below n.

### What the checker hands in

A count is only as good as what is counted, so the checker's answer has a fixed shape, as in [Use subagents sparingly](2-3-subagents.html). A script checks that shape after the answer. It drops a finding whose file or line does not exist. A FAIL with nothing left is **invalid**: the check is given back, so a vague checker does not eat the budget.

The script checks the shape, not the judgment. Whether the checker is right is still a model's opinion. [Can a model check a model?](5-6-model-checks-model.html) takes that up.

## Costs and traps {#costs-and-traps}

**The fingerprint has to be right.** If it includes too much, every small edit cancels the passes and you pay for checks again. If it includes too little, a change slips past a pass. I have not found a perfect list; I decide by asking "does this file change what the work is?".

**A counted pass is only as strong as the checker.** The counter proves that a check happened on this exact version. It does not prove the checker was right. Two checkers can give different verdicts on the same work ([Can a model check a model?](5-6-model-checks-model.html)); that is one reason to allow more than one pass in a row for important changes. I have not measured how often a checker is wrong.

**It does not replace running things.** A pass counted from a read-only checker is a pass about reading. For checks the agent can run (tests, linters), see [Let the agent check its own work](5-4-self-checks.html). The same warning applies there: a test that "passed" means little unless you can see the command and its output. Anthropic's guide says it directly: "'All tests pass' on its own tells you very little" ([Best practices](https://code.claude.com/docs/en/best-practices)).

**Waivers can become a habit.** If a person waives every time the limit is hit, the limit is decoration. The record of waivers is how you notice.

## When to delete it {#when-to-delete-it}

A counter like this exists because the platform has no built-in notion of "this work was independently checked, n times, on this version". If a platform adds that, with a record the agent cannot change, use it and drop the counter. The idea does not retire: the person, not the agent, decides what counts as checked.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look at how this project shows that a check really happened: CI configuration, required reviews, status checks, review comments, and any file the agent writes to say it checked something. For each kind of record, tell me whether it is tied to the exact commit, who or what can edit or fake it (including the agent), and what happens to it if the code changes afterwards. Point out any place where the only evidence is someone's sentence. Do not change any files.
:::

## Go deeper {#go-deeper}

- Claude Code docs: [Best practices](https://code.claude.com/docs/en/best-practices) (ask for evidence, not a claim)

## Explore it in the harness {#explore}

The counting, the limit, the waiver and the catch-up at stop all run in Copilot Harness. The harness can teach them to you from the inside, with a real record of checks. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Make a pass count". Teach me how this harness counts independent checks (topic 11): how the passes in a row are worked out, what the limit is, what allowing more checks, waiving and setting a check aside do, and what happens when checks are on but nothing was checked. Open a real task's record of checks with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.