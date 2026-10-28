This chapter assumes you have used an AI coding agent, such as Copilot in agent mode. Nothing else.

## In one sentence {#in-one-sentence}

An agent's summary can be wrong; a log can be checked. Record every call (one line each, without its arguments) and every refusal, and when something fails, read the trace.

## For leaders {#for-leaders}

- **The decision:** require that every agent task leaves a record written by code, and decide who reads it and when.
- **The risk:** the agent's own summary is then the only account of what happened, and a summary can be wrong. In the one run I read closely (one run, not a pattern), the agent's own account said nothing about the handover that cost the most.
- **The cost of doing it right:** one small program that writes a line per tool call, plus someone's time to read the record when a run fails. Mostly setup time.
- **Ask the team:** "For the last task that mattered, show me what the agent did from the record, not from its summary."

## The problem {#problem}

At the end of a task the agent writes something like: "I changed three files, ran the tests, and they pass." That is a story about what happened, told by the one who did it. Most of the time it is right. When it is wrong, you cannot tell from the story alone.

Three words first.

- A **log** is a list of what happened, written down at the moment it happened, one line per event.
- A **trace** is the log of one run, read from the first call to the last: what the agent did, in order.
- A **record** is any such written-down fact that you can look at later. In this chapter, "record" means something the agent did not write.

The idea is simple. When a fact matters, get it from a record that code wrote, not from the agent's own words. I used this idea first in [Use subagents sparingly](2-3-subagents.html). There I read the records of the runs to see where the extra money in the three-role team went. In the one run I read closely (so this is one run, not a pattern), the agent's own account said nothing about the handover that cost the most. And a later chapter, [Make a pass count](5-5-counted-checks.html), rests on the same thing: the checker's answer is saved by code, not by the agent.

So the question is what to record, who writes it, and how to read it when a run goes wrong.

## How it works {#how-it-works}

### The log is written by code that the agent does not control

A **hook** is a small program that the tool runs at fixed moments, for example just before each tool call, where it can refuse a command before it runs, and just after. ([Hooks](2-2-hooks.html) says how they work and where they have gaps.) A hook is a good place to write the log, for two reasons. It runs on every call, so nothing depends on the agent remembering to write something down. And the agent's tools do not write the log, the hook does; the files that hold it can be put out of the agent's reach like any other protected file ([Guard the files that hold the rules](4-3-guardrails.html)). This holds only while the hook sees the call and the fence holds. See the gaps in Costs below.

What each line holds is a choice. In my setup there is one line per hook call:

- **The event:** before a call, after a call, a prompt, the agent stopping.
- **The kind of tool:** read, edit, run a command, start a subagent.
- **The result:** let through, or refused, and which rule refused it.
- **The time it took.**
- **The skills used.** Using a skill is one tool call, so it shows up for free.

**What the log leaves out is as deliberate as what it keeps.** It does not record the arguments of a call or the text of the prompts, because those can hold code or secrets. The exception is a call that was refused or needed a person's confirmation: for that one, the path and the command are recorded, cut to a fixed length. The reason is simple. When something was refused, the one thing you will want to know is what the agent tried. The logs stay on the computer and are not put into git. Old ones can be deleted.

There is a middle way that I have not built: keep the light line for every call, and switch on a full record (arguments and all) only for refused calls, for one task you are debugging, or when a switch is on. That keeps the secrets out by default and still gives you something to replay when it matters. A full transcript of the run is better than any log for this, because it shows what the agent saw and said between the calls; the log tells you which transcript to open.

### Reading a bad run

This is the part that earns the whole chapter. A run failed, or went strangely. You have the trace. What do you do with it?

1. **Start from the symptom, not from the start of the log.** What was wrong with the result? Which file, which turn?
2. **Find the first refusal or failed call.** A rule that refused something is a clue. A tool that failed and was retried is another. Many bad runs begin with one small refusal that the agent worked around in a way nobody wanted.
3. **Put the agent's account next to the record.** Did it say it ran the tests? Is there a call that ran them? Did it say a file was untouched? Is there an edit of that file? Where the two disagree, believe the record.
4. **Look at where the time and usage jump.** One prompt that took far longer than the others, or one turn that read the same files again, tells you where the run went off course.
5. **Decide which kind of problem it is.** A missing rule? A rule the agent could not understand? A refusal message that did not say what to do instead? A step the model is simply bad at? The fix depends on the answer, and a trace is how you get to the answer instead of guessing.

For example, suppose the agent's last message says "the tests pass", and the log has no call that ran a test command. Step 3 catches that in a minute, and no amount of reading the message would.

Anthropic makes the same point about evaluations: "You won't know if your graders are working well unless you read the transcripts and grades from many trials." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents))

### Eight questions

Once the log exists, other records can grow around it. In my setup there are eight, and the clearest way to see why is to list the question each one answers. If you build only one thing, build the hook log, with the refusals in it.

