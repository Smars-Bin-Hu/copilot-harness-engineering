This chapter assumes you have read [Hooks](2-2-hooks.html), or know that a hook is code the platform runs before tool calls, and that it can refuse the call.

## In one sentence {#in-one-sentence}

The enforcement layer is software, and it will fail. Decide in advance whether a failure lets the call through or blocks it, and build the layer so it can be tested and moved to another platform.

## For leaders {#for-leaders}

- **The decision:** decide, and write down, whether the guard fails open (lets the call through) or fails closed (blocks it) when it breaks, and name the person who owns the layer.
- **The risk:** nobody decides this on purpose; it is decided by whatever the script does when it crashes. The platform has its own rules too: a crash can refuse the call, while a timeout is a silent pass for every event. A guard that fails open and says nothing leaves a hole nobody knows about.
- **The cost of doing it right:** for a small setup, one short script is enough. The structure in the chapter pays off when rules multiply, when several people edit them, or when a second platform arrives. Someone must own the layer and re-run fixed scenarios after each platform update.
- **Ask the team:** "If our guard crashes tomorrow, what happens to the next action, and who would see the error?"

## The problem {#problem}

The first hook is easy. It is one script with a few `if` lines: if the command contains `rm -rf`, refuse. It works, and you are pleased.

Then the rules grow. One rule guards a list of folders. One keeps a record of every call. One keeps count of something. One has to know which task the agent is working on. Each of them needs the same input, so each is added to the same script, and the script becomes a tangle. Three things go wrong.

- **You cannot change a number safely.** The limit on repeated refusals, the list of protected folders, the time limit: they sit in the middle of the code. To change one you read all of it.
- **You cannot test it.** The platform calls the script with a long piece of JSON. To check a rule you must run the agent and hope it does the thing you want to see.
- **You cannot move it.** The script reads the platform's field names. When the platform renames one, or you add a second platform, every rule changes.

There is a fourth problem, and it is the one this chapter is about. This script runs before tool calls, so a bug in it is a bug in everything the agent does. What should happen when the hook itself breaks? Block the call, or let it through? Nobody decides this on purpose. It gets decided by whatever the script happens to do when it crashes. [Hooks](2-2-hooks.html) showed that the platform itself decides two cases for you, and they point in opposite directions. Better to decide yours first.

## How it works {#how-it-works}

Four design choices make the layer something you can change, test and move. Then one decision, and one way to test it. If you read only one part, read the decision, "when the layer itself fails". The four design choices are more structure than a small setup needs (see the traps below); skim them unless you are building one.

### One call through the layer

Some words first. The **enforcement layer** is everything that stands between the model and the tools and says yes or no: the hooks and the code behind them. A **module** is one part of that code that is responsible for one thing, such as "protect these folders" or "record calls". An **adapter** is a small part that translates between two formats. The **core** is the part that runs the modules and combines what they say.

::: figure 4-4-one-call

### 1. One entry, and an adapter that is the only part that knows the platform

The platform is told about one hook, not ten. Every event goes to the same entry point. I did it this way for a practical reason: the platform does not filter by tool name for me, so ten small hooks would start ten processes for every call, most of them with nothing to do. I expect one entry that decides inside which modules care to be cheaper; I did not time it.

The first thing the entry does is hand the platform's JSON to the adapter. The adapter reads the platform's field names and spellings (tool names, upper and lower case, where the arguments are) and produces one **common event** that the rest of the code uses. On the way out, it does the reverse.

This is what makes the layer movable. When the platform changes a field, or you add a second platform, you write or change one adapter. The modules and their tests stay as they are. When the platform changes, I record real input from it first, check that the adapter reads the recording, and only then touch anything else.

### 2. Modules give opinions; the core decides

Each module sees the common event and returns one of: no opinion, allow, ask, deny, or "add these words for the model to read". A module imports only the shared basics, never another module. So you can add a module, or switch one off, without reading the others.

The core merges the opinions with a fixed order: **deny beats ask, and ask beats allow.** If any module says deny, the answer is deny, whatever the others think. The words that modules want to add are joined in order. This is the same idea as a vote where any single member can veto, and it means a new module can only make the layer stricter, never quietly weaker.

