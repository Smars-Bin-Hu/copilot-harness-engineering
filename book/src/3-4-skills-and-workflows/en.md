This chapter assumes you have read [Instructions and skills](3-3-instructions-and-skills.html): a skill is a manual that the agent reads when a job comes up.

## In one sentence {#in-one-sentence}

A good skill says how this job is done here and where it goes wrong, not what a textbook says. When a job with several steps has been done by hand about three times the same way, turn it into a workflow: the steps, the check on each, and which step needs a person.

## For leaders {#for-leaders}

- **The decision:** decide which routines the team repeats by hand and is ready to write down, and who owns each skill or workflow once it is written.
- **The risk:** a skill that repeats what the agent already knows costs room and adds nothing. A written workflow runs the same way every time, even when that way is wrong, and it goes stale when the way things are done here changes. I have no measured before-and-after for skills.
- **The cost of doing it right:** my rule of thumb is to write a routine down the third time it is done by hand, a number I chose rather than tested. The real price is designing and testing the workflow, and then keeping it up to date.
- **Ask the team:** "Which multi-step job have we done by hand three times, and where did the agent go wrong last time?"

## What is worth putting in a skill? {#problem}

The first skill most people write is a tutorial, something like "How to write a SQL query" or "How to do a code review". But the agent read a thousand tutorials like that while it was trained. A skill of that kind adds nothing it did not know, yet it still costs room in the window each time it loads.

What the agent does not know is your place: which table is the real one and which is a leftover, which step people forget, which file looks unused but is read by another team. You know these things and the agent does not. That is what is most worth putting in a skill.

A **skill**, as [Instructions and skills](3-3-instructions-and-skills.html) described it, is a manual for one kind of job. Some of what you know, though, is not about one job but about how several jobs follow each other. For that there is a **workflow**, a skill-sized idea one level up: a fixed order of several jobs, with a check after each and a note of where a person must decide. Think of a recipe card in a restaurant kitchen, as opposed to a cooking textbook. Be careful with the word, because Anthropic uses it for something else, a system where code fixes the path and calls the model at set points ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). Here a workflow is a written routine that an agent follows.

I have no measured before-and-after for skills, only reasoning I follow and tests at the end of the next section that you can run yourself. So what does a skill look like when it holds only what is particular to your place?

## How to write a skill, and when it becomes a workflow {#how-it-works}

Before the details, here is the difference between the two in one picture:

::: figure 3-4-skill-vs-workflow

### 1. Write only what the agent would get wrong

Every line in a draft skill has to pass one question: if I delete this, will the agent get something wrong or miss something? If not, delete it.

The lines that pass tend to be of four kinds. Two are habits of the team: your conventions, such as naming, layering and where a new thing is registered, and the defaults that are not obvious, the things everyone does without thinking about them. The other two are traps, things that look right and are not, and your tools, meaning the exact command with the flag that matters.

What goes is how the language works, what a library does, or anything on the first page of its documentation. Anthropic's own guide to writing skills gives a small example. A paragraph that explains what a PDF is, and that you need a library to read one, teaches the model what it already knows, while one line, "Use pdfplumber for text extraction", tells it the choice that was made. Their rule of thumb is "Default assumption: Claude is already very smart. Only add context Claude doesn't already have." ([Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

A skill without those lines is short. That is fine, because a short skill is read whole and followed. Once a skill is cut down to these lines, the next question is how to lay them out.

### 2. A skeleton to start from

A skill is a folder, but the part that matters is one file with a header and a body. A skeleton for that file looks like this:

- A header: a name, and a description that says what the skill does, when to use it, and the words a person would say.
- When to use it, and when not to.
- What it needs first, for example an open task or a tool installed.
- The steps, if the job is a fixed process. For open-ended work, give the standards to judge by instead of fixed steps, because a rigid recipe breaks when the case is a little different.
- Gotchas.

Of these, **gotchas are the most valuable part.** They are warnings written ahead of time, one per line, with the rule in bold and then the reason. Treat them as a living list that grows by one line every time the agent gets this job wrong. It is the cheapest way to improve a skill, and also the part that improves most with use.

