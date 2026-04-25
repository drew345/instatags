# Session Log

## 2026-04-25
- Turned the local selector into a deployed Google Apps Script web app so it can be used from phone/laptop without running the local Python server.
- Created and connected the Apps Script project `InstaTags` with script ID `1ABG6UcS9rPUtqIhr7xwkTo8oiGCXvmaaojkW6YpSUjf3MGvTVTMYjzzk` via `.clasp.json`.
- Wired the hosted app to Google Sheet `1xoEg3HIEAsMlGvIeAGs09ZzcNB32RssaaMc4Vrozs28`.
- Apps Script deployment URL currently in use: `https://script.google.com/macros/s/AKfycbyZqHXt7itB4fnPlXWSEf-4sY8KU9qYySrrD5DmOV4Q4x7ZO_x6zbKMQhYNrAjql2b2FA/exec`.
- The app created/updates Google Sheet tabs `ranked_tags`, `current_deck`, `state`, and `history`.
- `ranked_tags` keeps the stable source list; `current_deck` shows the readable shuffled queue; `state` stores the authoritative JSON queue and iteration; `history` logs generated tag sets.
- The hosted state was initialized from a baked 100-warmup queue, not the raw top-five-heavy ranked order.
- Removed `bucket` as an active selector concept and from the hosted sheet output; categories and rank are now the meaningful fields.
- Verified from the user's desktop/phone that Generate Next 5 returns five tags and updates `state`, `current_deck`, and `history`.
- Known issue: Google's Apps Script banner may take too much screen space on phone. Compare deployment settings with the user's weight uploader next time, or consider GitHub Pages front-end plus Apps Script backend.
- Next possible work: phone/home-screen icon and metadata, phone UI optimization after real use, history distribution summary after 10-20 uses, and later category/forced-tag design.

## 2026-04-24
- Implemented the raw logistic S-curve rank score in `app/selector.py` using the user's preferred Excel-style form scaled by `active_deck_size`.
- Added `active_deck_size` as a data-derived selector concept so the current 66-tag deck can grow or shrink without hard-coding the bottom rank.
- Normalized saved selector state so old queue entries are dropped and newly added active tags are appended when the ranked deck changes.
- Defined cooldown as a 1-based insertion position against the active deck before selected tags are removed.
- Implemented score-derived cooldown ranges:
  - minimum cooldown: `active_deck_size * (0.5 - 0.375 * score)`
  - maximum cooldown: `active_deck_size * (1.5 - (7 / 6) * score)`, capped at `active_deck_size`
- The actual cooldown position is now a random integer between the computed min and max positions.
- Updated docs/UI wording so the selector is described as local and queue-based rather than deterministic.
- Changed blank focus categories to mean no category emphasis rather than defaulting to `modeling`.
- Removed the cherry blossom forced-tag placeholder from the UI/docs to avoid implying a defined special behavior.
- Moved selector simulation scratch state away from `playwright_state` to keep step-3 testing conceptually separate from the old Instagram collection workflow.
- Generated `data/selector_simulation_counts.csv` for Excel plotting of rank-by-rank selection frequency.
- Reviewed the simulation results with the user; the top-five distribution and full-rank selection curve looked good enough to stop for the day.
- Next step: decide whether to polish the current local website into a true offline daily-use version or first define category focus / forced-tag behavior more carefully.

