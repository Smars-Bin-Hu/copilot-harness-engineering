This chapter assumes you have used an AI coding agent. It builds on [The agent loop](2-1-agent-loop.html): the agent asks the model, runs a tool, and feeds the result back.

## In one sentence {#in-one-sentence}

Give the agent a way to check its own work: run the tests, the linter, the program. A check it can run and read gives it feedback inside the loop; a reviewer only finds problems afterwards.

## For leaders {#for-leaders}

- **The decision:** require that every task comes with a check the agent can run and read itself, such as tests, a build or a linter, and decide which of those checks the agent may not edit.
- **The risk:** an agent stops when its work looks done, and in my own use models often lean towards reporting success; I have not recorded how often. Anthropic describes a later agent that would "declare the job done" after seeing progress. An agent can also pass by weakening the test. I have not recorded such a case, so it is a risk to design for.
- **The cost of doing it right:** often one line in the instruction file: the command that runs the project's check. Slow suites need a fast subset to run often. I have not measured how much a self-check improves results.
- **Ask the team:** "What can the agent run to know that its work is done, and can it change that check?"

## The problem {#problem}

An agent stops when its work *looks* done. Looks done is a feeling the model has about its own code. It has not run anything. It says "I have made the change", you read it, and you find the bug.

If the agent has nothing to run that says whether the work is done, you are the test suite. Every mistake waits until you notice it. That is slow, and it needs you in front of the screen.

In my own use I have often seen models lean towards reporting success; I have not recorded how often. Anthropic describes the same pull in long runs, where a later agent instance would "declare the job done" after seeing that progress had been made ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). And an agent that checks its own work by reading it shares its own blind spots, since the same reasoning that wrote the mistake reads it ([Use subagents sparingly](2-3-subagents.html)).

The way out is not a smarter agent. It is a check that does not depend on the agent's feeling.

## How it works {#how-it-works}

### One of the most useful things you can add

Compare two cases.

In the first, the agent changes code and says "done". You run the tests; two fail. You tell the agent. It fixes one. You run again.

In the second, the agent changes code and runs the tests itself. Two fail. It reads the output and fixes both. It runs the tests again. They pass. It says "done" and shows the output.

Same model. The difference is that in the second case the result of the check came back **inside the loop**, before the agent finished. The loop in [The agent loop](2-1-agent-loop.html) already has a place for this: a tool result goes back to the model, and the model decides the next step. A test run is just a tool whose result says, plainly, pass or fail.

::: figure 5-4-check-loop

Anthropic's guide for Claude Code says the same thing in its own words: give the agent something it can run that comes back pass or fail, and it can keep going on its own, so that you do not have to watch. ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)) I put this near the top of the levers. A reviewer is also valuable, but it works afterwards, on finished work. A self-check changes what the agent does while it works.

### What can be run

Anything that gives a result the agent can read:

- **Tests:** the project's own tests, or a new test written for this change.
- **A build or typecheck:** the exit code alone says it works or not.
- **A linter or formatter:** quick, and it catches a class of mistakes.
- **A script that compares output with a known-good file:** good for data work, where the right answer is a table.
- **Running the program:** for a pipeline, run it on a small input and look at the output.
- **A screenshot next to a mockup:** for user interfaces.

If a repository already has one of these, the most useful single line in the agent's instruction file is the command that runs it. The agent cannot guess which command the project trusts.

There are also levels of how firmly you ask for it, from soft to hard. This is the ladder from [A rule in a prompt is a request](4-1-requests-and-rules.html):

1. **In the prompt:** "run the tests after, and keep going until they pass". The agent decides when it is satisfied.
2. **As a stop condition:** a hook ([Hooks](2-2-hooks.html)) runs at the moment the agent tries to stop. If the check fails, the hook sends the agent back to work. The platform enforces it, so the agent cannot end its turn with a failing check. Claude Code's documentation describes this with a Stop hook ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)). I have not tested the same in Copilot for this chapter.
3. **Counted by code:** the number of passes is counted by a program, not reported by the agent ([Counted checks](5-5-counted-checks.html)).

### Make the result short and readable

The agent reads the check's output, and the output goes into its context ([Context is a budget](3-1-context-budget.html)). Two things go wrong.

- **Too long.** A test run that prints thousands of lines fills the context, and the failure the agent needs is lost in them. Print the failures, with the file and line, and a count. Hide the passing noise.
- **Too vague.** "Error" alone gives the agent nothing to act on. A good failure says what was expected, what happened, and where.

This is the same advice as for tool messages in [Tool calling](1-2-tool-calling.html): the agent is an unreliable user, and what it reads decides what it does next. A check whose output is cheap and clear is worth more than a thorough check that nobody can read.

Ask also for evidence. "All tests pass" is a claim. The command that was run, and its output, is evidence. When you were not watching, it is the only evidence you have.

### What a self-check cannot catch

A passing check says: "this does what the check tests." It does not say: "this is what you wanted." Two gaps matter.

**The requirement is wrong.** If the page the agent works from is not what the person meant ([The agent writes the requirement](5-2-requirements.html)), then perfect code that passes every test is perfect code for the wrong thing. No test the agent writes from a wrong requirement will find that. Only a person, reading the requirement, can.

