This chapter assumes you have read [Instructions and skills](3-3-instructions-and-skills.html): a skill is a manual that the agent reads when a job comes up.

## In one sentence {#in-one-sentence}

A good skill says how this job is done here and where it goes wrong, not what a textbook says. When a job with several steps has been done by hand about three times the same way, turn it into a workflow: the steps, the check on each, and which step needs a person.

## For leaders {#for-leaders}

- **The decision:** decide which routines the team repeats by hand and is ready to write down, and who owns each written skill or workflow.
- **The risk:** a skill that repeats what the agent already knows costs room and adds nothing. A written workflow runs the same way every time, including a wrong way, and it goes stale when how things are done here changes. I have no measured before-and-after for skills.
- **The cost of doing it right:** my rule of thumb is to write a routine down the third time it is done by hand (a number I chose, not tested). Designing and testing a workflow, and keeping it up to date, is the real price.
- **Ask the team:** "Which multi-step job have we done by hand three times, and where did the agent go wrong last time?"

## The problem {#problem}

The first skill most people write is a tutorial. "How to write a SQL query." "How to do a code review." The agent read a thousand tutorials like that while it was trained. Your skill adds nothing it did not know, and it costs room in the window each time it loads.

What the agent does not know is your place. Which table is the real one and which is a leftover. Which step people forget. Which file looks unused and is read by another team. That is what you know and it does not, and it is what is most worth putting in a skill.

Two words first.

- A **skill** is a manual for one kind of job (see [Instructions and skills](3-3-instructions-and-skills.html)).
- A **workflow** is a skill-sized idea one level up: a fixed order of several jobs, with a check after each and a note of where a person must decide. Think of a recipe card in a restaurant kitchen, as opposed to a cooking textbook. Careful: Anthropic uses the same word for something else, a system where code fixes the path and calls the model at set points ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). Here a workflow is a written routine that an agent follows.

I do not have a measured before-and-after to give you for skills. The reasoning below is what I follow, and the tests at the end let you measure it yourself.

## How it works {#how-it-works}

The difference in one picture:

::: figure 3-4-skill-vs-workflow

### 1. Write only what the agent would get wrong

For every line in a draft skill, ask: if I delete this, will the agent get something wrong or miss something? If not, delete it.

What stays:

- **Your conventions.** Naming, layering, where a new thing is registered.
- **Defaults that are not obvious.** The thing everyone on the team does without thinking about it.
- **Traps.** What looks right and is not.
- **Your tools.** The exact command, with the flag that matters.

What goes: how the language works, what a library does, anything on the first page of its documentation. Anthropic's own guide to writing skills gives a small example: a paragraph that explains what a PDF is and that you need a library to read one teaches the model what it already knows, while one line, "Use pdfplumber for text extraction", tells it the choice that was made. Their rule of thumb is "Default assumption: Claude is already very smart. Only add context Claude doesn't already have." ([Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

A skill with no such line is short. That is fine. A short skill is read whole and followed.

### 2. A skeleton to start from

A skill is a folder. The part that matters is one file, with a header and a body:

- **Header:** a name, and a description that says what it does, when to use it, and the words a person would say.
- **When to use it** (and when not to).
- **What it needs first.** For example, an open task, or a tool installed.
- **The steps**, if the job is a fixed process. For open-ended work, give the standards to judge by instead of fixed steps: a rigid recipe breaks when the case is a little different.
- **Gotchas.**

**Gotchas are the most valuable part.** They are warnings written ahead of time, one per line: the rule in bold, then the reason. Treat them as a living list: every time the agent gets this job wrong, add one line. That is the cheapest way to improve a skill, and it is the part that improves most with use.

Examples of the shape, from an "impact analysis" skill, which finds everything a change touches before the plan is written:

- A column named only by its bare name matches everything. Search the table and the column together.
- Names built at run time are not found by any text search. Say so in the result instead of reporting "no impact".
- No hit does not mean unused: readers outside the repositories you can see are invisible. Write that, and ask who else reads it.

None of these is in a textbook. Each is something that a competent agent gets wrong the first time. The third also shows a habit worth teaching: **the skill tells the agent to say what it could not see.**

**Scripts.** If part of the job has one right answer (find every file that mentions a name, count the uses), put it in a script the skill tells the agent to run. The script gives the same answer every time at no cost in reading; the model does the part that needs judgment. That skill does this: one command in place of a run of searches, then the model sorts the hits.

**Length.** When a skill grows past about 200 lines, move the detail into separate files and keep the main file as the flow and the links. The detail then loads only at the step that needs it.

### 3. Take it from real work, not from imagination

The best source of a skill is a job you have just done and corrected. Before you write, open the last real task of this kind and ask:

- Where did the agent go wrong? Each of those is a gotcha.
- Where did you correct it? Each of those is a convention.
- What did you have to look up that it could have been told?

Write the skill from those, not from what you think a good manual should say. I have a skill that does only this: at the end of a task, it drafts what a later agent would get wrong, with the evidence from the task, and a person decides what stays. [Memory](3-5-memory.html) covers why a person decides.

### 4. From skill to workflow

If you only write single skills, you can skip to "Test your own setup". The rest is for routines of many steps.

One job is a skill. A routine of several jobs is a workflow. "Every time we add a pipeline, we do these eight steps." If you do it by hand and the agent has to be told each time, that is the sign.

My rule of thumb: **the third time you do the same multi-step thing, stop and write it down.** One time is an accident. Two could be a coincidence. Three is a routine. I picked three myself; I have no test that shows it is the right number. A workflow pays when the routine comes back often and a missed step is costly. Against that stand the cost of designing it, testing it and keeping it up to date.

