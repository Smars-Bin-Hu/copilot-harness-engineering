This appendix is for the day something goes wrong. Find your symptom, do the first check, then read the chapter it points to. Everything here comes from the chapters and the harness docs, so each piece is advice I can point to. It is not a complete list of causes.

## How to use it {#how-to-use}

Two rules apply to almost every symptom.

- **Look at what happened, not at what the agent said.** The agent's account of its own work can be wrong, but a log can be checked ([Record what happened](6-1-observe.html)).
- **Change one thing, then run the same task again.** Otherwise you cannot tell which change helped ([Fixed tasks, scored by a script](6-3-eval-tasks.html)).

Find your symptom by what you see:

- A rule is not followed: [ignored](#rule-ignored), [dropped in a long chat](#rule-drift).
- A skill is not used: [never used](#skill-not-loaded).
- A hook is silent or too strict: [did not fire](#hook-silent), [refuses real work](#false-refusal).
- The agent will not stop, or stops badly: [goes in circles](#agent-loops), [says done too early](#done-too-early).
- The bill is high: [the bill](#bill).
- You cannot tell what happened: [no record](#cannot-tell).

## Rules and instructions {#rules}

### The agent ignores a rule {#rule-ignored}

**Check first.** Is the rule actually loaded? To find out, open a new chat and ask a question only your rules can answer ([A minimal harness](0-2-minimal-harness.html)). If it is loaded, go through the usual causes in order: the file is too long, two rules conflict, the rule sits far from where it applies, it gives no reason, or it is only a request. If the rule must hold, move it into code.

**Chapter.** [Instructions and skills](3-3-instructions-and-skills.html), section "Why a written rule is ignored", then [A rule in a prompt is a request](4-1-requests-and-rules.html).

### The rules file is long and getting worse {#rules-rot}

**Check first.** Ask of every line whether the agent would get it wrong without it. Cut the lines that fail, then run the same task and see whether anything got worse. Keep each rule in one place, too.

**Chapter.** [A minimal harness](0-2-minimal-harness.html), "How the starter set goes wrong", and [Instructions and skills](3-3-instructions-and-skills.html).

### A rule is followed in a short chat and dropped in a long one {#rule-drift}

**Check first.** Look at how far the rule now sits from the work. A rule written in the first message is far away after hours of work, so put it nearer by loading it from a file or having a hook repeat a few lines. A cheap test is to ask the agent, after an hour, to state the rule.

**Chapter.** [Long chats get worse](3-2-long-sessions.html) and [Instructions and skills](3-3-instructions-and-skills.html).

## Skills {#skills}

### A skill is never used {#skill-not-loaded}

**Check first.** Open a new chat, since an old one may already hold the skill, and ask in the words a person would use rather than typing the skill's name. Then look at which skills were loaded, using the platform's log if it has one. If the skill did not load, the description lacks the user's words. And if you have many skills, a neighbour may be taking the request, so keep each skill narrow and say what it is not for.

**Chapter.** [Instructions and skills](3-3-instructions-and-skills.html), "Three questions and three tests", and [A minimal harness](0-2-minimal-harness.html) (step 2).

### A skill loads when it should not {#skill-too-wide}

**Check first.** The description is too wide. Narrow it, then turn the neighbouring requests that must not trigger it into test cases.

**Chapter.** [Instructions and skills](3-3-instructions-and-skills.html).

### A skill loads but nothing changes {#skill-no-effect}

**Check first.** Run the same task twice in new chats, once with the skill and once without. If you see no difference, cut the lines that make none, since the agent already knew them. After that, check that the skill is not out of date.

**Chapter.** [Instructions and skills](3-3-instructions-and-skills.html) and [Skills as workflows](3-4-skills-and-workflows.html).

## Hooks and refusals {#hooks}

### The hook did not fire {#hook-silent}

**Check first.** Four things can keep a hook silent. They are what I found in October 2026, and they will change.

- The hook file is read when the window starts, so reload the window after a change.
- The hooks did not run when I used the command-line mode of Copilot.
- An organization policy can turn hooks off for a workspace.
- A setting that looks like an off switch may not stop them in newer sessions.

Then test with the smallest hook your platform allows, one that only appends the event name to a file.

**Chapter.** [Hooks](2-2-hooks.html), "What a hook cannot see" and "Three questions and a small test".

### The hook fired but the model did not get the message {#hook-lost-message}

**Check first.** Look at what the model really received, not at what the hook returned. In my case some prompts arrived without the rules, because the platform's own reminders took the slot the hook used (the numbers are in the chapter below).

**Chapter.** [Hooks](2-2-hooks.html), the story at the top.

### Every tool is refused after I changed the hook {#hook-wont-start}

**Check first.** If the hook program cannot start (for example, the interpreter is not found), Copilot treats that as a refusal, so no tool can run. All the screen says is that the hook errored. Run the hook command by hand in a terminal to see the real error.

**Chapter.** [A minimal harness](0-2-minimal-harness.html) and [Hooks](2-2-hooks.html), "Three ways a hook goes wrong".

### A hook that should have blocked a call let it through, with no notice {#hook-timeout}

**Check first.** Look at how long the hook takes. A hook that runs past its limit is treated as a pass, and nothing tells you so. Measure it and keep the hook cheap.

**Chapter.** [Hooks](2-2-hooks.html) and [Build the enforcement layer like software](4-4-enforcement-design.html), which is about deciding in advance whether a failure blocks or lets through.

### The agent keeps trying the same refused thing {#refusal-loop}

**Check first.** Read the refusal reason. A reason that only says "denied" makes the agent retry or try something worse, so rewrite it to say why and what to do instead. But do not explain how to dodge the rule.

**Chapter.** [Hooks](2-2-hooks.html) (the reason is part of the design) and [Asking is not a limit](4-2-ask-vs-refuse.html).

### A refusal blocks real work {#false-refusal}

**Check first.** The pattern is too wide. Because the agent cannot argue with a refusal, a false refusal is a stuck task. Narrow the pattern, keep a way for a person to approve what is wrong to refuse, and read the logs to see which rule fired.

**Chapter.** [A rule in a prompt is a request](4-1-requests-and-rules.html) and [Asking is not a limit](4-2-ask-vs-refuse.html).

### The agent got around a rule, or changed the rule files {#rule-bypassed}

**Check first.** Is the rule in a prompt or in a hook? If it is in a hook, does the hook see the text of the call, or its effect? A hook stops the common spellings, not an agent set on getting around it. Also check that the files holding the rules and the hook are on the guarded list. For things that must never be touched, do not give them to the agent at all.

**Chapter.** [Guard the files that hold the rules](4-3-guardrails.html) and [Some things you never hand over](4-5-least-privilege.html).

### The agent approved something for itself {#self-approval}

**Check first.** Test it by asking the agent to run the approval command, and check that it is refused. If the hook that refuses it was removed, edited or failed, an agent that can run commands could approve for itself.

**Chapter.** [Two gates: where a person approves](5-3-two-approvals.html).

## Loops, stops and cost {#loops}

### The agent goes in circles {#agent-loops}

**Check first.** Does anything outside the agent judge that it is stuck? Something should, because the agent itself is the worst judge of that. Put stop rules in code and have them judge from facts: a limit on turns and time, a limit on refusals, no progress over several rounds, a changed plan, checks used up. Also see whether it keeps trying something the guardrails block.

**Chapter.** [Unattended: when it must stop](5-7-when-to-stop.html).

### A stopped run left the person with a puzzle {#stop-vague}

**Check first.** Does the stop hand back, in one sentence, why it stopped, where it is, and what a person has to decide? "Ran into a problem" is not enough.

**Chapter.** [Unattended: when it must stop](5-7-when-to-stop.html), "What the person coming back should find".

### The agent says "done" and the tests fail {#done-too-early}

**Check first.** Did it run a check and show the command and its output? A claim of "all tests pass" tells you very little by itself. So give it a way to run the checks inside its loop, and let the run end on facts (steps ticked, a counted check passed) rather than on the agent's word.

**Chapter.** [Let the agent check its own work](5-4-self-checks.html) and [Unattended: when it must stop](5-7-when-to-stop.html), "When 'done' comes too early".

### Subagent usage does not add up {#subagent-usage}

**Check first.** A tool often shows the usage of the main conversation only. Check whether yours counts subagents too. Remember also that each subagent starts with an empty context and reads from zero, so several of them cost several times one agent. A limit on how many start is not a budget.

**Chapter.** [Use subagents sparingly](2-3-subagents.html), "What the extra cost bought, and what else it costs", and [Unattended: when it must stop](5-7-when-to-stop.html), section "A budget is a total, not a count".

### The bill is higher than expected {#bill}

**Check first.** Start with what the agent reads. Every turn rereads the whole context, so what is read matters more than how clever the model is. Look at tool results and loaded rules first, then at how often a task is redone. When you cut, stop short of the point where tasks fail and are thrown away. Check the usage numbers of one whole run, not one message. Cached context is billed at a lower rate (Anthropic's docs: about a tenth of the base price), though I have not verified that on Copilot, so look at what your own plan shows.

**Chapter.** [Don't pick a model by token price alone](1-1-models-and-cost.html), [The agent loop](2-1-agent-loop.html) and [Context is a budget](3-1-context-budget.html).

## Checks {#checks}

### The checks never pass {#checks-never-pass}

**Check first.** Read the findings. If each round brings new findings, the loop is open-ended, so use a limit and let the person extend or waive it. Findings that do not point to a real file and line are noise. If the verdict is wrong, a false FAIL sends the author to fix a problem that is not there. And if edits keep cancelling earlier passes, the fingerprint of the work may include too much, such as progress notes.

**Chapter.** [Make a pass count](5-5-counted-checks.html) and [Can a model check a model?](5-6-model-checks-model.html).

### Checks are on, but nothing was checked {#checks-silent}

**Check first.** The agent may simply never have called the checker, and then no FAIL is ever recorded. A rule in a prompt will not catch this. Put the check at a point the agent must pass, such as the moment it tries to stop.

**Chapter.** [Make a pass count](5-5-counted-checks.html), "Checks on, but nothing checked".

### A test passes sometimes and fails sometimes {#flaky}

**Check first.** A test that fails at random sends the agent hunting for a bug that is not there, or teaches it to rerun until green. Fix it or drop it. If the full suite is slow, give the agent a fast subset to run often.

**Chapter.** [Let the agent check its own work](5-4-self-checks.html).

### Two runs of the same task give different results {#variance}

**Check first.** That is normal. Run the task several times, look at the spread, and read the runs that failed. One run proves nothing. What is not normal is a spread so wide that no result can be trusted. When you see that, the task is too loose or the check is too weak, and that is what to fix first.

**Chapter.** [One run proves nothing](6-4-variance.html).

## Context and memory {#context}

### A long chat got worse {#long-chat}

**Check first.** Do not rely on the model to remember. Write what matters into a file, then start a fresh chat from that file. To test whether you did, ask what you would lose if this chat disappeared now. If chats get long because the task is too big, the fix is a smaller task.

**Chapter.** [Long chats get worse](3-2-long-sessions.html).

### The notes or memory file says something false {#notes-wrong}

**Check first.** Treat notes as the agent's report and check the ones that matter against the source. Keep the notes short and cut what is done, because a growing notes file fills the window. Memory that an agent writes should carry a source and a date, and a person should review it.

**Chapter.** [Long chats get worse](3-2-long-sessions.html) and [What an agent should remember](3-5-memory.html).

### The agent obeyed text it read in a file or a web page {#injection}

**Check first.** Count the three circles of risk: can it read private data, does it read untrusted text, and can it send data out? Remove any one of them. Keep in mind that a summary of untrusted text is untrusted too. Re-check whenever you add a tool.

**Chapter.** [Text the agent reads can give it orders](4-6-untrusted-input.html) and [MCP servers](1-3-mcp.html).

## Seeing what happened {#seeing}

### I cannot tell what the agent did {#cannot-tell}

**Check first.** Is there a record, written by code, of every call and every refusal? If there is, read the trace of a failed run, not the agent's summary. Even then, a hook sees only what the platform shows it, so a clean log can still have a hole.

**Chapter.** [Record what happened, not what the agent said](6-1-observe.html) and [A report a person can read in five minutes](6-2-task-report.html).

### A new model made things worse {#model-upgrade}

**Check first.** An upgrade is not better at every task, so rerun your fixed tasks. Then remove old rules and steps one at a time, running the evals after each.

**Chapter.** [When the model is upgraded, delete](6-5-model-upgrades.html).
