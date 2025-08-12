# python3
import sys


def inverse_bwt(bwt: str) -> str:
    """
    Inverse Burrows-Wheeler Transform using LF-mapping.
    Works in O(n) time and O(n) memory.
    """
    n = len(bwt)
    # Compute rank of each character occurrence in L (the BWT string)
    counts = {}
    ranks = [0] * n
    for i, ch in enumerate(bwt):
        counts.setdefault(ch, 0)
        counts[ch] += 1
        ranks[i] = counts[ch]  # rank (1-based) of ch at position i in L

    # Compute first occurrence of each character in F = sorted(L)
    chars = sorted(counts.keys())
    first = {}
    cum = 0
    for ch in chars:
        first[ch] = cum
        cum += counts[ch]

    # Start from the row corresponding to '$' in L
    # find index of the '$' in L (there is exactly one)
    idx = bwt.index('$')

    # Reconstruct text by repeatedly applying LF: idx = first[ch] + rank[idx] - 1
    res = []
    for _ in range(n - 1):
        ch = bwt[idx]
        idx = first[ch] + ranks[idx] - 1
        res.append(ch)

    # res currently holds characters in reverse order (from last to first),
    # so reverse and append '$' at the end
    text = ''.join(reversed(res)) + '$'
    return text


if __name__ == "__main__":
    transform = sys.stdin.readline().strip()
    print(inverse_bwt(transform))
