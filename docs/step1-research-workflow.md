# Step 1 Research Workflow

This project starts with a focused hashtag study for `raw345ig`.

## Goal

Build a high-quality candidate list of hashtags that help with:

- customer discovery
- search visibility
- account growth

The target customer is someone looking for a senior male foreign model/actor in South Korea.

## Research principles

- Stay niche-first before going broad
- Prefer hashtags that a casting-related customer might realistically use
- Track evidence for every hashtag instead of collecting tags with no context
- Avoid letting broad, noisy tags dominate the dataset
- Keep Korean and English hashtags both in scope

## Collection sources

Start here first:

1. Your profile: `raw345ig`
2. Seed hashtag pages:
   - `#외국인모델`
   - `#외국인남자모델`
   - `#외국인중년모델`
   - `#외국인남자배우`

Then expand to:

3. Accounts repeatedly appearing under those tags
4. Posts from those accounts that match your niche
5. Additional hashtags repeatedly co-occurring with the seed tags

## Two-hop limit

To keep the research practical, only branch two hops:

- Hop 0: your profile and current seed hashtags
- Hop 1: posts/accounts directly discovered from those seeds
- Hop 2: related hashtags found repeatedly in hop 1

If a tag appears only once and seems off-niche, do not expand from it yet.

## What counts as a strong candidate hashtag

A strong candidate usually has at least one of these properties:

- clearly describes your niche
- matches a customer hiring search
- is used by similar foreign male talent in Korea
- is specific enough that you might realistically surface under it
- works well for either actor, model, or senior-foreign-talent positioning

## What counts as a weak candidate hashtag

Be cautious with hashtags that are:

- too broad to be useful
- unrelated to acting, modeling, or foreign talent in Korea
- clearly aimed at vanity engagement only
- inconsistent with your age, look, or market
- spammy or repetitive

## Dataset fields

Every collected hashtag should be recorded in `data/hashtag_candidates.csv` with:

- `tag`
- `language`
- `theme`
- `source_type`
- `source_value`
- `hop_depth`
- `times_seen`
- `customer_intent`
- `fit_for_raw345ig`
- `notes`

## Recommended first-pass themes

- foreign model
- foreign actor
- male model
- male actor
- senior model
- middle-aged model
- Korea / Seoul
- casting / audition
- commercial / advertising
- lifestyle / fashion / portrait

## First milestone

Collect 30-50 candidate hashtags with context.

That is enough to:

- see the main clusters
- identify obvious gaps
- begin the first ranking model

## Initial working assumptions

- customer discovery matters more than pure follower growth
- English and Korean tags should both be studied
- the final website should return exactly 5 hashtags
- the final mix will likely be 1-2 broader tags and 3-4 targeted tags
