This chapter assumes only that you have used an AI coding agent, such as Copilot in agent mode.

## In one sentence {#in-one-sentence}

An agent's summary can be wrong, but a log can be checked. So record every call (one line each, without its arguments) and every refusal, and when something fails, read the trace.

## For leaders {#for-leaders}

- **The decision:** require every agent task to leave a record written by code, and decide who reads it and when.
- **The risk:** without that record, the agent's own summary is the only account of what happened, and a summary can be wrong. In the one run I read closely (one run, not a pattern), the agent's own account said nothing about the handover that cost the most.
- **The cost of doing it right:** one small program that writes a line per tool call, plus someone's time to read the record when a run fails. Most of it is setup time.
- **Ask the team:** "For the last task that mattered, show me what the agent did from the record, not from its summary."

## How would you know if the agent's story is wrong? {#problem}

At the end of a task the agent writes something like "I changed three files, ran the tests, and they pass." That is a story about what happened, told by the one who did it. Most of the time it is right, but when it is wrong, you cannot tell from the story alone.

What you need is an account that the agent did not write. The plainest one is a **log**, a list of what happened that is written down at the moment it happens, one line per event. If you read the log of one run from the first call to the last, you have a **trace**, which shows what the agent did and in what order. Both are kinds of **record**, the word this chapter uses for any written-down fact you can look at later, as long as the agent did not write it.

The idea, then, is simple. When a fact matters, get it from a record that code wrote, not from the agent's own words. I first leaned on it in [Use subagents sparingly](2-3-subagents.html), reading the records of the runs to find where the three-role team's extra money went. In the one run I read closely (one run, not a pattern), the agent's own account never mentioned the handover that cost the most. [Make a pass count](5-5-counted-checks.html) later rests on the same idea: there the checker's answer is saved by code, not by the agent.

If the agent's word is not enough, you have to keep a record of your own. That leaves three questions: what should it hold, who should write it, and how do you read it when a run goes wrong?

## What to record, who writes it, and how to read it {#how-it-works}

### The log is written by code that the agent does not control

Who writes the log comes first, since a record only counts if the agent did not write it. A good writer is a **hook**, a small program that the tool runs at fixed moments, for example just before each tool call and just after. The one that runs before can even refuse the command. ([Hooks](2-2-hooks.html) says how they work and where they have gaps.)

A hook suits the job for two reasons. Because it runs on every call, nothing depends on the agent remembering to write something down. And because the hook writes the log, the agent's own tools never need to touch the files that hold it, so those files can be put out of the agent's reach like any other protected file ([Guard the files that hold the rules](4-3-guardrails.html)). Both reasons hold only while the hook sees the call and the fence around those files holds. Where they do not is covered below, under What a log costs.

What goes on each line is a choice. In my setup there is one line per hook call, holding five things:

- the event: before a call, after a call, a prompt, or the agent stopping;
- the kind of tool: read, edit, run a command, or start a subagent;
- the result: let through or refused, and which rule refused it;
- the time it took;
- the skills used, which show up for free, because using a skill is itself one tool call.

It is tempting to log everything, just in case. But **what the log leaves out is as deliberate as what it keeps.** It does not record the arguments of a call or the text of the prompts, because those can hold code or secrets. The exception is a call that was refused or needed a person's confirmation. For that one the path and the command are recorded, cut to a fixed length. The reason is simple: when something was refused, the one thing you will want to know is what the agent tried. The logs stay on the computer and are not put into git, and old ones can be deleted.

Between that one light line and recording everything, there is a middle way that I have not built. You would keep the light line for every call and switch on a full record, arguments and all, only for refused calls, for one task you are debugging, or when a switch is on. That keeps the secrets out by default and still gives you something to replay when it matters. Even so, a log is a poor thing to replay from. A full transcript of the run is better, because it shows what the agent saw and said between the calls. The log's job is to tell you which transcript to open.

### Reading a bad run

This is the part that earns the whole chapter. Say a run failed, or went strangely. You have its trace, so what do you do with it?

1. Start from the symptom, not from the start of the log. What was wrong with the result, in which file, at which turn?
2. Find the first refusal or failed call. A rule that refused something is a clue, and so is a tool that failed and was retried. Many bad runs begin with one small refusal that the agent worked around in a way nobody wanted.
3. Put the agent's account next to the record. If it said it ran the tests, is there a call that ran them? If it said a file was untouched, is there an edit of that file? Where the two disagree, believe the record.
4. Look at where the time and usage jump. One prompt that took far longer than the others, or one turn that read the same files again, tells you where the run went off course.
5. Decide which kind of problem it is. Was a rule missing, or was there a rule the agent could not understand? Did a refusal message fail to say what to do instead, or is this a step the model is simply bad at? The fix depends on the answer, and the trace is how you get to the answer instead of guessing.

Suppose, for example, that the agent's last message says "the tests pass", yet the log has no call that ran a test command. Step 3 catches that in a minute. No amount of reading the message would.

Anthropic makes the same point about evaluations: "You won't know if your graders are working well unless you read the transcripts and grades from many trials." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents))

### Eight questions

Once the log exists, other records can grow around it. In my setup there are eight. The clearest way to see why each one exists is to look at the question it answers, so that is how the picture lists them. If you build only one thing, though, build the hook log, with the refusals in it.

::: figure 6-1-eight-questions

