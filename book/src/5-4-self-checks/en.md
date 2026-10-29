This chapter assumes you have used an AI coding agent. It builds on [The agent loop](2-1-agent-loop.html): the agent asks the model, runs a tool, and feeds the result back.

## In one sentence {#in-one-sentence}

Give the agent a way to check its own work, such as running the tests, the linter or the program. A check it can run and read gives it feedback inside the loop, while a reviewer only finds problems afterwards.

## For leaders {#for-leaders}

- **The decision:** require every task to come with a check the agent can run and read itself, such as tests, a build or a linter, and decide which of those checks the agent may not edit.
- **The risk:** an agent stops when its work looks done, and in my own use models often lean towards reporting success, though I have not recorded how often. Anthropic describes a later agent that would "declare the job done" after seeing progress. An agent can also pass by weakening the test. I have not recorded such a case, so treat it as a risk to design for.
- **The cost of doing it right:** often one line in the instruction file, the command that runs the project's check. Slow suites need a fast subset that can run often. I have not measured how much a self-check improves results.
- **Ask the team:** "What can the agent run to know that its work is done, and can it change that check?"

## Why "looks done" is not done {#problem}

An agent stops when its work *looks* done. But looking done is only a feeling the model has about its own code, and nothing has been run to back it up. So the agent says "I have made the change", you read it, and you find the bug.

If the agent has nothing to run that tells it whether the work is done, then you are the test suite. Every mistake waits until you notice it. That is slow, and it needs you in front of the screen.

In my own use I have often seen models lean towards reporting success, although I have not recorded how often. Anthropic describes the same pull in long runs, where a later agent instance would "declare the job done" after seeing that progress had been made ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). You might think the fix is to have the agent read its work over. That does not work either, because an agent that reads its own work shares its own blind spots: the same reasoning that wrote the mistake is now reading it ([Use subagents sparingly](2-3-subagents.html)).

So the way out is not a smarter agent but a check that does not depend on the agent's feeling. What changes once the agent has one?

## A check inside the loop, and where it falls short {#how-it-works}

### One of the most useful things you can add

The clearest way to see it is to compare two runs of the same task. In the first, the agent changes the code and says "done". You run the tests and two fail, so you tell the agent. It fixes one, and you run them again.

In the second, the agent changes the code and runs the tests itself. When two fail, it reads the output and fixes both, then runs the tests again. This time they pass, and only then does it say "done", with the output attached.

The model is the same in both. What differs is that in the second run the result of the check came back **inside the loop**, before the agent finished. The loop in [The agent loop](2-1-agent-loop.html) already has a place for this, because a tool result goes back to the model and the model decides the next step. A test run is just a tool whose result says, plainly, pass or fail.

::: figure 5-4-check-loop

Anthropic's guide for Claude Code says the same thing in its own words. Give the agent something it can run that comes back pass or fail, and it can keep going on its own, so that you do not have to watch ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)). Of all the things you can add around an agent, I put this near the top. A reviewer is also valuable, but it can only work afterwards, on finished work, whereas a self-check changes what the agent does while it works.

### What can be run

So what can the agent run? Almost anything, as long as its result is something it can read:

- **Tests:** the project's own tests, or a new test written for this change.
- **A build or typecheck:** the exit code alone says whether it works.
- **A linter or formatter:** quick, and it catches a class of mistakes.
- **A script that compares output with a known-good file:** good for data work, where the right answer is a table.
- **Running the program:** for a pipeline, run it on a small input and look at the output.
- **A screenshot next to a mockup:** for user interfaces.

If a repository already has one of these, the most useful single line in the agent's instruction file is the command that runs it, since the agent cannot guess which command the project trusts.

Knowing what to run still leaves the question of how firmly you ask for it. The answer is a scale from soft to hard, the same ladder as in [A rule in a prompt is a request](4-1-requests-and-rules.html):

1. The softest is a line in the prompt, such as "run the tests after, and keep going until they pass". The agent then decides for itself when it is satisfied.
2. Firmer is a stop condition. A hook ([Hooks](2-2-hooks.html)) runs at the moment the agent tries to stop, and if the check fails, the hook sends the agent back to work. Because the platform enforces this, the agent cannot end its turn with a failing check. Claude Code's documentation describes this with a Stop hook ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)), although I have not tested the same in Copilot for this chapter.
3. Firmest is to have a program count the passes, so that the number is not something the agent reports ([Counted checks](5-5-counted-checks.html)).

### Make the result short and readable

Whatever the check is, the agent reads its output, and that output goes into its context ([Context is a budget](3-1-context-budget.html)). It can go wrong by saying too much or by saying too little. A test run that prints thousands of lines fills the context, and the one failure the agent needs gets lost among them. So print only the failures, each with its file and line, plus a count. The passing noise can stay hidden. At the other extreme, "Error" alone gives the agent nothing to act on. A good failure says what was expected, what happened, and where.

This is the same advice as for tool messages in [Tool calling](1-2-tool-calling.html): the agent is an unreliable user, and what it reads decides what it does next. A check whose output is cheap and clear is worth more than a thorough check that nobody can read.

The output has one more use, as evidence. "All tests pass" is only a claim, while the command that was run and its output are evidence, so ask for them. When you were not watching, they are the only evidence you have.

### What a self-check cannot catch

Even a short, clear check that passes says less than it seems to. It says "this does what the check tests", not "this is what you wanted", and between those two statements two gaps open up.

One gap is in the requirement. If the page the agent works from is not what the person meant ([The agent writes the requirement](5-2-requirements.html)), then perfect code that passes every test is perfect code for the wrong thing. No test the agent writes from a wrong requirement will find that. Only a person reading the requirement can.

