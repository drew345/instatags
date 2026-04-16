# Session Log

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