How to get a workflow without inventing it:

1. **Take two or three finished examples.** Real ones, already done by a person.
2. **Put them side by side** and replace each example's name with a placeholder. Parts that look the same in every example are the skeleton. Parts that change with the name are parameters. Parts that differ beyond the name are where judgment lives.
3. **Sort every step into one of four kinds**, asking in this order and stopping at the first yes:

   | Ask | If yes, it is | What to do |
   | --- | --- | --- |
   | Does it need authority (an approval, a production run, a protected file)? | **Human** | It stays with a person. |
   | Did the same inputs give the same result in the examples? | **Fixed** | A script can do it, with a test. |
   | Is it a check of a result? | **Check** | A script if a command can check it; otherwise a checklist for the model and an independent reviewer ([Use subagents sparingly](2-3-subagents.html)). |
   | Does it need to understand the requirement? | **Judgment** | The model's job, with a checklist, pointers to your documents, and the common mistakes. |
4. **Do not design from the description alone.** What people say they do and what the examples hold differ. That difference is the most useful finding. If you have no examples, say the design is a guess.
5. **Write it down for approval before building anything.** A workflow touches many files. A person approves the design first.

When unsure whether a step is fixed or judgment, choose judgment. Judgment can be turned into code later; code that was wrong about a judgment is harder to find.

### 5. What each step carries

A workflow is a chain, so each link says three things:

- **In:** what must be true before this step.
- **Out:** what exists after it, in a form the next step can read.
- **Check:** how it is known to be right. A command if possible.

And the steps that wait for a person say so. Two things to guard against. The workflow must not skip the approvals your setup already has. And it should leave room: write defaults and conditions ("skip when..."), not a fixed script, and say what to do when a case fits none of them.

If a workflow has more than about a dozen steps, or two different kinds of result, split it.

### 6. Two examples

**Impact analysis** (a skill with a script). Before a plan, find what a change touches. The script searches every repository for the names being changed. The skill makes the model sort the hits into must change, must check, and no effect, and requires a list of what the search cannot see. This is the case the [subagents chapter](2-3-subagents.html) mentions: once, in one case, a builder missed two references across areas, and only an independent check found them. It is one case, not a rate. A skill that does this search first moves that catch earlier.

**A test guide** (a workflow step that ends at a person). After a change is written back, the agent cannot run anything in the test environments; a person does. So the skill writes what to run in each environment, with expected results and what to send back. When the person brings the results, the skill judges them against the criteria written before. The point of the design is where it stops: at the person, with a clear list of what to do and what to bring back.

### Test your own setup

**Is it found, and does it change anything?** The two tests for a single skill are in [Instructions and skills](3-3-instructions-and-skills.html). Anthropic's guide adds one habit: build the test cases before you write much, from tasks the agent got wrong without the skill, then write just enough to fix them.

**Does the workflow hold?** Run it on a case that is not one of your examples. Where it fails is a missing variant or a step you sorted wrongly.

## Costs and traps {#costs-and-traps}

**A skill can go stale.** It states how things are done here, and here changes. A skill that says to use a command that no longer exists is worse than none. Look at each one when the thing it describes changes, and give each an owner.

**Wrong gotchas teach wrongly.** A gotcha written from a single case can mislead in the next. Keep the reason with the rule, so a reader can judge whether it still applies.

**Fixed steps cost flexibility.** A tight recipe is right for a fixed process and wrong for open work. If the agent follows your steps into a case they do not fit, they were too tight.

**A workflow can be wrong in a way nobody sees.** It runs the same way every time, including a wrong way. The checks are there for this; give each step one.

**What I did not measure.** I have not compared an agent with and without a given skill across many runs. The skill tests above are a first pass, not a measurement ([Run it several times](6-4-variance.html) says how to measure).

## What the industry says {#industry}
{status: industry}

VS Code's skills documentation describes the same format and the three-stage loading, and says to write instructions that are "clear" and "specific" with step-by-step procedures where they apply. It also says plainly that discovery does not guarantee a skill is used. ([Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)) Anthropic's skill-writing guide gives the same advice I follow: assume the model is already very smart and add only what it does not have, and challenge each paragraph with "Does this paragraph justify its token cost?". ([Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)) It also suggests building the test cases first and keeping the skill under about 500 lines; my own limit of about 200 is stricter and is a habit, not a measured value.

## When to delete it {#when-to-delete-it}
{status: industry}

A gotcha goes when the model stops making the mistake, or when the code makes it impossible. Check them when you change models: some may be dead weight, and a dead gotcha only takes room. A fixed step goes when the platform does it for you. A whole workflow goes when it has not run for a long time, or when the routine itself is gone.

What stays is the habit: after a real task, look at what the agent got wrong, and write that down in the place it will be read.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look through the recent git history of this repository for changes that repeat the same multi-step pattern (for example, adding a new module, a new endpoint or a new job, which touches the same set of places each time). List up to three such routines with the commits that show them. For each, say which steps looked identical every time, which varied with the name, and which needed a person's decision. Say which routine is worth writing down first. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- Anthropic: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- In this book: [Instructions and skills](3-3-instructions-and-skills.html), [Memory](3-5-memory.html), [Use subagents sparingly](2-3-subagents.html)

## Explore it in the harness {#explore}

Copilot Harness ships a skill that builds new skills, a skill that designs a workflow from examples, and the two examples above. The harness can open them with you. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Turn your way of working into skills". Teach me how this harness writes and tests skills (topic 3): open the skill that builds skills, then the workflow-design skill and the impact-analysis skill, and show me where their gotchas came from and how a skill is tested to be found.
:::

It teaches one small piece at a time and opens the files with you.