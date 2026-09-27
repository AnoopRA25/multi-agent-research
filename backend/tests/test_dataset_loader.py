from backend.app.evaluation.dataset_loader import (
    get_evaluation_case,
    load_evaluation_dataset,
)


def test_evaluation_dataset_loads():
    dataset = load_evaluation_dataset()

    assert isinstance(dataset, list)
    assert len(dataset) == 20


def test_evaluation_cases_have_required_fields():
    dataset = load_evaluation_dataset()

    for case in dataset:
        assert "id" in case
        assert "question" in case
        assert "criteria" in case

        assert isinstance(case["id"], str)
        assert isinstance(case["question"], str)
        assert isinstance(case["criteria"], list)

        assert len(case["criteria"]) > 0


def test_evaluation_case_ids_are_unique():
    dataset = load_evaluation_dataset()

    ids = [case["id"] for case in dataset]

    assert len(ids) == len(set(ids))


def test_get_evaluation_case():
    case = get_evaluation_case("eval_001")

    assert case is not None
    assert case["id"] == "eval_001"
    assert "question" in case
    assert "criteria" in case