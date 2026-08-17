import pytest

from governed_banking_agent.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k_deduplicates_retrieved_documents() -> None:
    assert recall_at_k(["A", "A", "B"], {"A", "B"}, k=3) == 1.0


def test_precision_at_k_uses_available_results_as_denominator() -> None:
    assert precision_at_k(["A"], {"A", "B"}, k=5) == 1.0


def test_reciprocal_rank_returns_first_relevant_rank() -> None:
    assert reciprocal_rank(["X", "B", "A"], {"A", "B"}) == 0.5


def test_recall_rejects_empty_gold_set() -> None:
    with pytest.raises(ValueError, match="relevant must not be empty"):
        recall_at_k(["A"], set(), k=5)

