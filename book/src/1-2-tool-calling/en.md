This chapter assumes you know that an AI coding agent can read files and run commands. You do not need to know how.

## In one sentence {#in-one-sentence}

A model only asks for a tool call, while the program around it runs the tool. So a tool is an interface for an unreliable user, and its description and error messages decide whether it is used well.

## For leaders {#for-leaders}

- **The decision:** treat the tools you give an agent as a product that needs a good description and good error messages, and decide which fixed steps go into a command rather than a prompt.
- **The risk:** the model can only guess from a tool's name and description, so a vague tool gets used wrongly or not at all. A rule written in a prompt is a request, while a step done by a command cannot be skipped on that path.
- **The cost of doing it right:** rewriting descriptions and error messages costs little. A command is code, and someone has to maintain it. Anthropic suggests five real tasks are enough to start testing tools.
- **Ask the team:** "If you read only the name and description of each tool, would you know when to use it? What does its error say?"

## Who actually runs the tool? {#problem}

When you watch an agent edit a file, it looks as if the model did it. It did not. A language model is a program that takes in text and produces text, so on its own it cannot open a file, run a command or send a request. It has no hands.

What it can do is write a sentence that means "please call the tool `read_file` with the path `src/app.py`". That sentence is a **tool call**: the model's request to use a **tool**, along with the arguments it chose. A tool here means one action the agent may ask for, such as reading a file, searching, editing a file, running a command or fetching a web page. The program around the model (the harness, in the first sense from [chapter 0.1](0-1-the-gap-and-the-map.html)) reads the sentence and does the work, then puts what came back into the conversation as more text. The model reads that text, the **tool result**, to decide what to do next.

This looks like a technical detail, but it changes how you should think about tools. Every action an agent takes passes through a call that the program could inspect, refuse or change. And the model is not a careful programmer calling a function. It is a reader guessing from a description, so treat it like a user who skims.

### One round trip

::: figure 1-2-tool-call

The provider's own documentation describes the same round trip. The model answers with a stop reason of `tool_use` and a block that names the tool and its arguments. Your code then runs the tool and sends back a `tool_result`. ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview))

There is one exception worth knowing. Some **server tools**, such as web search, run on the provider's side, so you never handle the call yourself. Most of what an agent in your editor does, though, goes through client tools, which run on your machine. The difference matters for this chapter, because with a server tool you cannot step in before or after it runs. The program never sees the call.

## Where you can step in, and what to write for the model {#how-it-works}

### Where you can step in

With a client tool, the program sits between the request and the action, which gives it two places to step in. Before the tool runs, it can let the call through, refuse it or change it. The usual way to do that is a hook ([chapter 2.2](2-2-hooks.html)). When a hook refuses, the reason it gives goes back to the agent. After the tool runs, the program can shorten, filter or add to the result before the model reads it.

That is the main reason it is possible to enforce rules on an agent at all. A rule that lives in the program is code that runs, whereas a rule in a prompt is a request ([chapter 4.1](4-1-requests-and-rules.html)).

But a hook can only judge a call the model has already made. Whether the model makes a good call in the first place depends on the middle of the trip, on what it sees before it calls and what it gets back afterwards, and both of those are text you write.

### A tool is an interface for an unreliable user

Think about what each side has to go on. A person using a command line can read documentation, ask a colleague, and notice that something looks wrong. The model has the tool's name, a short description and the list of parameters, and nothing more. So it can guess wrongly, and the provider's documentation says as much: given a tool that needs a location and a request that does not give one, a model might make one up. ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview))

Designing a tool for an agent, then, means designing for a user who decides when to use it from the name and description alone, and who fills in the arguments by guessing from context. It does not know anything the tool does not tell it, and it reads the result as plain text, however much room that takes in the context window.

Anthropic's advice on writing tools for agents makes the same point in other words: "Even small refinements to tool descriptions can yield dramatic improvements." ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)) The five rules below follow from it, and they come roughly in the order a call meets them.

### 1. Write the description like a brief for a new hire

Before any call, the description is the only place the model learns what a tool is for, so it has to say what the tool does, when to use it, and when not to. A vague one means the tool is used wrongly or never. Names need the same care, because a parameter called `user` can mean a name, an ID or an email, while `user_email` can mean only one thing. And if two tools look alike, each description should say how it differs from the other.

### 2. Write errors for the agent to read

When a call goes wrong, the next thing the model reads is the error. A person can look at a stack trace and stop to think, but a model takes the text it is given and goes on. If the error is `Error 400`, the model guesses, often the same thing again. If the error says what was wrong and what to try next, it fixes the call.

The same goes for a refusal, which should say what to do instead ([chapter 4.2](4-2-ask-vs-refuse.html)).

### 3. Keep the output short, and let it be paged

When the call works, what the model reads is the output. Everything a tool returns goes into the context window ([chapter 3.1](3-1-context-budget.html)), and it is read again on every later turn ([chapter 1.1](1-1-models-and-cost.html)). So a tool that returns a whole large file when the agent wanted one line not only wastes tokens but can also crowd useful things out of the window.

The fix is to give results sensible limits, such as a default cap, a way to ask for a range or the next page, or a filter. Anthropic also describes letting the agent choose between a concise and a detailed response. When there are many tools, grouping related ones under a common name prefix helps the agent tell them apart. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

