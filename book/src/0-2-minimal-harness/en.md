This chapter assumes you have used Copilot in agent mode on a project of your own, and that you have read [What is Harness Engineering?](0-1-the-gap-and-the-map.html) or at least know the word "harness".

## In one sentence {#in-one-sentence}

Write one page of rules, add one skill, then write one hook that blocks dangerous commands, and leave everything else until a real pain calls for it.

## For leaders {#for-leaders}

- **The decision:** build the smallest set first (one page of rules, one skill, one hook that blocks dangerous commands), and for each thing you add later, be able to name the real pain it solves.
- **The risk:** a big harness built in one go is expensive to maintain, and nobody can say which part helped. The small set is not foolproof either: rules and skills are only requests, so the model may not follow them, and although the model cannot get around a hook, a hook stops only the spellings of a command it recognizes.
- **The cost of doing it right:** if the project is already open in VS Code, about half an hour for one person. After that, the team reviews the rule and hook files the way it reviews code.
- **Ask the team:** "Which parts of our setup came from real failures, and which did we copy from a template?"

## Don't try to get it perfect at the start {#problem}

After reading about the seven layers in the last chapter, it's tempting to build everything at once: a task board, a knowledge base, human in the loop (review and approve), subagents, guardrails, permission management, a sandbox... You don't have to do all of that in one go. In my experience it's better to start with the smallest piece that works and iterate, and to think about adding something only when you run into a problem or a pain, and I've been caught by false needs too: some things I added early on turned out to be the wrong idea, so I deleted them later.

Anthropic's advice to teams building agents is the same: "we recommend finding the simplest solution possible, and only increasing complexity when needed", and "consider adding complexity only when it demonstrably improves outcomes". ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))

So follow along with this chapter, build a minimal demo first, and then you'll see what a harness really is. I want to teach you to write a one-page rules `.md` file, then add a skill, and finally write a hook, so you get a feel for these three layers. If your project is already open in VS Code, the whole thing takes about half an hour.

## Three steps to the smallest set {#how-it-works}

::: figure 0-2-grow-by-pain

### Why rules, then a skill, then a hook

Each of the three holds the agent harder than the one before and costs more to build, so start with the cheapest.

A rules file is usually `AGENTS.md` (Codex, Copilot), `CLAUDE.md` (Claude Code) or `.github/copilot-instructions.md` (Copilot). You can just create the first two at the root of your repository, and the third goes in the `.github/` folder. Rules take a few minutes and no code, and they tell the agent what it can't guess for itself: how the project is built, how to run the tests, what not to touch. At the start of every session, the agent looks for this file automatically and, if it finds one, loads it into context. A rule is only a request, and the model can ignore it. In my experience it follows what's written most of the time, but when the context gets long it sometimes ignores some of the rules, so a rules file can't give you a 100% guarantee.

A skill is a folder: `.github/skills/` for Copilot, `.claude/skills/` for Claude Code, `.agents/skills/` for Codex. Inside is a `SKILL.md` file with a name and a description at the top and, below them, the steps for one kind of job, such as cutting a release or adding a database table. Long procedures like these don't belong in the rules file, because that file is loaded in full every time, and the more steps you put there, the more tokens you pay every time ([Instructions and skills, load only what you need](3-3-instructions-and-skills.html)). With a skill, the agent normally sees only the name and the description, and it reads the full text when a request matches. A skill's weakness is one more layer of uncertainty than a rule has: it's only a request too, and on top of that the agent decides for itself whether to use it, so with a poor description it won't think of it.

A hook is a small program of your own that the platform calls at fixed moments. Before each tool runs, for example, the platform hands it the details of the call (which tool, with what arguments), and the program decides whether to let the call through or refuse it. Rules and skills are written for the model, which may not follow them. A hook is different, because the decision is made by a program outside the model: when it says no, the model cannot get around it, so the few things that must never happen belong there. It comes last because it's code you have to write, test and maintain, and because it sees only this one call, not what the command does once it runs ([Hooks, the point every call passes through](2-2-hooks.html)). That means it stops only the spellings it recognizes, and the same command written another way may slip through.

