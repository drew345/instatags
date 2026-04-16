# Project Context

Last Updated: 2026-04-14

## Project
instatags is a local project to build an automatic Instagram hashtag workflow for `raw345ig`, a senior male foreign model/actor in South Korea. The long-term output is a simple local website that accepts a short post description and returns exactly 5 useful hashtags.

## Current Goal
Complete step 1: automatically collect and organize a focused universe of candidate hashtags from Instagram for later ranking.

## Current Status
Project scaffolding exists. Initial research docs and seed datasets are in place. A first local Playwright-based Instagram collector has been created and browser dependencies were installed. The collector has not yet been run successfully in a live browser session because the GUI launch was not completed before stopping for the day.

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

## Important Files
- `README.md` — general project overview and current scope
- `docs/step1-research-workflow.md` — step 1 collection rules and dataset logic
- `docs/collector-usage.md` — how to run the local collector
- `data/seed_hashtags.csv` — initial seed hashtags
- `data/customer_search_intents.csv` — customer-intent phrases to guide ranking
- `data/hashtag_candidates.csv` — initial working candidate dataset
- `data/targets.json` — collector target profile, seed hashtags, and crawl limits
- `scripts/collect_instagram_hashtags.py` — local Instagram hashtag collector

## Open Problems
- The collector has not yet been live-tested against Instagram.
- PowerShell displayed Korean text with encoding issues during verification; file contents should be checked in a UTF-8-friendly editor if needed.
- The collector may need selector updates once tested against real Instagram pages.
- Ranking logic for step 2 has not been implemented yet.

## Next Steps
- Run `python scripts\collect_instagram_hashtags.py`.
- Log into Instagram in the opened browser and let the first collection pass complete.
- Review `data/raw_hashtag_observations.csv` and `data/collected_hashtag_summary.csv`.
- Clean and categorize the first 30-50 useful candidate hashtags.
- Build the first rules-based ranking model.

## Gotchas / Things to Avoid
- Do not paste Instagram credentials into chat.
- Do not assume Instagram pages are easily scrapeable without testing; the collector is intended to be practical, not aggressive.
- Do not let broad generic hashtags dominate the dataset before customer-intent tags are established.
- Do not use README as the only memory source; keep project memory in this file and `SESSION_LOG.md`.
