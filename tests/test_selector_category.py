import json
import tempfile
import unittest
from pathlib import Path

from app.selector import RANKED_TAGS_PATH, SELECTION_COUNT, HashtagSelector


ROOT = Path(__file__).resolve().parents[1]
SAVED_STATE_PATH = ROOT / "data" / "selector_state.json"


class CategorySelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.selector = HashtagSelector(
            ranked_tags_path=RANKED_TAGS_PATH,
            state_path=Path(self.temp_dir.name) / "selector_state.json",
        )

    def saved_queue(self):
        with SAVED_STATE_PATH.open("r", encoding="utf-8") as fh:
            return list(json.load(fh)["queue"])

    def lookbook_count(self, details):
        return sum(1 for detail in details if "lookbook" in detail.get("categories", []))

    def select(self, queue, forced_text=""):
        forced_tags = self.selector._normalize_forced_tags(forced_text)
        return self.selector._select_tags(queue, ["lookbook"], forced_tags)

    def test_lookbook_focus_raises_three_category_tags_from_deeper_queue(self):
        selected, details, deck_tags = self.select(self.saved_queue())

        self.assertEqual(SELECTION_COUNT, len(selected))
        self.assertEqual(SELECTION_COUNT, len(deck_tags))
        self.assertEqual(3, self.lookbook_count(details))

    def test_forced_tags_reduce_category_target_to_remaining_slots(self):
        cases = [
            ("one two", 3),
            ("one two three", 2),
            ("one two three four", 1),
            ("one two three four five", 0),
        ]

        for forced_text, expected_lookbook_count in cases:
            with self.subTest(forced_text=forced_text):
                selected, details, deck_tags = self.select(self.saved_queue(), forced_text)

                self.assertEqual(SELECTION_COUNT, len(selected))
                self.assertEqual(max(0, SELECTION_COUNT - len(forced_text.split())), len(deck_tags))
                self.assertEqual(expected_lookbook_count, self.lookbook_count(details))

    def test_category_tags_already_in_normal_picks_count_toward_target(self):
        lookbook_tags = [
            record.tag
            for record in self.selector.records
            if "lookbook" in record.categories
        ]
        non_lookbook_tags = [
            record.tag
            for record in self.selector.records
            if "lookbook" not in record.categories
        ]
        queue = lookbook_tags[:1] + non_lookbook_tags + lookbook_tags[1:]

        selected, details, deck_tags = self.select(queue)

        self.assertEqual(SELECTION_COUNT, len(selected))
        self.assertEqual(SELECTION_COUNT, len(deck_tags))
        self.assertEqual(3, self.lookbook_count(details))

    def test_forced_tag_matching_ranked_tag_stays_outside_deck(self):
        forced_ranked_tag = next(
            record.tag
            for record in self.selector.records
            if "lookbook" in record.categories
        )

        selected, details, deck_tags = self.select(self.saved_queue(), forced_ranked_tag)

        self.assertEqual(forced_ranked_tag, selected[0])
        self.assertNotIn(forced_ranked_tag, deck_tags)
        self.assertEqual(3, self.lookbook_count([detail for detail in details if detail.get("source") == "ranked"]))


if __name__ == "__main__":
    unittest.main()
