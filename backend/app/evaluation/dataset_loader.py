import json
from pathlib import Path


DATASET_PATH = (
    Path(__file__).resolve().parents[3]
    / "evaluation"
    / "datasets"
    / "research_questions.json"
)


def load_evaluation_dataset() -> list[dict]:
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def get_evaluation_case(case_id: str) -> dict | None:
    dataset = load_evaluation_dataset()

    for case in dataset:
        if case["id"] == case_id:
            return case

    return None