### Step 1: write one page of rules (about 10 minutes)

Create an `AGENTS.md` at the root of your project. If you're not sure which file to use, use this one, because Copilot and Codex both read it, and Claude Code reads it when there's no `CLAUDE.md`. Write in it only what the model would get wrong or miss, meaning your project's own commands, limits and traps, and leave out what it already knows, such as how to write a loop in your language. Shorter is better. Five to ten lines is plenty for a first version, and the Claude Code docs suggest keeping each file under 200 lines, because a longer file takes up more context and the model follows it less well ([How Claude remembers your project](https://code.claude.com/docs/en/memory)).

One line is worth adding early: the command to run after a change (the tests, the linter), with "do not say done until it passes". It's the cheapest check there is ([Let the agent check its own work](5-4-self-checks.html)).

The real file in my setup is longer, and its two core limits look like this:

::: code harness AGENTS.md L44-L45 "Two core limits from the shipped rules file: look before you act, and keep the user's own changes."

Once it's written, check that it works. Open a new chat and ask something only your rules can answer, such as "How do I run the tests in this project?" If the answer follows your rules, the file is loaded, and if the agent is guessing, check the file name and location. In VS Code you can also expand References under the response, or run **Chat: Open Customizations** from the Command Palette and look for the file in the list.

### Step 2: add a skill (about 10 minutes)

Pick a job you've explained to the agent more than once, create a folder for it under `.github/skills/`, and put a `SKILL.md` in it with a name and a description at the top. The name can use only lowercase letters, numbers and hyphens and must match the folder name, and the description can be up to 1024 characters.

The description matters most, because it's what the agent normally sees, so whether the agent thinks of this skill at the right moment depends on how well you wrote it. VS Code's advice is to be specific about both what the skill does and when to use it, and I also include the words a user might say.

::: code harness .github/skills/generic-code-standards/SKILL.md L1-L6 "The top of a real skill: the name and the description are what the agent sees first."

Below the top, write the steps, then a short list of traps, the places where the agent usually goes wrong. From then on, add one every time you see it fail, which is the most useful habit I know for writing skills ([Turn your way of working into skills](3-4-skills-and-workflows.html)).

Check this one too. Type `/` in the chat box and the skill should appear in the list, then make a request that fits the description without naming the skill, and see whether the agent uses it. If it never picks the skill, the problem is usually the description.

### Step 3: write a hook that blocks dangerous commands (about 10 minutes)

The terminal is the most powerful tool an agent has, so the first hook starts there, blocking commands whose damage can't be undone, such as recursively deleting a folder, or downloading a script and running it in one line.

A hook has two parts: a configuration file that tells the platform which program to call on which event, and the program, which makes the decision. VS Code reads the configuration from `.github/hooks/*.json` in the repository, and in my setup every event points at the same program:

::: code harness .github/hooks/harness.json L40-L51 "The configuration for the moment before a tool runs: it just names the program to call."

Before each tool runs, the platform hands the call to the program, and if the command matches a pattern you block, the program returns a refusal (it sets `permissionDecision` to `deny`) along with a reason. The reason should say what to do instead, because the agent sees it, and without that the agent will try the same thing again ([Asking is not a limit](4-2-ask-vs-refuse.html)). Here is one of my patterns. It's this long because the same command can be spelled many ways, but you don't need a file this big on day one, and three or four patterns are enough to start.

::: code harness .harness/policies/gate.json L59-L62 "One real refusal rule: recursive force-delete of the root, home or current folder, with a reason the agent can read."

Don't test a hook with a command that's really dangerous. Add a harmless rule first, for example one that refuses the command `echo hook-test`, and ask the agent to run it. You should see a refusal with the reason you wrote, and then you remove the rule.

Hooks have three traps, and I've fallen into all of them:

- If the hook program can't start (the interpreter isn't found, for example), the call counts as refused, which is also what GitHub's docs say: when a preToolUse command errors, the tool call is denied. The agent then can't use any tool at all, while the screen shows only that the hook errored, so test it once before you rely on it.
- If the hook times out (30 seconds in my setup), the platform treats it as having no opinion and handles the call under the normal permission rules. If that command is normally auto-approved, it just runs, as if there were no hook, so keep the program fast.
- In my setup, the hook configuration is read when the window starts, so after changing it, reload the VS Code window.

