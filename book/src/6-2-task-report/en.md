This chapter assumes you have used an AI coding agent. It helps to have read [Record what happened, not what the agent said](6-1-observe.html), but you can follow without it.

## In one sentence {#in-one-sentence}

Every finished task needs a report that a person can read in five minutes. When you run many tasks at once, a board is the one page that tells you which one to open.

## For leaders {#for-leaders}

- **The decision:** require that every finished task has a one-page report, written by code, and decide what the page must show.
- **The risk:** a log is not a report. Nobody reads thousands of lines, so the only thing a colleague or a leader reads is the agent's own summary, which is what the log exists to check. A report is also only as honest as its sources: a hole in the log is a hole in the report.
- **The cost of doing it right:** one program that reads the task folder and the log. The real cost is defending the five-minute limit against requests for one more number.
- **Ask the team:** "Show me the report of the last finished task. Can I read it in five minutes, and does it say who approved it and what was refused?"

## The problem {#problem}

A log is not a report. After [the previous chapter](6-1-observe.html) you may have a log with thousands of lines. Nobody reads that to answer "what did this task do?". And the agent's own summary, which is short enough to read, is the thing the log exists to check.

Who needs the answer? Three people, at three times.

- **You, the next morning.** The work was yesterday. You do not remember which files changed, or why a check was done twice.
- **A colleague or a leader** who did not watch. They want to know what was done and whether anyone checked it, and they will give it a few minutes.
- **You, when something goes wrong later.** Someone asks "who approved this change?" and "was it checked?". You want the answer from a document, not from memory.

If the report takes an hour to read, these people will not read it. So the report is a design problem: what to put on one page, and what to leave to the log.

## How it works {#how-it-works}

### One page per task, written by code

A **task** here is one piece of work with its own folder: the request, the plan, the checks and the changes ([Manage tasks, not chats](5-1-tasks.html)). When the task closes, a program reads the folder and the records, and writes one report. The agent does not write it.

That one choice carries most of the weight. A report written by the agent is a summary, and a summary is what you could not trust in the first place. A report put together by a program from the folder and the log has the same facts every time, in the same places, so a reader learns where to look.

::: figure 6-2-report-page

### What goes on the page

Start from the questions the three readers ask, and give each a place. In my setup the report holds:

1. **What was asked and what was done.** The requirement the person confirmed, and the plan.
2. **Who approved, and when.** The times of the two approvals ([Two gates](5-3-two-approvals.html)).
3. **What changed.** Which files, how many lines added and removed, and which knowledge-base files were read ([A knowledge base](8-1-why-a-knowledge-base.html)).
4. **The checks.** How many independent checks, and the verdict of each ([Make a pass count](5-5-counted-checks.html)).
5. **What was refused.** The calls the rules turned down, and why. This part surprises people, and it often explains why a task took longer than expected.

Here is the layout, as a template and not a real report:

- Asked: *the confirmed requirement, in one paragraph*
- Approved: *plan, at (time); write-back, at (time)*
- Changed: *(n) files, +(a) / -(b) lines; knowledge-base files read: (list)*
- Checks: *(n) independent checks; verdict of each*
- Refused: *each refused call and the rule that refused it*

What is left out is the log itself. The report points at the facts and does not repeat all of them. A good test is the five minutes: if a reader cannot finish the page in that time, something on it belongs in the log instead.

### Where the time and usage went

A second page next to the report answers a different question: not "what happened?" but "where did the time and the usage go?". It splits each prompt into the model thinking, tools running, subagents, and **waiting for the person**. Then it sums these by **stage** (requirement, plan, development, write-back, done; an independent check is a stage of its own).

The waiting time is the number I did not expect to matter. Suppose a task "took three days", and the page shows the agent worked for forty minutes and waited for a person the rest (the numbers are an example, not a result). Then the cost is waiting, not the agent. That is a different problem from a slow agent, and it has a different fix: fewer or cheaper gates, or someone to answer them ([Ten things at once](7-2-many-tasks.html)).

