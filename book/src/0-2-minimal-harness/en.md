This chapter assumes you have used Copilot in agent mode on a project of your own, and that you read [the first chapter](0-1-the-gap-and-the-map.html) or know the word "harness".

## In one sentence {#in-one-sentence}

Start with one page of rules, one skill and one hook that blocks dangerous commands. Add more only when a real pain asks for it.

## For leaders {#for-leaders}

- **The decision:** start with the smallest set (one page of rules, one skill, one blocking hook) and let each later part be approved by a real pain, not by a plan.
- **The risk:** a big harness built in one go costs maintenance and you cannot tell which part helped. A rule is only a request; a hook is a rule the model cannot argue with, but it stops only the commands it recognizes.
- **The cost of doing it right:** by my estimate about half an hour for one person who already has a project open. A team adds review of the rule and hook files, like code.
- **Ask the team:** "Which part of our setup came from a real failure, and which came from a template?"

## The problem {#problem}

When people hear "harness", many picture a big system: [two approval gates](5-3-two-approvals.html), a [task board](7-2-many-tasks.html), a knowledge base, reports. Then they either give up or build all of it in one go. Both are mistakes.

A big harness has a price. Every part is something to write, to keep true, and to debug when it misfires. And you cannot tell which part helped, because you added them all at once. Mine did not start big. It grew one pain at a time, and I have since removed parts that bought nothing ([chapter 7.3](7-3-what-we-cut.html)).

So this chapter is about the smallest set that is worth having, in the order I would build it. By my estimate it takes about half an hour if you already have a project open in VS Code.

## How it works {#how-it-works}

::: figure 0-2-grow-by-pain

### Why this order

The three parts differ in how hard they hold the agent.

1. **Rules come first.** They cost a few minutes and no code. They tell the agent what it cannot guess: how your project is built, what not to touch. A rule is a request, and the model may ignore it, but in my experience it does what is written most of the time.
2. **A skill comes second.** A **skill** is a short manual for one kind of job. The agent sees only its name and a one-line description at first, and reads the full text when a request matches. You need it because some knowledge is too long to put in the rules page: if every procedure sat there, the agent would carry all of it in every conversation ([chapter 3.3](3-3-instructions-and-skills.html) explains why that is expensive).
3. **A hook comes last.** A **hook** is a small program the platform runs at fixed moments, for example just before the agent runs a tool. It can say no, and the model cannot argue with it. Rules and skills are requests. The hook is the first part that is a rule you can rely on. It is third because it is code you must write and maintain, so it should be spent on the few things that must never happen.

### Step 1: one page of rules (about 10 minutes)

Create one instruction file at the root of your project. VS Code and Copilot read files such as `AGENTS.md` or `.github/copilot-instructions.md` and give them to the agent in every conversation. Check the current VS Code docs for the exact names it accepts.

Write only what the model would get wrong or miss: your project's own commands, limits and traps. Do not write what it already knows, such as how to write a loop in your language. Shorter is better, because a long rules file is easy for the model to ignore. One line is worth adding early: the command to run after a change (the tests, the linter) and "do not say done until it passes". It is the cheapest check there is ([chapter 5.4](5-4-self-checks.html)).

A good first page has five to ten lines. The real file in my setup is longer, but its core limits look like this:

::: code harness AGENTS.md L44-L45 "Two core limits from the shipped rules page: look before you act, and keep the user's own changes."

**How to check it works.** Open a new chat and ask a question that only your rules can answer, such as "How do I run the tests in this project?" If it answers from your rules, the file is loaded. If it guesses, check the file name and location.

### Step 2: one skill (about 10 minutes)

Pick a job you explained to the agent more than once. A skill is a folder with a `SKILL.md` file. The top of the file has a name and a **description**, and the description matters most. It decides whether the agent finds the skill at all. A good description says what the skill does, when to use it, and which words a user might say.

::: code harness .github/skills/generic-code-standards/SKILL.md L1-L6 "The top of a real skill: the name and the description are what the agent sees first."

Below that, write the steps, and then a short list of traps: the places where the agent usually goes wrong. Adding a trap each time you see it fail is the most useful habit I know for skills ([chapter 3.4](3-4-skills-and-workflows.html)).

**How to check it works.** Type `/` in the chat and look for the skill's name. Then say a request that matches the description without naming the skill, and see whether the agent uses it. A skill the agent never picks is usually a description problem.

### Step 3: one hook that blocks dangerous commands (about 10 minutes)

The terminal is the most powerful tool an agent has, so start there. Pick commands whose damage you cannot undo, such as recursively deleting a folder, or downloading a script and running it in one line.

The setup has two parts. A configuration file tells the platform which moments to call your program at. In my setup there is one file, and every moment points at the same program:

::: code harness .github/hooks/harness.json L40-L51 "The configuration for the moment before a tool runs: it just names the program to call."