### How much harness do you need?

Whether these three parts are enough depends on who is affected when the agent gets it wrong.

| You are | Probably enough | Why |
| --- | --- | --- |
| One person on your own project | The three parts above | You see every change, and mistakes cost only you |
| A small team on a shared repository | The three parts, with the rules and hook files reviewed like code, plus a place to record what the agent did | Others inherit the agent's mistakes, and "who changed the rules" becomes a question ([Roll out and govern a harness](7-4-rollout-and-governance.html)) |
| A large team, or code with compliance duties | The above, plus [approval points](5-3-two-approvals.html), [counted checks](5-5-counted-checks.html) and reports, as your risks require | A mistake costs others, and you must be able to show what happened |

Most readers are in the first row, and things like two approvals and a task board can wait.

### What to add next, by pain

Once all three are in place, you don't need to read this book front to back. When something hurts, go and read the chapter that matches.

| The pain | Read |
| --- | --- |
| The agent ignores a rule, again and again | [4.1](4-1-requests-and-rules.html) |
| A command asked for approval a hundred times, and you click Allow without reading | [4.2](4-2-ask-vs-refuse.html) |
| It says "done" and the tests fail | [5.4](5-4-self-checks.html) |
| Long chats get worse and it forgets things | [3.2](3-2-long-sessions.html) |
| The bill is higher than you expected | [1.1](1-1-models-and-cost.html) |
| You want to split work across agents | [2.3](2-3-subagents.html) |
| You cannot tell what it did | [6.1](6-1-observe.html) |

### How do you know it got better?

Each time you add something, you'll want to know whether it helped, but a feeling isn't reliable. What works is to pick a few tasks you know the right answer to, run them before and after each change, and score them the same way (the method is in [Part 6](6-3-eval-tasks.html)). Even a rough version beats guessing: five tasks, plus a list of what "right" means written before you run them, with each task run a few times, because the result of one run may be luck ([One run proves nothing](6-4-variance.html)).

## Rules files keep growing, and hooks make people too comfortable {#costs-and-traps}

The rules file goes wrong first. A line gets added after every incident, so after a while the file is long, some entries contradict each other, and the model stops following it, so cut it back regularly and keep each rule in one place.

The hook's problem is quieter: it makes people too comfortable. Because it stops only the spellings it recognizes, don't say "the agent can't delete things". Say "the agent can't run these specific commands".

## When to delete each part {#when-to-delete-it}
{status: industry}

Every part of this starter set is something platforms are slowly building in. When the platform's own permission system refuses the same dangerous commands out of the box, delete your hook. When it learns your project's commands by itself, shorten your rules file. And re-read your rules after every major model upgrade ([When the model is upgraded, delete](6-5-model-upgrades.html)), because lines written for an older model may have become dead weight.

## Try it on your own setup {#try-it}

::: prompt
Check this repository against a minimal setup of three parts: one short page of rules, one skill, one blocking hook. For each part, say whether it exists, where, and whether it works. For the rules, list lines that are long, stale or contradict each other, and say which commands and limits the model could not guess are missing. For the hook, list which irreversible commands (such as recursive delete) nothing stops. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- VS Code docs: [Create and manage agent customizations](https://code.visualstudio.com/docs/copilot/customization/overview)
- VS Code docs: [Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Claude Code docs: [How Claude remembers your project](https://code.claude.com/docs/en/memory)

## Explore it in the harness {#explore}

My own setup is the grown-up version of this chapter, with one page of rules, many skills and a hook that guards every tool call. The harness can show you each one from the inside, and help you set up your own.

::: prompt
/harness-rookie-wondering I have read the chapter "A minimal harness in 30 minutes". Teach me how this harness does its rules page, its skills and its hook. Open the real files with me, show me how the hook refuses a command, and help me see what I could copy into my own project.
:::
