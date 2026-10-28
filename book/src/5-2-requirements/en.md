This chapter assumes you have used an AI coding agent. It builds on [Manage tasks, not chats](5-1-tasks.html): a task is one job with one folder of files.

## In one sentence {#in-one-sentence}

People's requests are vague and they shift. Have the agent write the requirement on one page and the person confirm that page; everyone then works from it.

## For leaders {#for-leaders}

- **The decision:** require, for anything bigger than a small change, a one-page requirement that the agent writes and the requester confirms before work starts.
- **The risk:** requests are vague, leave things out and shift over time. If the agent starts from the first message, every guess is built into the result and you find out at the end. I have no numbers on how often this happens.
- **The cost of doing it right:** a few minutes of reading from the requester per task. For a one-line change it is too much, so small tasks can skip it. Too many questions also wear people out, and I have not measured how many is too many.
- **Ask the team:** "Where is the page the requester confirmed, and what does its 'not clear yet' list say?"

## The problem {#problem}

You write: "add the customer region to the daily report." The agent does it. It is not what you meant. You meant the region of the shipping address; it used the billing one. Neither of you was wrong about the words. The words were not enough.

This is the normal case, not the odd one. A request to an agent has three weaknesses:

- **It leaves things out.** You know the context, so you skip it. The agent does not know it, and it fills the gap with a guess.
- **It is read in more than one way.** "Region" can mean several things.
- **It changes.** Over a few turns you add a condition, drop another, change your mind. Which version is the request?

Here is the trap. If you let the agent start work from the first message, every guess is built into the result, and you find out at the end.

So the question is what the whole job should go by. The tempting answer is: the person's words, kept exactly. I tried to design that, and gave it up.

## How it works {#how-it-works}

### Why I do not keep the person's exact words

My first idea was to record every prompt, so that "what the person asked" is always on disk. It fails for the reasons above. The words leave things out and are unclear. The requirement shifts over turns, so the first prompt is not it and the last prompt alone is not it either. Keeping them all also fills the context ([Context is a budget](3-1-context-budget.html)) with chatter that the agent then has to sort out again.

So the exact words are not the requirement. The requirement is what the person *means*, written down so that they can check it.

### The agent writes it; the person confirms it

The agent writes the requirement from the conversation, as **one page**. The person reads that page and confirms it. This is the **requirement file**, the one file every later step goes by.

::: figure 5-2-one-page

Why this order, and not "the person writes it"? Because people do not like writing specifications, and the page is much easier to check than to write. Reading "you will use the shipping address" and saying "yes" or "no, billing" is cheap. Producing the whole page from nothing is not. It uses what the agent is good at (turning a mess into a structure) and what the person is good at (knowing what they meant).

It also gives the confirmation a clear meaning. The person is not confirming "I understood you". They are confirming "this page is what I want".

### What goes on the page

Keep it to what the later steps need:

- **The goal:** what should be true when this is done.
- **What to do, and what not to do:** the scope and its limits.
- **Done when:** the checks that show it is finished, each one something a person or a program can verify.
- **Where each point came from:** the file and place in the sources, or the person's answer.
- **Not clear yet:** the open questions. This is an honest list, not a hidden guess.

"Done when" matters most. The independent check ([Use subagents sparingly](2-3-subagents.html)) goes by this page alone, and so do the self-checks in [Let the agent check its own work](5-4-self-checks.html).

### How the agent asks

An agent that asks too much is as bad as one that guesses. The rules I give it come from my own use; I have not tested them against other ways of asking:

1. **Stop before work.** While things are unclear it only reads. It changes nothing.
2. **Look up what can be looked up.** Which test framework the project uses is in the repository. Asking about it wastes the person's time.
3. **Ask only what cannot be looked up:** intent, preference, trade-offs, what counts as done.
4. **Give options and a recommendation.** "A, B or C; I suggest B because..." is easier to answer than "what do you want?". A recommendation is advice; it does not count until the person confirms.
5. **Do not take a shrug as a yes.** "Whatever" is not a confirmation. Ask back once: "I will do X. Is that all right?" and write down that the person agreed to leave it to the agent.
6. **Ask in batches that follow dependencies.** Upstream questions first, a few at a time.

