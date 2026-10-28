This chapter assumes only that you have typed a request into an AI chat box.

## In one sentence {#in-one-sentence}

The same model does far more inside a good harness than in a chat box, because most of the gap lies outside the model.

## For leaders {#for-leaders}

- **The decision:** where the team's effort should go: into a better model, or into the setup around it (the rules, checks and limits that surround the model).
- **The risk:** if most of the gap sits outside the model, switching models will not fix a disappointing result. One team changed only the setup of a coding agent and saw its score on a public benchmark go from 52.8% to 66.5%, though that is one team on one benchmark, measuring its own work.
- **The cost of doing it right:** the next chapter starts from the smallest set that is still useful; beyond that, the cost is mostly setup time.
- **Ask the team:** "The last time the agent let us down, was it the model, or something missing around it: a check, a rule, a view of the files?"

## If the model is the same, where does the gap come from? {#problem}

Picture an ordinary afternoon. Users report that the export button sometimes produces an empty file. When you paste their description into a chat box, a strong model soon gives you a confident explanation and a code fix.

Now put the same model in a different setup, facing the same bug. This time it can open your files, search them and run your tests. Before it touches anything, it reads the rules written down for the project and shows you a plan. And when it finally says "fixed", you do not have to take its word for it, because a check outside the model has already run the tests.

Neither the model nor the bug has changed, yet the two afternoons could hardly be more different. I made the scene up as a thought experiment, to show the shape of the gap rather than to measure it. What, exactly, did the second setup give the model that the chat box did not?

### What the chat box leaves out

In the chat box, the model had only what you pasted, so it could not see your files and had to guess at them. It could not run its fix either, which meant nobody knew whether the fix was right. And since it did not know the project's rules, nothing stopped it from suggesting something you forbid. None of these is a skill the model lacks. Each is something missing around it.

### Is there evidence beyond a made-up afternoon?

There is some. When a team at LangChain kept the model of a coding agent fixed and changed only its harness, the agent's score on a public coding benchmark (Terminal Bench 2.0) went from 52.8% to 66.5%. Their changes were things like a step that makes the agent verify its work before it exits, a map of the working folder given at the start, and a nudge to reconsider after repeated edits to the same file. ([Improving deep agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering))

Each of these changes adds something the model does not supply for itself: a check from outside, a view of the folder, a break in a loop. This is one team's result on one benchmark, from a harness the team changed and measured itself, so it is a sign rather than a law. Still, it points the same way as the thought experiment: much of what separates a good result from a poor one is not in the model.

## A map of what surrounds the model {#how-it-works}

### From a model to an agent

If the difference lies around the model, it helps to name what is there, piece by piece. Start with the **model** itself, the program that reads text and writes text. It is the "brain", but on its own it can only answer. To act, it needs **tools**, each of them one thing it can ask for, such as reading a file, searching, changing a file or running a command. These are its "hands". How the model asks for one is the subject of [Tool calling](1-2-tool-calling.html).

A brain and a pair of hands still do not make a worker, though. Something has to ask the model what to do, run the tool it asks for, show it the result, and repeat until the model says it is done. Connected in that loop, the two become an **agent** ([Chapter 2.1](2-1-agent-loop.html) walks through the loop). The loop does not write itself. Somebody has to program it, and that program is the **harness**, in the first of its two meanings.

### The two meanings of "harness"

People use the word in two ways, and mixing them up causes a good deal of confusion. The first is the **general harness**, the program that runs the loop. Claude Code, Codex and Copilot's agent mode are all general harnesses, the kind you buy or download. The second is **a team's harness**: the layer you build on top of a general harness for your own team, made of rules, skills, checks, limits and reports. It plugs into the extension points that the general harness leaves open.

This book is about the second kind, built on VS Code Copilot. When I say "harness engineering", I mean the work of building that layer.

### Seven layers

A team's harness has many pieces, so to keep them apart I sort everything around a model into seven layers. The frame is my own (more on where it can mislead you [later](#costs-and-traps)). What makes it useful is that each layer comes with a question that stays the same when the tools and models change.

::: figure 0-1-seven-layers

Read it from the bottom up. Each layer has an everyday picture and a question.

| Layer | Picture | The question |
| --- | --- | --- |
| Model | the brain | How deeply can it think, and what does that cost? |
| Tools | the hands | What can it reach? |
| Runtime | joining brain and hands | Who runs the loop, and where does the loop leave a gap for me? |
| Context | company training | What should it know, and what should it not read? |
| Control | fences | Why should I trust it? |
| Flow | how work gets done | How is the job split, who judges, when does it stop, when is a person called? |
| Evidence | being able to explain | What did it do, was it right, what did it cost? |

