EXACT = "exact"
SUBSTITUTION = "substitution"
DELETION = "deletion"
INSERTION = "insertion"


def calculate_score(
    input_length: int,
    match_type: str,
    error_position: int | None = None
) -> int:
    """Calculate the score defined by the autocomplete assignment."""
    base_score = input_length * 2

    if match_type == EXACT:
        return base_score

    if error_position is None:
        return 0

    if match_type == SUBSTITUTION:
        penalty = max(1, 5 - error_position)
    elif match_type in (DELETION, INSERTION):
        penalty = max(2, 10 - 2 * error_position)
    else:
        return 0

    return base_score - penalty