For a sense of scale, Claude Code caps tool responses at 25,000 tokens by default (Anthropic's figure at the time of writing). Whatever the cap, when you cut the output, say so, and tell the agent how to narrow its query. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

### 4. Fewer tools choose better

So far each rule has been about one tool, but the number of tools matters too. You might think an extra tool does no harm when it is not used. It still costs something, because every tool's name, description and parameters are sent to the model on every call. More tools mean more tokens and more chances to pick the wrong one, especially when they overlap. So prefer a small set of clearly different tools, and merge related operations into one where you can. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

### 5. Do the fixed steps in a command, not in a prompt

The first four rules are about tools you already have. The last is about which work should become a tool at all, and it is the one I would stress most. Some jobs have steps that always go the same way and where there is a right and a wrong: make the folder for a new task, copy the files, compute a hash, write the record, check that everything is ready before writing back. You can describe those steps in the instructions and ask the agent to follow them, and it will, most of the time.

Or you can write them once as a **command**, a small program the agent runs as a tool. The command does the steps, checks the preconditions itself and returns a short result. On the path through the command, the agent cannot skip a step or write a wrong state, because it never writes the state at all.

::: figure 1-2-prompt-vs-command

The fit is for steps that need no judgment. If a step needs the agent to decide something, leave that part to the agent and let the command do only the fixed work around it. This is what my harness does. A command line creates a task folder (the unit of work in [Manage tasks, not chats](5-1-tasks.html)), fetches files, works out diffs and counts checks, and the model only runs the command and reads the answer. The result is the same every time, and the model never has to get the steps right. Progress is a good example of why: the task list reads a data file that commands write, not the Markdown notes an agent wrote by hand, because hand-written progress misses ticks and goes wrong.

A command is also friendlier to an agent when its output says what to do next, because then the agent does not have to guess. And since the same command is read by people in a terminal and by scripts through a pipe, it can print aligned text for the first and JSON for the second, with the same fields in both.

A command has limits of its own, though. It only helps if the agent actually uses it, and it only guards what goes through it. If the agent can do the same thing another way, say by editing the file by hand, the command is a convenience, not a limit. [Chapter 4.1](4-1-requests-and-rules.html) takes that further.

### How to check your own tools

You can start with three questions about any tool you give an agent.

1. If you read only its name and description, would you know when to use it and when not to?
2. When it fails, does the message tell the agent what to do next?
3. How big can its output be, and what happens to the context if it is large?

The quickest experiment needs nothing installed. Ask the agent to call one of your tools in a way that you know is wrong, and read what comes back. If you were the agent, would it be clear enough to tell you what to do? If not, that is the message to rewrite.

If you build tools, Anthropic's method is the same idea at scale. Write tasks drawn from real use, run them, read the raw transcripts (the calls and the results, not only the final answer), and fix the descriptions and errors where the agent went wrong. Five tasks are enough to start. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

## What good tools cost, and where they go wrong {#costs-and-traps}

None of this comes free. Even a good description costs tokens, because a long one is sent on every call. So write what the model needs to choose and use the tool, and put the long manual in a file the agent reads when needed.

A command costs something different, because it is code to maintain. When your project changes, the command can be wrong in a way a prompt cannot, so keep each one small and give it a test.

Cost is not the only way tools go wrong. A tool call is not a trusted act, because the model chose the arguments after reading text that may have come from anywhere. Do not treat a call as the user's wish. [Chapter 4.6](4-6-untrusted-input.html) explains why.

One last, practical trap: tool names change between versions. If your rules or hooks match on tool names, keep the mapping in one place, so that a rename means one change.

## Does Anthropic see it the same way? {#industry}
{status: industry}

The advice in this chapter rests on two sources, and both come from Anthropic. Its advice on writing tools treats tool design as part of the work, with descriptions and error messages that deserve testing like code ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)). Its tool use documentation says that the application runs client tools and sends back the results, and that the model "might guess values you didn't supply" ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)). Both agree with the argument here, that the tool is an interface and its text is part of the interface.

## When to delete a command {#when-to-delete-it}
{status: industry}

Of the advice above, the commands are the part most likely to age, because a command that checks preconditions is scaffolding around the model's weak spots. If models become reliable enough at following multi-step instructions, a command may no longer beat a good prompt. Even then, I would keep commands for anything that has to be exactly the same every time, or that needs a record. The reasoning about descriptions and errors is a different matter, since it holds for as long as the model reads text.

## Try it on your own setup {#try-it}

::: prompt
Find every tool, command or script in this repository that an agent is meant to run (look in agent files, scripts, task runners and instruction files). For each, judge four things: is its name and description clear about when to use it and when not to; does its error message say what to do next; how large can its output get; does a fixed multi-step procedure described in the instructions belong in a command instead. List the three worst and say how to fix each. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Anthropic docs: [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

## Explore it in the harness {#explore}

My harness gives the agent a command line for the steps that must be certain, and a hook that stands at the door of every tool call. The harness can open the real files with you and show you both from the inside.

::: prompt
/harness-rookie-wondering I have read the chapter "Tool calling, and designing tools for an agent". Teach me what tools this harness gives the agent: the built-in ones, and its command line. Open the real files with me, show me a refusal and its reason, and draw how one tool call travels.
:::
