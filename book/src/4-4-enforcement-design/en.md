This chapter assumes you have read [Hooks](2-2-hooks.html), or know that a hook is code the platform runs before tool calls, and that it can refuse the call.

## In one sentence {#in-one-sentence}

The enforcement layer is software, and it will fail. Decide in advance whether a failure lets the call through or blocks it, and build the layer so it can be tested and moved to another platform.

## For leaders {#for-leaders}

- **The decision:** decide, and write down, whether the guard fails open (lets the call through) or fails closed (blocks it) when it breaks, and name the person who owns the layer.
- **The risk:** nobody decides this on purpose, so it ends up decided by whatever the script does when it crashes. The platform has its own rules on top of that: a crash can refuse the call, while a timeout is a silent pass for every event. A guard that fails open and says nothing leaves a hole nobody knows about.
- **The cost of doing it right:** for a small setup, one short script is enough. The structure in this chapter pays off when rules multiply, when several people edit them, or when a second platform arrives. Either way, someone must own the layer and re-run fixed scenarios after each platform update.
- **Ask the team:** "If our guard crashes tomorrow, what happens to the next action, and who would see the error?"

## What goes wrong as the hook grows? {#problem}

The first hook is easy to write. It is one script with a few `if` lines (if the command contains `rm -rf`, refuse), and it works, so you are pleased.

Then the rules grow. One guards a list of folders, another keeps a record of every call, a third keeps count of something, and a fourth has to know which task the agent is working on. They all need the same input, so each is added to the same script. Before long it is a tangle, and three things go wrong.

Changing a number is no longer safe. The limit on repeated refusals, the list of protected folders and the time limit all sit in the middle of the code, so to change one you have to read all of it. Testing gets hard too, because the platform calls the script with a long piece of JSON, and to check a rule you must run the agent and hope it does the thing you want to see. And the script cannot be moved, since it reads the platform's field names directly. When the platform renames one, or you add a second platform, every rule changes.

A fourth problem is the one this chapter is really about. The script runs before tool calls, so a bug in it is a bug in everything the agent does. What, then, should happen when the hook itself breaks: block the call, or let it through? Nobody decides this on purpose. It gets decided by whatever the script happens to do when it crashes, and [Hooks](2-2-hooks.html) showed that the platform itself already settles two cases for you, in opposite directions. Better to decide yours first.

## How to build the layer, and what to do when it breaks {#how-it-works}

The first three problems have the same kind of answer. Four design choices make the layer something you can change, test and move. The fourth problem needs something else: one decision, and a way to test that it holds. If you read only one part, read the one on the decision, "when the layer itself fails". The four design choices are more structure than a small setup needs (see the costs further down), so skim them unless you are building one.

### One call through the layer

To follow a call through, it helps to name the parts. The **enforcement layer** is everything that stands between the model and the tools and says yes or no: the hooks and the code behind them. Inside that code, a **module** is a part responsible for one thing, such as "protect these folders" or "record calls". An **adapter** is a small part that translates between two formats. The **core** is the part that runs the modules and combines what they say.

::: figure 4-4-one-call

### 1. One entry, and an adapter that is the only part that knows the platform

The platform is told about one hook, not ten, so every event goes to the same entry point. I did it this way for a practical reason. The platform does not filter by tool name for me, so ten small hooks would start ten processes for every call, most of them with nothing to do. I expect a single entry that figures out for itself which modules care to be cheaper, but I have not timed it.

The first thing the entry does is hand the platform's JSON to the adapter. The adapter reads the platform's field names and spellings (tool names, upper and lower case, where the arguments are) and produces one **common event** for the rest of the code to use. On the way out, it does the reverse.

This is what makes the layer movable. When the platform changes a field, or you add a second platform, you write or change one adapter, while the modules and their tests stay as they are. So when the platform does change, I start with the adapter: I record real input from the platform, check that the adapter reads the recording, and only then touch anything else.

### 2. Modules give opinions; the core decides

Each module looks at the common event and returns one of these: no opinion, allow, ask, deny, or "add these words for the model to read". A module imports only the shared basics and never another module, so you can add a module, or switch one off, without reading the others.

The core merges the opinions in a fixed order: **deny beats ask, and ask beats allow.** If any module says deny, the answer is deny, whatever the others think. The words that modules want to add are joined in order. It is the same idea as a vote where any single member can veto. What it buys you is that a new module can only make the layer stricter, never quietly weaker.

