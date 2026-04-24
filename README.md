# instatags

instatags is a local project for building a practical Instagram hashtag workflow for `raw345ig`.

The long-term goal is a simple website where a short photo description returns 5 useful hashtags:

- 1-2 broad hashtags for reach
- 3-4 targeted hashtags for customer discovery

The project is organized into three steps:

1. Research candidate hashtags for a senior male foreign model/actor in South Korea
2. Rank those hashtags for both reach and findability
3. Build a lightweight website that chooses 5 hashtags automatically

## Current focus

We are now focused on step 3: tuning and testing the local selector website. The original harvest and ranking work are preserved as project history and source data, but normal work should not rerun the Instagram collector.

## Profile

- Instagram handle: `raw345ig`
- Core niche: senior male foreign model/actor in South Korea
- Seed hashtags:
  - `#외국인모델`
  - `#외국인남자모델`
  - `#외국인중년모델`
  - `#외국인남자배우`

## Project structure

- `docs/step1-research-workflow.md`: repeatable research process
- `docs/web-selector.md`: how to run the local hashtag selector website
- `data/seed_hashtags.csv`: starting hashtag list
- `data/customer_search_intents.csv`: target customer search phrases
- `data/hashtag_candidates.csv`: working research dataset
- `data/ranked_hashtags_v2.csv`: current ranked tag list
- `data/selector_state.json`: current selector queue state
- `app/selector.py`: selection engine
- `app/main.py`: local FastAPI app
- `web/`: local web interface

## Historical step 1

The first research pass collected nearby hashtags from relevant accounts and posts. That work is considered complete unless we intentionally decide to refresh the dataset later. The collector should not be part of normal step-3 selector work.

- foreign talent in Korea
- male model / actor searches
- senior / middle-aged positioning
- customer-intent discovery, not just broad social growth

The first collection pass should stay within two hops:

1. `raw345ig` and the seed hashtags
2. relevant nearby accounts/posts using related hashtags

## Next action

Run the local selector website and review successive iterations:

```powershell
python scripts\run_app.py
```

Then open `http://127.0.0.1:8000`.
