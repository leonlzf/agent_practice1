def _unique_ranked(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    if not relevant:
        raise ValueError("relevant must not be empty")
    top_k = set(_unique_ranked(retrieved)[:k])
    return len(top_k & relevant) / len(relevant)


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    top_k = _unique_ranked(retrieved)[:k]
    if not top_k:
        return 0.0
    return sum(item in relevant for item in top_k) / len(top_k)


def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    for rank, item in enumerate(_unique_ranked(retrieved), start=1):
        if item in relevant:
            return 1.0 / rank
    return 0.0

