# Personal Context (example)

Copy this file to `agents/personal-context.md` and replace the contents with your own.
That path is gitignored, so your copy stays local and affects nobody else.

This file takes precedence over `agents/agent-instructions.md`. Where the two conflict,
this one wins.

Everything below is an example. Delete what does not apply to you — a short file that
is true beats a long one you stopped maintaining.

---

## Communication

How I want to be worked with.

- Don't give me multiple-choice prompts. Explain the tradeoffs in prose and tell me
  which one you'd pick.
- Lead with the substance. Skip the preamble restating what I asked for.
- One thing at a time. If there are four decisions to make, walk me through them
  individually rather than presenting all four at once.
- Tell me when you're unsure. I'd rather hear "I haven't verified this" than a
  confident guess.

## Workspace

Where to work, and what to work with.

- Scratch files, throwaway scripts, and intermediate output go in `agents/cache/`. Not
  `/tmp`, and not the repo root.
- Use `conda` for virtual environments. Don't create a `venv/` or install into the
  system Python.
- Clean up after yourself: a temporary script that outlived its purpose gets deleted,
  not left in the source tree.
- Build out of tree, into `build/`.

## Environment

Machine-specific facts that are not discoverable from the repo, or that would cost you
time to rediscover.

- Tests run in the `project-dev` conda env, not the system Python. Activate it first.
- The full suite takes about 20 minutes. Use `pytest -x tests/unit` while iterating and
  save the full run for the end of a chunk.
- My local database is seeded with test fixtures, not a production snapshot. Data that
  looks wrong is probably the fixture, not a bug.
- `rg` is available; `ag` is not.

## Workflow overrides

Deliberate contradictions of the primary instructions.

- Push to my own branches freely. Don't push to `main` or to anything with an open PR
  from someone else.
- Squash review fixes into the chunk's commit rather than adding follow-up commits.
- Don't stop to ask about small naming and style choices. Pick one, note it, and keep
  going.

## Notes

Anything else that does not fit above.

- I work in short sessions. Write the session log more often than the instructions
  require, so that picking up tomorrow is cheap.
