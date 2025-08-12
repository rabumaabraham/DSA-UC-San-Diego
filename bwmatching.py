# python3
import sys


def preprocess_bwt(bwt):
    """
    Preprocess BWT (Last column) to compute:
      - first_occurrence: dict char -> first index in FirstColumn (sorted L)
      - occ_counts_before: dict char -> list of length n+1 where occ_counts_before[c][i]
                           = count of c in L[0:i] (i.e., first i chars)
    This lets us compute Count(symbol, i) quickly and implement BetterBWMatching.
    """
    n = len(bwt)
    # Alphabet includes '$' and A,C,G,T (but we build just for chars present)
    alphabet = sorted(set(bwt))  # usually ['$','A','C','G','T']
    # Build occ_counts_before
    occ_counts_before = {ch: [0] * (n + 1) for ch in alphabet}
    for i, ch in enumerate(bwt):
        for c in alphabet:
            occ_counts_before[c][i + 1] = occ_counts_before[c][i]
        occ_counts_before[ch][i + 1] += 1

    # First column is sorted(bwt). Compute first_occurrence map
    sorted_chars = sorted(bwt)
    first_occurrence = {}
    for i, ch in enumerate(sorted_chars):
        if ch not in first_occurrence:
            first_occurrence[ch] = i

    return first_occurrence, occ_counts_before


def count_occurrences(pattern, bwt, first_occurrence, occ_counts_before):
    """
    BetterBWMatching to count occurrences of pattern in original text using BWT.
    Returns integer count.
    """
    top = 0
    bottom = len(bwt) - 1
    pat = pattern
    while top <= bottom:
        if pat:
            symbol = pat[-1]
            pat = pat[:-1]
            # Check if symbol occurs between top and bottom in last column
            # Count of symbol in L[0:top] and L[0:bottom+1]
            if symbol not in occ_counts_before:
                return 0
            top_count = occ_counts_before[symbol][top]
            bottom_count = occ_counts_before[symbol][bottom + 1]
            if bottom_count - top_count > 0:
                top = first_occurrence[symbol] + top_count
                bottom = first_occurrence[symbol] + bottom_count - 1
            else:
                return 0
        else:
            return bottom - top + 1
    return 0


if __name__ == "__main__":
    data = sys.stdin.read().split()
    # Input formats can vary: often it's
    # line1: BWT(Text)
    # line2: n
    # line3: p1 p2 ... pn   (or patterns may be on next lines)
    # We'll parse defensively.
    if not data:
        sys.exit(0)
    bwt = data[0]
    if len(data) == 1:
        # no patterns
        print()
        sys.exit(0)
    # Next token is n
    n = int(data[1])
    patterns = data[2:2 + n]
    # If patterns are fewer, maybe they were separated across lines, but we read all tokens so it's fine.

    first_occurrence, occ_counts_before = preprocess_bwt(bwt)
    answers = []
    for pat in patterns:
        cnt = count_occurrences(pat, bwt, first_occurrence, occ_counts_before)
        answers.append(str(cnt))
    print(' '.join(answers))