The numbers come from the hook log and the platform's own session record, not from the agent's word ([Record what happened, not what the agent said](6-1-observe.html) says where usage comes from and what happens when that record cannot be read). Opening the page costs no tokens. If you want the agent to explain it to you, you ask for that on purpose, and then it reads the page.

### The board: many tasks at a glance

When you have one task, you do not need a board. When you have ten, the question changes from "what did this task do?" to "which task needs me now?". A **board** is one page that lists every open task, what it is waiting for, and for how long. It is built from the same task folders and records as the report, so the two cannot disagree. [Ten things at once: parallel tasks](7-2-many-tasks.html) has the design.

### Try it by hand

You do not need a program to see whether the idea works. After your next agent task, write five lines from the diff and the tool-call history: what was asked, what changed, what was run, what was refused or failed, and who said yes. Then ask yourself whether you would read that page tomorrow, and whether a colleague could use it. If it takes you more than a few minutes to write, that tells you what the program has to collect.

### Where the person steps in

The report and the board are where a person meets the system. Three points matter.

- **The board is for steering.** You open a task from it, approve a plan, or pause a task. Approvals still go through a channel the agent cannot reach.
- **The report is for reading afterwards.** It is written when the task closes, so it shows the task as it ended.
- **A saved copy is for people with no access.** The task page can be saved as a single file that opens offline, for a leader who has no access to your board. It is a copy from the moment you saved it, with no buttons. Read it before you send it, and take out internal names and paths before it goes outside the group that owns the task.

What an agent writes is drawn as plain text on these pages, so a task file cannot make the page run anything ([Text the agent reads can give it orders](4-6-untrusted-input.html)).

## Costs and traps {#costs-and-traps}

**A report is only as honest as its sources.** It is built from the log and the folder. If the log has a hole ([Record what happened](6-1-observe.html)), the report has the same hole and does not say so.

**Five minutes is a limit you have to defend.** Everyone wants one more number on the page. Move it to the log or the analysis page; keep the report short.

**A report says what happened, not whether it was good.** It can show that the task went through the two approvals and that its checks passed. It cannot show that the work was better than last week's, because nothing scores quality across tasks; I have no such score. To get one you would run fixed tasks before and after a change ([the next chapters](6-3-eval-tasks.html)), which are not real work, or have a person read a sample of finished tasks.

**A report is a record, not a signature.** Whether it counts as evidence for approving a change, how long it is kept, and who may edit it are decisions for the team ([Roll out and govern a harness](7-4-rollout-and-governance.html)). The report itself is written once, by code, at close.

**Nobody reads a report that nobody asks for.** If no one ever opens the reports, ask why before you improve them.

## When to delete it {#when-to-delete-it}
{status: industry}

My report and board exist because the platform shows a chat, not a task. If the platform gives you tasks with their own history, approvals and usage per task, use that and drop the page you built. If it can show a leader a read-only view with the same facts, drop the saved copy too.

The reasoning stays. A person who did not watch needs to know what was done, who approved it, what was checked and what it cost, in a form that takes minutes. I would look again at the board if I found that I never run more than two tasks at once.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Take the last three merged changes in this repository. For each one, write a five-line report from git history and any linked review or task notes only: what was asked, what changed (files, lines), what was run or checked, what was refused or failed, and who said yes. Where a fact cannot be found in the repository, write "not recorded". Then tell me which of the five facts are missing most often. Do not change any files.
:::

## Go deeper {#go-deeper}

- In this book: [Record what happened, not what the agent said](6-1-observe.html), [Manage tasks, not chats](5-1-tasks.html), [Two gates](5-3-two-approvals.html)

## Explore it in the harness {#explore}

Copilot Harness writes a report and an analysis page for every task it closes, and has a board of all open tasks. The harness can show you the real pages. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "A report a person can read in five minutes". Teach me how this harness reports on a task (topic 12): what the task report holds, how the analysis page gets its time and usage, and what the board shows. Open a real report with me and point out where each part comes from.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.