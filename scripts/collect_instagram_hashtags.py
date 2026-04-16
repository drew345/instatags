import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Set

from playwright.sync_api import BrowserContext, Page, TimeoutError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
STATE_DIR = ROOT / "playwright_state" / "instagram"
TARGETS_PATH = DATA_DIR / "targets.json"
RAW_OUTPUT_PATH = DATA_DIR / "raw_hashtag_observations.csv"
SUMMARY_OUTPUT_PATH = DATA_DIR / "collected_hashtag_summary.csv"
HASHTAG_PATTERN = re.compile(r"#([\w\u00C0-\u024F\u0400-\u04FF\u0600-\u06FF\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]+)")


def load_targets() -> Dict[str, object]:
    with TARGETS_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def ensure_directories() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def slugify_hashtag(tag: str) -> str:
    return tag.lstrip("#").strip()


def detect_language(tag: str) -> str:
    normalized = slugify_hashtag(tag)
    if re.search(r"[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]", normalized):
        if re.search(r"[A-Za-z]", normalized):
            return "mixed"
        return "ko"
    if re.search(r"[A-Za-z]", normalized):
        return "en"
    return "unknown"


def extract_hashtags(text: str) -> List[str]:
    if not text:
        return []
    matches = HASHTAG_PATTERN.findall(text)
    cleaned = []
    seen: Set[str] = set()
    for match in matches:
        tag = f"#{match}"
        key = tag.lower()
        if key not in seen:
            cleaned.append(tag)
            seen.add(key)
    return cleaned


def wait_for_login() -> None:
    print("A browser window has opened.")
    print("Log into Instagram there if needed, then press Enter here to continue.")
    input()


def collect_post_links(page: Page, limit: int) -> List[str]:
    hrefs = page.locator("a").evaluate_all(
        """
        elements => elements
          .map(el => el.getAttribute('href'))
          .filter(Boolean)
        """
    )
    post_links: List[str] = []
    seen: Set[str] = set()
    for href in hrefs:
        if "/p/" not in href and "/reel/" not in href:
            continue
        absolute = href if href.startswith("http") else f"https://www.instagram.com{href}"
        if absolute not in seen:
            post_links.append(absolute)
            seen.add(absolute)
        if len(post_links) >= limit:
            break
    return post_links


def safe_page_text(page: Page) -> str:
    selectors = ["article", "main", "body"]
    for selector in selectors:
        try:
            text = page.locator(selector).inner_text(timeout=5000)
            if text:
                return text
        except TimeoutError:
            continue
    try:
        return page.locator("body").inner_text(timeout=5000)
    except TimeoutError:
        return ""


def observe_post(page: Page, post_url: str, source_type: str, source_value: str, hop_depth: int) -> List[Dict[str, str]]:
    page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2500)
    text = safe_page_text(page)
    hashtags = extract_hashtags(text)
    observations = []
    for tag in hashtags:
        observations.append(
            {
                "tag": tag,
                "language": detect_language(tag),
                "source_type": source_type,
                "source_value": source_value,
                "post_url": post_url,
                "hop_depth": str(hop_depth),
                "context_excerpt": text[:300].replace("\n", " ").strip(),
            }
        )
    return observations


def collect_from_profile(context: BrowserContext, handle: str, limit: int) -> List[Dict[str, str]]:
    page = context.new_page()
    profile_url = f"https://www.instagram.com/{handle}/"
    print(f"Collecting from profile: {profile_url}")
    page.goto(profile_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    post_links = collect_post_links(page, limit)
    observations: List[Dict[str, str]] = []
    for post_url in post_links:
        observations.extend(observe_post(page, post_url, "profile_post", handle, 0))
    page.close()
    return observations


def collect_from_hashtag(context: BrowserContext, hashtag: str, limit: int) -> List[Dict[str, str]]:
    page = context.new_page()
    slug = slugify_hashtag(hashtag)
    hashtag_url = f"https://www.instagram.com/explore/tags/{slug}/"
    print(f"Collecting from hashtag: #{slug}")
    page.goto(hashtag_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3500)
    post_links = collect_post_links(page, limit)
    observations: List[Dict[str, str]] = []
    for post_url in post_links:
        observations.extend(observe_post(page, post_url, "hashtag_page", f"#{slug}", 1))
    page.close()
    return observations


def write_raw_observations(rows: Iterable[Dict[str, str]]) -> None:
    rows = list(rows)
    fieldnames = [
        "tag",
        "language",
        "source_type",
        "source_value",
        "post_url",
        "hop_depth",
        "context_excerpt",
    ]
    with RAW_OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: Iterable[Dict[str, str]]) -> None:
    rows = list(rows)
    counter = Counter(row["tag"].lower() for row in rows)
    language_by_tag: Dict[str, str] = {}
    sources_by_tag: Dict[str, Set[str]] = {}
    canonical_tag: Dict[str, str] = {}

    for row in rows:
        key = row["tag"].lower()
        canonical_tag[key] = row["tag"]
        language_by_tag[key] = row["language"]
        sources_by_tag.setdefault(key, set()).add(f"{row['source_type']}:{row['source_value']}")

    fieldnames = ["tag", "language", "times_seen", "distinct_sources"]
    with SUMMARY_OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for key, times_seen in counter.most_common():
            writer.writerow(
                {
                    "tag": canonical_tag[key],
                    "language": language_by_tag.get(key, "unknown"),
                    "times_seen": times_seen,
                    "distinct_sources": len(sources_by_tag.get(key, set())),
                }
            )


def main() -> None:
    ensure_directories()
    targets = load_targets()
    handle = str(targets["profile_handle"])
    seed_hashtags = [str(tag) for tag in targets["seed_hashtags"]]
    profile_post_limit = int(targets.get("profile_post_limit", 8))
    hashtag_post_limit = int(targets.get("hashtag_post_limit", 6))

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(STATE_DIR),
            headless=False,
            viewport={"width": 1400, "height": 1000},
        )
        landing_page = context.new_page()
        landing_page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=30000)
        wait_for_login()
        landing_page.close()

        observations: List[Dict[str, str]] = []
        observations.extend(collect_from_profile(context, handle, profile_post_limit))
        for hashtag in seed_hashtags:
            observations.extend(collect_from_hashtag(context, hashtag, hashtag_post_limit))

        context.close()

    write_raw_observations(observations)
    write_summary(observations)

    print(f"Wrote {len(observations)} raw observations to {RAW_OUTPUT_PATH}")
    print(f"Wrote summary to {SUMMARY_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