A module that raises an error is treated as having no opinion. One broken module cannot take the others with it. Note what follows: if the broken module was a deny rule, its refusal is gone and the call passes. That is the fail-open choice below, applied module by module.

### 3. Numbers live in files, not in code

How many refusals in a row before the breaker trips ([Guard the files that hold the rules](4-3-guardrails.html)), which folders are guarded, how long a granted exception lasts: these are all **policy files**, plain data that code reads and never contains. The reasons for this are plain. A person who is not a programmer can read them and change one. A company can put its own values in a separate override next to the standard ones, so updating the standard never collides with local changes. And a rule's number is written in one place, so the docs cannot disagree with the code.

The texts people read follow the same idea: every refusal reason and message sits in a table, one table per language, with the same names. A test fails if one language lacks a name.

### 4. State lives in files, one writer per field

The layer runs as a fresh process for every event. It cannot keep anything in memory between two calls. So whatever must be remembered (which task is active, how many refusals so far, whether a human override is on) goes in a small file per session, read under a lock and written back. Each field has one module that is allowed to write it. A version number in the file lets old files be upgraded rather than break.

Files also make the layer easy to inspect. When something odd happens, you open the file and see what the layer believed.

### The decision: when the layer itself fails

::: figure 4-4-fail-choice

Now the question from the start. There are two ways to fail.

- **Fail open:** when the hook's own code breaks, let the call through and write the error to a log.
- **Fail closed:** when it breaks, block the call.

In my setup the hook fails open. The reason is a cost comparison, and I only claim it for this kind of project. The hook runs before tool calls. If a bug in it blocked every call, the agent would be useless until someone fixed the bug, and the person would be angry at the harness. If it lets one call through, the cost is one missed stop, and the error is in a log and shows up in a **health check** (a command that tests whether the setup is sound). In a project that is only code under version control, a missed stop can usually be found and undone. Blocked work cannot be made up as easily.

The platform adds its own rules, and they need care. VS Code's page points to GitHub's hook reference for the exit-code rules ([GitHub hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks), checked 2026-10-28). For a before-tool command hook: exit code 2 is a deny, and any other non-zero exit is also a deny ("hook errored"), so a crash or a failed start refuses the call. If the hook takes longer than its time limit, it is killed and the call goes on through the normal permission flow: a silent pass, for every event. On other events, a non-zero exit is only logged and the run continues. My own measurement agreed on the crash and the timeout. So "fail open" is not something you get by doing nothing. The hook has to catch its own errors and answer "no opinion" on purpose, so that an ordinary bug does not turn into the platform's refusal. A crash of the whole program is a different case, which the platform decides. And "too slow" is a failure too: I run the hook once on purpose in that health check, and warn when the slowest recent call comes near the time limit, so I find out before the platform quietly drops my rules.

A rough guide, from the cost comparison above:

| Your project | Lean towards |
| --- | --- |
| Code under version control, a missed stop can be found and undone | Fail open, with a visible log |
| Touches production data or credentials | Fail closed on a short list, or better, do not rely on a hook ([Least privilege](4-5-least-privilege.html)) |
| Many people write rules, or you add a second platform | Add the structure above, and the failure tests below |

**This choice is not for everything.** Fail open is right when a missed stop is cheap to find and fix. It is wrong where a missed stop cannot be undone: a command that touches production data, a file that holds credentials. For those, one design is to fail closed, rule by rule, on a short list: if the hook breaks and the call touches anything on that list, block. I have not built this. But the better answer is the next chapter's: do not rely on a hook for those things at all ([Least privilege](4-5-least-privilege.html)).

Whichever you pick, **write it down and make a failure visible.** A layer that fails open and says nothing is the worst of both: you have a hole and do not know.

### How to test it

The layer's input is data, so the test is easy: feed in an event and read the answer. Three kinds of test matter.

