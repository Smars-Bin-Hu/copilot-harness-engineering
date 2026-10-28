This chapter assumes you have read [Hooks](2-2-hooks.html), so you know that a hook is code that tool calls pass through and that it can refuse the call.

## In one sentence {#in-one-sentence}

A rule in a prompt is only a request; a rule in code is a rule. Start with words, then move a rule into code when it keeps being broken or the harm cannot be undone.

The concern here is how firmly a rule is held, a matter of safety. A different question is who, or what, can make a judgment most cheaply, which is the subject of [Who decides](5-9-who-decides.html).

## For leaders {#for-leaders}

- **The decision:** which rules may stay as written words, and which must be enforced by code. A rule moves to code when it keeps being broken, when breaking it would do harm that cannot be undone, or when other steps rely on it.
- **The risk:** a rule written in a prompt is only a request, which may not even reach the model. In October 2026 I counted a batch of prompts in my own setup. A hook that put my rules at the start of each prompt ran every time, yet many prompts still arrived without them. That is one setup and one batch, not a general rate. I also have no numbers on how often written rules are broken.
- **The cost of doing it right:** code has a price, because it must be written, tested and kept up as the platform changes. Most rules do not need it, so you pay that price for a few rules, not for all of them.
- **Ask the team:** "Which of our rules would do damage we cannot undo if the agent broke it once, and is each of those held by code, or only written in a prompt?"

## Why does a clear rule still get broken? {#problem}

You write a rule in the instruction file that says "never touch the generated files". For a week the agent follows it, but then one day it does not. When you go back to the rule, it is still there and still clear. Nothing in the file has changed. What changed is that the agent had other things to think about.

To see how that can happen, look at the rule the way the model sees it. Everything the model reads, from your request to the instruction files and the skills it has loaded, is called the **prompt**. Inside the prompt your rule is just one sentence among many, which the model weighs against all the others. Sometimes the others win. And the longer the chat, the more of them there are ([Long chats get worse](3-2-long-sessions.html)).

All of this assumes the rule reaches the model at all, which is not certain either. In [Hooks](2-2-hooks.html) I counted a batch of prompts from my own setup in October 2026. A hook put my rules at the start of each prompt and ran every time, yet many prompts still arrived without them. That is only one setup and one batch, not a general rate, but if even delivering a rule can fail, obeying it can fail more.

So what we call a rule is really two different things that are easy to mix up. The first is a **request**: you ask the model to behave, and it usually does, though no one can promise it always will. The second is a **rule** in the strict sense, where code stands in the way. As long as that code runs and sees the call, the call is refused, whatever the model thinks.

Anything that must hold has to be the second kind. But code is not free, and most rules do not need it. So which rule goes where?

## Which rule goes where? {#how-it-works}

### Four levels of firmness

The short answer is that each rule goes on the lowest level that is enough for it. Of the four levels at which a rule can be held, three hold it more firmly the higher you go, which is why they form a ladder. Each level promises something different and has its own limit.

::: figure 4-1-ladder

| Level | What it is | What it promises | Its limit |
| --- | --- | --- | --- |
| **Words** | The rule is written in an instruction file, a skill, or the body of an agent | The agent knows the rule and why it exists | It may not comply |
| **A command that checks itself** | The agent does the operation through a small program of yours, which checks the conditions before it acts | The same result every time, on any platform | It guards only what goes through it. If the agent edits the file by hand, the command is never called |
| **A hook that refuses** | Code the platform runs before tool calls, which can say no | The call is stopped, in the modes I tried, even when no one is watching | It depends on the platform, and it sees the call, not the effect ([Hooks](2-2-hooks.html)) |
| **Found afterwards** | A health check (a command that tests whether the setup is sound), a test run, a read of the logs | A breach can be found and counted | It cannot prevent anything. It is detection, not prevention |

The last level is different in kind, because it does not hold the rule at all but only tells you whether the others held. You need it whatever level a rule sits at, since a rule you cannot see being broken is a rule you are only guessing about.

The two levels in the middle work in opposite ways. A **command** here is a program you give the agent alongside its built-in tools. Instead of creating the folder, copying the files and writing the state one at a time, the agent runs a single command that does all three. If a precondition is false, the command refuses to start. The rule lives inside the command. A **hook** works the other way round: the agent does what it likes, while the hook looks at each call before it runs.

### When to move a rule up, and how far

Every new rule starts at the bottom, in words, because a sentence is cheap to write and cheap to change, and for most rules the model will follow it. Move a rule up when one of three things is true.

1. It keeps being broken. You have seen it happen more than once, and a better sentence did not fix it. When a rule is ignored because it sits far back in a long chat, rewording will not help, but code will.
2. The harm cannot be undone, as with a deleted branch, a pushed commit or an overwritten file nobody backed up. Then one breach is already one too many, so do not wait for the second.
3. Other parts rely on it. If a later step trusts that the rule held (a "check passed" record, an approval), a broken rule breaks that later step too.

Once a rule has to move, pick the lowest level that is enough. If a command can hold the rule, do not build a hook. Besides being written and tested, a hook has to be kept alive as the platform changes ([Enforcement design](4-4-enforcement-design.html)). Save the hook for when the agent can get to the thing in many ways and you cannot route them all through your command.

