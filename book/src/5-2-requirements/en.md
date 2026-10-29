This chapter assumes you have used an AI coding agent. It builds on [Manage tasks, not chats](5-1-tasks.html): a task is one job with one folder of files.

## In one sentence {#in-one-sentence}

People's requests are vague and they shift. So have the agent write the requirement on one page, have the person confirm it, and from then on let everyone work from that page.

## For leaders {#for-leaders}

- **The decision:** for anything bigger than a small change, require a one-page requirement that the agent writes and the requester confirms before work starts.
- **The risk:** requests are vague, leave things out and shift over time. If the agent starts from the first message, every guess it makes is built into the result, and you only find out at the end. I have no numbers on how often this happens.
- **The cost of doing it right:** a few minutes of reading from the requester for each task. That is too much for a one-line change, so small tasks can skip it. Too many questions also wear people out, though I have not measured how many is too many.
- **Ask the team:** "Where is the page the requester confirmed, and what does its 'not clear yet' list say?"

## Why the words are not enough {#problem}

You write "add the customer region to the daily report", and the agent does it, yet the result is not what you meant. You meant the region of the shipping address, while the agent used the billing one. Neither of you was wrong about the words. The words were not enough.

This is the normal case, not the odd one. A request leaves things out, because you know the context and skip it, while the agent does not know it and fills the gap with a guess. Even what you do write can be read in more than one way, since "region" can mean several things. And the request does not hold still, because over a few turns you add a condition, drop another and change your mind. Which version, by then, is the request?

This is where the trap lies: if you let the agent start work from the first message, every guess is built into the result, and you find out only at the end. So before work starts, there has to be one thing everyone can point to.

What should that be? The tempting answer is the person's words, kept exactly as they said them. I tried to design that, and gave it up.

## From what was said to what was meant {#how-it-works}

### Why I do not keep the person's exact words

My first idea was to record every prompt, so that "what the person asked" would always be on disk. It fails for the reasons above: the words leave things out and are unclear. And because the requirement shifts over turns, neither the first prompt nor the last one on its own is the requirement. Keeping them all also fills the context ([Context is a budget](3-1-context-budget.html)) with chatter that the agent then has to sort out again.

So the exact words are not the requirement. The requirement is what the person *means*, written down so that they can check it.

### The agent writes it; the person confirms it

Someone has to do that writing, and here it is the agent. From the conversation, it writes the requirement as **one page**, and the person reads that page and confirms it. This is the **requirement file**, the one file every later step goes by.

::: figure 5-2-one-page

Why this order, and not "the person writes it"? Because people do not like writing specifications, and the page is much easier to check than to write. Reading "you will use the shipping address" and answering "yes" or "no, billing" is cheap, while producing the whole page from nothing is not. In this order each side does what it is good at. The agent turns a mess into a structure, and the person knows what they meant.

It also gives the confirmation a clear meaning. The person is not confirming "I understood you" but "this page is what I want".

### What goes on the page

Keep it to what the later steps need:

- **The goal:** what should be true when this is done.
- **What to do, and what not to do:** the scope and its limits.
- **Done when:** the checks that show it is finished, each one something a person or a program can verify.
- **Where each point came from:** the file and place in the sources, or the person's answer.
- **Not clear yet:** the open questions, kept as an honest list rather than a hidden guess.

Of these, "done when" matters most. The independent check ([Use subagents sparingly](2-3-subagents.html)) goes by this page alone, and so do the self-checks in [Let the agent check its own work](5-4-self-checks.html).

### How the agent asks

Where the conversation leaves gaps, the agent has to ask, but an agent that asks too much is as bad as one that guesses. The rules I give it come from my own use, and I have not tested them against other ways of asking.

1. **Stop before work.** While things are unclear, it only reads and changes nothing.
2. **Look up what can be looked up.** Which test framework the project uses is in the repository, so asking about it wastes the person's time.
3. **Ask only what cannot be looked up:** intent, preference, trade-offs, what counts as done.
4. **Give options and a recommendation.** "A, B or C; I suggest B because..." is easier to answer than "what do you want?". A recommendation is only advice, though. It does not count until the person confirms.
5. **Do not take a shrug as a yes.** "Whatever" is not a confirmation. Ask back once ("I will do X. Is that all right?") and write down that the person agreed to leave it to the agent.
6. **Ask in batches that follow dependencies:** upstream questions first, a few at a time.

The method is plain, but its point is the first rule: **the agent must not fill in with its own guess what the person did not say.** A default that looks obvious is where a guess goes wrong most easily.

### When the requirement is a pile of documents