Your program reads the call it is given. If the command matches a pattern you blocked, it answers with a refusal and a reason. The reason matters: the agent sees it, so write what to do instead, or the agent will try the same thing again ([chapter 4.2](4-2-ask-vs-refuse.html)). Here is one of my patterns. It is long because the same command can be spelled many ways:

::: code harness .harness/policies/gate.json L59-L62 "One real refusal rule: recursive force-delete of the root, home or current folder, with a reason the agent can read."

This is a real file, and it is far bigger than you need on day one. Start with three or four patterns.

**How to check it works.** Do not test it with a command that is actually dangerous. First add a harmless test rule, for example one that refuses the command `echo hook-test`, and ask the agent to run it. You should see a refusal with your reason. Then remove the test rule.

Three traps I know from my own hooks:

- **If the hook program cannot start** (for example, the interpreter is not found), the platform counts it as a refusal, and the agent cannot use any tool at all. The screen only says the hook errored. Test it once before you rely on it.
- **If the hook runs past its time limit**, the platform lets the call through, with no notice. In my setup the limit is 30 seconds. This fails open: a slow hook is a hole, so keep the program fast.
- **Configuration is read when the window starts.** After you change it, reload the VS Code window.

What a hook cannot do is just as important. It sees a call, not what the command does once it runs ([chapter 2.2](2-2-hooks.html)). A pattern list stops the common spellings of a dangerous command, not every spelling. It is a seat belt, not a sandbox.

### How much harness do you need?

It depends on who is affected when the agent gets it wrong.

| You are | Probably enough | Why |
| --- | --- | --- |
| One person on your own project | The three parts above | You see every change, and mistakes cost you only |
| A small team on a shared repository | The three parts, with the rules and hook files reviewed like code, plus a place to record what the agent did | Others inherit the agent's mistakes, and "who changed the rules" becomes a question ([chapter 7.4](7-4-rollout-and-governance.html)) |
| A large team, or code with compliance duties | The above, plus [approval points](5-3-two-approvals.html), [counted checks](5-5-counted-checks.html) and reports, as your risks require | A mistake costs others, and you must show what happened |

I guess most readers are in the first row. Two approval gates and a task board are not a starting point.

### What to add next, by pain

Do not read the rest of the book front to back. Wait until something hurts, then go to the chapter that matches.

| The pain | Read |
| --- | --- |
| The agent ignores a rule, again and again | [4.1](4-1-requests-and-rules.html) |
| A command asked for approval a hundred times, and you click Allow without reading | [4.2](4-2-ask-vs-refuse.html) |
| It says "done" and the tests fail | [5.4](5-4-self-checks.html) |
| Long chats get worse and it forgets | [3.2](3-2-long-sessions.html) |
| The bill is higher than you expected | [1.1](1-1-models-and-cost.html) |
| You want to split work across agents | [2.3](2-3-subagents.html) |
| You cannot tell what it did | [6.1](6-1-observe.html) |

### Did it get better?

Do not trust a feeling. Choose a few tasks you know the right answer to, run them before and after each change, and score them the same way. [Chapter 2.3](2-3-subagents.html) shows one such comparison, and [Part 6](6-3-eval-tasks.html) covers the method. Even a rough version, five tasks and a list of what "right" means, beats a guess. Write the list of what "right" means before you run, and run each task a few times, because one run can be luck ([chapter 6.4](6-4-variance.html)).

## Costs and traps {#costs-and-traps}

**The first page of rules grows and goes stale.** People add a line for every incident. After a while it is long, parts contradict each other, and the model ignores it. Cut it back from time to time and keep each rule in one place.

**A hook gives false comfort.** It stops what it recognizes. Do not describe it as "the agent cannot delete things". Describe it as "the agent cannot run these specific commands".

**I have not tested every VS Code setting.** File names, hook support and settings change between versions. The steps above work in my setup; check the current docs for yours.

## When to delete it {#when-to-delete-it}
{status: industry}

Every part of this starter set is on the list of things platforms are absorbing. When the platform's own permission system refuses the same dangerous commands out of the box, drop your hook. When it learns your project's commands by itself, shorten your rules page. Re-read your rules after every major model upgrade ([chapter 6.5](6-5-model-upgrades.html)); lines written for an older model may be dead weight.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Check this repository against a minimal setup of three parts: one short page of rules, one skill, one blocking hook. For each part, say whether it exists, where, and whether it works. For the rules, list lines that are long, stale or contradict each other, and say which commands and limits the model could not guess are missing. For the hook, list which irreversible commands (such as recursive delete) nothing stops. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Create and manage agent customizations](https://code.visualstudio.com/docs/copilot/customization/overview)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

My own setup is the grown-up version of this chapter: a rules page, many skills, and a hook that guards every tool call. The harness can show you each one from the inside, and help you set up your own. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "A minimal harness in 30 minutes". Teach me how this harness does its rules page, its skills and its hook. Open the real files with me, show me how the hook refuses a command, and help me see what I could copy into my own project.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