What if a module itself breaks? A module that raises an error is treated as having no opinion, so one broken module cannot take the others with it. Notice what follows, though: if the broken module was a deny rule, its refusal is gone and the call passes. That is the fail-open choice below, applied module by module.

### 3. Numbers live in files, not in code

How many refusals in a row before the breaker trips ([Guard the files that hold the rules](4-3-guardrails.html)), which folders are guarded, how long a granted exception lasts: all of these are **policy files**, plain data that the code reads but never contains. This pays off in three ways. Someone who is not a programmer can read these files and change a value. A company can put its own values in a separate override next to the standard ones, so updating the standard never collides with local changes. And since a rule's number is written in one place, the docs cannot disagree with the code.

The texts people read follow the same idea. Every refusal reason and message sits in a table, one table per language with the same names in each. A test fails if one language lacks a name.

### 4. State lives in files, one writer per field

Because the layer runs as a fresh process for every event, it cannot keep anything in memory between two calls. Whatever must be remembered (which task is active, how many refusals so far, whether a human override is on) goes in a small file per session instead, read under a lock and written back. Each field has one module that is allowed to write it. A version number in the file lets old files be upgraded rather than break.

Files also make the layer easy to inspect: when something odd happens, you open the file and see what the layer believed.

### The decision: when the layer itself fails

::: figure 4-4-fail-choice

Now back to the question from the start. When the hook's own code breaks, there are two ways for it to fail. It can **fail open**, letting the call through and writing the error to a log, or it can **fail closed** and block the call.

Blocking sounds like the safe default. Why, then, would anyone let a call through? In my setup the hook fails open, and the reason is a cost comparison that I only claim for this kind of project. Because the hook runs before tool calls, a bug that blocked every call would leave the agent useless, and the person angry at the harness, until someone fixed it. A bug that lets one call through costs one missed stop. The error is in a log and shows up in a **health check** (a command that tests whether the setup is sound). In a project that is only code under version control, a missed stop can usually be found and undone, while blocked work cannot be made up as easily.

As the opening said, the platform already makes part of this decision for you. VS Code's page points to GitHub's hook reference for the exit-code rules ([GitHub hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks), checked 2026-10-28). For a before-tool command hook, exit code 2 is a deny. Any other non-zero exit is also a deny ("hook errored"), so a crash or a failed start refuses the call. A timeout goes the other way. If the hook takes longer than its time limit, it is killed and the call goes on through the normal permission flow, a silent pass for every event. On other events, a non-zero exit is only logged and the run continues. My own measurement agreed on the crash and the timeout.

So "fail open" is not something you get by doing nothing. The hook has to catch its own errors and answer "no opinion" on purpose, or an ordinary bug turns into the platform's refusal. A crash of the whole program is a different case, which the platform decides.

Slowness needs its own check, because the platform lets a timeout through silently. In the health check I mentioned above, I run the hook once on purpose and warn when the slowest recent call comes near the time limit, so that I find out before the platform quietly drops my rules.

From the cost comparison above comes a rough guide:

| Your project | Lean towards |
| --- | --- |
| Code under version control, a missed stop can be found and undone | Fail open, with a visible log |
| Touches production data or credentials | Fail closed on a short list, or better, do not rely on a hook ([Least privilege](4-5-least-privilege.html)) |
| Many people write rules, or you add a second platform | Add the structure above, and the failure tests below |

Fail open is not the answer for everything. It is right when a missed stop is cheap to find and fix. Where a missed stop cannot be undone, as with a command that touches production data or a file that holds credentials, it is wrong. For those, one design I have not built is to fail closed rule by rule, on a short list: if the hook breaks and the call touches anything on that list, block it. The better answer, though, is the next chapter's: do not rely on a hook for those things at all ([Least privilege](4-5-least-privilege.html)).

Whichever you pick, **write it down and make a failure visible.** A layer that fails open and says nothing is the worst of both, because you have a hole and do not know it is there.

### How to test it

Because the layer's input is data, testing it is easy: feed in an event and read the answer. Three kinds of test matter.

