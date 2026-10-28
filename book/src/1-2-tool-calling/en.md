This chapter assumes you know that an AI coding agent can read files and run commands. You do not need to know how.

## In one sentence {#in-one-sentence}

A model only asks for a tool call; the program around it runs the tool. So a tool is an interface for an unreliable user, and its description and error messages decide whether it is used well.

## For leaders {#for-leaders}

- **The decision:** treat the tools you give an agent as a product that needs a good description and good error messages, and decide which fixed steps go into a command, not a prompt.
- **The risk:** the model only guesses from a tool's name and description, so a vague tool is used wrongly or never. A rule written in a prompt is a request; a step done by a command cannot be skipped on that path.
- **The cost of doing it right:** rewriting descriptions and error messages is small. A command is code someone has to maintain. Anthropic suggests five real tasks are enough to start testing tools.
- **Ask the team:** "If you read only the name and description of each tool, would you know when to use it? What does its error say?"

## The problem {#problem}

When you watch an agent edit a file, it looks as if the model did it. It did not. A language model is a program that takes in text and produces text. It cannot open a file, run a command or send a request. It has no hands.

What it can do is write a sentence that means "please call the tool `read_file` with the path `src/app.py`". That sentence is the **tool call**. The program around the model (the harness, in the first sense from [chapter 0.1](0-1-the-gap-and-the-map.html)) reads the sentence, does the work, and puts the result back into the conversation as more text. The model then reads that result and decides what to do next.

This looks like a technical detail, but it changes how you should think about tools. Every action an agent takes passes through a call that the program could inspect, refuse or change. And the model is not a careful programmer calling a function: it is a reader guessing from a description. Treat it like a user who skims.

### Three words first

- A **tool** is one action the agent may ask for: read a file, search, edit a file, run a command, fetch a web page.
- A **tool call** is the model's request to use one, with the arguments it chose.
- A **tool result** is the text the program sends back after running it.

### One round trip

::: figure 1-2-tool-call

The provider's own documentation describes the same round trip: the model answers with a stop reason of `tool_use` and a block that names the tool and its arguments; your code runs it and sends back a `tool_result`. ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)) One exception is worth knowing: some **server tools**, such as web search, run on the provider's side, so you never handle the call yourself. Most of what an agent in your editor does are client tools, run on your machine. The difference matters for this chapter: for a server tool, you cannot step in before or after it runs, because the program never sees the call.

## How it works {#how-it-works}

### Where you can step in

Because the program sits between the request and the action, there are two places to step in:

- **Before the tool runs.** The program can let the call through, refuse it, or change it. A hook ([chapter 2.2](2-2-hooks.html)) is the usual way to do that, and a refusal comes with a reason that goes back to the agent.
- **After it runs.** The program can shorten, filter or add to the result before the model reads it.

That is the main reason it is possible to enforce rules on an agent at all. A rule that lives in the program is code that runs; a rule in a prompt is a request ([chapter 4.1](4-1-requests-and-rules.html)).

The rest of this chapter is about the middle of that trip: what the model sees and what it gets back. Both are text you write.

### A tool is an interface for an unreliable user

A person using a command line can read documentation, ask a colleague, and notice that something looks wrong. The model has the tool's name, a short description, and the list of parameters. That is all. It can guess wrongly, and the provider's documentation says so: given a tool that needs a location and a request that does not give one, a model might make one up. ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview))

So designing a tool for an agent is designing for someone who:

- reads only the name and description to decide when to use it,
- fills the arguments by guessing from context,
- does not know what the tool does not tell it,
- reads the result as text, with whatever room it takes in the context window.

Anthropic's advice on writing tools for agents says the same in other words: "Even small refinements to tool descriptions can yield dramatic improvements." ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)) The five rules below follow from it.

### 1. Write the description like a brief for a new hire

Say what the tool does, when to use it, and when not to. Make names unambiguous: a parameter called `user` can mean a name, an ID or an email; `user_email` cannot. If two tools look alike, say in each one how it differs. The description is the only place the model learns this, so a vague one means the tool is used wrongly or never.

### 2. Write errors for the agent to read

A person can look at a stack trace and think. A model gets the text and goes on. If the error is `Error 400`, the model guesses, often the same thing again. If the error says what was wrong and what to try next, it fixes the call.

The same goes for a refusal: say what to do instead ([chapter 4.2](4-2-ask-vs-refuse.html)).

### 3. Keep the output short, and let it be paged

Everything a tool returns is put in the context window ([chapter 3.1](3-1-context-budget.html)), and it is read again on every later turn ([chapter 1.1](1-1-models-and-cost.html)). A tool that returns a whole large file when the agent wanted one line wastes tokens, and it can crowd useful things out of the window.