What does a gotcha look like? Here are a few from an "impact analysis" skill, which finds everything a change touches before the plan is written:

- A column named only by its bare name matches everything. Search the table and the column together.
- Names built at run time are not found by any text search. Say so in the result instead of reporting "no impact".
- No hit does not mean unused: readers outside the repositories you can see are invisible. Write that, and ask who else reads it.

None of these is in a textbook, yet each is something a competent agent gets wrong the first time. The third also shows a habit worth teaching: **the skill tells the agent to say what it could not see.**

Gotchas guard the parts of a job that need judgment. Other parts need none, because they have one right answer, such as finding every file that mentions a name or counting the uses. Put those in a script that the skill tells the agent to run. The script gives the same answer every time at no cost in reading, while the model does the part that needs judgment. The impact-analysis skill works this way, with one command in place of a run of searches before the model sorts the hits.

Length is the last thing to watch. When a skill grows past about 200 lines, move the detail into separate files and keep the main file as the flow and the links. The detail then loads only at the step that needs it.

### 3. Take it from real work, not from imagination

All of this assumes you know what the agent gets wrong. The best source for that is a job you have just done and corrected. Before you write, open the last real task of this kind and ask:

- Where did the agent go wrong? Each of those is a gotcha.
- Where did you correct it? Each of those is a convention.
- What did you have to look up that it could have been told?

Write the skill from the answers, not from what you think a good manual should say. I have a skill that does only this. At the end of a task, it drafts what a later agent would get wrong, with the evidence from the task, then leaves it to a person to decide what stays. [Memory](3-5-memory.html) covers why a person decides.

### 4. From skill to workflow

If you only write single skills, you can skip to "How to test a skill and a workflow". The rest is for routines of many steps.

One job is a skill, while a routine of several jobs is a workflow: "Every time we add a pipeline, we do these eight steps." If you do such a routine by hand and the agent has to be told each time, that is the sign it should become a workflow.

When is it time to write one? My rule of thumb: **the third time you do the same multi-step thing, stop and write it down.** One time is an accident and two could be a coincidence, but three is a routine. I picked three myself, without any test that shows it is the right number. A workflow pays when the routine comes back often and a missed step is costly. Against that stand the cost of designing it, testing it and keeping it up to date.

You also do not have to invent the workflow. It can be taken from work that has already been done:

1. Take two or three finished examples, real ones that a person has already done.
2. Put them side by side and replace each example's name with a placeholder. The parts that look the same in every example are the skeleton. The parts that change with the name are parameters, and the parts that differ beyond the name are where judgment lives.
3. Sort every step into one of four kinds, asking in this order and stopping at the first yes:

   | Ask | If yes, it is | What to do |
   | --- | --- | --- |
   | Does it need authority (an approval, a production run, a protected file)? | **Human** | It stays with a person. |
   | Did the same inputs give the same result in the examples? | **Fixed** | A script can do it, with a test. |
   | Is it a check of a result? | **Check** | A script if a command can check it; otherwise a checklist for the model and an independent reviewer ([Use subagents sparingly](2-3-subagents.html)). |
   | Does it need to understand the requirement? | **Judgment** | The model's job, with a checklist, pointers to your documents, and the common mistakes. |
4. Do not design from the description alone. What people say they do and what the examples hold differ, and that difference is the most useful finding. If you have no examples, say the design is a guess.
5. Write the design down for approval before building anything. A workflow touches many files, so a person approves the design first.

When you are unsure whether a step is fixed or judgment, choose judgment. Judgment can be turned into code later, but code that was wrong about a judgment is harder to find.

### 5. What each step carries

Because a workflow is a chain, each link says three things:

- **In:** what must be true before this step.
- **Out:** what exists after it, in a form the next step can read.
- **Check:** how it is known to be right. A command if possible.

A step that waits for a person says so as well. Once the steps are written, two things can still go wrong. One is skipping the approvals your setup already has. The workflow must not do that. The other is leaving no room. Write defaults and conditions ("skip when...") rather than a fixed script, and say what to do when a case fits none of them.

If a workflow has more than about a dozen steps, or two different kinds of result, split it.

### 6. Two examples

