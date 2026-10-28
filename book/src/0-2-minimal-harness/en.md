This chapter assumes you have used Copilot in agent mode on a project of your own, and that you read [the first chapter](0-1-the-gap-and-the-map.html) or know the word "harness".

## In one sentence {#in-one-sentence}

Start with one page of rules, one skill and one hook that blocks dangerous commands. Add anything more only when a real pain asks for it.

## For leaders {#for-leaders}

- **The decision:** start with the smallest set (one page of rules, one skill, one blocking hook), and let a real pain, not a plan, approve each part you add later.
- **The risk:** a big harness built in one go costs maintenance, and you cannot tell which part helped. Even in the small set, a rule is only a request. A hook is a rule the model cannot argue with, but it stops only the commands it recognizes.
- **The cost of doing it right:** by my estimate about half an hour for one person who already has a project open. A team also reviews the rule and hook files, the way it reviews code.
- **Ask the team:** "Which part of our setup came from a real failure, and which came from a template?"

## Why not build it all at once? {#problem}

When people hear "harness", many of them picture a big system, with [two approval gates](5-3-two-approvals.html), a [task board](7-2-many-tasks.html), a knowledge base and reports. Faced with that picture, they either give up or build all of it in one go. Both are mistakes.

The trouble with building it all at once is that a big harness has a price. Every part is something you have to write, keep true and debug when it misfires. And since you added the parts all together, you cannot tell which of them helped. I know this from my own harness, which did not start big. It grew one pain at a time, and I have since removed parts that bought nothing ([chapter 7.3](7-3-what-we-cut.html)).

So it is worth starting from the other end, with the smallest set that is worth having, built in the order I would build it. If you already have a project open in VS Code, I estimate that takes about half an hour.

## The smallest set, in the order I would build it {#how-it-works}

::: figure 0-2-grow-by-pain

### Why rules, then a skill, then a hook

The three parts differ in how hard they hold the agent, each one harder than the one before. That raises a fair question. If the hook holds hardest, why build it last?

Rules come first. They cost only a few minutes and no code, yet they tell the agent what it cannot guess, such as how your project is built and what not to touch. A rule is a request, so the model may ignore it, but in my experience it does what is written most of the time.

The rules page has a limit, though, because some knowledge is too long for it. If every procedure sat there, the agent would carry all of it in every conversation ([chapter 3.3](3-3-instructions-and-skills.html) explains why that is expensive). That is what a **skill** is for: a short manual for one kind of job. At first the agent sees only its name and a one-line description, and only when a request matches does it read the full text.

Rules and skills are still both requests, which the model can ignore. A **hook** is the first part that is a rule you can rely on. It is a small program the platform runs at fixed moments, for example just before the agent runs a tool, and when it says no, the model cannot argue with it. It still comes last, because it is code you must write and maintain, and that effort should be spent on the few things that must never happen.

### Step 1: one page of rules (about 10 minutes)

Start by creating one instruction file at the root of your project. VS Code and Copilot read files such as `AGENTS.md` or `.github/copilot-instructions.md` and give them to the agent in every conversation (check the current VS Code docs for the exact names it accepts).

Write in it only what the model would get wrong or miss, which means your project's own commands, limits and traps. Leave out what it already knows, such as how to write a loop in your language. Shorter is better, because a long rules file is easy for the model to ignore. Short as the page should be, one line earns its place early: the command to run after a change (the tests, the linter), with "do not say done until it passes". It is the cheapest check there is ([chapter 5.4](5-4-self-checks.html)).

A good first page has five to ten lines. The real file in my setup is longer, but its core limits look like this:

::: code harness AGENTS.md L44-L45 "Two core limits from the shipped rules page: look before you act, and keep the user's own changes."

To check that the file works, open a new chat and ask a question that only your rules can answer, such as "How do I run the tests in this project?" If the answer comes from your rules, the file is loaded. If the agent guesses, check the file name and location.

### Step 2: one skill (about 10 minutes)

For the skill, pick a job you have explained to the agent more than once. A skill is a folder with a `SKILL.md` file in it, and the top of that file holds a name and a **description**. The description matters most, because it decides whether the agent finds the skill at all. A good one says what the skill does, when to use it, and which words a user might say.

::: code harness .github/skills/generic-code-standards/SKILL.md L1-L6 "The top of a real skill: the name and the description are what the agent sees first."

Below the top, write the steps, followed by a short list of traps, the places where the agent usually goes wrong. Adding a trap each time you see it fail is the most useful habit I know for skills ([chapter 3.4](3-4-skills-and-workflows.html)).

To check that the skill works, type `/` in the chat and look for its name. Then make a request that matches the description without naming the skill, and see whether the agent uses it. When the agent never picks a skill, the problem is usually the description.

### Step 3: one hook that blocks dangerous commands (about 10 minutes)

The terminal is the most powerful tool an agent has, so that is where the hook starts. Pick commands whose damage you cannot undo, such as recursively deleting a folder, or downloading a script and running it in one line.

The setup has two parts: a configuration file that tells the platform at which moments to call your program, and the program itself. In my setup there is one configuration file, and every moment points at the same program:

::: code harness .github/hooks/harness.json L40-L51 "The configuration for the moment before a tool runs: it just names the program to call."

