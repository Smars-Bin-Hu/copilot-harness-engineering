This chapter follows [Learning in batches](8-4-kb-learning.html). It is step seven of the road, and it never ends. For why notes should carry a source and a date in general, see [What an agent should remember](3-5-memory.html); this chapter shows it for code.

## In one sentence {#in-one-sentence}

Knowledge goes stale. So each card records the commit it was read at, and when the code changes you can list the stale cards and fix only the lines that changed.

## For leaders {#for-leaders}

- **The decision:** name an owner for the knowledge base and agree how often stale notes are refreshed, and who may mark a note as checked.
- **The risk:** a base that was true once and is never checked can be worse than none, because people believe it. A stamp that says "checked" is only as good as the check before it. The list of stale notes misses the callers of a changed object; I have not tested how often that leaves a note wrong.
- **The cost of doing it right:** each refresh reads only what changed in the code, not the whole file, in tasks of at most about 20 notes. The list of stale notes costs no reading.
- **Ask the team:** "How many of our notes are older than the code they describe, and who is responsible for them?"

## The problem {#problem}

A team writes good cards in March. By June, a third of the files they came from have been changed. Nobody can say which cards are now wrong. So readers lose trust in all of them, and the base is ignored. A base that was true once and is never checked can be worse than none, because it is believed.

Two ways to deal with this fail. One is "rewrite everything now and then": it costs as much as the first build. The other is "hope people fix cards when they notice": they do not notice.

The fix is to make staleness *visible and cheap*. A card says exactly which version of the code it read, and then a script can answer "what has moved?". You can try the idea without any tool: write down the commit a note was read at, and later run `git diff <that commit>..HEAD -- <the file>`. If the diff is empty, the note's source has not changed.

## How it works {#how-it-works}

### The version on the card

Commits and shas were explained in [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html). The **object index** is the script-built list of every object and its source file.

Three places hold a version:

- **Every line of the object index** keeps the sha of the source file at the time the card was written.
- **Every card** carries a mark that says it was verified against the code, and at which commit it was read. The mark tells the reader whether the card was checked against code or not.
- **The domain** records the commit of each repository it was learned at.

### Listing the stale cards

A script compares the sha on each index line with the file on the base branch (the main line of the code) now. A card is **stale** when its source changed. A card whose source was deleted is listed too.

::: figure 8-5-stale-cards