Sometimes the request does not arrive as a message at all, but as a business paper, a spreadsheet of mappings and some emails. This section is only about that case. Giving such files to the agent as they are costs context and invites mistakes, because a Word file carries a cover page, a revision history and comments, while a spreadsheet has hidden sheets and colours that mean something. A binary file is not text at all.

So a program, not a model, turns them into plain text first. Word becomes Markdown and each sheet becomes a table in a text file, while the original is kept untouched. A short report lists what the program left out, such as hidden sheets or pictures. The conversion costs no tokens and should change no number. It can still lose meaning that sits in layout or colour, and we come back to that loss among the costs below. The person then trims the text and adds a short note on what the job is, and only then does the agent read it and write the one page.

Two rules keep the agent honest here. A number that looks wrong is quoted and asked about, never corrected. Two sources that disagree are a finding to report, not something for the agent to settle by itself. This is the same split as in [Who decides](5-9-who-decides.html), with a program for the fixed conversion and a model for the reading.

### Reviewing the page before work starts

Whichever way the page was written, it can be checked before any work starts. In my setup the agent compares it with what is known about the system, such as the knowledge base, an index of the code kept for the agent ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)). If you have no knowledge base, skip this step. Each problem it finds goes into the "not clear yet" list with the question, why it matters and the source. The agent then asks the person the few most blocking questions, puts each answer into the page, and repeats until the list is empty and the person confirms.

Two things guard against a bad review. The agent asks only where the documents contradict each other, are wrong, or do not match the system. It never asks the person to confirm what the documents clearly say. And the page has a confirmation line that is left to the person: only they fill it in.

### When the request changes

The request will change even after the page is confirmed, and when it does, the **page changes first**. The agent edits the requirement and adds a line to the change record, and only then touches the work. If the person's latest instruction conflicts with the page, a hook reminds the agent to bring the two in line before doing anything else.

Changing the page first matters because the plan stands on the confirmed requirement. In my setup, approving a plan is refused while the requirement is unconfirmed or has changed since it was confirmed ([Two gates](5-3-two-approvals.html)). So if the requirement changes after work has begun, the person confirms it again and approves the plan again. The work already done is checked again, not thrown away.

### Test it with a request that contradicts itself

To see how your own setup behaves, give the agent a short request with two sentences in conflict, for example one saying the report is daily and another saying it is weekly. Does the page it writes list the conflict under "not clear yet", or does it quietly pick one? If it picks one, the page is sounding sure about a guess.

## What the page costs, and where it can still go wrong {#costs-and-traps}

Is the page worth it? It costs the person a few minutes of reading. For a one-line change that is too much, so a small task can skip the page (the sizes are in [Manage tasks, not chats](5-1-tasks.html)).

You might think that once the person has confirmed the page, it must be right. It need not be: people confirm pages they only skimmed, so a page can be wrong and confirmed at once. A confirmation is not a proof. What the page does is make a misunderstanding visible earlier, nothing more.

The agent can also write a page that sounds sure, as in the test above. A good page has an honest "not clear yet" list, so on a complex request an empty list is a warning sign, not a good sign.

Questions, too, can become a chore if there are too many of them, or if they are about what could have been looked up, until the person starts answering "whatever". I have not measured how many questions is too many.

Finally, if the requirement came as documents, remember that colours, comments and pictures do not survive the conversion. The program's report says what was left out, so read it.

## What can shrink or go, and what stays {#when-to-delete-it}

Two parts of this can shrink or go as agents get better. One is the asking method, whose rules you can shorten as models ask better questions on their own. The other is the conversion program, which can go if agents come to read Word and Excel reliably, with the noise left out. I have not tested this.

What stays is the one page and the confirmation, because they are about the person, not the model.

## Try it on your own setup {#try-it}

::: prompt
Look at the most recent merged pull request or the latest few commits in this repository, together with any issue or ticket text they link to. Reconstruct the request as a one-page requirement: the goal, what was in and out of scope, what "done" would have meant, and where each point comes from. Then list what the request left out or left open, and what in the change shows that someone guessed. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Manage tasks, not chats](5-1-tasks.html): where the requirement file lives.
- [Two gates](5-3-two-approvals.html): a plan is approved against a confirmed requirement.
- [Let the agent check its own work](5-4-self-checks.html): the checks go by "done when".

## Explore it in the harness {#explore}

The requirement file, the asking method, the review of a requirement and the conversion of business files all run in Copilot Harness.

::: prompt
/harness-rookie-wondering I have read the chapter "The agent writes the requirement, the person confirms it". Teach me how this harness does it (topic 9, the requirement part, and topic 15 on why the exact words are not kept). Open a real requirement file with me, show how a change goes into it first, and draw how the pieces fit together.
:::