The lower three layers are mostly bought. Model makers and platform makers build them, and they change fast. The upper four are yours to build, because they depend on your code, your colleagues and your risks. They also last longer: a platform update rarely erases your rules, but it may well make obsolete a clever trick you built to get around a weak model.

That is why this book spends little time on the lower layers and most of its pages on the upper ones. Part 1 and Part 2 cover what you need to know about the bought layers, while Parts 3 to 6 take one upper layer each.

### The edges are not clean

The layers are a way of sorting, not a law of nature, so it is no surprise that some pieces sit right on a border. Take the **hook**, a small program the platform runs at fixed moments, such as just before a tool runs. Those moments come round in every [turn](2-1-agent-loop.html) of the loop, that is, in every round of asking the model, running its tools and handing back the results. The platform provides the slot, which belongs to the runtime, but what you put in the slot is control (more on hooks in [Chapter 2.2](2-2-hooks.html)).

A skill is another border case. It is a written manual the agent reads when it needs it, which makes it context. Only the scripts attached to it count as hands.

### Three ways it fails

Why give control, flow and evidence a layer each? Because each of them fails in its own way.

When control fails, the agent causes damage: it deletes the wrong thing, or changes a file it should not touch. A failure of flow looks different. The work comes back to you, because the agent said "done" too early or tried to do everything in one go. Anthropic saw both patterns in long-running agents, where "the agent tended to try to do too much at once", and a later session "would look around, see that progress had been made, and declare the job done". ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)) Evidence, finally, can fail even when the work is fine. Then nobody can say what happened: you cannot show that the work is right, cannot find the cause when it breaks, and cannot tell whether a change helped. If the bill goes up, say, you cannot tell which task caused it.

This is where the map earns its keep. When something goes wrong, asking "which of the three is this?" is often faster than asking "which model should I switch to?". Try it on the next failure you see.

## Where the map can mislead you {#costs-and-traps}

Seven layers can make it look as if a good harness needs something in every one of them. It does not. Every layer you add is something to maintain and something that can fail, which is why [Chapter 0.2](0-2-minimal-harness.html) starts from the smallest useful set, and why every chapter ends with a section on when to delete what it describes.

The map can also make the model look as if it hardly matters. That is not my claim either. A stronger model does help. My claim is narrower: for the same model, most of the difference you can influence comes from the layers around it. I have not measured that split, and the LangChain result is a single benchmark.

And the map can look more official than it is. The seven layers are my own frame rather than a standard, one way among others to put the pieces in order.

## What LangChain and Anthropic found {#industry}
{status: industry}

Both sources point the same way, though they show different things. LangChain changed only the harness and saw a large gain on one benchmark. Anthropic's write-up on long-running agents describes the failures it saw (doing too much at once, declaring the job done too early) and the fixes it made with files, checklists and structure around the agent. Since it does not compare against a stronger model, it shows where the failures were, not how much a better model would have helped. Neither source claims that the model does not matter.

## When to redraw the map, or delete it {#when-to-delete-it}
{status: industry}

The seven-layer picture is a teaching tool, so treat it like one. If a layer does not help you sort a problem, redraw it. What I would keep is the idea underneath it: when an agent disappoints you, look at what surrounds the model before you blame the model.

## How to read this book {#how-to-read}

Every chapter has two parts. **The Knowledge** explains the idea and is meant to stand on its own, while **In my practice** points to the real files in my own setup, so you can look inside.

If you have little time, read the chapters marked as core. They carry the main line of the book, so you can follow it without the rest. The others are there for when a problem sends you to them. And if you decide where the team's time and budget go, start with [0.2](0-2-minimal-harness.html), [1.1](1-1-models-and-cost.html) and [7.4](7-4-rollout-and-governance.html).

## Try it on your own setup {#try-it}

::: prompt
Look at how you are set up in this repository: the instruction files, tools, hooks, checks and any written rules. Sort what you find into seven layers: model, tools, runtime, context, control, flow, evidence. For each layer, say what exists, and mark the layers where nothing exists. Then name the one missing piece that would most likely cause a bad result here. Do not change any files.
:::

## Go deeper {#go-deeper}

- LangChain: [Improving deep agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Explore it in the harness {#explore}

Copilot Harness is a team harness in the second sense above, with a part for each of the four upper layers. It can walk you through them from the inside, with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "The gap is outside the model". Teach me how a coding agent works in this harness: the loop, the tools, and where the harness steps in. Open the real files with me and draw how the pieces fit together.
:::
