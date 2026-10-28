This chapter assumes you have typed a request into an AI chat box. Nothing else.

## In one sentence {#in-one-sentence}

The same model does far more inside a good harness than in a chat box, because most of the gap lies outside the model.

## For leaders {#for-leaders}

- **The decision:** decide where the team's effort goes: a better model, or the setup around it (the rules, checks and limits that surround the model).
- **The risk:** if most of the gap sits outside the model, switching models does not fix a disappointing result. One team changed only the setup of a coding agent and its score on one public benchmark went from 52.8% to 66.5%. That is one team, one benchmark, measured by the team itself.
- **The cost of doing it right:** the next chapter starts from the smallest useful set. Beyond that, mostly setup time.
- **Ask the team:** "When the agent let us down last time, was it the model, or something missing around it: a check, a rule, a view of the files?"

## The problem {#problem}

Picture a bug in your project. Users say the export button sometimes produces an empty file. You paste the description into a chat box, and a strong model answers with a confident explanation and a code fix.

Now picture the same model, the same bug, in a different setup. It can open your files and search them. It can run your tests. It starts by reading the rules written down for the project. Before it changes anything, it shows you a plan. When it says "fixed", something other than its own word has run the tests.

Same model. Very different afternoon. This is a thought experiment, not a measurement: I made it up to show the shape of the gap. The rest of the chapter explains where the gap comes from.

### What the chat box leaves out

In the chat box the model has only what you paste. It cannot see your files, so it guesses at them. It cannot run the fix, so nobody knows whether it works. It does not know the project's rules, and nothing stops it from suggesting something you forbid. Each of these is a missing thing around the model, not a missing skill in the model.

### Some evidence from outside this book

A team at LangChain changed only the harness of a coding agent and kept the model fixed. On a public coding benchmark (Terminal Bench 2.0) its score went from 52.8% to 66.5%. Their changes were things like a step that makes the agent verify its work before it exits, a map of the working folder given at the start, and a nudge to reconsider after repeated edits to the same file. ([Improving deep agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering))

Look at what these changes have in common. Each adds something the model does not supply for itself: a check from outside, a view of the folder, a break in a loop. That is one benchmark and one team, and the team changed its own harness and measured it themselves, so treat it as a sign, not a law. But it points the same way as the thought experiment: much of what separates a good result from a poor one is not in the model.

## How it works {#how-it-works}

### Three words first

- A **model** is the program that reads text and writes text. It is the "brain". Alone, it can only answer.
- A **tool** is one thing the model can ask for: read a file, search, change a file, run a command. Tools are the "hands". [Tool calling](1-2-tool-calling.html) explains how the model asks for one.
- An **agent** is a program that connects the two in a loop: ask the model what to do, run the tool it asks for, show the model the result, repeat until the model says it is done. [Chapter 2.1](2-1-agent-loop.html) walks through the loop.

A model plus tools is still not an agent. Somebody has to write the loop. That program is the **harness** in its first meaning.

### The two meanings of "harness"

People use the word in two ways, and mixing them causes confusion.

1. **The general harness:** the program that runs the loop. Claude Code, Codex and Copilot's agent mode are general harnesses. You buy or download them.
2. **A team's harness:** the layer you build on top of a general harness for your own team: rules, skills, checks, limits, reports. It uses the extension points the general harness leaves open.

This book is about the second one, built on VS Code Copilot. When I say "harness engineering", I mean the work of building that layer.

### Seven layers

I find it useful to sort everything around a model into seven layers. This frame is my own, not a standard (more on that under Costs and traps). For each layer there is one question that does not change when tools and models change.

::: figure 0-1-seven-layers

Read it from the bottom. Each layer has an everyday picture and a question.

| Layer | Picture | The question |
| --- | --- | --- |
| Model | the brain | How deeply can it think, and what does that cost? |
| Tools | the hands | What can it reach? |
| Runtime | joining brain and hands | Who runs the loop, and where does the loop leave a gap for me? |
| Context | company training | What should it know, and what should it not read? |
| Control | fences | Why should I trust it? |
| Flow | how work gets done | How is the job split, who judges, when does it stop, when is a person called? |
| Evidence | being able to explain | What did it do, was it right, what did it cost? |

