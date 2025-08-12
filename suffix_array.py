# python3
import sys


def build_suffix_array(text):
    """
    Build suffix array by sorting suffixes (works for |text| <= 10000).
    Returns list of starting positions.
    """
    n = len(text)
    suff = list(range(n))
    suff.sort(key=lambda i: text[i:])
    return suff


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    sa = build_suffix_array(text)
    print(' '.join(map(str, sa)))
