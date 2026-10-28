This chapter assumes you have read [Hooks](2-2-hooks.html): a hook is code that tool calls pass through, and it can refuse the call.

## In one sentence {#in-one-sentence}

A rule in a prompt is only a request; a rule in code is a rule. Start with words, and move a rule into code when it keeps being broken or the harm cannot be undone.

This chapter is about how firmly a rule is held (safety). It is not about which is the cheapest thing that can make a call; that is [Who decides](5-9-who-decides.html).

## For leaders {#for-leaders}

- **The decision:** decide which rules may stay as written words and which must be enforced by code. A rule moves to code when it keeps being broken, when the harm cannot be undone, or when other steps rely on it.
- **The risk:** a rule written in a prompt is only a request. In my own setup, a hook that put my rules at the start of each prompt ran every time, yet many prompts still arrived without them. That was one setup and one batch in October 2026, not a general rate, and I have no numbers on how often written rules are broken.
- **The cost of doing it right:** code has a price: it must be written, tested and kept up when the platform changes. Most rules do not need it, so this is a few rules, not all of them.
- **Ask the team:** "Which of our rules would do damage we cannot undo if the agent broke it once, and is each of those held by code or only written in a prompt?"

## The problem {#problem}

You write a rule in the instruction file: "never touch the generated files". The agent follows it for a week. Then it does not. You read the rule again. It is still there, and it is clear. Nothing in the file changed. What changed is that the agent had other things to think about.

A **prompt** is the text the model reads: your request, the instruction files, the skills it loaded. A rule written there is a sentence like any other. The model weighs it against the other sentences, and sometimes the others win. The longer the chat, the more other sentences there are ([Long chats get worse](3-2-long-sessions.html)).

Even getting the sentence in front of the model is not certain. In [Hooks](2-2-hooks.html) I counted a batch of prompts in my own setup in October 2026: a hook that put my rules at the start of each prompt ran every time, yet many prompts still arrived without them. It is one setup and one batch, not a general rate. If delivering a rule can fail, obeying it can fail more.

So there are two kinds of rule, and they are easy to mix up:

- **A request.** You ask the model to behave. It usually does. No one can promise it always will.
- **A rule.** Code stands in the way. As long as the code runs and sees the call, it is refused whatever the model thinks.

Anything that must hold has to be the second kind. But code is not free, and most rules do not need it. The question of this chapter is: which rule goes where?

## How it works {#how-it-works}

### Four levels of firmness

A rule can be held at four levels. Each one promises something different, and each one has a limit.

::: figure 4-1-ladder

| Level | What it is | What it promises | Its limit |
| --- | --- | --- | --- |
| **Words** | The rule is written in an instruction file, a skill, or the body of an agent | The agent knows the rule and why it exists | It may not comply |
| **A command that checks itself** | The agent does the operation through a small program of yours, which checks the conditions before it acts | The same result every time, on any platform | It guards only what goes through it. If the agent edits the file by hand, the command is never called |
| **A hook that refuses** | Code the platform runs before tool calls, which can say no | The call is stopped, in the modes I tried, even when no one is watching | It depends on the platform, and it sees the call, not the effect ([Hooks](2-2-hooks.html)) |
| **Found afterwards** | A health check (a command that tests whether the setup is sound), a test run, a read of the logs | A breach can be found and counted | It cannot prevent anything. It is detection, not prevention |

The last level is different in kind. It does not hold the rule; it tells you whether the others held. You need it at every level, because a rule you cannot see being broken is a rule you are guessing about.

The middle two need a word of explanation. A **command** here is a program you give the agent next to its built-in tools. Instead of "create the folder, copy the files, write the state", the agent runs one command that does all three and refuses to start if a precondition is false. The rule is inside the command. A **hook** is the other way round: the agent does what it likes, and the hook looks at each call before it runs.

### Where does a rule go

Start every rule at the bottom, in words. A sentence is cheap to write and cheap to change, and for most rules the model will follow it. Move it up when one of three things is true.

1. **It keeps being broken.** You have seen it happen more than once, and a better sentence did not fix it. Rewording is the wrong answer to a rule that is ignored for being far away; code is the right one.
2. **The harm cannot be undone.** A deleted branch, a pushed commit, an overwritten file nobody backed up. One breach is one too many, so do not wait for the second.
3. **Other parts rely on it.** If a later step trusts that an earlier rule held (a "check passed" record, an approval), then a broken rule breaks the later step too.

Then pick the lowest level that is enough. If a command can hold the rule, do not build a hook. A hook has to be written, tested, and kept alive across platform changes ([Enforcement design](4-4-enforcement-design.html)). Use the hook when the agent can get to the thing in many ways and you cannot route them all through your command.

