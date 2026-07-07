# Agent Context

Last Updated: 2026-07-08

## Project

`instatags` is a practical Instagram hashtag workflow for `raw345ig`, a senior male foreign model/actor in South Korea.

The active product is a hosted Google Apps Script web app backed by a Google Sheet. It returns exactly 5 useful hashtags for real Instagram posts, with forced custom tags first and ranked-deck tags filling the remaining slots.

## How To Work Here

- Start by reading this file, then `PROGRESS.md`, then `SESSION_LOG.md` if historical context is needed.
- Keep normal work focused on step 3: selector behavior, cooldown tuning, UI polish, hosted Apps Script behavior, and real-use feedback.
- Use the hosted Apps Script app for day-to-day real posts; use the local FastAPI app for development previews.
- Preserve source data and harvest artifacts, but do not rerun the old Instagram/Playwright collector unless Andrew explicitly asks to revisit research.

## Key Conventions

- Output should always be exactly 5 hashtags.
- The active ranked list is `data/ranked_hashtags_v2.csv`.
- The selector uses a queue-like rotation model with random cooldown insertion, not pure random choice.
- Blank category focus means no category emphasis.
- Active categories are `acting`, `chinese`, `commercial`, `drama`, `lookbook`, `senior`, and `shortform`.
- Forced tags are post-specific custom tags. They do not remove matching ranked tags, trigger cooldown, update queue position, or count as deck tags.
- Step 3 should stay local/app-script based and should not call an LLM.

## Key Decisions

- Customer discovery matters more than pure follower growth.
- English, Korean, and China-facing hashtags are all in scope.
- `v1` is the broad superset; `v2` is the near-final active ranked deck.
- Generic model tags are penalized unless qualified by traits like male, senior, foreign, acting, casting, commercial, or similar customer intent.
- `modeling` was removed as too broad; `lookbook` marks clothes/fashion/fitting/lookbook work.
- Category focus should affect only deck-selected tags, not forced tags.

## Important Commands

```powershell
python scripts\run_app.py
```

Then open `http://127.0.0.1:8000`.

## Where Memory Lives

- `AGENTS.md` - concise always-loadable project context and standing instructions.
- `PROGRESS.md` - current status, next actions, important live details, and gotchas.
- `SESSION_LOG.md` - chronological history.
- `archives/AGENT_CONTEXT-legacy-2026-07-08.md` - preserved legacy memory file that was replaced by `AGENTS.md` plus `PROGRESS.md`.

## Things To Avoid

- Do not paste Instagram credentials into chat or memory files.
- Do not rerun the Instagram/Playwright collector during normal selector tuning.
- Do not let broad generic hashtags dominate the active deck.
- Do not use `README.md` as the project memory source.
- Do not trust raw PowerShell display for Korean or Chinese text; use UTF-8-aware reads/editors.
- Do not reintroduce removed metadata columns such as `language`, `source_basis`, or `notes` unless there is a clear need.
