import gzip
from typing import List


def write_compressed(path: str, lines: List[str]) -> None:
    with gzip.open(path, "at", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")