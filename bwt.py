# python3
import sys


def bwt(text: str) -> str:
    """
    Compute Burrows-Wheeler Transform by building all cyclic rotations
    and taking the last column after lexicographic sort.
    Works for |text| up to ~1000 comfortably.
    """
    n = len(text)
    rotations = [text[i:] + text[:i] for i in range(n)]
    rotations.sort()
    last_col = ''.join(row[-1] for row in rotations)
    return last_col


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    print(bwt(text))