Two examples show how these pieces fit together. The first is the impact-analysis skill we met above, a skill with a script. Before a plan is written, its script searches every repository for the names being changed. The skill then has the model sort the hits into must change, must check and no effect, and requires a list of what the search cannot see. The [subagents chapter](2-3-subagents.html) tells of one case where the agent that made the changes missed two references across areas, and only an independent check found them. It is one case, not a rate, but a skill that does this search first moves that catch earlier.

The second, a test guide, is a workflow step that ends at a person. After a change has been written back to the real repository, the agent cannot run anything in the test environments; a person does. So the skill writes what to run in each environment, with expected results and what to send back. When the person brings the results, the skill judges them against the criteria written before. The point of the design is where it stops: at the person, with a clear list of what to do and what to bring back.

### How to test a skill and a workflow

Whether any of this works is something you can test. A single skill has two tests, whether it is found and whether it changes anything, both described in [Instructions and skills](3-3-instructions-and-skills.html). Anthropic's guide adds one habit: build the test cases before you write much, from tasks the agent got wrong without the skill, then write just enough to fix them.

A workflow, though, needs one more test, which is whether it holds. Run it on a case that is not one of your examples. Where it fails, you have found a missing variant or a step you sorted wrongly.

## What a written routine costs, and how it goes wrong {#costs-and-traps}

A skill that passes those tests can still go stale. It states how things are done here, and here changes. A skill that says to use a command that no longer exists is worse than none, so look at each one when the thing it describes changes, and give each an owner.

The gotchas themselves can be wrong, and a wrong gotcha teaches the agent wrongly. One written from a single case, for example, can mislead in the next. So keep the reason with the rule, where a reader can judge whether it still applies.

Fixed steps cost something too: flexibility. A tight recipe is right for a fixed process and wrong for open work. If the agent follows your steps into a case they do not fit, they were too tight.

A workflow can also be wrong in a way nobody sees, because it runs the same way every time, including a wrong way. That is what the checks are for, so give each step one.

As I said at the start, I have not compared an agent with and without a given skill across many runs, so the skill tests above are a first pass, not a measurement ([Run it several times](6-4-variance.html) says how to measure).

## Do the official guides agree? {#industry}
{status: industry}

On the main point, Anthropic's skill-writing guide does. It gives the same advice I follow: assume the model is already very smart, add only what it does not have, and challenge each paragraph with "Does this paragraph justify its token cost?". ([Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)) It also suggests building the test cases first and keeping the skill under about 500 lines. My own limit of about 200 is stricter, but it is a habit, not a measured value. VS Code's skills documentation, for its part, describes the same format and the three-stage loading. It asks for instructions that are "clear" and "specific", with step-by-step procedures where they apply. It also says plainly that discovery does not guarantee a skill is used. ([Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills))

## When to delete a gotcha, a step or a workflow {#when-to-delete-it}
{status: industry}

A gotcha goes when the model stops making the mistake, or when the code makes it impossible. So check them when you change models: some may have become dead weight, and a dead gotcha only takes room. A fixed step goes when the platform does it for you. A whole workflow goes when it has not run for a long time, or when the routine itself is gone.

What stays is the habit: after a real task, look at what the agent got wrong, and write that down in the place it will be read.

## Try it on your own setup {#try-it}

::: prompt
Look through the recent git history of this repository for changes that repeat the same multi-step pattern (for example, adding a new module, a new endpoint or a new job, which touches the same set of places each time). List up to three such routines with the commits that show them. For each, say which steps looked identical every time, which varied with the name, and which needed a person's decision. Say which routine is worth writing down first. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- Anthropic: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- In this book: [Instructions and skills](3-3-instructions-and-skills.html), [Memory](3-5-memory.html), [Use subagents sparingly](2-3-subagents.html)

## Explore it in the harness {#explore}

Copilot Harness ships a skill that builds new skills, a skill that designs a workflow from examples, and the two examples above. The harness can open them with you.

::: prompt
/harness-rookie-wondering I have read the chapter "Turn your way of working into skills". Teach me how this harness writes and tests skills (topic 3): open the skill that builds skills, then the workflow-design skill and the impact-analysis skill, and show me where their gotchas came from and how a skill is tested to be found.
:::