- **Rule tests.** For each rule, a few events that must be refused, a few that must pass. Use input recorded from the real platform, not input you made up. Made-up input has the spellings you expect, and the platform does not.
- **Failure tests.** Break a module on purpose and check that the others still answer. Feed in a broken settings file and check the result is the one you chose, fail open or closed. Platform docs tell you to do this: "Test the exit-code and timeout rules instead of assuming that every failure blocks work."
- **Delivery tests.** The layer can be right and the answer can still be lost on the way ([Hooks](2-2-hooks.html) has an example). Check what the model really received.

Add one more habit. Keep a small set of fixed scenarios ("this command must be refused", "this edit must pass") and run them after every platform update. An update changes your layer without your changing a line of it.

### Test your own setup

**Three questions:**

1. If your hook crashes tomorrow, what happens to the next tool call? Do you know, or are you guessing?
2. If the platform renames a field, how many files do you edit?
3. Can you change the number of a rule without reading the code that uses it?

**A test you can run today.** Add a deliberate bug to a copy of your hook (a line that raises an error). Run a harmless task. Watch what the platform does and what your log says. Then fix the bug.

## Costs and traps {#costs-and-traps}

**This is more structure than the first hook needs.** One script of twenty lines is fine for a dozen rules. The structure pays when rules multiply, when more than one person edits them, or when you plan a second platform. I grew into it; I did not start with it.

**An adapter hides the differences, not removes them.** Platforms differ in what a hook can see and when it runs. A common event is a lowest common denominator, and anything the adapter cannot fill in is missing from every module. I use one platform today, so I have not tested the idea on a second.

**Fail open is a bet, and it can be lost.** It was cheap in my project. Take care if you copy it: ask what the worst missed stop would be in yours. The person who owns the project should make this choice, not the script's author by accident.

**Platform updates change your layer.** Someone has to own the layer and run the fixed scenarios after each update. If no one does, the layer drifts without anyone noticing.

**Veto power makes a bad module costly.** A module that wrongly says deny blocks everything. The tests above, and refusal reasons that say what to do instead, are how I keep it in check.

**A record nobody reads is no use.** The error log of a layer that fails open is the only sign that it failed. Read it, or have a command that reports it.

## What the industry says {#industry}
{status: industry}

The VS Code docs agree on the cautions. They describe a command hook's error on a before-tool event as denying the call, say that a timeout falls through to normal permissions, and tell you to test both (the exact exit codes are in GitHub's reference, above). They also say that hooks and instructions are "not substitutes for enforced permissions, sandboxing, or enterprise controls". ([Agent hooks in VS Code](https://code.visualstudio.com/docs/copilot/customization/hooks)) I did not find a published recommendation on fail open versus fail closed for agent hooks, so that part of the chapter is my reasoning, not a standard.

## When to delete it {#when-to-delete-it}
{status: industry}

The adapter is there because platforms differ and change. If the platforms converge on one hook format, the adapter shrinks to nothing. The timing check goes when a timeout is reported and not silent. If the platform one day offers enforced policy of its own (a rule file it checks itself, with a defined failure mode), I would move the hard rules there and keep the hook for records and reminders. The question of what happens when the enforcement fails does not retire: it moves to that policy.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
If this project uses hooks or a similar enforcement layer, read it and answer: (1) what happens to the next tool call if a hook crashes or times out, for each hook; (2) where the numbers and patterns of the rules live, in data files or inside the code; (3) which tests or fixed scenarios exist, and whether they use input recorded from the real platform; (4) where errors are logged and whether anyone would see them. If there is no hook, say so and stop. Do not change any files, and do not run the hooks.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [Hooks](2-2-hooks.html): the moments, and the three ways a hook goes wrong
- [Least privilege](4-5-least-privilege.html): what to do for what must never be touched

## Explore it in the harness {#explore}

The harness has this layer: one hook entry, an adapter for Copilot, modules, a core that merges, policy files, session state files, and a health check that tries the hook. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Build the enforcement layer like software". Teach me how this harness is built inside: the one hook entry, the adapter, the modules and the merge (topic 14), and why the hook lets a call through when it fails itself (topic 15.5). Open the real files with me, and show me what is in the error log.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.