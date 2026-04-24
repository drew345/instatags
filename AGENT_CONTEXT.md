# Project Context

Last Updated: 2026-04-24

## Project
instatags is a local project to build an automatic Instagram hashtag workflow for `raw345ig`, a senior male foreign model/actor in South Korea. The long-term output is a simple local website that accepts a short post description and returns exactly 5 useful hashtags.

## Current Goal
Pause after a successful step-3 selector tuning session. The next work session should decide whether to turn the prototype into a true offline daily-use website or first define category focus / forced-tag behavior more carefully.

## Current Status
The project now has: step 1 harvest data, preserved harvest snapshots, protected must-keep hashtags, ranked lists `v1` and `v2`, a local selector website prototype, and a repeatable selector simulation report. `v1` is the widest practical superset of candidates to consider, including older manually supplied variants. `v2` is now treated as a near-final active ranked list with 66 active tags. The ranked CSVs were simplified to operational columns only: `rank`, `tag`, `bucket`, and `categories`. The selector uses `ranked_hashtags_v2.csv`, a saved queue state, optional category emphasis, optional forced tags, a logistic rank score called `base`, and score-derived random cooldown insertion. The repo is backed up to GitHub at `https://github.com/drew345/instatags` on branch `main`.

## Key Decisions
- The project has 3 phases: research hashtags, rank hashtags, then build the website.
- The final website should be lightweight, local-first, and mostly automatic.
- Output should always be exactly 5 hashtags.
- Default output shape is likely 1-2 broader tags plus 3-4 targeted tags.
- Ranking should prioritize customer discovery over pure follower growth.
- English and Korean hashtags are both in scope.
- The main audience is casting-style customers looking for a senior male foreign model/actor in Korea.
- Step 1 should stay practical and lightweight, with a two-hop discovery limit.
- Data collection should run locally on the user's machine through a real browser session, not via pasted credentials in chat.
- The repo name should use lowercase `instatags` for consistency locally and on GitHub.
- Step 2 produced a re-ranked `v2` list where generic model tags are penalized unless qualified by traits like male, senior, foreign, acting, casting, or commercial.
- `v1` should function as the broad "everything worth considering" list rather than a tight shortlist.
- `v2` should not be thought of as a hard split between "main" and "reserve"; it is a continuous ranking with gradual degradation from top to bottom.
- Lower-ranked but still natural search variants may belong in `v2` even if they are intended for low-frequency use.
- Tags can and should carry categories such as `modeling`, `acting`, `drama`, `casting`, `commercial`, `lifestyle`, and `chinese` so the selector can later emphasize a requested theme.
- The selector's rank strength uses the raw logistic S-curve, and cooldown ranges are derived from that score.
- The user currently considers the `v2` hashtag list itself close to final.
- The active categories were simplified; the currently tracked categories in `v2` are `acting`, `chinese`, `commercial`, `drama`, `modeling`, `senior`, and `shortform`.
- The preferred China-facing tags are now `#短剧`, `#微短剧`, `#竖屏短剧`, `#外籍演员`, `#外国演员`, with `#外国资深演员` and `#竖屏剧` retained as lower-frequency supporting variants.
- The China-facing tags were intentionally spaced through the ranked list at ranks `7`, `16`, `25`, `34`, `43`, `52`, and `60` so the strongest one can recur more often while the weakest stays low-frequency.
- The current preferred ranking function is a raw logistic S-curve using rank `1` as the top tag. The user liked the Excel form `=1/(1+EXP((A2-30)/10))` and does not currently want exact normalization to `1.0` and `0.0`.
- The user wants to think of ranking and cooldown as separate functions, even if they are related.
- The final output goal remains: Instagram now effectively allows 5 hashtags, with roughly 1-2 of those usually coming from the strongest top-ranked candidates and the remaining 3-4 drawn from the rest of the ranked deck.
- Step 3 should be local-only; it should not call an LLM.
- Current active work is step 3 only: selector behavior, cooldown tuning, UI, and local testing.
- Do not rerun the old Instagram/Playwright collector as part of normal step-3 work.
- The selector should use a queue-like rotation model with random cooldown insertion rather than pure random selection.
- Blank category focus should mean no category emphasis; `modeling` is no longer an implicit default.
- Cooldown is defined as a 1-based insertion position against the active deck before the selected tags are removed.
- Cooldown minimum is `active_deck_size * (0.5 - 0.375 * score)`, rounded up and clamped to the active deck.
- Cooldown maximum is `active_deck_size * (1.5 - (7 / 6) * score)`, rounded down and capped at the active deck.
- The actual cooldown position is a random integer between the min and max positions.