Only the cards that changed need attention, so a small change in a big code base means a short list. The share of stale cards is also the number to put on a board. One gap to know about: the list names the cards whose own source changed, not the cards of their callers (see [Costs and traps](#costs-and-traps)).

### Refresh: read the diff, not the file

For each stale card the agent reads the **diff**: exactly what changed in the source since the card was written. That is cheaper than reading the file again, and it points at the lines of the card that may be wrong.

- If the change does not touch what the card says (a comment, formatting, a part the card does not cover), the text stays.
- If it does, the agent changes only the lines it touches.
- Then it **stamps** the card: it records that the card was checked against the code as it is now. A stamp is a claim, so it is only for cards the agent really checked. Stamping a card nobody read hides a wrong card until the next change.

A refresh is a task like any other: a plan listing each card and what is expected to change, a person's approval, then a write-back ([Two gates: where a person approves](5-3-two-approvals.html)). At most about 20 cards per task; for more, do the most used first.

**When a source is gone**, the agent looks for a rename first. If it was renamed, the path is updated. If it was removed, the agent asks a person whether to drop the card or keep it. A card that is kept is marked "source gone", and its mark becomes *unknown*, so it does not read like checked knowledge.

### What a finished task teaches

Cards also go wrong in another way: while doing a task, an agent finds that a card is wrong or missing. It notes this in the task's log as it works. When the task ends, a separate step (I call it **capture**) picks out what is worth keeping and **drafts** it for a person to approve. Nothing goes into the base by itself. "It will still be true next month" is only a prediction by the model, so the person's approval is the real check.

It keeps an item only if all of these hold: a future agent would get it wrong without it; the task holds the evidence (a file and line); it is not already recorded; and it will still be true next month. "Nothing here is worth keeping" is a good answer. The general rules for what to remember are in [What an agent should remember](3-5-memory.html).

### The requests list: what the code cannot tell

By my own guess (not a measurement), a small part of the base cannot come from code. It comes from people and from running systems. So each domain has a **requests list**: one row for each thing a person must give. A row has:

- a **kind**: *code* (a source that is in no repository), *runtime* (a value from one environment), *history* (something to find in git), or *decision* (a choice someone must make);
- a read-only command or query the person can run as it is;
- a **status**: *open*, *answered* (when, by whom, where it went), or *declined* (and then it is not asked again).

The agent asks at its next stop, never in the middle of work. Rows come from the places the map is blind ([8.3](8-3-kb-audit.html)): dynamic names, outside names, deleted sources.

What comes back goes into a second file of **environment facts**: one fact per row, such as whether a job is enabled or what a rule table holds. Each row has the environment, the date, the object, the sha of its code that day, and who gave it. When the code moves on, you can see that the fact was seen against older code. What a person pastes back is still untrusted text: it can hold dirty data or even instructions, so treat it as in [Text the agent reads can give it orders](4-6-untrusted-input.html).

### Bringing in a base you already have

If you already have notes about the code, they can be moved into this form. Set each sha to the commit the old notes were written at, not to today. Then the stale list is honest from the first day: it shows what changed since the notes were written. Old notes often do not say which commit they came from; then you must guess, and a wrong guess hides stale cards. Expect this to be harder than it sounds.

### Test your own setup

1. Take three cards. Write the commit each was read at.
2. Change one source file. List the cards whose source changed.
3. Refresh from the diff only. Count how many lines you read compared with the whole file (`git diff --stat` shows the lines changed; `wc -l` shows the file).
4. Add one row to a requests list, with a kind, a read-only query and a status.

## Costs and traps {#costs-and-traps}

- **Staleness is per source file.** If object A calls B and only B changes, B's card is listed, A's is not. A's card might need a change too if the meaning of the call moved. I have not tested how often this leaves a caller's card wrong. Cards that only point down and do not copy the lower card's content lose less. The map already knows who uses B, so a cheap fix is to list the callers of every stale card as "may be stale". I have not built or tested that.
- **A stamp can lie.** Its value is only as good as the check before it. Stamp only what you read. Decide who may stamp, and keep a record of who did. You can also have an independent reviewer re-read a few stamped cards against the code, as in the audit ([8.3](8-3-kb-audit.html)).
- **Someone must own the refresh.** The list shows what is stale. It does not fix anything by itself.
- **Declined requests are a loss, not a fix.** A declined row stays visible, so the gap is honest.
- **Capture can fill the base with noise.** The four conditions above are there to keep it small.

## When to delete it {#when-to-delete-it}

If a platform tracks which stored notes are older than the code they describe, use it, and drop your own comparison. The habit of recording a version with every fact still applies.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find the documents in this repository that describe the code (design notes, READMEs of modules, architecture pages, runbooks). For each, use git history to tell me when it was last changed and how many commits have touched the code it describes since then. Rank them from most to least out of date. Mark any that state no date or commit they were written against. Do not change any files.
:::

## Go deeper {#go-deeper}

- [What an agent should remember](3-5-memory.html): sources, dates and review for notes in general.
- [Learning in batches](8-4-kb-learning.html): where the cards come from.
- [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)

## Explore it in the harness {#explore}

Copilot Harness lists stale cards, refreshes them from the diff, drafts what a task taught, and keeps the requests list. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Keeping the knowledge base true". Teach me topic 16, part 16.7: how stale cards are found, how a refresh works, and what the requests file looks like. Open the refresh and capture skills with me.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.