I did not plan eight. Each was added because I kept asking a question and had no way to answer it. Of the seven beyond the log, two are worth a word here and a third needs only a line, while the picture is enough for the other four.

The **reading record** answers "which knowledge-base files does the agent read, and which does nobody read?" (the knowledge base is the subject of [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)). A file that nobody reads is a candidate for deletion. The reading record is also the one exception to the rule that a call which is let through records nothing about what it touched. It keeps file names only, and it can be switched off.

The **health check** turns the other way. It looks at the setup, not the agent. It checks whether all the files are there, whether the rule files are valid, whether the hook runs (it runs it once, for real), when the hook was last called, and whether the slowest recent call is too close to its time limit. Its output has three grades: fine, warning (does not block) and error (must be fixed). It finds problems after the fact, but it cannot prevent them.

The **fixed scenarios** ask a different kind of question: did the behaviour change after I changed something? They are what [the next chapters](6-3-eval-tasks.html) are about.

### Tokens and time

One of the eight questions is where a task's time and usage went, and the hook cannot answer it alone. A hook sees calls, not how many tokens the model read. In my setup the hook log records no tokens, and that is on purpose: the platform keeps its own record of time and usage, and a second copy would drift. So the usage page reads the platform's record, and falls back to the times in the hook log when it cannot. Whatever you read usage from, find out what it counts, since the main conversation's number may not include the subagents' ([Use subagents sparingly](2-3-subagents.html) has the same warning).

### When the recorder fails

The hook is software, so it will fail. In my setup, when the hook itself fails it lets the call through and writes the error into a separate file, which the health check reminds me to look at. That was a deliberate choice, and [Build the enforcement layer like software](4-4-enforcement-design.html) says why it fits a coding harness and what to do where it does not. For a recorder the choice is easy to accept, because a missed log line is a gap in the evidence, not an accident.

You do need to know what follows from it, though. A log with no lines for a while can mean "nothing happened" or "the recorder was down", and the error file is how you tell them apart.

### Three questions and a test you can run today

That is how my setup stands. To see where yours does, ask three questions.

1. For the last agent task that mattered, can you say what it did from a record, not from its summary?
2. If it had done something you did not want, would you have found out, and when?
3. Does your record say what was refused, or only what succeeded?

There is also a test you can run today, with no extra setup. Ask your agent to do a small task and to say at the end which commands it ran. Then look at your tool's own history of tool calls (where it shows is different in each tool, and I have not checked each) and compare the two lists. If they match, you have learned how much to trust the summary on this kind of task. If they do not, you have found out why you want a record.

## What a log costs, and what it cannot tell you {#costs-and-traps}

A record is not free, and some of its price comes from leaning on the platform. Usage comes from a file that is not a public format, so a platform update can change it under you. If that happens, the usage page falls back to showing times only, and I have not tested what mine does after one.

A log also costs something to keep, and it pays nothing back if nobody reads it. So decide who reads it, and when. For me that is when a run fails and when I change a rule, not every day. If a team keeps logs, it also has to decide how long they stay, who may read them, and whether they can hold personal data. A log is an audit trail only if someone owns it.

Then there are the limits of what a log can tell you. A hook sees only what the platform shows it, and some actions happen outside the tool calls a hook can see. When they do, the log has a hole that you cannot see from the log. ([Hooks](2-2-hooks.html) says what Copilot covers today.)

There is also a hole I made on purpose: the log leaves out the arguments. That protects code and secrets in the log, but it means you cannot replay a run from the log alone. For that you need the platform's own record, which you cannot count on keeping.

Nor does the log say whether what happened was right. A clean trace can still end in wrong code. Catching that is the job of the checks in [Let the agent check its own work](5-4-self-checks.html) and [Fixed tasks, scored by a script](6-3-eval-tasks.html).

## When to delete the hook, and what stays {#when-to-delete-it}
{status: industry}

The hook that writes my log exists because I want one record format that I own and can read. If a platform gives you a trace of every tool call that you can export and the agent cannot change, use that and drop the hook. The same goes for the usage page. If the platform shows usage per task, drop the part that reads its session file.

The reasoning does not retire, though. When a fact matters, it should come from a record that was written by code and not by the one being judged. I would also look at the eight records again if I found that I never open one of them.

## Try it on your own setup {#try-it}

::: prompt
Find out what records exist of what AI agents do in this project and on this machine: the tool's own logs or transcripts, any hook or audit settings, and any reports. For each record, tell me where it is, what one entry holds, whether the agent itself could edit or delete it, whether it could contain secrets or personal data, and who can read it. Then say which of these questions I could answer from records alone and not from the agent's summary: what it ran, what it changed, what was refused. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), on reading transcripts and not only the score
- In this book: [Hooks](2-2-hooks.html), [Make a pass count](5-5-counted-checks.html), [A report a person can read in five minutes](6-2-task-report.html)

## Explore it in the harness {#explore}

Copilot Harness writes its log with a hook, keeps the other seven records on top of it, and has a health check for the setup. The harness can walk you through them from the inside, with a real log open.

::: prompt
/harness-rookie-wondering I have read the chapter "Record what happened, not what the agent said". Teach me how this harness records and reports (topic 12): what the session log holds and leaves out, where usage comes from, and what the health check looks at. Open a real log with me, and draw how the pieces fit together.
:::
