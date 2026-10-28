This chapter assumes you have used an AI coding agent, and read [the context budget](3-1-context-budget.html) (everything the agent reads shares one window of limited size).

## In one sentence {#in-one-sentence}

Load the fewest rules by default and read the rest only when needed. A skill is a manual read on demand, and like any written rule it is not enforced.

## For leaders {#for-leaders}

- **The decision:** keep the always-loaded rules few, and decide who owns the rule files and cuts what is no longer needed.
- **The risk:** a long rule file is followed less well than a short one, and two files that disagree make the model pick one. A rule in a file is still a request: the model can do otherwise. Anything that must hold goes into code. I have no measured case of an ignored rule to quote.
- **The cost of doing it right:** an owner and a regular trim of the rule files. Cutting lines the agent would get right anyway costs little; in my own files I usually saw nothing get worse, but I have not tested this systematically.
- **Ask the team:** "Which lines in our always-loaded file would the agent get wrong without them, and who owns that file?"

## The problem {#problem}

The natural way to teach an agent your project is to write everything down in one file: the rules, the conventions, the warnings, the how-to for every job. Each time the agent makes a mistake, you add a line. After a few weeks the file is long, and the agent follows it less well than when it was short.

Two things go wrong. They are the subject of this chapter.

- **Everything is paid for every turn.** The file sits in the window all the time, whether or not this job needs it. A rule about database migrations takes room while you fix a typo. This room is the same budget that [the context budget](3-1-context-budget.html) is about; what it costs per turn is in [Models and cost](1-1-models-and-cost.html).
- **More rules means each rule is followed less.** Long files make rules compete. Two lines may disagree; an important line is lost among small ones. The docs of both Claude Code and VS Code advise keeping instruction files short, and Claude Code's warns that when two instructions contradict each other the model may pick one arbitrarily.

Three words first.

