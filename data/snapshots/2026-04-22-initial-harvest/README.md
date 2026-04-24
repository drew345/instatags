# Initial Harvest Snapshot

This folder preserves the first completed Instagram collection run from 2026-04-22 before step 2 work begins.

## Purpose

- keep the raw harvested output untouched
- preserve the first summary exactly as generated
- give step 2 a stable baseline even if later collection logic changes

## Files

- `raw_hashtag_observations.csv` — raw hashtag observations from the completed run
- `collected_hashtag_summary.csv` — distinct-tag summary generated from that run

## Notes

- This run included some hashtags from `raw345ig`'s own posts before the collector logic was tightened toward peer-focused discovery.
- The snapshot is still valuable as a baseline dataset and should not be overwritten.
