This chapter assumes you know what a tool call is. If you don't, start with [When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html).

## In one sentence {#in-one-sentence}

MCP is a standard protocol for connecting tools to an agent, and it usually doesn't give the agent any new abilities, but every server you connect brings in someone else's code, your permissions, someone else's text and a token cost, so check first whether a command would do, and once a server is connected, manage it as a dependency.

## For leaders {#for-leaders}

- **The decision:** treat every MCP server as a dependency that needs approval, the way you'd treat a library you didn't write yourselves, and when an ordinary command can do the job, prefer the command.
- **The risk:** a server brings in someone else's code, your permissions and text the model will take at face value, and it can still change after you approve it. npm has already seen a server whose first 15 versions were clean and which added a backdoor only in 1.0.16. Whether hooks can control MCP tools in Copilot isn't in the docs, and I haven't tested it.
- **The cost of doing it right:** a short review of each server (who wrote it, what it can touch, where its credentials live, whether its version is pinned), and rereading the tool list every so often.
- **Ask the team:** "Which servers are connected right now? For each one, who approved it, what can it touch, and is its version pinned?"

## Without MCP, every tool gets written once per platform {#problem}

In this chapter I want to teach you three things to think through before you connect an MCP server: what it actually changes, what comes in with it, and when a single command would do.

What an agent can do depends on the tools it has, and sooner or later you'll want it to read your issue tracker, query a database or drive a browser, and somebody has to write those tools. Each platform (VS Code Copilot, Claude Code, Codex) connects tools in its own way, so without a shared standard, three platforms and three tools can mean nine connectors, and every platform or tool you add multiplies the code there is to write and maintain.

::: figure 1-3-mcp-plug

**Model Context Protocol** (MCP) is the standard that solves this, and Anthropic open-sourced it in November 2024. It sets the format of the messages between AI applications and tools, so a tool only has to be written once, as an **MCP server**, and a platform only has to implement the protocol once. After that, any server works on any platform that supports MCP, and nine connectors turn into three plus three. The official docs compare it to a USB-C port. VS Code, Claude Code, Codex, Cursor and ChatGPT all support it today. ([What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro))

There are two more roles in the protocol you need to know. The **MCP host** is the AI application itself, such as VS Code or Claude Code, and for each server it connects to, the host creates an **MCP client**, which maintains the connection to that server. ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture))

You might expect MCP to give the agent new abilities, but usually it doesn't. It changes how tools get connected, and most of what a server can do, the agent could also do with a command or an API call. The exception is a remote server hosted by the vendor with its own sign-in, which can give you access you couldn't get any other way. So when you connect a server, don't start by asking what more it gives you. Start by asking what else came in along with the tools.

## What actually comes in when you connect a server {#how-it-works}

Connecting a server adds a dependency you didn't write to your setup. It has its own code and its own release pace, it works with the permissions you give it, and it writes into the model's context.

### A server can offer three things

The protocol defines three things a server can offer, and what separates them is who decides to use them. **Tools** are functions the model decides to call by itself, for things like working with files, calling an API or querying a database, and they're what most people mean when they say MCP. **Resources** are read-only data, such as file contents or a database schema, and the application decides whether they go into the context. **Prompts** are reusable templates that the user invokes explicitly. ([Understanding MCP servers](https://modelcontextprotocol.io/docs/learn/server-concepts))

Once connected, the host sends a `tools/list` request and gets back each tool's name, description and parameters, then merges the tools from all its servers into one table for the model. When the model wants a tool, the host sends a `tools/call` to the right server and puts the result back into the conversation. So to the model, an MCP tool looks the same as a built-in one. It still has only the name, description and error messages to go on, and every rule from the previous chapter applies, except that someone else wrote those words now.

### A local server runs on your machine, a remote server runs on someone else's

A server can run in two ways, and both use the same messages. A **local** server uses the stdio transport: the host starts a process on your machine and talks to it through its standard input and output, so what you put in your configuration is really just a startup command, like the Playwright example in the VS Code docs, `npx -y @playwright/mcp@latest`. A **remote** server uses the Streamable HTTP transport: it runs on someone else's machine, the host talks to it over HTTP, you usually have to sign in, and one server usually serves many users, as Sentry's official server does.

