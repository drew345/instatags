# Web Selector

This is the first local website for hashtag selection.

## Run it

```powershell
python scripts\run_app.py
```

Then open:

`http://127.0.0.1:8000`

## What it does

- uses `data/ranked_hashtags_v2.csv` as the base ranked list
- keeps a saved queue in `data/selector_state.json`
- returns 5 hashtags per iteration
- supports category emphasis such as `modeling`, `acting`, `drama`, and `senior`
- supports an optional forced custom tag
- rotates tags with score-derived min/max cooldown ranges and a random insertion point

## Main controls

- `Preview 6 Iterations`
  - shows the next 6 cycles without changing the saved queue
- `Use Next 5`
  - commits one iteration and updates the saved queue
- `Reset Queue`
  - returns the saved queue to the initial ranked order

## Current design

- selection is local and queue-based
- queue order matters more than raw rank once the app is running
- top-ranked tags still dominate
- lower-ranked tags can appear when the queue rotates and when the chosen categories fit
- no LLM is involved

## Important files

- `app/selector.py` — selection and cooldown logic
- `app/main.py` — API routes and static site serving
- `web/index.html` — UI markup
- `web/app.js` — UI behavior
- `web/styles.css` — interface styling