## 2026-04-23
- Reviewed an older manual hashtag list against the current ranked sets.
- Expanded `data/ranked_hashtags_v1.csv` so it acts as the broad superset of realistic candidates rather than a fixed 50-tag shortlist.
- Confirmed that `v2` should be understood as a continuous ranking with gradual degradation, not a hard split between a main pool and a reserve pool.
- Reconfirmed that the selector's cooldown period is driven by the same piecewise scoring curve used for rank strength.
- Flagged two variants, `#남자중년외국인` and `#남자시니어외국인`, as the most awkward phrasing; keep them in `v1` only and do not promote them into `v2`.
- Removed 8 tags from the active `v2` list: `#배우프로필사진`, `#commercialmodel`, `#editorialmodel`, `#라이프스타일모델`, `#프리랜서외국인모델`, `#maturemodel`, `#방송배우`, and `#외국인모델서울`.
- Promoted 17 older-list variants into `v2` and expanded the active ranked list from 50 to 59 tags.
- Rewove the promoted tags through the middle and lower ranks rather than appending them at the bottom, preserving the continuous-ranking model.
- Added 5 Chinese-language tags to `v1` and `v2` so China-facing acting/drama visibility can surface occasionally in the active selector rotation.
- Reconfirmed that category labels are part of the intended selector design and can be used later to stress themes such as `modeling`, `acting`, `drama`, `lookbook`, and `chinese`.
- Replaced the initial Chinese tag set after checking current Instagram-facing term counts and user-supplied observations.
- Current preferred Chinese set is `#短剧`, `#微短剧`, `#竖屏短剧`, `#外籍演员`, `#外国演员`, with `#外国资深演员` and `#竖屏剧` retained as lower-frequency supporting variants.
- Simplified the ranked CSV structure by removing `language`, `source_basis`, and `notes` from the active ranked files now that the hashtag set is close to final.
- The active operational ranked-list fields are now `rank`, `tag`, `bucket`, and `categories`.
- The user now sees the `v2` hashtag list itself as near-final.
- The preferred ranking score curve is now a logistic-style S-curve; the user liked the Excel form `=1/(1+EXP((A2-30)/10))` with rank `1` as the top tag and does not currently want exact normalization.
- The ranking and cooldown models should be treated as separate functions conceptually.
- The intended selector behavior remains: usually output 5 hashtags, with roughly 1-2 from the strongest top-ranked candidates and the remaining 3-4 from the rest of the deck.
- Began defining cooldown anchors as ranges rather than single values:
  - rank `1` -> cooldown about `4` to `10`
  - rank `30` -> cooldown about `20` to `67`
  - rank `67` -> cooldown about `50` to `67`
- Next step when resuming: derive simple cooldown-min and cooldown-max functions, likely linear first, and compare them numerically at representative ranks before changing selector logic.

## 2026-04-22
- Confirmed the user wanted a step-3 deterministic website rather than more abstract planning.
- Built the first local FastAPI web selector with a queue-based deterministic hashtag rotation engine.
- Added category emphasis and optional forced-tag support, plus preview / next / reset controls in the browser UI.
- Created `data/selector_state.json` to persist queue state between runs.
- Verified the API and generated the first 6 preview iterations for modeling-focused selection.
- Re-ranked against the full harvested set in `data/ranked_hashtags_v2.csv`, lowering generic model tags unless they are qualified.
- Next step when resuming: inspect the first generated runs together and tell the user how to run the selector locally.

## 2026-04-22
- Ran the first live Instagram collection session and produced `400` raw observations across `235` distinct hashtags.
- Confirmed the collected dataset is usable, though it still includes some of the user's own post hashtags from the earlier collector behavior.
- Preserved the first completed run in `data/snapshots/2026-04-22-initial-harvest/` before step 2 work.
- Added `data/must_keep_hashtags.csv` to protect the user's approved core hashtags during later cleaning and ranking.
- Verified that all user-priority hashtags were present in the harvest except `#외국인캐스팅`, which was added to the protected list manually.
- Next step: begin step 2 by cleaning the candidate set and building the first ranking model.

## 2026-04-16
- Normalized the project naming from `Instatags` to `instatags` in repo docs and memory files.
- Confirmed the physical folder rename to lowercase did not break the project.
- Initialized git locally, created the first commit, added the GitHub remote, and pushed `main` to `https://github.com/drew345/instatags`.
- Confirmed the repo is clean and portable for cloning on another laptop.
- Implementation work is still paused; next build step remains the first live run of `python scripts\collect_instagram_hashtags.py`.

## 2026-04-14
- Defined the instatags project clearly as a 3-step workflow: hashtag research, hashtag ranking, then a lightweight local website.
- Locked in the target niche as `raw345ig`: senior male foreign model/actor in South Korea.
- Chose customer discovery as the main optimization target, with account growth as a secondary benefit.
- Chose English and Korean hashtags as the study/output languages.
- Created initial project docs and seed data files for step 1 research.
- Installed Playwright and the Chromium runtime locally.
- Added a first local collector script that opens a browser, allows manual Instagram login, visits the target profile and seed hashtag pages, and writes CSV outputs.
- Did not complete a live collector run; GUI launch was attempted but not completed before ending the session.
- Next step: run `python scripts\collect_instagram_hashtags.py`, gather the first dataset, then clean candidates and implement ranking.