This difference decides what you're defending against. A local server is code running on your computer with your permissions, so what worries you is what it does on your machine. A remote server is someone else's service, so what worries you is the data you send it and the account access you hand it.

### Four things come in with every server

::: figure 1-3-what-comes-in

1. Someone else's code. A local server is a program running on your machine, and it's running from the moment it starts, without waiting for the model to call a tool. The VS Code docs put it plainly: "Local MCP servers can run code on your machine, and tools can access external services using your permissions." ([Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers))
2. Your permissions. A server acts with the access you give it, such as your database account or your issue tracker token, and through the server the agent gets that access too. So however wide the token's scope is, that's roughly how much damage is possible when the agent makes a mistake or gets tricked.
3. Someone else's text. Tool descriptions are written by someone else, and the model reads them and believes them. What tools return (the body of an issue, a web page) is written by someone else too, and this text can hide commands aimed at the model ([Text the agent reads can give it orders](4-6-untrusted-input.html)).
4. A fixed token cost. Tool names, descriptions and parameters all count as model input, and if the host sends all of them to the model, they go along with every request. Caching makes that cheaper, but it doesn't free up any of the context window, and the more tools there are, the more likely the model is to pick the wrong one.

The fourth one can get large. Anthropic gives an example with five servers: GitHub's 35 tools take about 26K tokens, Slack's 11 take about 21K, and with Sentry, Grafana and Splunk added, 58 tools take up about 55K tokens before the conversation starts ([Introducing advanced tool use for Claude](https://www.anthropic.com/engineering/advanced-tool-use)). What a host can do about it is tool search: instead of sending the tool definitions to the model, it gives the model a search tool and loads a full definition only when that tool is needed. Claude Code does this by default, loading just the tool names and server instructions at session start ([Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)). VS Code has it on by default too for Claude Sonnet 4.5, Opus 4.5 and later, keeping only a small core set loaded, such as reading and writing files and running commands, and in a live experiment its team saw the median user's token usage over a whole session fall by about 18% with Claude models ([Improving token efficiency for GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot)). So how big this cost is depends on your host, your model and how many tools you've connected, and it's best to count your own.

### First see whether a command will do

A lot of what an agent needs already exists as command-line programs, such as `git`, `gh`, test runners and the cloud platforms' CLIs, and as long as the agent can use a terminal, it can use them without any server. I lean toward commands first, because they add less code and fewer permissions to your setup, and you can always switch to MCP later, once sharing one tool across platforms is worth the extra dependency.

The tool vendors themselves say the same. The VS Code docs say right at the start that if your existing tools meet your needs, you don't need another server. The Claude Code docs recommend preferring CLIs like `gh`, `aws` and `gcloud`, because they don't add a tool listing to the context ([Manage costs effectively](https://code.claude.com/docs/en/costs)). And the README of Microsoft's Playwright MCP tells people using coding agents that a CLI plus skills may suit them better, leaving MCP for long loops that need to keep browser state ([Playwright MCP](https://github.com/microsoft/playwright-mcp)).

How many tokens you save depends on the job, though. In July 2026, Stefan Judis at Checkly ran the same browser task three times each in Claude Code: with Playwright MCP the context ended up at about 48K to 50K, and with `playwright-cli` at about 45K to 48K. That's a small gap, and his explanation is that tool definitions are loaded lazily now ([CLIs are more token-efficient than MCP. Or are they?](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/)). So on a host with tool search, the advantage of a command is mainly fewer dependencies and permissions, not tokens.

MCP has things a command can't match, too. Each of its tools has a name and a parameter schema, so the host can approve tool by tool, whereas once an agent has a terminal it can run any command, and all a hook sees is the command's text ([Hooks, the point every call passes through](2-2-hooks.html)). So if you're building an interface to an internal system with a lot of write operations, a few narrow MCP tools may be easier to control than one command-line program that can do everything.

| Choose | When |
| --- | --- |
| A command-line program | It already exists, it runs locally, its output is short and clear, and the agent can use a terminal |
| An MCP server | You want to share one tool across platforms, you need structured input, you have to sign in to a remote service, you want to approve tool by tool, or the agent runs somewhere with no terminal |

### Ask five questions before you connect one

A server is a dependency, so whatever you'd ask about a dependency, you should ask about a server. Here are five questions, in the order I'd ask them.

- Who wrote it, and who keeps it up to date? VS Code's advice is to review "the publisher, command or endpoint, and requested access" before installing or starting a server ([Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)). Being listed doesn't mean being reviewed either: the official MCP Registry only stores metadata and verifies publishers' namespaces, and it leaves security scanning to package registries like npm and to downstream marketplaces ([The MCP Registry](https://modelcontextprotocol.io/registry/about)).
- What can it touch? Prefer a server limited to what the task needs. A server that reads issues shouldn't be holding a token that can delete repositories.
- Where do its credentials live? Not in the chat and not committed to the project, and the VS Code docs add that a personal configuration file isn't a place for secrets either ([MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)).
- Is the version pinned? If the startup command says `@latest`, then as soon as the package updates, later starts may run new code, so pin a version you've looked at.
- Can you trust what it returns? If the text comes from outside, like public web pages or tickets anyone can file, treat it as untrusted.

### Whether a hook can control MCP tools depends on the platform

The Claude Code docs spell it out: MCP tools appear in events like `PreToolUse` and `PostToolUse` just as ordinary tools do, named `mcp__<server>__<tool>` ([Hooks reference](https://code.claude.com/docs/en/hooks)). The Copilot side doesn't say. GitHub's hook reference only says `preToolUse` fires "Before each tool executes", the tool names it lists are all built-in ones, and the VS Code hook docs don't mention MCP either ([GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)). My own harness doesn't set up any MCP server, because these servers are something each company configures for its own environment, and some companies forbid unofficial ones, so I haven't tested whether MCP tools on Copilot pass through hooks or whether a hook sees the complete arguments.

If you want to rely on a hook, test it first with a harmless server: write a hook that only records its input, call an MCP tool once, and look in the record for that call and its full arguments. Even if the call does pass through the hook, all the hook sees is the arguments of this one call. It can't see what the server does after receiving them.

### How to check after connecting

Servers you've already connected deserve a second look too. Ask three questions about each one:

1. Do I know who wrote it and what it can touch?
2. Could a command-line program do the same thing?
3. How many of its tools do I actually use?

You can answer the third without installing anything. In VS Code, open the Tools page in **Chat: Open Customizations** to see how many tools are enabled in each group and how many there are in total, and in Claude Code, use `/context` to see what's taking up the context. Once you've counted, think about which ones you used last week. All the others carry cost and risk with no benefit, so turn those tools off or disable the whole server.

## Official servers can go wrong too, and a server you reviewed can change {#costs-and-traps}

Every server is a route for outside text and outside code to reach the agent, so the more you connect, the more places there are for something to go wrong, and that doesn't only count the ones you're using. A server you added to try out and then forgot about is still there.

A big name is no reason to skip the review. In May 2025, Invariant Labs published a case where an attacker files an issue on a public repository with instructions for the agent hidden inside. The user only asks the agent to look at that repository's issues, but the agent is connected to the official GitHub MCP server and has access to the user's private repositories, and it ends up writing private repository contents into a pull request on a public repository. Invariant says this isn't a flaw in the server's code and that GitHub can't fix it by changing the server alone, and they recommend narrowing permissions, for example letting the agent touch only one repository per session ([GitHub MCP Exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability)). Untrusted text, private data and a way out were all present here ([Text the agent reads can give it orders](4-6-untrusted-input.html)). "Official" only tells you who wrote the code. The server still holds your credentials and still reads text other people wrote.

Even a server you reviewed carefully can change without your knowing, in three places.

- The tool list. The protocol lets a server update its tools and then tell the client to fetch the list again, so a server can change a tool's description after you've approved it, a move known as a rug pull. Invariant Labs showed what a description can hide, in an attack they call tool poisoning: an `add` tool that looks like it only does addition has a passage hidden in its description telling the model to read `~/.ssh/id_rsa` and send the contents back in a parameter ([Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)).
- The code. `postmark-mcp` on npm borrowed Postmark's name, its first 15 versions were clean, and 1.0.16 added a backdoor that quietly BCC'd emails to an outside server ([Security Alert: Malicious 'postmark-mcp' npm Package](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)).
- The configuration. In VS Code, the workspace `.mcp.json` and `.vscode/mcp.json` follow Workspace Trust, so in a trusted workspace you won't be asked again when they change, and what they hold is a command that will run. So review a pull request that changes these files the way you'd review a code change ([Manage and troubleshoot MCP servers](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers)).

So reread the tool list every so often, and pin versions wherever you can.

Another trap is assuming that the same standard means the same behavior. The protocol only standardizes the messages between host and server. Where the configuration lives, which parts of the protocol are supported and how approval works are all up to each vendor. VS Code alone has two configuration formats, one with the top-level key `mcpServers` and one with `servers`, and you can't copy directly between them. For where each platform keeps its configuration, see the [Extension points cheat sheet](a-extension-points.html). The protocol itself is still changing as well: the current version is 2026-07-28, which removed the connection handshake and sessions and marked sampling, roots and logging as deprecated, only eight months after the previous version ([Key Changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)). If you only use other people's servers you probably won't notice these changes, but if you write your own, leave time to keep up with the versions.

## The protocol and VS Code both leave the decision to you {#industry}
{status: industry}

The protocol's docs say MCP covers only the exchange of context and "does not dictate how AI applications use LLMs or manage the provided context" ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)). The specification requires hosts to get explicit user consent before invoking any tool, and it also admits that MCP itself can't enforce these principles at the protocol level ([Specification](https://modelcontextprotocol.io/specification/latest)). VS Code is one such host. It has you look at the publisher and the requested access and approve only the operations you understand, and for organizations it offers the `ChatMCP` policy, which can restrict servers to a registry, although the policy doesn't reach servers the Copilot runtime discovers on its own ([Secure AI-assisted development in VS Code](https://code.visualstudio.com/docs/agents/run/security)). So the two agree on who does what: the protocol makes connecting easy, and deciding what to connect is still your job.

## When to delete a server {#when-to-delete-it}
{status: industry}

When you no longer use a server's tools, or an ordinary command can do the job, remove it.

When you can relax this caution depends on the platform. If a platform put local servers in a sandbox by default, a bad server could do far less, but as I write this we're not there yet: VS Code's Copilot session sandbox is off by default, and even when it's on, it doesn't block outbound network access by default ([Sandbox Copilot agent sessions](https://code.visualstudio.com/docs/agents/run/agent-sandboxing)). A sandbox also contains only the server's process. It can't limit the remote account you gave the server or the text the server returns to the model, so even with a sandbox I'd still check the publisher and the access before adding one.

## Try it on your own setup {#try-it}

::: prompt
Find every MCP server configured for this project or editor (check the editor and project settings, and all MCP configuration files). For each one, tell me: who published it, whether it runs locally or remotely, whether its startup command pins a version, what credentials it uses and where they are stored, how many tools it exposes, and whether an ordinary command-line program could do the same job. Flag any credentials stored in committed files. Do not print any secret values, and do not change any files.
:::

## Go deeper {#go-deeper}

- Model Context Protocol: [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture), [Specification](https://modelcontextprotocol.io/specification/latest), [Client Best Practices](https://modelcontextprotocol.io/docs/develop/clients/client-best-practices), [Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- VS Code docs: [Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers), [Manage and troubleshoot MCP servers](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers), [MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
- Anthropic: [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp), which has the agent write code to call servers so that intermediate results stay out of the model's context, at the price of needing a secure sandbox
- Invariant Labs: [Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [GitHub MCP Exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability)

## Explore it in the harness {#explore}

My harness gives the agent three kinds of tools: built-in tools, its own command-line tool, and optional MCP, and it doesn't set up any MCP server of its own. The harness can open the real files with you and show you where MCP would connect and how the other tools are sorted.

::: prompt
/harness-rookie-wondering I have read the chapter "What should you think through before connecting an MCP server?". Teach me the three kinds of tools in this harness and where MCP fits. Open the real files with me, and show me how tool names are sorted into kinds.
:::
