This chapter assumes you have used an AI coding agent and read [the context budget](3-1-context-budget.html) (everything the agent reads shares one window of limited size).

## In one sentence {#in-one-sentence}

Load the fewest rules by default and read the rest only when they are needed. A skill is a manual read on demand. Like any written rule, it is not enforced.

## For leaders {#for-leaders}

- **The decision:** keep the always-loaded rules few, and decide who owns the rule files and cuts what is no longer needed.
- **The risk:** a long rule file is followed less well than a short one, and when two files disagree, the model picks one. Even a rule in a file is only a request that the model may not follow, so anything that must hold goes into code. I have no measured case of an ignored rule to quote.
- **The cost of doing it right:** an owner and a regular trim of the rule files. Cutting lines the agent would get right anyway costs little; in my own files I usually saw nothing get worse, though I have not tested this systematically.
- **Ask the team:** "Which lines in our always-loaded file would the agent get wrong without them, and who owns that file?"

## Why does a longer rule file work worse? {#problem}

The natural way to teach an agent your project is to write everything down in one file: the rules, the conventions, the warnings, the how-to for every job. Each time the agent makes a mistake, you add a line. After a few weeks the file is long, yet the agent follows it less well than it did when the file was short.

Why would more rules leave the agent following them worse? Two things go wrong as the file grows, and only the second is about obedience.

The first is that everything in the file is paid for on every turn. The file sits in the window all the time, whether or not the job in hand needs it, so a rule about database migrations takes room while you fix a typo. That room comes out of the same budget that [the context budget](3-1-context-budget.html) is about. What it costs per turn is in [Models and cost](1-1-models-and-cost.html).

The second is that the more rules there are, the less well each one is followed. In a long file the rules compete with each other. Two lines may disagree, or an important line may be lost among small ones. The platforms' own docs point the same way. Both Claude Code's and VS Code's advise keeping instruction files short, and Claude Code's also warns that when two instructions contradict each other, the model may pick one arbitrarily.

