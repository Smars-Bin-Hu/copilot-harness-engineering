This chapter assumes you have read [Ask or refuse](4-2-ask-vs-refuse.html) and [Guardrails](4-3-guardrails.html): why "ask me first" is not a limit, and why the agent must not be able to edit the rules.

## In one sentence {#in-one-sentence}

Put a person at the points that cost money, grant power or cannot be undone. Make the approval come through a channel the agent cannot reach, and bind it to exactly the plan that was approved.

## For leaders {#for-leaders}

- **The decision:** decide where a person must approve: at points that cost money, grant power or cannot be undone, and nowhere else. The approval must come through a channel the agent cannot reach, and it must belong to exactly the plan or change the person read.
- **The risk:** a confirmation box can be switched off for the session without anyone noticing, and an approval the agent can give itself is not an approval. A tired person can still approve without reading; binding the approval to the content stops a swap, not a careless yes.
- **The cost of doing it right:** each gate costs a person one read and one command. Too many gates and people stop reading. In my setup, snapshots at the gates are kept for 14 days by default.
- **Ask the team:** "Which approvals in our flow could the agent give itself or switch off, and does an approval still count if the plan changes afterwards?"

## The problem {#problem}

You want a person to approve the important steps. The obvious tool is the confirmation box that the agent tool shows: "Allow this?" It does not work well, for two reasons.

First, people click Allow. By the hundredth box they are not reading it ([Ask or refuse](4-2-ask-vs-refuse.html)). Second, many tools let you tick "allow for this session", and then the box never appears again. The approval you relied on is gone, and nothing tells you.

A third problem is subtler. Suppose the approval is a command the person types. If the agent can run commands, it can type that command too. An approval that the agent can give is not an approval.

So the question is where to put the person, and how to make their yes something the agent cannot produce or reuse.

## How it works {#how-it-works}

### Where to put the person

A person's attention is the scarcest thing in the system. Spend it on three kinds of point, and nowhere else:

- **Points that cost money.** For example, starting an expensive run.
- **Points that grant power.** Letting the agent write to a shared repository.
- **Points that cannot be undone.** Something that cannot be taken back once done.

Everything inside a task folder is cheap to redo, so the agent works there freely ([Manage tasks, not chats](5-1-tasks.html)). A task that changes a real repository has two such points. I call each a **gate**: the task cannot pass until a person approves.

::: figure 5-3-two-gates

### Gate 1: approve the plan

The agent writes the requirement and a plan, then stops. The person reads the plan, and only then approves. Before this, the agent may draft and read; it may not start changing the work files.

The point of this gate is cost. A wrong plan is cheap to fix as a paragraph and expensive to fix as a finished change. In my setup the plan also stands on a confirmed requirement ([The agent writes the requirement](5-2-requirements.html)), so one approval can confirm both.

### Gate 2: approve the write-back

The agent has made the changes in the task folder, and checks have run. Now the result is about to go to the real repository. Copying it there is the **write-back**. The person reads the exact **diff**: the list of lines that would change. Then they approve.

At the write-back, the result goes to a new branch of the repository and is left uncommitted. It never touches the main branch directly. And before it is written, code checks that:

- the working tree is clean,
- the branch name is free,
- none of the files to change has moved on the main branch since it was copied.

If any repository fails a check, nothing is written. This is also where two people, or two tasks, changing the same file are found: by the program here, not later in a review.

### Why the approval is typed in a terminal

A confirmation box in the chat can be switched off by "allow for this session". A code that the person types in a terminal cannot. The approval command needs a real terminal, and when an agent runs it, it is refused. Three points make this hold:

1. **The terminal is not a wall.** A check that "this is a terminal" is not a security boundary; a determined program can imitate one.
2. **A hook is the second leg.** It is code that refuses the agent's attempt to run the approval command at all, and it sits outside the agent's reach, as [Guardrails](4-3-guardrails.html) explains. If that hook is gone, or the agent can edit it, the approval is only a polite request. The design stands on both legs, and neither is enough alone.
3. **The refusal must survive an error.** The enforcement layer lets a call through when it breaks itself ([Build the enforcement layer like software](4-4-enforcement-design.html)). So the refusal of the approval command belongs on the short list of rules that must block even when the hook errors; otherwise this leg breaks exactly when it is needed.