### Stop with code, teach with text

When you move a rule into code, do not delete the sentence. Keep one. They do different jobs.

- **The code stops.** It does not depend on what the model remembers.
- **The text teaches.** It tells the agent why the rule exists and what to do instead, before it runs into the wall.

Without the text, the agent runs into the refusal again and again, and tries other ways round it. Without the code, the text is a request again. The refusal message is the bridge: it is code that carries a sentence. A good one says why it was refused and what to do next ([Asking is not a limit](4-2-ask-vs-refuse.html) is about writing these).

The other side of the same split: do not put into code what only a judgment can decide. "Is this the right requirement?" and "is this change good?" have no pattern to match. Those stay as words, and you check them from outside, with an independent reviewer ([Use subagents sparingly](2-3-subagents.html)).

### An example of moving up

Say your rule is: "generated files are never edited by hand". The steps look like this.

1. **Words.** One line in the instructions, with the reason: they are rebuilt, and hand edits are lost.
2. **It happens twice.** You add a check at the level of the hook: a call to the edit tool on those paths is refused, with the reason and the command that regenerates them.
3. **A new gap.** The agent now uses the terminal to write the file. You add the common spellings of that to the hook. You also know it will not catch a script written first and run later, so you keep the one sentence of words, and a test that finds changed generated files after the fact.

This is a made-up case to show the steps. At each step a level was added and none was removed.

### Test your own setup

**A three-minute exercise.** Write down three rules you give your agent today. For each, answer: is it words, a command, a hook, or a check afterwards? Would one breach be undoable? Has it been broken twice? Any rule that is "no" to the first question, "cannot undo" to the second, and "yes" to the third is the one to move up first.

## Costs and traps {#costs-and-traps}

**Code has a price.** It has to be written, tested, and updated when the platform changes tool names or events. The more rules you move into code, the more of that you carry.

**Code stops the wrong things too.** A pattern that is too wide blocks real work. The agent cannot argue with a refusal, so a false refusal is a stuck task. Every code rule needs a reason in the message, and a way to see which rule fired.

**A hook only sees calls.** A rule in a hook holds for the spellings it knows. It does not hold against an agent set on getting around it. For things that must never be touched, see [Least privilege](4-5-least-privilege.html).

**Code can fail too.** A hook is software. If it breaks, the platform may refuse every call, or let every call through, depending on how it broke ([Enforcement design](4-4-enforcement-design.html)).

**A rule that only the agent keeps is not a record.** Do not let the agent be the only witness that it followed a rule. For anything you will rely on later, have code write the record ([Counted checks](5-5-counted-checks.html)).

**I did not count how often each level fails.** The ladder comes from experience with one harness and from the docs. I do not have numbers for how often words alone are broken, and I would not trust anyone who gave you one without saying what model and what task.

## What the industry says {#industry}
{status: industry}

The platform docs agree on the split, though they put it in their own words. The VS Code hooks page says hooks and instructions are not substitutes for enforced permissions, sandboxing or enterprise controls ([hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)). Read that both ways: instructions are the weakest level, and a hook is not the strongest level either. The next chapters go up that ladder.

## When to delete it {#when-to-delete-it}
{status: industry}

Two things shrink the ladder over time.

- **The model gets better at following words.** Some rules you moved to code because the model ignored them may now be followed. The way to find out is to run the same tasks with the code rule switched off and count ([When the model is upgraded](6-5-model-upgrades.html)). Choose tasks that used to trip the rule, run each a few times, and count the breaches. A handful of runs shows only a large change. I have not run this. Switch it off only where a breach can be undone.
- **The platform takes over.** When the platform itself can refuse a path or a command in every mode, your own hook for it can go. Keep the sentence of text.

What does not go away is the question: which rule is held how firmly, and why.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Read every rule this project gives the agent: instruction files, skills, agent files, hook and permission settings. For each rule, say which level holds it: words only, a command that checks itself, a hook or permission setting that refuses, or a check run afterwards. Then list the rules that are words only but would cause harm that cannot be undone, or that other steps rely on. Output a table with the rule, its level, and your recommendation to keep or move up. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- In this book: [Hooks](2-2-hooks.html), [Instructions and skills](3-3-instructions-and-skills.html), [Asking is not a limit](4-2-ask-vs-refuse.html)

## Explore it in the harness {#explore}

The four levels all exist in Copilot Harness: rules in text, commands that check their own conditions, a hook that refuses, and checks that look back. The harness can show you which rule sits at which level, and why, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "A rule in a prompt is a request". Teach me how this harness decides where each rule lives: the ladder of enforcement (topic 14) and the design choices behind it (topic 15). Pick three rules, show me which level each one is at and what would make you move it, and open the real files with me.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.