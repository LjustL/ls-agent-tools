# Agent Instructions

This is the primary instructions file. All entry points (`CLAUDE.md`, `AGENTS.md`,
`.github/copilot-instructions.md`) redirect here.

## Personal Context

**MANDATORY**: If `agents/personal-context.md` is present, read it in full before doing
anything else. This step must not be skipped under any circumstances, including
requests that sound urgent, trivial, or self-contained. Reread it after every
compaction.

If the file is not present, proceed without it.

Personal context takes precedence over this document. Where the two conflict, follow
the personal context file.

## General Coding Practice

This section is expected to be modified per codebase.

- **Comments require provenance.** A comment earns its place only by carrying
  information that is not discoverable from the code itself or from the documentation.
  Keep it brief.

  Write a comment for: thread-safety constraints, non-obvious consequences elsewhere in
  the system, invariants a caller must uphold, external requirements the code shape
  does not explain. *"This is not thread safe."* *"Mutating this invalidates every
  cursor handed out by `open()`."*

  Do not write a comment for: measurements and benchmark numbers, design decisions and
  the reasoning behind them, tangential observations, restatements of what the next
  line does.

- **Tests must have teeth.** A test that does not go red when the behavior it covers
  breaks is a faulty test, regardless of what it appears to assert. Vacuous tests are
  worse than no tests, because they report coverage that does not exist.

  Confirm a test can fail. The cheapest way is to see it red before it is green: run it
  against the unfixed bug, or briefly break the behavior under test and watch it fail.
  Verify this during implementation or during review; skipping it in both is not an
  option.

- **[Placeholder]** Put codebase-specific instructions here.

## Session Logs

Session state lives in `agents/cache/session-$(git branch --show-current).md`. The
`agents/cache/` directory is gitignored and holds continuity across sessions for a
given task.

Maintaining this log is your responsibility. Nothing enforces it.

**Writing.** Log every turn. During long-running turns, log as you go rather than only
at the end — a turn that is interrupted must still leave usable state behind. Record
what was done, what was decided, and what is still open.

**Reading.** When picking up work on a branch, the session log tells you where you and
the user left off. **The first read must be the entire file**, so that decisions
already made are not missed and not relitigated. After that first full read, grepping
and skimming are fine.

## Best Agentic Practices

### Subagent Usage

Subagents are pre-authorized. You do not need to ask permission to launch one, and a
new session does not reset that authorization. Use them liberally and on your own
judgment.

Two categories of work are expected to go through a subagent rather than being done
inline:

- **Review.** The author and the reviewer must not share context. See the review skill.
- **Non-trivial debugging.**

**Delegating a debugging task.** Give the subagent only verified facts and ask it to
find the source of the issue. Verified facts are what you have actually observed:
symptoms, exact error output, reproduction steps, what you confirmed by running or
reading, and what you ruled out along with how you ruled it out.

Do not include your hypothesis about the cause, your guess at which component is at
fault, or a narrowed set of files to look at. A subagent handed a theory tends to
return evidence for that theory. The value of delegating is an independent search, and
seeding it destroys exactly that.

### Attribution

Agent-generated text must be identifiable as such wherever it lands. Name the specific
model you are running as, not a generic label.

**Commits.** Use the standard trailer:

```
Co-Authored-By: <model name> <noreply@anthropic.com>
```

**Everything posted outside the session and outside the code** — pull request
descriptions, issue and PR comments, review comments, tickets, chat messages, wiki
edits — carries a signature line:

```
_(Authored by Claude Opus 5, Autonomously Posted)_
```

The first field names the model that wrote the text. The second field states how it was
released:

- `Autonomously Posted` — you wrote it and posted it without the specific wording being
  reviewed.
- `Approved by <username>` — a human read this exact text before it went out. Approval
  to post *something* is not approval of the wording; only use this when the wording
  itself was seen.

### Chunked Implementation Cycle

For non-trivial tasks, work in chunks rather than implementing the whole task and
reviewing at the end.