- **Instructions** are rule files written for the agent to read. Some are loaded in every conversation. Others are loaded only when the agent works on certain files.
- A **skill** is a folder with a manual for one kind of job. The agent reads the manual when the job comes up, not before.
- **Progressive disclosure** is the idea behind both: show the agent a little, and let it read more only when it needs more. Like a shop with a menu at the door and the full recipe in the kitchen. Anthropic names it "the core design principle that makes Agent Skills flexible and scalable" ([Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).

I have no measured case of an ignored rule to quote, so this chapter gives the reasoning and the checks.

## How it works {#how-it-works}

### 1. Three places for a rule

Where you put a rule decides when it costs room and when the agent sees it.

::: figure 3-3-places

- **Always loaded.** A short file in the root of the repository, read in every conversation. Only the rules that every job needs go here: the safety limits, how to start, what to do when something is refused. In my setup this is one short page. If a rule is needed for one job in ten, it does not belong here.
- **Loaded by file.** Rules that apply to one kind of file. In VS Code, an instruction file has a header line, `applyTo`, with a pattern like "all files under this folder". The rules load only when the agent opens a file that matches. Rules for how to write a skill are loaded when it opens a skill file, and cost nothing when it edits a pipeline. Here is the top of one such file:

::: code harness .github/instructions/skills.instructions.md L1-L4 "An instruction file that loads only for skill files: the applyTo line is the pattern."
- **Read on demand.** Everything else: long how-tos, rarely needed details. This is where skills and reference notes go. The agent reads them when the job calls for them.

A fourth way: a **hook** (a small program the platform runs at fixed moments; see [Hooks](2-2-hooks.html)) can put a few lines at the top of every message you send, to repeat a rule near the point of use. Keep it to a few lines, or you rebuild the long file.

The question for every rule is: **how often is this needed, and what happens if the agent misses it?** Needed every time and costly to miss: always loaded. Needed for one kind of file: by file. Needed for one job: a skill.

### 2. A skill loads in three levels

A skill is a folder. The main file, `SKILL.md`, has a header (a name and a description) and a body (the manual). Next to it can be longer notes, scripts and templates.

::: figure 3-3-three-layers

The agent does not see all of it at once.

1. **Always, the name and description of every skill.** This is the menu. It is small, but it is paid for every turn, for every skill you have installed.
2. **When the request fits a description, the whole manual.** The agent decides this itself, or you type the skill's name.
3. **Only when the manual points to them, the extra files.** A long reference or a script is read at the step that needs it.

So you can install many skills without filling the window.

**The description decides whether the skill is ever found.** At level 1 the description is all the agent has. A vague one ("helps with code quality") never matches anything. A good description says three things: what the skill does, when to use it ("use when..."), and the words a person would actually say when they need it. The platform limits its length, and a wordy one costs room for every other skill too.

Even a good description does not guarantee use. VS Code's documentation says plainly that discovery makes skills available but does not guarantee the model uses one. So test it (below).

**A menu can grow too long.** With a few dozen skills, the menu is a real cost and many are never chosen. One answer is to keep the skills of a single business area out of the menu until the task is about that area.

### 3. One rule, one source

If the same rule is written in three files, a change misses one of them, and the agent reads three versions that slowly differ. Write a rule in one place. Other places hold a link and one sentence. A rule you have to restate everywhere is a sign the structure is wrong. Rule files are shared code, so give them an owner who cuts the lines that are no longer needed.

### 4. Why a written rule is ignored

A rule can be loaded and still not followed. The usual causes:

1. **The file is too long.** Ask of each line: would the agent get it wrong without it? If not, delete the line.
2. **Rules conflict.** Two files say different things. The model picks one, and not always the one you want. VS Code's docs say instruction sources are additive and that you should not depend on file order to settle a conflict. So conflicts are your job to remove: search for them, and fix the wording so only one version remains.
3. **The rule is far from where it applies.** It was in the first message, now thousands of lines up. A rule-by-file or a hook reminder puts it nearer.
4. **It has no reason.** "Never do X" is easy to rationalise away. "Never do X, because Y breaks" lets the model apply the idea to cases you did not list.
5. **It is a request.** This is the deepest cause. Whatever you write in a file is read by the model, and the model can do otherwise. The Claude Code docs put it plainly: the memory files are "context, not enforced configuration", and to block an action regardless of what the model decides, use a hook. The text of a skill is the same. It makes the work go smoothly; it does not make the wrong thing impossible. A skill's header may carry stronger settings on some platforms, and you should check what they do. In Claude Code, for example, `allowed-tools` only pre-approves tools and does not restrict them, and a skill can register hooks, which are code ([Skills](https://code.claude.com/docs/en/skills)).

For the fifth, the fix is not better wording. A rule that must hold goes into code. That choice is the subject of [A rule in a prompt is a request](4-1-requests-and-rules.html). The text then only has to explain why, so the agent does not try again to get around the refusal. In my setup a rule that matters has both layers: the text teaches, the code stops.

### 5. One more choice: language

If you work in more than one language, I keep one copy of the rules and skills, in English, and tell the model which language to answer in. A second copy of prose slowly drifts from the first. That is my choice; the principle is only to have one copy.

### Test your own setup

**Three questions for any rule you add:**

1. How often is this needed? If rarely, it does not go in the always-loaded file.
2. Is it already written somewhere? If so, link to it.
3. If the agent ignores it, what happens? If the answer is "something bad that cannot be undone", it is not a text job.

**A test you can run today, with no extra setup.** Look at your always-loaded file. For every line, ask whether the agent would get it wrong without it. Cut every line that fails. Then run the same task as before and see whether anything got worse. When I have cut lines from my own rules file, I usually saw nothing get worse. I have not tested this systematically.

**Test that a skill is found.** Write the requests first, in the words a person would use, not the words of the description: three ways of asking for the job, and two neighbouring requests that should not trigger it. Open a new chat for each (an old chat may already hold the skill) and do not type the skill's name. Then look at which skills were loaded. Use the platform's log if it has one, since what the agent says is not evidence. If it did not load, the description lacks the user's words. If it loaded when it should not, the description is too wide.

**Test that a skill changes anything.** Run the same task twice in new chats, with and without the skill. If you cannot see a difference, cut the lines that make none. The agent already knew them.

## Costs and traps {#costs-and-traps}

**Splitting has a price.** A rule in a skill is only read if the skill is found. A rule that matters but sits in a skill with a weak description may never be read. That is the cost of saving room. If missing it is costly, keep it in a place that loads.

**A skill is not a setting.** It depends on the model choosing it. The same request can load it once and not the next time.

**More skills, harder choice.** Even a good description may be confused with its neighbour. Keep each one narrow and say what it is not for.

**Hooks that inject text add up.** Each line is repeated on every message. The Claude Code docs suggest under about 200 lines for a project file; that is a rule of thumb, not a measured limit. Measure your own.

## What the industry says {#industry}
{status: industry}

- **VS Code** has the three-level loading for skills: it reads the name and description first, loads the body "once the skill is relevant", and reads other files "only when it references them". It also says that discovery "does not guarantee that it invokes a skill for every relevant prompt". For instruction files it advises to "keep your instructions short and self-contained", to "include the reasoning behind rules", and says the sources are "additive". ([Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions))
- **Anthropic** describes the same three levels for Agent Skills: the name and description first, the body when the skill applies, linked files only as needed. ([Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills))
- **Claude Code** suggests keeping each memory file under 200 lines, moving part-of-the-code rules into files that load only for matching paths, and removing contradictions. It treats them as "context, not enforced configuration". ([How Claude remembers your project](https://code.claude.com/docs/en/memory))

The two platforms use the same shape: always-on file, path-scoped rules, on-demand skills. The idea is the same across tools, so what you build here moves with you.

## When to delete it {#when-to-delete-it}
{status: industry}

The by-hand parts that the platform may take over: listing only the skills of the current area, and cutting a long menu. If the platform learns to load skills by relevance better, the area trick can go.

The reasoning does not retire. A bigger window does not make a long rule file better; it only lets you hold more before the problem shows up. And no loading scheme makes a written rule enforced. I would look again if a platform could show, on my own tasks, that long rule files are followed as well as short ones.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

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

Copilot Harness uses all three places, the three levels of loading, and the rule that a rule has one source. The harness can show you each with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Instructions and skills". Teach me how this harness uses the three places for rules, how its skills load in three levels, and why it says a skill is not enforced (topics 2, 3 and 15). Open the real files with me, starting from the shortest one.
:::

It teaches one small piece at a time and opens the files with you.
