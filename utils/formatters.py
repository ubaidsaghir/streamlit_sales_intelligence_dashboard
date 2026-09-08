from pathlib import Path


def compact_filename(filename: str, max_length: int = 28) -> str:
    """Shorten a long filename while preserving its extension."""
    filename = str(filename)
    if len(filename) <= max_length:
        return filename

    path = Path(filename)
    suffix = path.suffix
    stem = path.stem
    available_length = max_length - len(suffix) - 1

    if available_length < 10:
        return filename[: max_length - 1] + "…"

    left_length = available_length // 2
    right_length = available_length - left_length
    return f"{stem[:left_length]}…{stem[-right_length:]}{suffix}"