### Stop with code, teach with text

When a rule moves into code, you might think its sentence has done its job and can go. Keep one, because the two do different jobs. The code does the stopping, without depending on what the model remembers. The text does the teaching, telling the agent why the rule exists and what to do instead before it runs into the wall. Without the text, the agent runs into the refusal again and again and tries other ways round it. Without the code, the text is a request again.

The bridge between the two is the refusal message, which is code that carries a sentence. A good one says why the call was refused and what to do next ([Asking is not a limit](4-2-ask-vs-refuse.html) is about writing these).

It also works the other way. Questions that only a judgment can decide, such as "is this the right requirement?" or "is this change good?", have no pattern to match, so they do not belong in code. They stay as words, checked from outside by an independent reviewer ([Use subagents sparingly](2-3-subagents.html)).

### How one rule climbs the ladder

To see what moving a rule up looks like, take a made-up rule of the same kind as the one this chapter opened with. Say the rule is "generated files are never edited by hand". At first it is only words, one line in the instructions that also gives the reason: the files are rebuilt, so hand edits are lost.

Then the rule is broken twice, so you move it up by adding a check at the hook level. Now a call to the edit tool on those paths is refused, with the reason and the command that regenerates the files. That holds for a while, until the agent finds a new gap and writes the file through the terminal instead. So you also add the common spellings of that to the hook, meaning the different ways a terminal command can write the same file. You know the hook will still not catch a script written first and run later. That is why you keep the one sentence of words and add a test that finds changed generated files after the fact.

Notice that on the way up, the rule only gained levels, without losing any of the earlier ones.

### A three-minute exercise

Before going on, try this with your own rules. Write down three rules you give your agent today, then ask three questions of each. Is it words, a command, a hook or a check afterwards? Could one breach be undone? Has it been broken twice? The rule to move up first is one held only by words, whose breach could not be undone and which has already been broken twice.

## What code costs, and what can still go wrong {#costs-and-traps}

Whichever rule you move, the code that holds it has a price. Like any software, it has to be written, tested and updated whenever the platform changes its tool names or events, so the more rules you move into code, the more of that you carry. It can also break. Depending on how a hook breaks, the platform may refuse every call or let every call through ([Enforcement design](4-4-enforcement-design.html)).

Even when it works, a code rule can go wrong in two opposite ways. If its pattern is too wide, it blocks real work, and because the agent cannot argue with a refusal, a false refusal leaves the task stuck. So every code rule needs a reason in its message and a way to see which rule fired. The opposite mistake is letting things through. A hook only sees calls, so it stops the spellings it knows and misses the rest. It will not hold against an agent set on getting around it, so for things that must never be touched, see [Least privilege](4-5-least-privilege.html).

There is also a trap that has nothing to do with refusing. If only the agent knows whether it kept a rule, you have no record, so do not let the agent be the only witness. For anything you will rely on later, have code write the record ([Counted checks](5-5-counted-checks.html)).

One last limit is the ladder itself. It comes from experience with one harness and from the docs, not from counting how often each level fails. I have no numbers for how often words alone are broken, nor would I trust anyone who gave you one without saying what model and what task.

## Does the platform agree? {#industry}
{status: industry}

The platform docs agree on the split, though they put it in their own words. The VS Code hooks page says hooks and instructions are not substitutes for enforced permissions, sandboxing or enterprise controls ([hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)). That sentence is worth reading in both directions: instructions are the weakest level, but a hook is not the strongest level either. The ladder goes on above it, and the next chapters climb it.

## When to delete a code rule {#when-to-delete-it}
{status: industry}

Of the two things that shrink the ladder over time, the first is a model that gets better at following words. Some rules you moved to code because the model ignored them may now be followed. The way to find out, though I have not run this myself, is to run the same tasks with the rule switched off and count the breaches ([When the model is upgraded](6-5-model-upgrades.html)). Switch it off only where a breach can be undone. Choose tasks that used to trip the rule and run each a few times. Even then, a handful of runs will show only a large change.

The second is the platform taking over. When the platform itself can refuse a path or a command in every mode, your own hook for it can go, though the sentence of text stays.

What does not go away is the question of how firmly each rule is held and why.

## Try it on your own setup {#try-it}

::: prompt
Read every rule this project gives the agent: instruction files, skills, agent files, hook and permission settings. For each rule, say which level holds it: words only, a command that checks itself, a hook or permission setting that refuses, or a check run afterwards. Then list the rules that are words only but would cause harm that cannot be undone, or that other steps rely on. Output a table with the rule, its level, and your recommendation to keep or move up. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- In this book: [Hooks](2-2-hooks.html), [Instructions and skills](3-3-instructions-and-skills.html), [Asking is not a limit](4-2-ask-vs-refuse.html)

## Explore it in the harness {#explore}

Copilot Harness has all four levels, from rules written as text, through commands that check their own conditions and a hook that refuses, to checks that look back. The harness can open the real files with you and show which rule sits at which level and why.

::: prompt
/harness-rookie-wondering I have read the chapter "A rule in a prompt is a request". Teach me how this harness decides where each rule lives: the ladder of enforcement (topic 14) and the design choices behind it (topic 15). Pick three rules, show me which level each one is at and what would make you move it, and open the real files with me.
:::
