This chapter assumes you have used an AI coding agent. Reading [Record what happened, not what the agent said](6-1-observe.html) first helps, but you can follow without it.

## In one sentence {#in-one-sentence}

Every finished task needs a report that a person can read in five minutes. When you run many tasks at once, a board is the one page that tells you which one to open.

## For leaders {#for-leaders}

- **The decision:** require that every finished task has a one-page report written by code, and decide what that page must show.
- **The risk:** a log is not a report. Nobody reads thousands of lines, so the only thing a colleague or a leader ends up reading is the agent's own summary, the very thing the log is there to check. And a report is only as honest as its sources: a hole in the log is a hole in the report.
- **The cost of doing it right:** one program that reads the task folder and the log. The real cost is defending the five-minute limit against requests for one more number.
- **Ask the team:** "Show me the report of the last finished task. Can I read it in five minutes, and does it say who approved it and what was refused?"

## Who needs to know what a task did? {#problem}

After [the previous chapter](6-1-observe.html) you may have a log with thousands of lines. A log, though, is not a report. Nobody reads thousands of lines to answer "what did this task do?". The agent's own summary is short enough to read, but it is the very thing the log exists to check.

So who needs that answer, and how long will they look for it? Three people need it, at three different times. One of them is you, the next morning, when the work was yesterday and you no longer remember which files changed, or why a check was done twice. Another is a colleague or a leader who did not watch the task. They want to know what was done and whether anyone checked it, and they will give it a few minutes. The last is you again, later, when something goes wrong and someone asks "who approved this change?" and "was it checked?". By then you want the answer from a document, not from memory.

If the report takes an hour to read, none of these people will read it. That makes the report a design problem. What goes on one page, and what is left to the log?

## A page for each task, and a board for many {#how-it-works}

### One page per task, written by code

Before deciding what goes on the page, decide who writes it. The page covers one **task**. A task here is one piece of work with its own folder: the request, the plan, the checks and the changes ([Manage tasks, not chats](5-1-tasks.html)). When the task closes, a program reads that folder and the records and writes one report. The agent does not write it.

That one choice carries most of the weight. Why not simply let the agent write it? Because a report written by the agent would be a summary, and a summary is what you could not trust in the first place. A report that a program puts together from the folder and the log has the same facts every time, in the same places, so a reader learns where to look.

::: figure 6-2-report-page

### What goes on the page

To decide what the page holds, start from the questions the three readers ask and give each of them a place. In my setup the report holds five things:

1. What was asked and what was done: the requirement the person confirmed, and the plan.
2. Who approved, and when: the times of the two approvals ([Two gates](5-3-two-approvals.html)).
3. What changed: which files, how many lines were added and removed, and which knowledge-base files were read ([A knowledge base](8-1-why-a-knowledge-base.html)).
4. The checks: how many independent checks ran, and the verdict of each ([Make a pass count](5-5-counted-checks.html)).
5. What was refused: the calls the rules turned down, and why. This part surprises people, and it often explains why a task took longer than expected.

On the page itself, those five things look like this (a template, not a real report):

- Asked: *the confirmed requirement, in one paragraph*
- Approved: *plan, at (time); write-back, at (time)*
- Changed: *(n) files, +(a) / -(b) lines; knowledge-base files read: (list)*
- Checks: *(n) independent checks; verdict of each*
- Refused: *each refused call and the rule that refused it*

What the page leaves out is the log itself: the report points at the facts rather than repeating all of them. The five minutes are the test of where to draw that line. If a reader cannot finish the page in that time, something on it belongs in the log instead.

### Where the time and usage went

The report answers "what happened?". Where the time and the usage went is a different question. The analysis page, a second page next to the report, answers it. It splits each prompt into the model thinking, tools running, subagents and **waiting for the person**, and then sums these by **stage**. The stages are requirement, plan, development, write-back and done, and an independent check counts as a stage of its own.

Of these numbers, the waiting time is the one I did not expect to matter. Suppose a task "took three days", and the page shows that the agent worked for forty minutes and waited for a person the rest of the time (the numbers are an example, not a result). Then what the task cost was waiting, not the agent. That is a different problem from a slow agent, and it has a different fix: fewer or cheaper gates, or someone to answer them ([Ten things at once](7-2-many-tasks.html)).

