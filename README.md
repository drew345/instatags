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

We are currently in step 1: building the initial hashtag universe and research rules.

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
- `data/seed_hashtags.csv`: starting hashtag list
- `data/customer_search_intents.csv`: target customer search phrases
- `data/hashtag_candidates.csv`: working research dataset

## How step 1 will work

Start from the profile and seed hashtags, then collect nearby hashtags from relevant accounts and posts. Keep the exploration focused on:

- foreign talent in Korea
- male model / actor searches
- senior / middle-aged positioning
- customer-intent discovery, not just broad social growth

The first collection pass should stay within two hops:

1. `raw345ig` and the seed hashtags
2. relevant nearby accounts/posts using related hashtags

## Next action

Use `docs/step1-research-workflow.md` while collecting the first 30-50 candidate hashtags.