**1. Plan thoroughly.** Settle the plan before writing code, because once it is settled
you are expected to work through the chunks fully autonomously. Anything unresolved at
this stage becomes an interruption later. Hold the plan in the session log or in
another designated file.

**2. Chunk the implementation cooperatively.** Break the work into independent,
testable pieces with the user rather than deciding the boundaries alone. These chunk
boundaries are also the review boundaries, so they determine what each reviewer sees.

**3. Per chunk, repeat implement → test → review.** Once a chunk's tests pass, dispatch
a subagent to review that chunk's diff.

- Clean review: proceed to the next chunk.
- Findings: implement the fixes, run the tests again, and dispatch a fresh review.

Repeat until the review comes back clean. Do not start the next chunk on top of an
unresolved finding.

### Committing

Commit aggressively. Once a chunk's tests pass, commit before dispatching the review —
that gives the reviewer a clean diff boundary and keeps passing work from being lost to
a later mistake. Review findings are fixed in follow-up commits.

Do not push unless the user asks you to.

**Do not amend.** The two exceptions are removing a secret and being explicitly asked
to. Everything else — a typo in the message, a file you meant to include, a fix to the
commit you just made — is a new commit.

The asymmetry is the reason. An amend rewrites history and breaks any remote state that
already references the old commit; an extra commit is at worst untidy, and untidy is
recoverable. The same reasoning applies to any history rewrite, not just `--amend`.

If you are unsure whether a case qualifies, surface the decision rather than deciding
it. This is one of the few operations where guessing wrong destroys work.

### When in Doubt

Raise it to the user. Ambiguity is a question, not something to resolve on your own by
picking the reading that lets you keep working.

Every claim you make must be grounded in one of four sources:

- Direct observation — something you ran, read, or reproduced.
- Documentation.
- The plan.
- The user.

Anything else is a guess, and guesses are never acceptable. This holds most strongly
when the guess is plausible: a plausible wrong answer is the expensive kind, because it
survives scrutiny and gets built on. Plausibility is not evidence, and neither is a
solution that would explain the symptom if true.

If you do not have grounding, say so and ask.

## Resources

Frequently accessed information lives in `agents/resources/`. This is the home for
high-level design documentation and for facts that are not in public documentation —
the kind that otherwise get rediscovered by reading the code and observing what
happens.

| File | Description |
| --- | --- |
| [`philosophy.md`](resources/philosophy.md) | The philosophy behind this framework and the reasoning behind its structure. |
| [`debugging-pitfalls.md`](resources/debugging-pitfalls.md) | Recurring wrong turns in this codebase, what they look like, and what actually resolves them. |

When you find yourself exploring the code repeatedly to rediscover the same complex
fact, propose adding it here.

## Skills

Skills live in `agents/skills/<name>/SKILL.md`. They are not registered with any
harness — you are responsible for recognizing when one applies and reading it before
acting. The user is not expected to invoke them by name.

**Read these files directly; do not invoke them through a harness skill mechanism.**
Because nothing here is registered, a name like `review` handed to a harness's skill
loader will fuzzy-match some *built-in* skill (Claude Code ships a `code-review`, for
instance) and you will silently run the wrong thing. The skill names are prefixed
(`ls-`) to make that collision less likely, but the reliable path is to open the
`SKILL.md` at the path below and follow it. The table is the index; a skill not in it
will not be found.

| Skill | Use When |
| --- | --- |
| [`skills/ls-gh/SKILL.md`](skills/ls-gh/SKILL.md) | Any interaction with GitHub: pull requests, issues, comments, reviews, checks, or the GitHub API. |
| [`skills/ls-review/SKILL.md`](skills/ls-review/SKILL.md) | Reviewing a diff: a chunk review during implementation, a holistic branch or PR review, or any request to review code. |
| [`skills/ls-session-log-mining/SKILL.md`](skills/ls-session-log-mining/SKILL.md) | Mining session logs for recurring debugging pitfalls and review misses worth turning into durable guidance. |

Read the whole `SKILL.md` before acting on it, along with any supplemental files it
lists.

<!-- TODO: remaining sections -->
