# instatags Agent Instructions

Last Updated: 2026-07-11

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

## Selector Model

- Rank `1` is the top tag.
- The preferred score curve is the raw logistic form `1/(1+EXP((rank-30)/10))`.
- Ranking and cooldown remain conceptually separate, even though cooldown ranges use the score.
- Cooldown is a 1-based insertion position against the active deck before selected tags are removed.
- Cooldown minimum is `active_deck_size * (0.5 - 0.375 * score)`, rounded up and clamped to the active deck.
- Cooldown maximum is `active_deck_size * (1.5 - (7 / 6) * score)`, rounded down and capped at the active deck.
- Actual cooldown position is a random integer between the minimum and maximum.

## Category Focus

- Stronger category focus is implemented in both the Python and Apps Script selectors.
- It affects only deck-selected tags and targets up to 3 category matches, reduced when forced tags leave fewer deck slots.
- Only final selected deck tags receive cooldown; inspected but unselected tags retain their queue order.
- When category matches are insufficient, remaining slots fall back to normal ranked queue tags.
- Tests should cover 0-5 forced tags, sparse categories such as `lookbook`, broader categories, and queue advancement by selected deck tags only.

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

## Active Files

- Selector and UI: `app/`, `apps-script/`, `web/`, `tests/`, and `scripts/simulate_selector.py`.
- Active data: `data/ranked_hashtags_v2.csv`, `data/selector_state.json`, and `data/selector_simulation_counts.csv`.
- Historical collector inputs and snapshots should generally be left alone.

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
- Do not store Instagram or Google credentials, tokens, or private account material in repository files.