::: figure 6-1-eight-questions

I did not plan eight. Each was added because I kept asking the question and had no way to answer it. Two are worth a word, and the third is one line.

- **The reading record** (of the knowledge base, see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)) answers "which knowledge-base files does the agent read, and which does nobody read?" It is the one exception to "a call that is let through records nothing about what it touched": it keeps file names only, and it can be switched off. A file that nobody reads is a candidate for deletion.
- **The health check** is the odd one. It does not look at the agent. It looks at the setup: are all the files there, are the rule files valid, does the hook run (it runs it once, for real), when was it last called, and is the slowest recent call too close to its time limit? Its output has three grades: fine, warning (does not block), error (must be fixed). It finds problems after the fact; it cannot prevent them.
- **The fixed scenarios** answer "did the behaviour change after I changed something?" That is [the next chapters](6-3-eval-tasks.html). The other four records are listed in the picture.

### Tokens and time

A hook sees calls, not how many tokens the model read. In my setup the hook log records no tokens, on purpose: the platform keeps its own record of time and usage, and a second copy would drift. The page that shows where a task's time and usage went reads that platform record, and falls back to times from the hook log when it cannot. Whatever you read usage from, find out what it counts: the main conversation's number may not include the subagents' ([Use subagents sparingly](2-3-subagents.html) has the same warning).

### When the recorder fails

The hook is software, and it will fail. In my setup, when the hook itself fails it lets the call through and writes the error into a separate file; the health check reminds me to look. That was a deliberate choice, and [Build the enforcement layer like software](4-4-enforcement-design.html) says why it fits a coding harness and what to do where it does not. For a recorder it is easy to accept: a missed log line is a gap in the evidence, not an accident. But know it: a log with no lines in a period can mean "nothing happened" or "the recorder was down". The error file is how you tell them apart.

### Test your own setup

**Three questions:**

1. For the last agent task that mattered, can you say what it did from a record, not from its summary?
2. If it had done something you did not want, would you have found out, and when?
3. Does your record say what was refused, or only what succeeded?

**A test you can run today, with no extra setup.** Ask your agent to do a small task and to say at the end which commands it ran. Then look at your tool's own history of tool calls (where it shows is different in each tool, and I have not checked each). Compare the two lists. If they match, you have learned how much to trust the summary on this kind of task. If they do not, you have found out why you want a record.

## Costs and traps {#costs-and-traps}

**Usage comes from a file that is not a public format.** It may change under you, and then the page shows times only. This is a dependency on the platform: an update can make your usage numbers stop working, and I have not tested what mine does after one.

**A log nobody reads is a cost with no benefit.** Decide who reads it, and when. For me it is: when a run fails, and when I change a rule. Not every day. If a team keeps logs, also decide how long they stay, who may read them, and whether they can hold personal data. A log is an audit trail only if someone owns it.

**A hook sees only what the platform shows it.** Some actions happen outside the tool calls a hook can see. Then the log has a hole you cannot see from the log. ([Hooks](2-2-hooks.html) says what Copilot covers today.)

**Leaving out arguments is a trade.** It protects code and secrets in the log. The price is that you cannot replay a run from the log alone. For that you need the platform's own record, which you cannot count on keeping.

**The log shows what happened, not whether it was right.** A clean trace can still end in wrong code. That is what the checks in [Let the agent check its own work](5-4-self-checks.html) and [Fixed tasks, scored by a script](6-3-eval-tasks.html) are for.

## When to delete it {#when-to-delete-it}
{status: industry}

The hook that writes my log exists because I want one record format that I own and can read. If a platform gives you a trace of every tool call that you can export and the agent cannot change, use that and drop the hook. The same goes for the usage page: if the platform shows usage per task, drop the part that reads its session file.

The reasoning does not retire. When a fact matters, it should come from a record that was written by code and not by the one being judged. I would look again at the eight records if I found that I never open one of them.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find out what records exist of what AI agents do in this project and on this machine: the tool's own logs or transcripts, any hook or audit settings, and any reports. For each record, tell me where it is, what one entry holds, whether the agent itself could edit or delete it, whether it could contain secrets or personal data, and who can read it. Then say which of these questions I could answer from records alone and not from the agent's summary: what it ran, what it changed, what was refused. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), on reading transcripts and not only the score
- In this book: [Hooks](2-2-hooks.html), [Make a pass count](5-5-counted-checks.html), [A report a person can read in five minutes](6-2-task-report.html)

## Explore it in the harness {#explore}

Copilot Harness writes the log with a hook, keeps the other seven records on top of it, and has a health check for the setup. The harness can show them to you from the inside, with a real log. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Record what happened, not what the agent said". Teach me how this harness records and reports (topic 12): what the session log holds and leaves out, where usage comes from, and what the health check looks at. Open a real log with me, and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.