Like the report, these numbers do not rest on the agent's word. They come from the hook log and the platform's own session record ([Record what happened, not what the agent said](6-1-observe.html) says where usage comes from and what happens when that record cannot be read). Opening the page costs no tokens, because the agent reads it only when you ask it, on purpose, to explain the page.

### The board: many tasks at a glance

With one task, you do not need a board. With ten, the question changes from "what did this task do?" to "which task needs me now?", and that is the question a **board** answers. It is one page that lists every open task, what it is waiting for, and for how long. Because it is built from the same task folders and records as the report, the two cannot disagree. [Ten things at once: parallel tasks](7-2-many-tasks.html) has the design.

### Try it by hand

Before any program exists, you can try the idea of the report by hand. After your next agent task, write five lines from the diff and the tool-call history: what was asked, what changed, what was run, what was refused or failed, and who said yes. Then ask yourself whether you would read that page tomorrow and whether a colleague could use it. If writing it takes you more than a few minutes, that tells you what the program will have to collect.

### Where the person steps in

Once the pages exist, the report and the board are where a person meets the system, and the two are used in different ways. The board is for steering. From it you open a task, approve a plan or pause a task. The approval itself, though, still travels through a channel the agent cannot reach. The report is for reading afterwards. It is written when the task closes, so it shows the task as it ended.

Some readers, a leader for example, have no access to your board. For them the task page can be saved as a single file that opens offline. It is a copy from the moment you saved it, with no buttons. Read it before you send it, and take out internal names and paths before it goes outside the group that owns the task.

These pages show what the agent wrote, but only as plain text, so a task file cannot make the page run anything ([Text the agent reads can give it orders](4-6-untrusted-input.html)).

## What a report cannot tell you, and what it costs to keep it short {#costs-and-traps}

A report is built from the log and the task folder, so it is only as honest as its sources. If the log has a hole ([Record what happened, not what the agent said](6-1-observe.html)), the report has the same hole and does not say so.

Sources aside, **a report says what happened, not whether it was good.** It can show that the task went through the two approvals and that its checks passed. It cannot show that the work was better than last week's, because nothing scores quality across tasks (I have no such score). One way to get a score is to run fixed tasks before and after a change ([the next chapters](6-3-eval-tasks.html)), although those are not real work. The other is to have a person read a sample of finished tasks.

Nor is a report a signature. It is a record, and whether it counts as evidence for approving a change, how long it is kept and who may edit it are decisions for the team ([Roll out and govern a harness](7-4-rollout-and-governance.html)). The report itself is written once, by code, at close.

Then there is the cost of keeping the report short. Five minutes is a limit you have to defend, because everyone wants one more number on the page. Each time, move that number to the log or the analysis page instead.

And a report nobody asks for is a report nobody reads. If no one ever opens the reports, ask why before you improve them.

## When to delete the pages, and what stays {#when-to-delete-it}
{status: industry}

My report and board exist because the platform shows a chat, not a task. If the platform gives you tasks with their own history, approvals and usage per task, use that and drop the page you built. If it can also show a leader a read-only view with the same facts, drop the saved copy too.

The reasoning stays, though. A person who did not watch still needs to know what was done, who approved it, what was checked and what it cost, in a form that takes minutes to read. As for the board, I would look at it again if I found that I never run more than two tasks at once.

## Try it on your own setup {#try-it}

::: prompt
Take the last three merged changes in this repository. For each one, write a five-line report from git history and any linked review or task notes only: what was asked, what changed (files, lines), what was run or checked, what was refused or failed, and who said yes. Where a fact cannot be found in the repository, write "not recorded". Then tell me which of the five facts are missing most often. Do not change any files.
:::

## Go deeper {#go-deeper}

- In this book: [Record what happened, not what the agent said](6-1-observe.html), [Manage tasks, not chats](5-1-tasks.html), [Two gates](5-3-two-approvals.html)

## Explore it in the harness {#explore}

Copilot Harness writes a report and an analysis page for every task it closes, and keeps a board of all open tasks. The harness can show you the real pages.

::: prompt
/harness-rookie-wondering I have read the chapter "A report a person can read in five minutes". Teach me how this harness reports on a task (topic 12): what the task report holds, how the analysis page gets its time and usage, and what the board shows. Open a real report with me and point out where each part comes from.
:::