The content is read elsewhere. Plans and diffs are hard to read in a terminal, so the person reads them in an editor, and the terminal shows only the file path and the code to type. Reading and approving are separate acts on purpose.

### Tie the approval to what was read

Suppose the person approves a plan, and then the agent edits the plan. Is the approval still good? It should not be. So the code the person types is derived from the plan's content: a hash, a fingerprint that changes if one character changes. When the plan changes after approval, the approval no longer matches, and the gate closes again.

The same goes for the write-back: the approval belongs to the exact diff that was shown. This is what "bind it to exactly the plan that was approved" means. Without it, a person approves one thing and the agent delivers another.

### Snapshots at the gates

When the plan is approved, before each check, and before the dry run of a write-back, a copy of the work (a snapshot) is saved automatically. When something breaks, the state of that moment can be found again. In my setup they are kept for 14 days by default.

A failure in the middle of a write to several repositories is not rolled back by itself. The task goes to a "partly written" state, and a person runs a recovery. I chose not to guess at an automatic undo.

### Without any of this machinery

The habit works by hand too. Read the plan before you tell the agent to go. Read the diff before you commit. Do not tick "allow for this session" on a tool that writes. The machinery above only makes sure these happen when you are tired or not there.

### Several rounds

After a write-back, the same goal can come back: a reviewer finds a defect, or a change is asked for. A new round starts. The old work moves aside, a new plan is written, and both gates apply again. A different goal is a new task.

Testing in other environments is not another round. The agent cannot run anything there; the person does. That becomes its own task of kind *testing*, where the agent writes the instructions, waits for the person's results, and judges them. A failed test goes back to the development task as a new round.

## Costs and traps {#costs-and-traps}

- **It stops the agent, and so it slows the work.** Each gate costs a person a read and a command. That is the price. If you put gates everywhere, people stop reading, and you are back at the hundredth box.
- **It holds only while the refusing hook is there.** If the hook that refuses the approval command is removed, edited or fails, an agent that can run commands could approve for itself. Protect that hook as the rules in [Guardrails](4-3-guardrails.html) say, and test it. A test is cheap: ask the agent to run the approval and check that it is refused.
- **A person can approve without reading.** Binding the approval to the plan stops a swap. It does not stop a tired yes. Making the diff short and the gates few helps; nothing here removes the problem. One idea I have not tried is to record how long each approval took and how big the diff was: a very fast yes on a big diff is a signal worth looking at.
- **The terminal check is not a lock.** Treat it as a guard against accidents, not against an attack ([Least privilege](4-5-least-privilege.html)).
- **No automatic undo across repositories.** A partial failure needs a person.

## When to delete it {#when-to-delete-it}

The typed-approval mechanism exists because a platform's own confirmation can be switched off for a session, and cannot be tied to a plan's hash. If a platform offers an approval that the agent cannot dismiss, that records what was shown, and that stops being valid when the content changes, use that and drop mine.

The idea stays: a person at the three kinds of point, and an approval that belongs to exactly what they read.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Walk through how work moves from this agent's changes to the main branch or to production in this project: pull requests, required reviews, CI, deploy steps, and any approval prompts in the agent tools. For each point where money is spent, power is granted or something cannot be undone, say who approves, through what channel, and whether the agent could give or skip that approval. Also say whether the approval would still stand if the change were edited after it was given. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Guardrails](4-3-guardrails.html): why the hook and its files must be out of the agent's reach.
- [Ask or refuse](4-2-ask-vs-refuse.html): why a confirmation box is not a limit.
- [Counted checks](5-5-counted-checks.html): the checks that run before the second gate.
- VS Code docs: [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), which say hooks and instructions are not substitutes for enforced permissions.

## Explore it in the harness {#explore}

The two gates, the typed approval, the plan hash, and the snapshots run in Copilot Harness. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Two gates". Teach me how this harness builds the two approvals (topic 9, and topic 8 on permissions): why they are typed in a terminal, what the approval is bound to, and which hook refuses the agent. Walk me through a real task going through both gates, and draw it.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.