## Important Files
Current step-3 work should focus on `data/ranked_hashtags_v2.csv`, `data/selector_state.json`, `data/selector_simulation_counts.csv`, `app/selector.py`, `app/main.py`, `web/`, `docs/web-selector.md`, `scripts/run_app.py`, and `scripts/simulate_selector.py`. Collector and harvest files below are preserved historical context and should not be rerun or edited during normal selector tuning.
- `README.md` — general project overview and current scope
- `docs/step1-research-workflow.md` — step 1 collection rules and dataset logic
- `docs/collector-usage.md` — how to run the local collector
- `data/seed_hashtags.csv` — initial seed hashtags
- `data/customer_search_intents.csv` — customer-intent phrases to guide ranking
- `data/hashtag_candidates.csv` — initial working candidate dataset
- `data/targets.json` — collector target profile, seed hashtags, and crawl limits
- `data/must_keep_hashtags.csv` — deduplicated user-approved hashtags that must remain in consideration
- `data/snapshots/2026-04-22-initial-harvest/` — preserved baseline outputs from the first completed collection run
- `data/ranked_hashtags_v2.csv` — current preferred ranked list
- `data/selector_state.json` — saved queue state for the selector
- `app/selector.py` — selection engine
- `app/main.py` — FastAPI app serving the selector
- `web/index.html` — local selector UI
- `web/app.js` — selector UI behavior
- `web/styles.css` — selector styling
- `docs/web-selector.md` — how to run the local selector website
- `scripts/collect_instagram_hashtags.py` — local Instagram hashtag collector
- `AGENT_CONTEXT.md` — current project memory / handoff file
- `SESSION_LOG.md` — recent dated work summary

## Open Problems
- PowerShell displayed Korean text with encoding issues during verification; file contents should be checked in a UTF-8-friendly editor if needed.
- The first harvest mixed peer-discovered tags with some hashtags from the user's own posts.
- Git commands that write `.git` metadata may need elevated execution in this environment.
- Two older-list variants, `#남자중년외국인` and `#남자시니어외국인`, were judged the most awkward and should remain in `v1` only, not be added to `v2`.
- The selector still needs tuning by inspecting real successive outputs in the browser.
- The current selector is working, but selection behavior should be reviewed visually before calling the logic stable.

## Next Steps
- Decide whether to polish the current local website into a true offline daily-use version.
- Alternatively, define category focus and forced-tag behavior before UI polish.
- Run `python scripts\run_app.py`, open `http://127.0.0.1:8000`, and use preview / next / reset to inspect selector behavior.
- Rerun `python scripts\simulate_selector.py --csv-output data\selector_simulation_counts.csv` after selector logic changes.
- After the next tuning step, update memory and push changes to GitHub.

## Gotchas / Things to Avoid
- Do not paste Instagram credentials into chat.
- Do not rerun the Instagram/Playwright collector unless the user explicitly decides to revisit step 1.
- Do not let broad generic hashtags dominate the dataset before customer-intent tags are established.
- Do not use README as the only memory source; keep project memory in this file and `SESSION_LOG.md`.
- Be aware that PowerShell may display Korean text incorrectly even when UTF-8 file contents are fine.
- When opening CSVs on Windows, prefer a UTF-8-aware editor or Excel import flow rather than trusting raw console output.
- Do not reintroduce removed metadata columns (`language`, `source_basis`, `notes`) into the active ranked files unless there is a clear need.