The way out is to stop putting everything in front of the agent at once. Show it a little, then let it read more only when it needs more. This idea is called **progressive disclosure**. It works like a shop that keeps a menu at the door and the full recipe in the kitchen. Anthropic names it "the core design principle that makes Agent Skills flexible and scalable" ([Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).

Two kinds of file put the idea to work. **Instructions** are rule files written for the agent to read. Some are loaded in every conversation, while others are loaded only when the agent works on certain files. A **skill** is a folder holding a manual for one kind of job. The agent reads that manual when the job comes up, not before.

With both kinds of file in hand, the first choice about any rule is where to put it. (What follows is reasoning and checks, since I have no measured case of an ignored rule to quote.)

## Where each rule goes, and why it can still be ignored {#how-it-works}

### 1. Three places for a rule

Where you put a rule decides when it costs room and when the agent sees it.

::: figure 3-3-places

The first place is always loaded. It is a short file in the root of the repository, read in every conversation, so only the rules that every job needs belong there: the safety limits, how to start, what to do when something is refused. In my setup this is one short page. If a rule is needed for one job in ten, it does not belong here.

Rules that apply to only one kind of file go in the second place, where they are loaded by file. In VS Code an instruction file has a header line, `applyTo`, with a pattern like "all files under this folder". Its rules load only when the agent opens a file that matches. The rules for how to write a skill, for instance, are loaded when the agent opens a skill file and cost nothing while it edits a pipeline. Here is the top of one such file:

::: code harness .github/instructions/skills.instructions.md L1-L4 "An instruction file that loads only for skill files: the applyTo line is the pattern."

Everything else is read on demand: long how-tos and details that are rarely needed. This is where skills and reference notes go, to be read only when the job calls for them.

There is also a fourth way to bring a rule in. A **hook** (a small program the platform runs at fixed moments, covered in [Hooks](2-2-hooks.html)) can put a few lines at the top of every message you send, so that a rule is repeated near the point where it is used. Keep it to a few lines, though, or you will have rebuilt the long file.

With these places in view, the question to ask of every rule is: **how often is this needed, and what happens if the agent misses it?** A rule that is needed every time and costly to miss is always loaded. A rule needed for one kind of file is loaded by file, while one needed for a single job goes in a skill.

That last place deserves a closer look, because a skill is not read all at once.

### 2. A skill loads in three levels

A skill is a folder whose main file, `SKILL.md`, has a header (a name and a description) and a body (the manual). Next to it there can be longer notes, scripts and templates.

::: figure 3-3-three-layers

The agent does not see all of it at once.

1. It always sees the name and description of every skill. This is the menu. It is small, but it is paid for on every turn, once for every skill you have installed.
2. When a request fits a description, it reads the whole manual. The agent decides this itself, or you type the skill's name.
3. It reads the extra files only when the manual points to them, so a long reference or a script is read at the step that needs it.

That is why you can install many skills without filling the window.

It also means that at level 1, the description is all the agent has to go on, so **the description decides whether the skill is ever found**. A vague one, such as "helps with code quality", never matches anything. A good one says three things: what the skill does, when to use it ("use when..."), and the words a person would actually say when they need it. Length matters too, since the platform limits it and a wordy description costs room for every other skill as well.

Even a good description does not guarantee that the skill is used. VS Code's documentation says plainly that discovery makes skills available but does not guarantee the model uses one, so it is worth testing (the tests are at the end of this section).

The menu itself can also grow too long. With a few dozen skills it becomes a real cost, and many of those skills are never chosen. One answer is to keep the skills of a single business area out of the menu until the task is about that area.

### 3. One rule, one source

Once rules live in several places, it is easy for the same rule to be written in three files. A change then misses one of them, leaving the agent to read three versions that slowly drift apart. So write each rule in one place. The other places hold a link and one sentence. If you find you have to restate a rule everywhere, that is a sign the structure is wrong. Rule files are shared code, too, so give them an owner who cuts the lines that are no longer needed.

### 4. Why a written rule is ignored

If a rule is loaded, why would the agent still ignore it? Getting a rule loaded is not the same as getting it followed, and there are five usual causes. The first four are about the text and where it sits:

1. The file is too long. Ask of each line whether the agent would get it wrong without it, and if not, delete the line.
2. Rules conflict. When two files say different things, the model picks one, and not always the one you want. VS Code's docs say instruction sources are additive and that you should not depend on file order to settle a conflict, so removing conflicts is your job. Search for them and fix the wording until only one version remains.
3. The rule is far from where it applies. It was in the first message and is now thousands of lines up. A rule loaded by file, or a hook reminder, puts it nearer.
4. It gives no reason. "Never do X" is easy to rationalise away, but "Never do X, because Y breaks" lets the model apply the idea to cases you did not list.

The fifth cause is the deepest, and no change to the text or its place will fix it: the rule is a request. Whatever you write in a file is read by the model, and the model can do otherwise. The Claude Code docs put it plainly: the memory files are "context, not enforced configuration". To block an action regardless of what the model decides, the same docs point to a hook. The text of a skill is no different. It makes the work go smoothly, but it does not make the wrong thing impossible.

So a rule that must hold goes into code, and that choice is the subject of [A rule in a prompt is a request](4-1-requests-and-rules.html). The text then only has to explain why, so that the agent does not try again to get around the refusal. In my setup a rule that matters has both layers: the text teaches and the code stops.

Does a skill's header change any of this? On some platforms the header can carry stronger settings, so check what they actually do. In Claude Code, for example, `allowed-tools` only pre-approves tools and does not restrict them. A skill can also register hooks, which are code ([Skills](https://code.claude.com/docs/en/skills)).

### 5. One more choice: language

The idea of one source also settles a question that comes up if you work in more than one language. I keep one copy of the rules and skills in English and tell the model which language to answer in, because a second copy of prose slowly drifts from the first. That is my own choice, but the principle is only to have one copy.

### Three questions and three tests

Before you add a rule, ask three questions of it:

1. How often is it needed? If rarely, it does not go in the always-loaded file.
2. Is it already written somewhere? If so, link to it.
3. If the agent ignores it, what happens? If the answer is "something bad that cannot be undone", it is not a job for text.

One test you can run today needs no extra setup. Go through your always-loaded file and ask of every line whether the agent would get it wrong without it. Cut every line that fails, then run the same task as before and see whether anything got worse. When I have cut lines from my own rules file, I usually saw nothing get worse, although I have not tested this systematically.

To check that a skill is found, start by writing the requests, in the words a person would use rather than the words of the description: three ways of asking for the job, and two neighbouring requests that should not trigger it. Open a new chat for each one, since an old chat may already hold the skill. Do not type the skill's name, either. Then look at which skills were loaded. Use the platform's log if it has one, because what the agent says is not evidence. If the skill did not load, the description lacks the user's words; if it loaded when it should not have, the description is too wide.

Whether a skill changes anything is a separate test. Run the same task twice in new chats, once with the skill and once without. If you cannot see a difference, cut the lines that make none. The agent already knew them.

## What loading less costs {#costs-and-traps}

If splitting rules up saves room, what does it cost? A rule in a skill is read only if the skill is found, so a rule that matters but sits in a skill with a weak description may never be read at all. That is the price of saving room. So when missing a rule is costly, the rule belongs in a place that loads.

Nor is being found something you settle once. A skill is not a setting but a choice the model makes each time, so the same request can load it once and not the next. The more skills you have, the harder the choice between them becomes, because even a good description may be confused with its neighbour. Keep each skill narrow, and say what it is not for.

The fourth way, a hook that injects text, has a trap of its own. Its lines add up, because each one is repeated on every message. The always-loaded file has a similar limit: the Claude Code docs suggest under about 200 lines. That is a rule of thumb rather than a measured limit, so measure your own.

## Do the platforms agree? {#industry}
{status: industry}

VS Code loads skills in the same three levels. It reads the name and description first, loads the body "once the skill is relevant", and reads other files "only when it references them". It also says that discovery "does not guarantee that it invokes a skill for every relevant prompt". For instruction files, its advice is to "keep your instructions short and self-contained" and to "include the reasoning behind rules", and it calls the sources "additive". ([Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions))

Anthropic describes the same three levels for Agent Skills: the name and description first, the body when the skill applies, and linked files only as needed ([Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)). Claude Code suggests keeping each memory file under 200 lines, moving rules for one part of the code into files that load only for matching paths, and removing contradictions. It treats these files as "context, not enforced configuration" ([How Claude remembers your project](https://code.claude.com/docs/en/memory)).

So the two platforms use the same shape: an always-on file, path-scoped rules and on-demand skills. Because the idea is the same across tools, what you build here moves with you.

## Which by-hand parts to delete, and what stays {#when-to-delete-it}
{status: industry}

Two things in this chapter are done by hand: listing only the skills of the current area, and cutting a menu that has grown too long. Both are the kind of work the platform may take over. If the platform learns to load skills by relevance better, the area trick can go.

The reasoning does not retire, though. A bigger window does not make a long rule file better. It only lets you hold more before the problem shows up. And no loading scheme makes a written rule enforced. I would look again if a platform could show, on my own tasks, that long rule files are followed as well as short ones.

## Try it on your own setup {#try-it}

::: prompt
Audit the instruction files and skills in this repository. List: lines in the always-loaded file that you would get right without being told; rules written in more than one place; pairs of rules that contradict each other; rules that give no reason; and skills whose description is too vague to be found or too wide, with a better description for each. Mark the rules where a mistake would be costly and irreversible, since those need code and not text. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- VS Code docs: [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- Anthropic: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- Claude Code docs: [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- In this book: [Skills and workflows](3-4-skills-and-workflows.html), [A rule in a prompt is a request](4-1-requests-and-rules.html)

## Explore it in the harness {#explore}

Copilot Harness uses all three places, the three levels of loading and the rule that a rule has one source. The harness can show you each of them in the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Instructions and skills". Teach me how this harness uses the three places for rules, how its skills load in three levels, and why it says a skill is not enforced (topics 2, 3 and 15). Open the real files with me, starting from the shortest one.
:::