So give results sensible limits: a default cap, a way to ask for a range or the next page, a filter. Anthropic also describes letting the agent choose between a concise and a detailed response. And when you have many tools, grouping related ones under a common name prefix helps the agent tell them apart. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)) Claude Code caps tool responses at 25,000 tokens by default (Anthropic's figure at the time of writing). When you cut the output, say so, and tell the agent how to narrow its query. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

### 4. Fewer tools choose better

Every tool's name, description and parameters are sent to the model on every call. More tools cost more tokens and give more chances to pick the wrong one, especially when they overlap. Prefer a small set that is clearly different, and merge related operations into one where you can. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

### 5. Do the fixed steps in a command, not in a prompt

This is the one I would stress most. Sometimes a job has steps that always go the same way and where there is a right and wrong: make the folder for a new task, copy the files, compute a hash, write the record, check that everything is ready before writing back. You can describe those steps in the instructions and ask the agent to follow them. It will, most of the time.

Or you can write them once as a **command**: a small program the agent runs as a tool. The command does the steps, checks the preconditions itself, and returns a short result. On the path through the command, the agent cannot skip a step and cannot write a wrong state, because it never writes it.

::: figure 1-2-prompt-vs-command

The fit is for steps that need no judgment. If a step needs the agent to decide something, leave that part to the agent and let the command do only what is fixed around it. This is what my harness does. A command line creates a task folder (the unit of work in [Manage tasks, not chats](5-1-tasks.html)), fetches files, works out diffs and counts checks, and the model only runs the command and reads the answer. Progress is a good example: the task list reads a data file that commands write, and not the Markdown notes an agent wrote by hand, because hand-written progress misses ticks and goes wrong. The result is the same every time, and the model does not have to get the steps right.

Two details make a command friendly to an agent:

- **A result that says what comes next.** The command's output tells the agent what to do next, so it does not have to guess.
- **Text for people, JSON for scripts.** The same command prints aligned text in a terminal and JSON when it is piped. The fields are the same.

A command only helps if the agent actually uses it, and it only guards what goes through it. If the agent can do the same thing another way (edit the file by hand), the command is a convenience, not a limit. [Chapter 4.1](4-1-requests-and-rules.html) takes that further.

### Test your own setup

**Three questions** for any tool you give an agent:

1. If you read only its name and description, would you know when to use it and when not to?
2. When it fails, does the message tell the agent what to do next?
3. How big can its output be, and what happens to the context if it is large?

**A zero-install experiment.** Ask the agent to call one of your tools in a way that you know is wrong, and read what comes back. Is it clear enough that you would know what to do if you were the agent? If not, that is the message to rewrite.

**A bigger loop, if you build tools.** Anthropic's method is the same idea at scale: write tasks drawn from real use, run them, read the raw transcripts (the calls and the results, not only the final answer), and fix the descriptions and errors where the agent went wrong. Five tasks are enough to start. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))

## Costs and traps {#costs-and-traps}

**Good descriptions cost tokens, too.** A long description is sent on every call. Write what the model needs to choose and use the tool, and put the long manual in a file the agent reads when needed.

**A command is code to maintain.** If your project changes, the command can be wrong in a way a prompt cannot. Keep each one small, and give it a test.

**A tool call is not a trusted act.** The model chose the arguments, after reading text that may have come from anywhere. Do not treat a call as the user's wish. [Chapter 4.6](4-6-untrusted-input.html) explains why.

**Tool names change between versions.** If your rules or hooks match on tool names, keep the mapping in one place so a rename means one change.

## What the industry says {#industry}
{status: industry}

- **Anthropic**: tool design is part of the work, and descriptions and error messages deserve testing like code. ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents))
- **Tool use documentation**: the application runs client tools and sends back results; the model "might guess values you didn't supply". ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview))

They agree with the argument here: the tool is an interface, and its text is part of the interface.

## When to delete it {#when-to-delete-it}
{status: industry}

A command that checks preconditions is scaffolding around the model's weak spots. If models become reliable enough at following multi-step instructions, a command may no longer beat a good prompt, but I would still keep commands for anything that has to be exactly the same every time, or that needs a record. The reasoning on descriptions and errors stays as long as the model reads text.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find every tool, command or script in this repository that an agent is meant to run (look in agent files, scripts, task runners and instruction files). For each, judge four things: is its name and description clear about when to use it and when not to; does its error message say what to do next; how large can its output get; does a fixed multi-step procedure described in the instructions belong in a command instead. List the three worst and say how to fix each. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Anthropic docs: [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

## Explore it in the harness {#explore}

My harness gives the agent a command line for the steps that must be certain, and a hook that stands at the door of every tool call. The harness can show you both from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Tool calling, and designing tools for an agent". Teach me what tools this harness gives the agent: the built-in ones, and its command line. Open the real files with me, show me a refusal and its reason, and draw how one tool call travels.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
