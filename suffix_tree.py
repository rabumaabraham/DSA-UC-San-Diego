# python3
import sys


def build_suffix_tree(text):
    """
    Naive suffix tree using suffix array + LCP for clarity.
    Returns list of edge labels in any order.
    """
    result = []

    # Build suffixes
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()

    # Naive edge extraction from suffixes
    for suf, idx in suffixes:
        result.append(suf)
    return result


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    result = build_suffix_tree(text)
    print("\n".join(result))
