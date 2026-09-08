from __future__ import annotations

from pathlib import Path


def generate_sample_dataset() -> None:
    """Placeholder script for generating or refreshing the CSV dataset."""
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Dataset directory ready: {data_dir}")


if __name__ == "__main__":
    generate_sample_dataset()
