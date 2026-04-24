import argparse
import csv
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.selector import RANKED_TAGS_PATH, SELECTION_COUNT, HashtagSelector  # noqa: E402


DEFAULT_SEED = 345
DEFAULT_WARMUP_ITERATIONS = 100
DEFAULT_MEASURED_ITERATIONS = 500
DEFAULT_SNAPSHOT_COUNT = 10
TOP_RANK_CUTOFF = 5
LOW_COUNT_THRESHOLD = 2
BOTTOM_SUMMARY_COUNT = 10
SIM_STATE_PATH = ROOT / ".tmp" / "selector_sim_state.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a non-mutating long-run selector simulation.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--warmup", type=int, default=DEFAULT_WARMUP_ITERATIONS)
    parser.add_argument("--iterations", type=int, default=DEFAULT_MEASURED_ITERATIONS)
    parser.add_argument("--snapshots", type=int, default=DEFAULT_SNAPSHOT_COUNT)
    parser.add_argument("--csv-output", type=Path, default=None)
    return parser.parse_args()


def ranks_for_details(details: Sequence[Dict[str, object]]) -> List[int]:
    return [int(detail["rank"]) for detail in details if detail.get("rank") is not None]


def tags_for_details(details: Sequence[Dict[str, object]]) -> List[str]:
    return [str(detail["tag"]) for detail in details]


def top_rank_bucket(count: int) -> str:
    if count >= 3:
        return "3+"
    return str(count)


def format_rank_list(ranks: Iterable[int]) -> str:
    ranks = list(ranks)
    return ", ".join(str(rank) for rank in ranks) if ranks else "none"


def write_csv_output(path: Path, selector: HashtagSelector, selected_counts: Counter[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "rank",
                "zero_based_rank",
                "tag",
                "base_score",
                "cooldown_min",
                "cooldown_max",
                "selected_count",
            ],
        )
        writer.writeheader()
        for record in selector.records:
            cooldown_min, cooldown_max = selector._cooldown_range(record.tag)
            writer.writerow(
                {
                    "rank": record.rank,
                    "zero_based_rank": record.rank - 1,
                    "tag": record.tag,
                    "base_score": f"{record.base_score:.3f}",
                    "cooldown_min": cooldown_min,
                    "cooldown_max": cooldown_max,
                    "selected_count": selected_counts[record.rank],
                }
            )


def main() -> None:
    args = parse_args()
    random.seed(args.seed)
    SIM_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        selector = HashtagSelector(ranked_tags_path=RANKED_TAGS_PATH, state_path=SIM_STATE_PATH)
        selector.reset()

        for _ in range(args.warmup):
            selector.next_selection(categories=[], forced_tag=None)

        selected_counts: Counter[int] = Counter()
        top_rank_distribution: Counter[str] = Counter()
        snapshots = []

        for measured_index in range(1, args.iterations + 1):
            result = selector.next_selection(categories=[], forced_tag=None)
            ranks = ranks_for_details(result.selected_details)
            tags = tags_for_details(result.selected_details)
            top_rank_count = sum(1 for rank in ranks if rank <= TOP_RANK_CUTOFF)

            selected_counts.update(ranks)
            top_rank_distribution.update([top_rank_bucket(top_rank_count)])

            if measured_index <= args.snapshots:
                snapshots.append(
                    {
                        "measured_index": measured_index,
                        "iteration": result.iteration,
                        "tags": tags,
                        "ranks": ranks,
                        "top_rank_count": top_rank_count,
                    }
                )

        expected_selection_slots = args.iterations * SELECTION_COUNT

        print("Selector Long-Run Simulation")
        print(f"Seed: {args.seed}")
        print(f"Active deck size: {selector.active_deck_size}")
        print(f"Warmup iterations: {args.warmup}")
        print(f"Measured iterations: {args.iterations}")
        print(f"Measured selection slots: {expected_selection_slots}")
        print()

        print("Snapshot selections after warmup")
        for snapshot in snapshots:
            tag_line = " ".join(snapshot["tags"])
            rank_line = ", ".join(str(rank) for rank in snapshot["ranks"])
            print(
                f"{snapshot['measured_index']:>2}. iteration {snapshot['iteration']}: "
                f"{tag_line} | ranks: {rank_line} | top-{TOP_RANK_CUTOFF}: {snapshot['top_rank_count']}"
            )
        print()

        print(f"Top-{TOP_RANK_CUTOFF} tags per measured selection")
        for bucket in ("0", "1", "2", "3+"):
            print(f"{bucket}: {top_rank_distribution[bucket]}")
        print()

        zero_selection_ranks = [
            record.rank
            for record in selector.records
            if selected_counts[record.rank] == 0
        ]
        low_selection_ranks = [
            record.rank
            for record in selector.records
            if selected_counts[record.rank] < LOW_COUNT_THRESHOLD
        ]
        bottom_records = selector.records[-BOTTOM_SUMMARY_COUNT:]

        print("Bottom-tag visibility")
        print(f"Ranks with 0 selections: {format_rank_list(zero_selection_ranks)}")
        print(f"Ranks with fewer than {LOW_COUNT_THRESHOLD} selections: {format_rank_list(low_selection_ranks)}")
        print(f"Bottom {BOTTOM_SUMMARY_COUNT} ranks:")
        for record in bottom_records:
            cooldown_min, cooldown_max = selector._cooldown_range(record.tag)
            print(
                f"{record.rank:>2} | {record.tag} | base {record.base_score:.3f} | "
                f"cooldown {cooldown_min}-{cooldown_max} | selected {selected_counts[record.rank]}"
            )
        print()

        print("Full rank frequency table")
        print("rank | tag | base | cooldown | selected")
        for record in selector.records:
            cooldown_min, cooldown_max = selector._cooldown_range(record.tag)
            print(
                f"{record.rank:>2} | {record.tag} | {record.base_score:.3f} | "
                f"{cooldown_min}-{cooldown_max} | {selected_counts[record.rank]}"
            )

        print()
        print(f"Diagnostic note: {expected_selection_slots} measured selections across {selector.active_deck_size} tags.")

        if args.csv_output:
            write_csv_output(args.csv_output, selector, selected_counts)
            print(f"CSV output: {args.csv_output}")
    finally:
        SIM_STATE_PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