- Rule tests give each rule a few events that must be refused and a few that must pass. Use input recorded from the real platform, not input you made up, because made-up input has the spellings you expect, not the ones the platform sends.
- Failure tests break a module on purpose and check that the others still answer, or feed in a broken settings file and check that the result is the one you chose, open or closed. The platform docs tell you to do this: "Test the exit-code and timeout rules instead of assuming that every failure blocks work."
- Delivery tests check what the model really received, since the layer can be right and its answer can still be lost on the way ([Hooks](2-2-hooks.html) has an example).

Add one more habit on top of these: keep a small set of fixed scenarios ("this command must be refused", "this edit must pass") and run them after every platform update, because an update changes your layer without your changing a line of it.

### Three questions and a small test

Before going on, ask three questions of your own setup.

1. If your hook crashes tomorrow, what happens to the next tool call? Do you know, or are you guessing?
2. If the platform renames a field, how many files do you edit?
3. Can you change the number of a rule without reading the code that uses it?

Then try a test you can run today: add a deliberate bug to a copy of your hook (a line that raises an error) and run a harmless task. Watch what the platform does and what your log says, then fix the bug.

## What the structure costs, and what can still go wrong {#costs-and-traps}

All of this is more structure than the first hook needs. One script of twenty lines is fine for a dozen rules. The structure pays when rules multiply, when more than one person edits them, or when you plan a second platform. I grew into it rather than starting with it.

The adapter has a limit of its own: it only hides the differences between platforms. It does not remove them. Platforms differ in what a hook can see and when it runs. A common event is a lowest common denominator: anything the adapter cannot fill in is missing from every module. I use one platform today, so I have not tested the idea on a second.

The core's veto cuts both ways. It keeps a new module from weakening the layer, but a module that wrongly says deny blocks everything. The tests above, and refusal reasons that say what to do instead, are how I keep it in check.

Fail open is a bet that can be lost. It was cheap in my project. If you copy it, first ask what the worst missed stop would be in yours. The person who owns the project should make this choice, not the script's author by accident.

When the bet is lost, you at least need to know it. A record nobody reads is no use: the error log of a layer that fails open is the only sign that it failed, so read it, or have a command that reports it.

Last, as the test section warned, platform updates change your layer too. Someone has to own the layer and run the fixed scenarios after each update. If no one does, the layer drifts without anyone noticing. How much of this do the platform docs back?

## What do the platform docs say? {#industry}
{status: industry}

The VS Code docs agree on the cautions. They describe a command hook's error on a before-tool event as denying the call, say that a timeout falls through to normal permissions, and tell you to test both (the exact exit codes are in GitHub's reference, above). They also say that hooks and instructions are "not substitutes for enforced permissions, sandboxing, or enterprise controls". ([Agent hooks in VS Code](https://code.visualstudio.com/docs/copilot/customization/hooks)) What I did not find is a published recommendation on fail open versus fail closed for agent hooks, so that part of the chapter is my reasoning, not a standard.

## When the adapter and the timing check can go {#when-to-delete-it}
{status: industry}

The adapter is there because platforms differ and change, so if the platforms converge on one hook format, the adapter shrinks to nothing. The timing check can go when a timeout is reported instead of silent. And if the platform one day offers enforced policy of its own (a rule file it checks itself, with a defined failure mode), I would move the hard rules there and keep the hook for records and reminders. Even then, the question of what happens when the enforcement fails does not retire. It moves to that policy.

## Try it on your own setup {#try-it}

::: prompt
If this project uses hooks or a similar enforcement layer, read it and answer: (1) what happens to the next tool call if a hook crashes or times out, for each hook; (2) where the numbers and patterns of the rules live, in data files or inside the code; (3) which tests or fixed scenarios exist, and whether they use input recorded from the real platform; (4) where errors are logged and whether anyone would see them. If there is no hook, say so and stop. Do not change any files, and do not run the hooks.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [Hooks](2-2-hooks.html): the moments, and the three ways a hook goes wrong
- [Least privilege](4-5-least-privilege.html): what to do for what must never be touched

## Explore it in the harness {#explore}

The harness has this whole layer, from one hook entry and an adapter for Copilot to modules, a core that merges, policy files, session state files, and a health check that tries the hook.

::: prompt
/harness-rookie-wondering I have read the chapter "Build the enforcement layer like software". Teach me how this harness is built inside: the one hook entry, the adapter, the modules and the merge (topic 14), and why the hook lets a call through when it fails itself (topic 15.5). Open the real files with me, and show me what is in the error log.
:::
