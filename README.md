# L's Agent Tools Framework

A baseline framework for agent instructions, skills, and reference material that works
the same way across harnesses. This repo is the rough shape that I've used in both
professional and personal contexts when trying to get the best performance out of
agentic AI tools. Every project I work on or maintain uses a variant of this and
the goal here is to standardize and publish this framework to be used elsewhere.

Everything lives under `agents/`. `agents/agent-instructions.md` is the one file that
matters; every harness entry point is a redirect to it.

**Start with [`agents/resources/philosophy.md`](agents/resources/philosophy.md).** It
explains why the framework is shaped this way, and most of the structure below only
makes sense in light of it.

## Structure

```
CLAUDE.md                        redirect stub
AGENTS.md                        redirect stub
.github/copilot-instructions.md  redirect stub

agents/
├── agent-instructions.md        the primary instructions
├── personal-context.example.md  template for per-developer preferences
├── personal-context.md          per-developer preferences (gitignored)
├── cache/                       session logs (gitignored)
├── resources/                   frequently accessed reference material
│   ├── philosophy.md
│   └── debugging-pitfalls.md
└── skills/
    ├── ls-gh/                   GitHub CLI usage
    ├── ls-review/               diff review, with triggered checks
    │   ├── match_checks.py
    │   └── checks/
    └── ls-session-log-mining/   mining logs for recurring problems
```

The entry points at the root are redirects and nothing else. Every harness reads a
different filename, so each gets a file, and all of them point at the same instructions.
On a platform with working symlinks you can replace them with links to
`agents/agent-instructions.md`; they are committed as stubs because git materializes
symlinks as one-line text files on Windows clones without symlink support, which fails
silently.

`agents/agent-instructions.md` indexes the skills and resources in tables. A skill that
is not in the table will not be found — nothing is registered with any harness.

## Using it in your own repo

Clone this repo and copy the applicable parts into yours. There is no installer, no
submodule, and no sync mechanism. The framework is a shape; once it is in your repo it
is yours to edit, and it is expected to diverge.

Carry over everything except two directories' contents:

- **`agents/resources/`** — copy the directory, not the documents in it. `philosophy.md`
  is about this framework rather than your project, and `debugging-pitfalls.md` is an
  empty destination that fills itself in over time.
- **`agents/skills/ls-review/checks/`** — same. `philosophy-adherence.md` exists to
  demonstrate the check format, and it only means anything alongside `philosophy.md`.

Everything else transfers as-is and works immediately: the three entry stubs,
`agents/agent-instructions.md`, the personal context example, and all three skills.

One thing to fix after copying: remove the Resources table rows in
`agents/agent-instructions.md` for the documents you did not bring. An index pointing at
a file that is not there is worse than an empty table — an agent will go looking for it.

**Pick a prefix that fits your project.** The skills here are prefixed `ls-` (for this
repo, `ls-agent-tools`). Choose your own logical prefix and rename the three skill
directories to match — updating their table rows in `agents/agent-instructions.md`, the
path examples inside each skill, the cross-references between skills and resource docs,
and this README's structure tree. `grep -rn skills/` finds them all. The prefix is not decoration: nothing here
is registered with a harness, so a bare name like `review` handed to a harness's skill
loader fuzzy-matches a *built-in* (Claude Code ships a `code-review`) and silently runs
the wrong thing. A distinctive per-project prefix keeps your skills from colliding with
whatever built-ins your harness provides.

## What to populate

The parts you copied empty are not setup work waiting to be finished. They fill in as
you work, and each has a mechanism that fills it.

- **`agents/resources/`** — starts empty. It fills with the design documents and
  hard-won facts that your agents would otherwise rediscover by reading code.
- **`agents/skills/ls-review/checks/`** — also starts empty. Real checks come from noticing
  what reviews keep missing, which is what session log mining is for. Expect early
  reviews to lean entirely on the baseline pass.
- **The General Coding Practice section** of the instructions — ships with two rules
  (comment provenance, tests having teeth) and a placeholder bullet. The rest is
  codebase-specific and is meant to be written by you.

The session log mining skill exists to drive the first two: it reads back over what
actually went wrong on past branches and proposes entries, so neither directory depends
on anyone maintaining a list by hand.

## Decisions you may want to revise

This is a baseline, not a finished configuration. These choices suit the way I work,
and some of them are wrong for other setups.

**Commit aggressively.** The instructions tell the agent to commit as soon as a chunk's
tests pass, before review, with fixes landing as follow-up commits. That produces a
messy branch history, which is fine if you squash on merge. If you merge without
squashing, or if people commit straight to `main`, this will put noise in the history
you keep. Change it to commit at review-clean boundaries instead.

**Subagents are expected, not just permitted.** Reviews and non-trivial debugging are
supposed to be dispatched rather than done inline. This costs real compute — every
review is a second agent reading the diff from nothing. The benefit is that the reviewer
has genuinely fresh eyes, which is the single highest-value practice in here and is not
achievable by asking the implementing agent to check its own work. Worth the cost in my
experience, but it is a cost, and it scales with how much you use it.

**The chunk cycle assumes an autonomous agent.** Plan and chunk cooperatively, then hand
over control: the agent works through implement → test → review per chunk without
checking in. That is deliberate — the planning phase is front-loaded precisely so the
execution phase does not need supervision. If you would rather approve each step, this
structure works against you, and you should add explicit check-in points at the chunk
boundaries.

**Personal context overrides the primary instructions.** A developer's gitignored
`agents/personal-context.md` wins on conflict, without limit. That is what makes local
customization real rather than advisory. It also means anything in the primary
instructions can be locally disabled by the person the instructions apply to. If you
need something to hold for everyone, this is not the place to enforce it.

**Nothing is registered with the harness.** Skills are found through a table in the
instructions file, not through a harness-native mechanism, so they work identically
everywhere. The cost is that you give up harness-native features — Claude Code's
frontmatter skill loading, for instance, and anything else a specific tool offers for
declaring capabilities. If you only ever use one harness, native registration is likely
better and this trade buys you nothing.