The other gap is in the test, which may check too little and pass with the bug still in. A test the agent wrote in the same session was written with the same understanding as the code, so it shares the same blind spot. If the agent misread the rule, its code and its test will agree with each other, and both will be wrong.

There is also a limit that is neither a gap in the requirement nor in the test. Some mistakes only show when the program runs in the real setting, with real data, and the agent cannot run it there. Those need a person's check, or a test environment's.

In all of these, the check simply misses something. The next problem is different: it comes from the check itself.

### When the agent weakens the test instead

Giving the agent a check also opens a new way to fail. The agent wants the loop to end with a pass, and the easy way to get one is to change the check, not the code. It can loosen an assertion until it passes, delete or skip the test that fails, change the expected value to whatever the code now gives, or catch an error and swallow it.

None of this needs bad intent. The agent is only doing what the loop rewards: finishing with a pass. I have not recorded a case of this in my own runs, so I describe it as a risk to design for, not as something I measured.

The defences run from cheapest to hardest. The cheapest is to say it in words: "Fix the code, not the tests. If a test seems wrong, say so and stop." That helps, but it is a request ([A rule in a prompt is a request](4-1-requests-and-rules.html)).

When a request is not enough, keep the tests out of the agent's reach. If the tests are part of what must not be edited, a hook refuses the change. [Guardrails](4-3-guardrails.html) explains why files that check the agent should be outside what the agent can write. That does not fit work where adding new tests is part of the job, so there you protect the existing tests and let the agent add new ones.

The hardest defence is to stop trusting the report and count instead. Look at the diff of the tests (the list of changed lines), where a change to a test that was failing is a flag. Better still, let code, not the agent, count the passes, with a record that the check ran ([Counted checks](5-5-counted-checks.html)).

### How it divides work with an independent check

If a self-check misses so much, is an independent reviewer the better tool? The two are not rivals, because they catch different things.

| | Self-check | Independent reviewer |
| --- | --- | --- |
| When | While the agent works | After it finishes |
| Catches | Things a program can judge: it runs, it passes, it matches a file | Things a program cannot judge: does it match the request, is the logic sound |
| Misses | Wrong requirement, weak test | Blind spots the reviewer shares with the author |
| Cost | Cheap, runs again and again | One more agent, several times the usage ([Use subagents sparingly](2-3-subagents.html)) |

So self-checks come first. Put them inside the loop, as many and as cheap as you can make them. Then, where it is worth the cost, add an independent check on the result. A reviewer who sees a green test run can spend its attention on the question tests cannot answer: is this the right thing?

## What a self-check costs, and how it can mislead {#costs-and-traps}

A self-check is cheap, but it is not free, and used badly it can mislead you. The worst case is a check that can pass wrongly. It is worse than having none, because it gives false comfort. A test that never fails is the extreme case: it passes, and it tells you nothing.

Other costs come from how a check behaves inside the loop. Speed is one. If the full suite takes twenty minutes, the agent runs it rarely, and the loop slows down. So give it a fast subset to run often, and the full suite at the end. A flaky check does a different kind of harm, because it teaches the agent the wrong thing. A test that fails at random sends the agent hunting for a bug that is not there, or teaches it to rerun until green.

Two more limits came up earlier. One is output that fills the context, covered under short, readable results. The other is code the agent cannot run at all. Where the real data, the real environment or the permission is not available to it, a self-check can only cover part of the work, so say which part and leave the rest to a person.

### A cheap test of your own checks

How much does a self-check actually improve results? I have not measured that in my own setup. The direction is clear from the vendor's guidance and from the loop itself, but I do not know the size of the effect. What you can measure cheaply is how much your own checks cover.

Put a bug into working code on purpose, then run the checks the agent would run. If they stay green, the check does not cover that part of the code, whatever the agent reports. It is a cheap way to see how much a passing check is worth.

## What Anthropic's guide says {#industry}
{status: industry}

Anthropic's Claude Code guide puts "give it a check to run" next to telling the agent what it cannot see. Its examples are a test file, a build exit code, a linter, a script that compares output with a fixture, and a browser screenshot. It also says to ask for the evidence, not only for "all tests pass", and mentions a command that builds and runs the app to catch what tests and typechecks miss ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)).

## When to delete the reminders and the hook {#when-to-delete-it}

Does all of this have to stay? The checks themselves do, for as long as there is code to check. What can retire is the scaffolding I put around the agent's use of them, meaning the repeated reminders to run the tests and the hook that sends it back. Those can go once the platform runs the project's checks as a normal step before the agent can finish, and the agent does not weaken them. I have not seen that yet.

## Try it on your own setup {#try-it}

::: prompt
Find out what a coding agent could run in this repository to check its own work: tests, build, typecheck, linter, formatter, example runs. For each, give the exact command, how long it takes if you can tell, and whether the output is short and clear enough for you to act on. Say whether the instruction files tell the agent about these commands. Then name the biggest part of the code that none of these checks would catch a bug in. Do not change any files, and do not run anything that takes more than a minute.
:::

## Go deeper {#go-deeper}

- [Counted checks](5-5-counted-checks.html): why code, not the agent, should count the passes.
- [Guardrails](4-3-guardrails.html): keeping the tests out of reach.
- [Use subagents sparingly](2-3-subagents.html): the independent check.
- Anthropic: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

## Explore it in the harness {#explore}

The harness asks for a record of self-testing before a development task counts as done, and it keeps a separate reviewer for what a self-check cannot judge.

::: prompt
/harness-rookie-wondering I have read the chapter "Let the agent check its own work". Teach me where this harness asks the agent to run its own checks, what counts as done for a development task, and how the independent check (topic 11) fits with it. Open the real files with me and draw the loop.
:::
