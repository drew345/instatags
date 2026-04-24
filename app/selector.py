import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RANKED_TAGS_PATH = DATA_DIR / "ranked_hashtags_v2.csv"
STATE_PATH = DATA_DIR / "selector_state.json"

SELECTION_COUNT = 5
DEFAULT_CATEGORIES: Tuple[str, ...] = ()
SIMILARITY_CATEGORIES = ("modeling", "acting", "drama", "senior", "casting", "commercial", "lifestyle")
REFERENCE_DECK_SIZE = 67
REFERENCE_SCORE_MIDPOINT = 30
REFERENCE_SCORE_SPREAD = 10


@dataclass(frozen=True)
class TagRecord:
    rank: int
    tag: str
    bucket: str
    categories: Tuple[str, ...]
    base_score: float


@dataclass
class SelectionResult:
    iteration: int
    categories: List[str]
    forced_tag: Optional[str]
    selected_tags: List[str]
    selected_details: List[Dict[str, object]]
    queue_head: List[str]


class HashtagSelector:
    def __init__(self, ranked_tags_path: Path = RANKED_TAGS_PATH, state_path: Path = STATE_PATH) -> None:
        self.ranked_tags_path = ranked_tags_path
        self.state_path = state_path
        self.records = self._load_ranked_tags()
        self.records_by_tag = {record.tag: record for record in self.records}
        self.base_queue = [record.tag for record in self.records]
        self._ensure_state()

    def _load_ranked_tags(self) -> List[TagRecord]:
        records: List[TagRecord] = []
        with self.ranked_tags_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            self.active_deck_size = len(rows)
            for row in rows:
                rank = int(row["rank"])
                categories = tuple(filter(None, row["categories"].split("|")))
                records.append(
                    TagRecord(
                        rank=rank,
                        tag=row["tag"],
                        bucket=row["bucket"],
                        categories=categories,
                        base_score=self._score_for_rank(rank),
                    )
                )
        return records

    def _score_for_rank(self, rank: int) -> float:
        score_midpoint = self._scale_rank_parameter(REFERENCE_SCORE_MIDPOINT)
        score_spread = self._scale_rank_parameter(REFERENCE_SCORE_SPREAD)
        return round(1 / (1 + math.exp((rank - score_midpoint) / score_spread)), 3)

    def _scale_rank_parameter(self, reference_value: float) -> float:
        return reference_value * (self.active_deck_size / REFERENCE_DECK_SIZE)

    def _ensure_state(self) -> None:
        if self.state_path.exists():
            return
        self._write_state({"iteration": 0, "queue": self.base_queue})

    def _read_state(self) -> Dict[str, object]:
        try:
            with self.state_path.open("r", encoding="utf-8") as fh:
                content = fh.read().strip()
            if not content:
                raise ValueError("Empty selector state")
            return self._normalize_state(json.loads(content))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            state = {"iteration": 0, "queue": self.base_queue}
            self._write_state(state)
            return state

    def _normalize_state(self, state: Dict[str, object]) -> Dict[str, object]:
        try:
            iteration = int(state.get("iteration", 0))
        except (TypeError, ValueError):
            iteration = 0

        queue = state.get("queue", [])
        if not isinstance(queue, list):
            queue = []

        seen = set()
        normalized_queue = []
        for tag in queue:
            if not isinstance(tag, str) or tag not in self.records_by_tag or tag in seen:
                continue
            normalized_queue.append(tag)
            seen.add(tag)

        for tag in self.base_queue:
            if tag not in seen:
                normalized_queue.append(tag)
                seen.add(tag)

        normalized_state = {"iteration": iteration, "queue": normalized_queue}
        if normalized_state != state:
            self._write_state(normalized_state)
        return normalized_state

    def _write_state(self, state: Dict[str, object]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.state_path.with_name(f"{self.state_path.name}.tmp")
        with temp_path.open("w", encoding="utf-8") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=2)
        temp_path.replace(self.state_path)

    def reset(self) -> Dict[str, object]:
        state = {"iteration": 0, "queue": self.base_queue}
        self._write_state(state)
        return state

    def preview(self, iterations: int, categories: Sequence[str], forced_tag: Optional[str]) -> List[SelectionResult]:
        state = self._read_state()
        queue = list(state["queue"])
        iteration = int(state["iteration"])
        previews: List[SelectionResult] = []
        for _ in range(iterations):
            iteration += 1
            selected, details = self._select_tags(queue, categories, forced_tag)
            queue = self._apply_cooldown(queue, selected, iteration)
            previews.append(
                SelectionResult(
                    iteration=iteration,
                    categories=list(categories),
                    forced_tag=forced_tag,
                    selected_tags=selected,
                    selected_details=details,
                    queue_head=queue[:12],
                )
            )
        return previews

    def next_selection(self, categories: Sequence[str], forced_tag: Optional[str]) -> SelectionResult:
        state = self._read_state()
        queue = list(state["queue"])
        iteration = int(state["iteration"]) + 1
        selected, details = self._select_tags(queue, categories, forced_tag)
        new_queue = self._apply_cooldown(queue, selected, iteration)
        self._write_state({"iteration": iteration, "queue": new_queue})
        return SelectionResult(
            iteration=iteration,
            categories=list(categories),
            forced_tag=forced_tag,
            selected_tags=selected,
            selected_details=details,
            queue_head=new_queue[:12],
        )

    def _select_tags(self, queue: List[str], categories: Sequence[str], forced_tag: Optional[str]) -> Tuple[List[str], List[Dict[str, object]]]:
        normalized_categories = self._normalize_categories(categories)
        forced_tag = self._normalize_forced_tag(forced_tag)
        scored_queue = self._score_queue(queue, normalized_categories)
        selected: List[str] = []
        selected_details: List[Dict[str, object]] = []

        if forced_tag:
            selected.append(forced_tag)
            selected_details.append(
                {
                    "tag": forced_tag,
                    "source": "forced",
                    "base_score": None,
                    "effective_score": None,
                    "categories": [],
                    "rank": None,
                }
            )

        for detail in scored_queue:
            if len(selected) >= SELECTION_COUNT:
                break
            tag = detail["tag"]
            if tag in selected:
                continue
            if self._is_too_similar(tag, selected):
                continue
            selected.append(tag)
            selected_details.append(detail)

        return selected[:SELECTION_COUNT], selected_details[:SELECTION_COUNT]

    def _normalize_categories(self, categories: Sequence[str]) -> List[str]:
        normalized = [category.strip().lower() for category in categories if category and category.strip()]
        return normalized

    def _normalize_forced_tag(self, forced_tag: Optional[str]) -> Optional[str]:
        if not forced_tag:
            return None
        forced_tag = forced_tag.strip()
        if not forced_tag:
            return None
        if not forced_tag.startswith("#"):
            forced_tag = f"#{forced_tag}"
        return forced_tag

    def _score_queue(self, queue: Sequence[str], categories: Sequence[str]) -> List[Dict[str, object]]:
        scored: List[Dict[str, object]] = []
        for queue_index, tag in enumerate(queue):
            record = self.records_by_tag.get(tag)
            if not record:
                continue
            category_matches = len(set(record.categories) & set(categories))
            category_shift = category_matches * 3
            bucket_shift = {"targeted": 1, "broad": 0, "reserve": -1}.get(record.bucket, 0)
            priority_position = queue_index - category_shift - bucket_shift
            effective_score = record.base_score + (category_matches * 0.08) + (0.02 if record.bucket == "targeted" else 0.0)
            scored.append(
                {
                    "tag": record.tag,
                    "rank": record.rank,
                    "base_score": round(record.base_score, 3),
                    "effective_score": round(effective_score, 3),
                    "priority_position": priority_position,
                    "bucket": record.bucket,
                    "categories": list(record.categories),
                    "category_matches": category_matches,
                    "queue_index": queue_index,
                    "source": "ranked",
                }
            )
        scored.sort(
            key=lambda item: (
                item["priority_position"],
                -item["effective_score"],
                -item["base_score"],
            )
        )
        return scored

    def _is_too_similar(self, candidate_tag: str, selected_tags: Sequence[str]) -> bool:
        candidate_record = self.records_by_tag.get(candidate_tag)
        candidate_categories = set(candidate_record.categories) if candidate_record else set()
        for selected in selected_tags:
            selected_record = self.records_by_tag.get(selected)
            if not selected_record:
                continue
            if candidate_tag == selected:
                return True
            if candidate_categories and set(selected_record.categories):
                overlap = candidate_categories & set(selected_record.categories)
                if len(overlap) >= 4:
                    return True
            if self._normalized_tag(candidate_tag) == self._normalized_tag(selected):
                return True
        return False

    def _normalized_tag(self, tag: str) -> str:
        return tag.lstrip("#").lower()

    def _apply_cooldown(self, queue: List[str], selected_tags: Sequence[str], _iteration: int) -> List[str]:
        remaining = [tag for tag in queue if tag not in selected_tags]
        cooldowns: List[Tuple[int, int, str]] = []
        for selection_index, tag in enumerate(selected_tags):
            if tag not in self.records_by_tag:
                continue
            cooldown_position = self._cooldown_position(tag)
            cooldowns.append((cooldown_position, selection_index, tag))

        for cooldown_position, _, tag in sorted(cooldowns):
            insert_index = min(cooldown_position - 1, len(remaining))
            remaining.insert(insert_index, tag)
        return remaining

    def _cooldown_position(self, tag: str) -> int:
        minimum, maximum = self._cooldown_range(tag)
        return random.randint(minimum, maximum)

    def _cooldown_range(self, tag: str) -> Tuple[int, int]:
        record = self.records_by_tag[tag]
        score = max(0.0, min(record.base_score, 1.0))
        deck_size = max(self.active_deck_size, 1)

        minimum = deck_size * (0.5 - 0.375 * score)
        maximum_uncapped = deck_size * (1.5 - (7 / 6) * score)
        maximum = min(maximum_uncapped, deck_size)

        minimum_position = self._clamp_cooldown_position(math.ceil(minimum))
        maximum_position = self._clamp_cooldown_position(math.floor(maximum))
        if maximum_position < minimum_position:
            maximum_position = minimum_position
        return minimum_position, maximum_position

    def _clamp_cooldown_position(self, position: int) -> int:
        return max(1, min(position, self.active_deck_size))


def serialize_selection(result: SelectionResult) -> Dict[str, object]:
    return {
        "iteration": result.iteration,
        "categories": result.categories,
        "forced_tag": result.forced_tag,
        "selected_tags": result.selected_tags,
        "selected_details": result.selected_details,
        "queue_head": result.queue_head,
    }