**The test is weak.** A test may check too little: it passes with the bug in. A test the agent wrote in the same session was written with the same understanding as the code, so it shares the same blind spot. If the agent misread the rule, its code and its test will agree with each other and both be wrong.

A third thing sits beside these: some mistakes only show when the program is run in the real setting, with real data, and the agent cannot run it there. That is a person's check, or a test environment's.

### The failure mode: the agent weakens the test

Here is a failure that follows from giving the agent a check. The agent wants the loop to end with a pass. The easy way to get a pass is to change the check, not the code. It can:

- loosen an assertion until it passes,
- delete or skip the test that fails,
- change the expected value to whatever the code now gives,
- catch an error and swallow it.

Nothing here needs bad intent. The agent is doing what the loop rewards: finishing with a pass. I have not recorded a case of this in my own runs, so I describe it as a risk to design for, not as something I measured.

Three defences, from cheapest to hardest:

1. **Say it in words.** "Fix the code, not the tests. If a test seems wrong, say so and stop." It helps and it is a request ([A rule in a prompt is a request](4-1-requests-and-rules.html)).
2. **Keep the tests out of its reach.** If the tests are part of what must not be edited, a hook refuses the change. [Guardrails](4-3-guardrails.html) explains why files that check the agent should be outside what the agent can write. This does not fit work where adding new tests is part of the job. There, protect the existing tests and let it add new ones.
3. **Do not trust the report; count.** Look at the diff of the tests (the list of changed lines). A change to a test that was failing is a flag. And let code, not the agent, count passes, with a record that the check ran ([Counted checks](5-5-counted-checks.html)).

### How it divides work with an independent check

The two are not rivals; they catch different things.

| | Self-check | Independent reviewer |
| --- | --- | --- |
| When | While the agent works | After it finishes |
| Catches | Things a program can judge: it runs, it passes, it matches a file | Things a program cannot judge: does it match the request, is the logic sound |
| Misses | Wrong requirement, weak test | Blind spots the reviewer shares with the author |
| Cost | Cheap, runs again and again | One more agent, several times the usage ([Use subagents sparingly](2-3-subagents.html)) |

So the order is: self-checks first, as many and as cheap as you can, inside the loop. Then, where it is worth the cost, an independent check on the result. A reviewer who sees a green test run can spend its attention on the question tests cannot answer: is this the right thing?

## Costs and traps {#costs-and-traps}

- **A check that can pass wrongly is worse than none.** It gives false comfort. A test that never fails tells you nothing.
- **Slow checks slow the loop.** If the full suite takes twenty minutes, the agent runs it rarely. Give it a fast subset to run often, and the full suite at the end.
- **Flaky checks teach the agent the wrong thing.** A test that fails at random sends the agent hunting for a bug that is not there, or teaches it to rerun until green.
- **Output can fill the context.** See above.
- **Some code cannot be run by the agent.** Where the real data, the real environment or the permission is not available to it, a self-check can only cover part. Say which part, and leave the rest to a person.
- **I have not measured how much a self-check improves results in my own setup.** The direction is clear from the vendor's guidance and from the loop itself; the size of the effect I do not know.

### Test your own setup

Put a bug into working code on purpose, then run the checks the agent would run. If they stay green, the check does not cover that part of the code, whatever the agent reports. This is a cheap way to see how much a passing check is worth.

## What the industry says {#industry}
{status: industry}

Anthropic's Claude Code guide puts "give it a check to run" next to telling the agent what it cannot see, and lists a test file, a build exit code, a linter, a script that compares output with a fixture, and a browser screenshot as examples. It also says to ask for the evidence, not only "all tests pass", and mentions a command that builds and runs the app to catch what tests and typechecks miss. ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices))

## When to delete it {#when-to-delete-it}

The checks themselves stay as long as there is code to check. What can retire is the scaffolding I put around the agent's use of them: the repeated reminders to run the tests, and the hook that sends it back. When the platform runs the project's checks as a normal step before the agent can finish, and the agent does not weaken them, those can go. I have not seen that yet.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find out what a coding agent could run in this repository to check its own work: tests, build, typecheck, linter, formatter, example runs. For each, give the exact command, how long it takes if you can tell, and whether the output is short and clear enough for you to act on. Say whether the instruction files tell the agent about these commands. Then name the biggest part of the code that none of these checks would catch a bug in. Do not change any files, and do not run anything that takes more than a minute.
:::

## Go deeper {#go-deeper}

- [Counted checks](5-5-counted-checks.html): why code, not the agent, should count the passes.
- [Guardrails](4-3-guardrails.html): keeping the tests out of reach.
- [Use subagents sparingly](2-3-subagents.html): the independent check.
- Anthropic: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

## Explore it in the harness {#explore}

The harness asks for a record of self-testing before a development task counts as done, and it has a separate reviewer for what a self-check cannot judge. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Let the agent check its own work". Teach me where this harness asks the agent to run its own checks, what counts as done for a development task, and how the independent check (topic 11) fits with it. Open the real files with me and draw the loop.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.