The method is plain, and the point is the first rule: **the agent must not fill in with its own guess what the person did not say.** The default that looks obvious is where a guess goes wrong most easily.

### When the requirement is a pile of documents

This part matters only when the request comes as business documents.

Sometimes the request is a business paper, a spreadsheet of mappings and some emails. Giving these to the agent as they are costs context and invites mistakes: a Word file carries a cover page, a revision history and comments; a spreadsheet has hidden sheets and colours that mean something. A binary file is not text at all.

So a program, not a model, turns them into plain text first. Word becomes Markdown; each sheet becomes a table in a text file. The original is kept untouched, and a short report lists what the program left out, such as hidden sheets or pictures. This costs no tokens, and it should change no number, though it can lose meaning that sits in layout or colour (see Costs). The person trims the text and adds a short note on what the job is. Then the agent reads that and writes the one page.

Two rules keep the agent honest here. A number that looks wrong is quoted and asked about, never corrected. Two sources that disagree are a finding to report, not something to settle by itself. This is the same split as [Who decides](5-9-who-decides.html): a program for the fixed conversion, a model for the reading.

### The review of the requirement

Once the page exists, it can be checked before any work starts. In my setup the agent compares it with what is known about the system, such as the knowledge base (an index of the code kept for the agent, [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html); skip this step if you have none), and writes each problem into the "not clear yet" list: the question, why it matters, and the source. It asks the person the few most blocking questions, puts each answer into the page, and repeats until the list is empty and the person confirms.

Two things guard against a bad review. The agent asks only where the documents contradict each other, are wrong, or do not match the system. It does not ask the person to confirm what the documents clearly say. And it leaves the confirmation line to the person: only they fill it in.

### When the request changes

It will change. The rule is that the **page changes first**. The agent edits the requirement, adds a line to the change record, and only then touches the work. If the person's latest instruction conflicts with the page, a hook reminds the agent to bring them in line before doing anything.

A plan stands on a confirmed requirement. In my setup, approving a plan is refused while the requirement is unconfirmed or has changed since ([Two gates](5-3-two-approvals.html)). If the requirement changes after work began, the person confirms it again, approves the plan again, and the work already done is checked again, not thrown away.

### Test your own setup

Give the agent a short request with two sentences that contradict each other, for example one that says the report is daily and one that says it is weekly. See whether the page it writes lists the conflict under "not clear yet", or quietly picks one. If it picks one, the page is sounding sure about a guess.

## Costs and traps {#costs-and-traps}

- **It costs the person a few minutes of reading.** For a one-line change this is too much. A small task can skip the page; see the sizes in [Manage tasks, not chats](5-1-tasks.html).
- **A confirmation is not a proof.** People confirm pages they skimmed. The page can be wrong and confirmed. It makes the misunderstanding visible earlier, nothing more.
- **The agent can write a page that sounds sure.** A good page has an honest "not clear yet" list. An empty list on a complex request is a warning sign, not a good sign.
- **Questions can become a chore.** Too many, or questions about what could be looked up, and the person starts answering "whatever". I have not measured how many questions is too many.
- **Conversion drops things.** Colours, comments and pictures do not survive. The report says what was left out; read it.

## When to delete it {#when-to-delete-it}

- **The asking method.** As models ask better questions on their own, shorten the rules for asking. Keep the one page and the confirmation: they are about the person, not the model.
- **The conversion program.** If agents read Word and Excel reliably, with the noise left out, the program can go. I have not tested this.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look at the most recent merged pull request or the latest few commits in this repository, together with any issue or ticket text they link to. Reconstruct the request as a one-page requirement: the goal, what was in and out of scope, what "done" would have meant, and where each point comes from. Then list what the request left out or left open, and what in the change shows that someone guessed. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Manage tasks, not chats](5-1-tasks.html): where the requirement file lives.
- [Two gates](5-3-two-approvals.html): a plan is approved against a confirmed requirement.
- [Let the agent check its own work](5-4-self-checks.html): the checks go by "done when".

## Explore it in the harness {#explore}

The requirement file, the asking method, the review of a requirement and the conversion of business files all run in Copilot Harness. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "The agent writes the requirement, the person confirms it". Teach me how this harness does it (topic 9, the requirement part, and topic 15 on why the exact words are not kept). Open a real requirement file with me, show how a change goes into it first, and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.