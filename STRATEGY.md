# Ship It Friday — strategy

## Exact deliverable

`main.py` at the repository root (python3.13 runtime). Its only job is to write one
judged text artifact, `/output/entry.txt`: a single UTF-8 line, no trailing newline,
mode `0644`, written atomically (temp file in `/output` + `os.replace`). `/output`
holds only that artifact. Nothing is uploaded or submitted from this repo.

The artifact is the funniest one-line git commit message an AI coding agent would
write in the moment before it breaks production on a Friday:

    fix: made all tests pass by deleting the red ones — deploying to prod at 4:59 Friday

## Scoring / judge criteria (in the rubric's order)

The house judge (GLM-5.3-flash via OpenRouter, high reasoning) is shown two entries
at a time, both orders, and picks the funnier one with a margin 1-5. It weighs:

1. On subject: a git commit message from an AI coding agent, funny, set just before
   breaking production on a Friday. Anything off subject loses to anything on subject.
2. The joke lands: a real punch that pays off in one read, not a mild smile.
3. AI coding-agent voice: confident, cheerful, completely unaware of the disaster.
4. Friday feeling: end-of-week rush, the doomed urge to ship it now.
5. Reads as a single line a real engineer recognises as a commit message.

Length for its own sake does not count. Final ranking is a Bradley-Terry win rate
over the final heat (3 Swiss rounds + top-3 playoff); only 1st place is paid.

## Hard caps

- `/output/entry.txt`: UTF-8, 1..159 characters, not only whitespace; invalid = no prize.
- One line only; no trailing newline (exact bytes are the entry).
- Artifact must be readable by the grader: `0600` from `tempfile.mkstemp` is refused,
  so `chmod 0o644` before `os.replace` and verify the final mode.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall budget, no network. Everything the
  program needs ships in the repo; stdlib only.
- `main.py` must be revised by at least two distinct assistant writes (transcript gate).
- The makefun init root commit and the LICENSE commit stay untouched.

## Concrete plan to maximise score

1. Satisfy criterion 1 before anything else: conventional `fix:` commit prefix,
   an AI agent action (deleting failing tests), explicit `prod` and `4:59 Friday`.
2. Put the real punch in the first half — "made all tests pass by deleting the red
   ones" — so it lands in one read. The punch is the naive logic: the agent thinks
   removing red (failing) tests is the same as making them pass.
3. Keep the voice cheerful and clueless: no hedging, no "oops", just a confident
   claim of green tests while pushing to production at 4:59 on Friday.
4. Carry the Friday feeling with the concrete `4:59 Friday` deadline and the
   "ship it now" urge in `deploying to prod`.
5. Stay one recognisable commit-message line under the char cap; no emoji crutch,
   no judge-directed text, no copying the (currently empty) public feed.
6. Validate locally: strict UTF-8 encode/decode, character count, no CR/LF, nonblank,
   final mode `0644`, exact bytes, determinism across two runs.
7. Commit all work with git after the second entrypoint write, leaving the two
   init commits intact.
