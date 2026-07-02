RANK_THRESHOLDS: list[tuple[int, str]] = [
    (50, "Guardian of the Garden"),
    (25, "Habitat Hero"),
    (10, "Wildlife Guardian"),
    (5, "Nature Ally"),
    (2, "Garden Friend"),
    (1, "Tiny Helper"),
    (0, "Garden Visitor"),
]


def get_rank(points: int) -> str:
    for threshold, rank in RANK_THRESHOLDS:
        if points >= threshold:
            return rank
    return "Garden Visitor"