The program is handed the tool call the agent is about to make, that is, which tool and with what input. If the command matches a pattern you blocked, it answers with a refusal and a reason. The reason matters because the agent sees it, so write what to do instead, or the agent will try the same thing again ([chapter 4.2](4-2-ask-vs-refuse.html)). Here is one of my patterns, which is long because the same command can be spelled many ways:

::: code harness .harness/policies/gate.json L59-L62 "One real refusal rule: recursive force-delete of the root, home or current folder, with a reason the agent can read."

This is a real file, far bigger than you need on day one. Start with three or four patterns.

Checking that the hook works takes a little care, because you should not test it with a command that is actually dangerous. Add a harmless test rule first, for example one that refuses the command `echo hook-test`, and ask the agent to run it. You should see a refusal with your reason. Then remove the test rule.

There are three traps I know from my own hooks:

- If the hook program cannot start (for example, the interpreter is not found), the platform counts it as a refusal, and the agent cannot use any tool at all. Yet the screen says only that the hook errored, so test it once before you rely on it.
- If the hook runs past its time limit (30 seconds in my setup), the platform lets the call through with no notice. In other words, the hook fails open: when it is too slow, the command runs as if no hook existed. Keep the program fast.
- The configuration is read when the window starts, so after you change it, reload the VS Code window.

What a hook cannot do matters just as much. It sees a call, not what the command does once it runs ([chapter 2.2](2-2-hooks.html)). So a pattern list stops the common spellings of a dangerous command, but not every spelling. It is a seat belt, not a sandbox.

### How much harness do you need?

Whether these three parts are enough depends on who is affected when the agent gets it wrong.

| You are | Probably enough | Why |
| --- | --- | --- |
| One person on your own project | The three parts above | You see every change, and mistakes cost you only |
| A small team on a shared repository | The three parts, with the rules and hook files reviewed like code, plus a place to record what the agent did | Others inherit the agent's mistakes, and "who changed the rules" becomes a question ([chapter 7.4](7-4-rollout-and-governance.html)) |
| A large team, or code with compliance duties | The above, plus [approval points](5-3-two-approvals.html), [counted checks](5-5-counted-checks.html) and reports, as your risks require | A mistake costs others, and you must show what happened |

I guess most readers are in the first row. The two approval gates and the task board from the picture at the start are not a starting point.

### What to add next, by pain

Once the three parts are in place, do not read the rest of the book front to back. Wait until something hurts, then go to the chapter that matches.

| The pain | Read |
| --- | --- |
| The agent ignores a rule, again and again | [4.1](4-1-requests-and-rules.html) |
| A command asked for approval a hundred times, and you click Allow without reading | [4.2](4-2-ask-vs-refuse.html) |
| It says "done" and the tests fail | [5.4](5-4-self-checks.html) |
| Long chats get worse and it forgets | [3.2](3-2-long-sessions.html) |
| The bill is higher than you expected | [1.1](1-1-models-and-cost.html) |
| You want to split work across agents | [2.3](2-3-subagents.html) |
| You cannot tell what it did | [6.1](6-1-observe.html) |

### How do you know it got better?

Each time you add a part, you will want to know whether it helped, and a feeling is a poor guide. Instead, choose a few tasks you know the right answer to, run them before and after each change, and score them the same way. [Chapter 2.3](2-3-subagents.html) shows one such comparison, and [Part 6](6-3-eval-tasks.html) covers the method. Even a rough version, five tasks and a list of what "right" means, beats a guess. Write that list before you run, though, and run each task a few times, because one run can be luck ([chapter 6.4](6-4-variance.html)).

## How the starter set goes wrong {#costs-and-traps}

Even this small set has its own ways of going wrong. The rules page goes wrong first, by growing and going stale. People add a line after every incident, so after a while the page is long, parts of it contradict each other, and the model ignores it. Cut it back from time to time, and keep each rule in one place.

The hook goes wrong more quietly, by giving false comfort. It stops only what it recognizes, so do not describe it as "the agent cannot delete things". Describe it as "the agent cannot run these specific commands".

A caveat to end on: I have not tested every VS Code setting. File names, hook support and settings change between versions, so although the steps above work in my setup, check the current docs for yours.

## When to delete each part {#when-to-delete-it}
{status: industry}

Besides watching these parts, you should know when to take them away, because every part of this starter set is the kind of thing platforms are starting to build in. When the platform's own permission system refuses the same dangerous commands out of the box, drop your hook. When it learns your project's commands by itself, shorten your rules page. And re-read your rules after every major model upgrade ([chapter 6.5](6-5-model-upgrades.html)), because lines written for an older model may be dead weight.

## Try it on your own setup {#try-it}

::: prompt
Check this repository against a minimal setup of three parts: one short page of rules, one skill, one blocking hook. For each part, say whether it exists, where, and whether it works. For the rules, list lines that are long, stale or contradict each other, and say which commands and limits the model could not guess are missing. For the hook, list which irreversible commands (such as recursive delete) nothing stops. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Create and manage agent customizations](https://code.visualstudio.com/docs/copilot/customization/overview)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

My own setup is the grown-up version of this chapter, with a rules page, many skills and a hook that guards every tool call. The harness can show you each one from the inside, and help you set up your own.

::: prompt
/harness-rookie-wondering I have read the chapter "A minimal harness in 30 minutes". Teach me how this harness does its rules page, its skills and its hook. Open the real files with me, show me how the hook refuses a command, and help me see what I could copy into my own project.
:::
