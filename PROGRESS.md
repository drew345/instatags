# Progress

Last Updated: 2026-07-08

## Current Status

The active `instatags` work is step 3: using and tuning the hosted hashtag selector for real Instagram posts.

This is a stable project. Local clones are optional as long as `main` is pushed to GitHub. Andrew can use the hosted Apps Script website day to day and reclone from `https://github.com/drew345/instatags` only if future code, data, or memory edits are needed.

The project has completed:

- Step 1 hashtag research and preserved harvest snapshots.
- Step 2 ranking into `v1` and the active `v2` ranked list.
- A local FastAPI selector prototype.
- A hosted Google Apps Script web app with shared Google Sheet state.
- Forced custom tags.
- Stronger category focus behavior.

The current hosted deployment is version `@8` of deployment `AKfycbyOWzu3dvfYtkQzKtboGW1dIeups2OlBG_KFSnVoiAE6AHhcNEPGODVSKJjFohWTdlrew`, with description `Stronger Category Focus`.

## Current Goal

Use the hosted Apps Script app for real posts, then improve phone polish and category behavior based on actual use.

## Important Live Details

- Spreadsheet ID: `1xoEg3HIEAsMlGvIeAGs09ZzcNB32RssaaMc4Vrozs28`
- Apps Script project name: `InstaTags`
- Apps Script ID: `1ABG6UcS9rPUtqIhr7xwkTo8oiGCXvmaaojkW6YpSUjf3MGvTVTMYjzzk`
- Current web app URL: `https://script.google.com/macros/s/AKfycbyOWzu3dvfYtkQzKtboGW1dIeups2OlBG_KFSnVoiAE6AHhcNEPGODVSKJjFohWTdlrew/exec`
- Google Sheet tabs managed by the app: `ranked_tags`, `current_deck`, `state`, `history`
- The active hosted app stores shared queue state in the Google Sheet so phone and laptop use the same deck.
- The local FastAPI app remains useful for development previews.

## Selector Behavior

- The selector uses rank, categories, a logistic rank score called `base`, and score-derived random cooldown insertion.
- The preferred ranking function is the raw logistic S-curve style `1/(1+EXP((rank-30)/10))`, with rank `1` strongest.
- Ranking and cooldown should remain conceptually separate, even though cooldown is derived from score.
- Cooldown is a 1-based insertion position against the active deck before selected tags are removed.
- Category focus first takes normal queue picks, then replaces enough noncategory deck picks with earliest available category matches to reach the target when practical.
- Only final selected deck tags are removed and reinserted via cooldown.

## Category Focus Rule

Category focus affects deck-selected tags only. Forced tags always consume output slots first.

Target category deck tags:

- 0 forced tags: try for at least 3 category deck tags.
- 1 forced tag: try for at least 3 category deck tags.
- 2 forced tags: try for 3 category deck tags.
- 3 forced tags: try for 2 category deck tags.
- 4 forced tags: try for 1 category deck tag.
- 5 forced tags: select no deck tags, so category does nothing.

If there are not enough available category tags to satisfy the target naturally, fill the rest from the normal ranked queue.

## Open Problems

- The selector still needs tuning by inspecting real successive outputs in the browser.
- The current selector is working, but selection behavior should be reviewed visually before calling the logic fully stable.
- Apps Script mobile banner may take too much phone screen space.
- PowerShell may display Korean or Chinese text incorrectly even when UTF-8 file contents are fine.
- Two awkward older Korean variants should remain in `v1` only and should not be promoted into `v2`.

## Next Actions

1. Use the hosted Apps Script app for real posts and note phone UI friction.
2. Watch whether focused categories, especially sparse `lookbook`, feel strong enough in actual use.
3. Add phone/home-screen polish such as icon and app metadata if the hosted app remains convenient.
4. Investigate whether the Apps Script banner can be reduced by deployment settings; compare with Andrew's weight uploader.
5. If the Apps Script banner remains too intrusive, consider a GitHub Pages front end with Apps Script as the stateful backend.
6. After 10-20 real uses, inspect `history` and optionally build a distribution summary.

## Memory Migration Note

On 2026-07-08, project memory was converted from legacy `AGENT_CONTEXT.md` to standard `AGENTS.md` plus `PROGRESS.md`. The old full-context file is preserved at `archives/AGENT_CONTEXT-legacy-2026-07-08.md`.

## Local Clone Note

On 2026-07-08, Andrew decided this project may not need to remain cloned on every computer because the hosted website is stable. Before deleting a local clone, confirm `git status` is clean and `main` is pushed to GitHub.