The lower three layers are mostly bought. Model makers and platform makers build them, and they change fast. The upper four are yours to build, because they depend on your code, your colleagues and your risks. They also last longer: a platform update rarely erases your rules, while it may well replace a clever trick that got around a weak model.

That split is why this book spends little time on the lower layers and most of its pages on the upper ones. Part 1 and Part 2 cover what you need to know about the bought layers. Parts 3 to 6 cover one upper layer each.

### The edges are not clean

Do not take the layers as a law of nature. A **hook** sits right on the border. A hook is a small program the platform runs at fixed moments in every [turn](2-1-agent-loop.html) of the loop (one round of asking the model, running its tools and handing back the results), such as just before a tool runs. The platform provides the slot (runtime), but what you put in it is control. [Chapter 2.2](2-2-hooks.html) explains hooks.

A skill is another case. It is a written manual the agent reads when it needs it. A manual is context, not a hand. Only the scripts attached to it are hands.

### Three ways it fails

Why split the upper layers into three? Because they fail in three different ways.

- **Control fails: the agent causes damage.** It deletes the wrong thing or changes a file it should not touch.
- **Flow fails: the work comes back.** The agent says "done" too early or tries everything in one go. Anthropic describes both patterns in long-running agents: "the agent tended to try to do too much at once", and a later session "would look around, see that progress had been made, and declare the job done". ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents))
- **Evidence fails: nobody can say what happened.** The work may be fine, but you cannot show it, cannot find the cause when it breaks, and cannot tell whether a change helped. For example, the bill goes up and you cannot tell which task caused it.

When something goes wrong, asking "which of the three is this?" is often faster than asking "which model should I switch to?". Try it on the next failure you see.

## Costs and traps {#costs-and-traps}

**More layers are not always better.** Every layer you build is something to maintain and something that can fail. [Chapter 0.2](0-2-minimal-harness.html) starts from the smallest useful set, and every chapter ends with a section on when to delete what it describes.

**The gap is not all outside the model.** A stronger model does help. My claim is narrower: for the same model, most of the difference you can influence comes from the layers around it. I have not measured the split, and the LangChain result is one benchmark.

**The seven layers are my own frame.** They are not a standard. They are a way to put the pieces in order, and you may draw the lines elsewhere.

## What the industry says {#industry}
{status: industry}

Both sources above point the same way. LangChain changed only the harness and saw a large gain on one benchmark. Anthropic's write-up on long-running agents describes failures it saw in long-running agents (doing too much at once, declaring the job done too early) and fixes made with files, checklists and structure around the agent. It does not compare against a stronger model, so it shows where the failures were, not how much a better model would have helped. Neither source claims the model does not matter.

## When to delete it {#when-to-delete-it}
{status: industry}

The seven-layer picture is a teaching tool. If you find that one of the layers does not help you sort a problem, redraw it. The idea underneath is what I would keep: when an agent disappoints, look at what surrounds the model before you blame it.

## How to read this book {#how-to-read}

Every chapter has two parts. **The Knowledge** explains the idea and is meant to stand alone. **In my practice** points to the real files in my own setup, so you can look inside.

If you have little time, read the chapters marked as core: they carry the main line of the book, and you can follow it without the rest. The others are there when a problem sends you to them. If you decide where the team's time and budget go, start with [0.2](0-2-minimal-harness.html), [1.1](1-1-models-and-cost.html) and [7.4](7-4-rollout-and-governance.html).

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look at how you are set up in this repository: the instruction files, tools, hooks, checks and any written rules. Sort what you find into seven layers: model, tools, runtime, context, control, flow, evidence. For each layer, say what exists, and mark the layers where nothing exists. Then name the one missing piece that would most likely cause a bad result here. Do not change any files.
:::

## Go deeper {#go-deeper}

- LangChain: [Improving deep agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Explore it in the harness {#explore}

Copilot Harness is a team harness in the second sense above, and it has a part for each of the four upper layers. The harness can walk you through it from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "The gap is outside the model". Teach me how a coding agent works in this harness: the loop, the tools, and where the harness steps in. Open the real files with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.