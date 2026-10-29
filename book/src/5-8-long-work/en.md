This chapter assumes you know the task folder from [Manage tasks, not chats](5-1-tasks.html), and that a chat gets shortened or ends ([Long chats get worse](3-2-long-sessions.html)).

## In one sentence {#in-one-sentence}

Long work survives across sessions only if its memory is in files: the requirement, the plan, the to-do list, the handover file. Split big work into tasks small enough to accept one by one.

## For leaders {#for-leaders}

- **The decision:** for work that spans days, decide that its memory lives in files, and that big work is split into tasks small enough to accept one by one.
- **The risk:** a new session knows nothing unless a file tells it. A big job handed over in one go gets started all at once and left half done, and a later session can see progress and call the job done too early. In my setup a person's "passed" on a step is only text, with nothing in code behind it. That is the weakest link.
- **The cost of doing it right:** the files cost effort, because every step writes a little and every new session reads a little. For a job that fits in one session, that is waste. I have not measured what a goal saves over starting a new chat.
- **Ask the team:** "For our longest-running job, which file tells a new session what step it is on, and who accepted the steps so far?"

## What tells a new session where the work stands? {#problem}

A job that takes three days will not fit in one chat. At some point the first session ends, or the tool shortens it to make room and the details go. Whichever session picks the work up next then knows nothing, unless something tells it.

So what can tell it? Not the agent's memory, because it has none between sessions. Not yours either, if that means explaining the background again every morning, slightly differently each time. The only thing that is the same every morning is a file.

There is also a second problem, one that comes from the size of the job. Handed a big job in one go, an agent tends to start everything at once, run out of room halfway, and leave things half done. Anthropic saw the same on a long coding project: "the agent tended to try to do too much at once" ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). The same article describes the opposite failure too, a later instance that would "declare the job done" too early. That failure is the subject of [Unattended: when it must stop](5-7-when-to-stop.html).

The files, then, have to do more than carry the memory from one session to the next. They also have to keep a big job in pieces small enough to finish and accept.

## Memory in files, work in small steps {#how-it-works}

### What a conversation loses

If a file is the only thing that stays the same, the first question is what it has to carry. A conversation holds four things that a later session needs: what was asked, what was decided and why, how far the work has got, and what comes next. When the conversation is shortened or ended, all four are at risk, and the agent does not know which ones it lost.

### What goes in the folder

Those four things belong where nothing can shorten them.

::: figure 5-8-shared-folder

- The requirement records what was asked, in a form a person confirmed ([The requirement on one page](5-2-requirements.html)).
- The plan covers how the work will be done, and what is out of scope.
- The to-do list breaks the work into steps, each small, each with a status and a way to tell it is done.
- The **handover file** is one short file saying which step the work is at and what comes next. It is the same file as in the chapter on tasks (Anthropic calls its version a progress file). It has to stay short, within one screen, or a new session spends its room reading it.

A fifth item helps too: a change log with one entry per finished step, saying what changed. When someone asks "why is it like this?", the answer is there.

### What a new session reads

A new session does not read the whole folder. It reads the short handover file first, then the to-do list, and only then whatever the current step needs. After that it checks what the files say against the disk: does the file really exist, did the step really happen? **When the record and the disk disagree, the disk wins.** ([Manage tasks, not chats](5-1-tasks.html) explains why.) A handover file that says "step 4 done" does not make step 4 done.

Anthropic's team did three things here that I do not do the same way. The agent committed to git after each step, so every step left a clean state to return to. Each new session ran a basic end-to-end test before starting new work, so the old state was checked and not only read about in a file. And the feature list was kept in JSON, because the model was less likely to change a JSON file by mistake than a Markdown one. I keep my files in Markdown and have not compared the two.

### Build the frame first, then step by step

That deals with memory. The other problem, starting everything at once, is settled before any work begins by starting with the frame, not the work. Only then do you go one step at a time:

1. Settle the central idea: the goal, what is in scope and what is not, and how the whole will be accepted.
2. Break it into small steps.
3. Have a person read both and confirm them.
4. Then do one step: do it, check it, and hand it to the person.
5. Count the step as done only when the person says it passed. Then write the log entry, update the handover file, and move to the next.

The person's "passed" is a gate ([Two gates](5-3-two-approvals.html)). How far that gate can be trusted comes up again under what the files cost.

### What is too big, and how to split it

Most jobs fit in one task. A job is too big for one task when one of these is true (these three are my rules of thumb, not tested):

- It cannot finish in one session, and nobody can say how far along it is.
- You cannot say how you would accept the whole of it at once.
- The plan keeps changing as you learn more.

Those are the jobs a **goal** is for. A goal keeps the big thing as one set of files, with a few **tasks** under it. A task is one delivery, as in [Manage tasks, not chats](5-1-tasks.html), with one folder, its own checks and its own acceptance. The goal holds the idea and the list, while each task does one piece.

::: figure 5-8-goal-tasks

A good task is small enough that you can say, in a sentence, how you will accept it. While you work on task 2, the goal does not need to know the details of task 3. That is the point: the plan can then change one task at a time without redoing what has already been accepted. Steps that were accepted are not rewritten: if one needs doing again, the redo is a new step.

### Common traps

Two of the traps are the failures this chapter started with. If the agent tries to finish the whole goal in one session, the fix is the list, where only one step is active at a time. If a new session sees progress and decides the job is finished, the fix is the same as for unattended work ([when to stop](5-7-when-to-stop.html)): done is a state that the files and the person confirm, not a thing the agent says.

The other two are about size. One is a handover file that grows past a screen: it stops being read, so the detail moves to the change log and the handover file stays short. The other is making a goal for a small job. Most jobs need one task, and a goal is for work that spans sessions and changes shape.

None of this comes free, and one link in it is weak.

## What the files cost, and where they are weak {#costs-and-traps}

The plainest cost is effort. Every step writes a little and every new session reads a little. For a job that fits in one session, the files are waste.

The person's "passed" is the weakest link in this chapter. [Two gates](5-3-two-approvals.html) binds an approval to the exact plan, and code checks it. The "passed" of a step here is not bound to anything. In my setup it is text, not code, and nothing in code stops an agent from writing "passed" for itself. What I rely on is the agent following the instruction and the person reading. That is a gap I know about.

Files can also lie. The agent writes them, so they can be wrong or stale. That is why the disk wins and why the person accepts the work step by step.

Then there is the risk of too many goals. To guard against it, only the person can start one in my setup. An agent may suggest a goal when a job looks long, but if it could begin one, every job would become a project.

What I have not measured is how much a goal saves over just starting a new chat and explaining. I think it saves the most when the job changes shape, but I have no numbers.

## When to delete the handover file, and what stays {#when-to-delete-it}

If the platform keeps a trustworthy memory of a long job across sessions, so that a new session can resume without reading files, the handover file can go. I would keep the requirement and the plan as files anyway, because a person can read them too, and that is how you accept the work.

## Go deeper {#go-deeper}

- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Explore it in the harness {#explore}

The task folder and the goal files run in Copilot Harness. The harness can teach them to you from the inside, with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Long work across sessions". Teach me how this harness keeps long work in files (topic 9): the task folder, the handover file a new session reads, and the goal that groups several tasks. Open real files with me and draw how the pieces fit together.
:::
