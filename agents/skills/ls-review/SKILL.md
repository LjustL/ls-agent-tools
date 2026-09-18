# Skill: Review

**Use when:** reviewing a diff — a chunk review during the implementation cycle, a
holistic review of a branch or PR, or any request to review code.

## Fresh eyes are required

The author and the reviewer must not share context. If you wrote the code, you do not
review it — dispatch a subagent.

Give the reviewer the scope to review and nothing else. Do not pass along your intent,
your reasoning, or a summary of what you believe the change does. A reviewer told what
the code is supposed to do will read the code as confirmation of that description; the
whole value of the review is that someone reads what is actually there.

The reviewer works from the diff, the surrounding code it can read, and the
instructions. Not from the author's account of the change.

## Pick the scope

Holistic review and mid-implementation review are the same procedure. Only the diff
differs.

| Situation | Scope |
| --- | --- |
| Chunk just committed | `HEAD~1` |
| Uncommitted work in progress | `HEAD` (the default) |
| Several commits | `HEAD~3..HEAD`, or the explicit range |
| A branch, holistically | `main...HEAD` |
| A pull request | `gh pr diff <n>` piped in |

## Procedure

**1. Determine which checks apply.**

```
agents/skills/ls-review/match_checks.py                  # working tree against HEAD
agents/skills/ls-review/match_checks.py HEAD~1           # one commit
agents/skills/ls-review/match_checks.py main...HEAD      # a branch
gh pr diff 123 | agents/skills/ls-review/match_checks.py # a PR, or any diff on stdin
```

The script matches changed file paths against each check's `triggers` and prints the
checks that fired, each with its `applies-when` text. It prints the `applies-when`
only, never the check body.

**2. Decide applicability from `applies-when`, then read.**

A trigger firing means *consider* the check, not that it applies. `applies-when`
describes the situation the check is written for; compare it to what the diff actually
does. If it applies, read that check file in full and follow it. If it does not, skip
it and say which you skipped and why — a silently dropped check is indistinguishable
from one that passed.

**3. Run the baseline pass regardless of which checks fired.**

Triggered checks are specialized knowledge layered on top of a normal review, not a
replacement for one. A diff that triggers no checks still gets reviewed. The baseline
covers correctness — logic errors, unhandled cases, broken assumptions, resource and
lifetime problems, concurrency — and the rules in the General Coding Practice section
of `agents/agent-instructions.md`, which review is responsible for enforcing.

**4. Report.**

Every finding names a file and line, states what is wrong, and states what goes wrong
as a result. Findings must be grounded in what you read, per the "When in Doubt"
section of the primary instructions — verify by reading the code, do not report what
would be a problem if some unverified assumption held.

A clean review is a valid and useful result. Say so plainly. Do not manufacture minor
findings to demonstrate that the review happened.

If the review is posted anywhere outside the session, it carries the attribution
signature from the primary instructions.

## Adding a check

When you encounter a category of problem worth checking for repeatedly — something you
had to reason out from scratch that will come up again — propose a new check file.

Create `agents/skills/ls-review/checks/<name>.md`:

```markdown
---
triggers: path/regex/one, another/path/prefix
applies-when: The situation this check is written for, and what it excludes.
---

<how to verify the change against this concern>
```

- `triggers` is a comma-separated list of regexes matched with `re.search` against
  repo-relative paths of changed files. Unanchored, so a bare directory prefix like
  `agents/resources/` works, and `.*` fires on everything. Escape dots when the
  distinction matters.
- `applies-when` is read by the reviewer to decide whether to open the file, so write
  it as a decision: state the situation it covers and, where useful, what it excludes.
  It should be answerable from the diff alone.
- The body is the check itself. Make it concrete enough to produce specific findings,
  and end it by saying what to report.

Keep triggers narrow. A check that fires on everything gets read on every review and
eventually gets skipped on every review.
