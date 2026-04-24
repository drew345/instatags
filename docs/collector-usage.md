# Collector Usage

This collector runs locally on your machine and uses a real browser session.

## What it does

- opens Instagram in Chromium
- lets you log in manually
- visits the seed hashtag pages in `data/targets.json`
- extracts hashtags from posts under those hashtag pages
- discovers the account handles behind those posts
- visits those peer profiles and extracts hashtags from their recent posts
- writes the results into CSV files

## Output files

- `data/raw_hashtag_observations.csv`
- `data/collected_hashtag_summary.csv`

## Run command

```powershell
python scripts\collect_instagram_hashtags.py
```

## Notes

- The first run will create a local browser profile in `playwright_state/instagram`
- That profile helps avoid logging in every time
- Instagram may block or slow some pages, so this collector is meant to be practical rather than aggressive
- If Instagram changes its page structure, selectors may need to be updated
- By default it skips crawling your own profile posts because the main goal is to learn from other similar accounts
