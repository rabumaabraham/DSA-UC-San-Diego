# python3
import sys
from collections import defaultdict


def sort_characters(string):
    order = [0] * len(string)
    count = defaultdict(lambda: 0)
    for i in range(len(string)):
        count[string[i]] += 1
    keys = sorted(count.keys())
    prev_key = keys[0]
    for key in keys[1:]:
        count[key] += count[prev_key]
        prev_key = key
    for i in range(len(string) - 1, -1, -1):
        c = string[i]
        count[c] += -1
        order[count[c]] = i
    return order


def compute_char_classes(string, order):
    char_class = [0] * len(string)
    char_class[order[0]] = 0
    for i in range(1, len(string)):
        if string[order[i]] != string[order[i - 1]]:
            char_class[order[i]] = char_class[order[i - 1]] + 1
        else:
            char_class[order[i]] = char_class[order[i - 1]]
    return char_class


def sort_doubled(string, length, order, char_class):
    n = len(string)
    count = [0] * n
    new_order = [0] * n
    for i in range(n):
        count[char_class[i]] += 1
    for j in range(1, n):
        count[j] += count[j - 1]
    for i in range(n - 1, -1, -1):
        start = (order[i] - length + n) % n
        c = char_class[start]
        count[c] += -1
        new_order[count[c]] = start
    return new_order


def update_classes(new_order, char_class, length):
    n = len(new_order)
    new_class = [0] * n
    new_class[new_order[0]] = 0
    for i in range(1, n):
        cur, prev = new_order[i], new_order[i - 1]
        mid, mid_prev = cur + length, (prev + length) % n
        if char_class[cur] != char_class[prev] or char_class[mid] != char_class[mid_prev]:
            new_class[cur] = new_class[prev] + 1
        else:
            new_class[cur] = new_class[prev]
    return new_class


def build_suffix_array(string):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically the smallest
    suffix of text starts.
    """
    order = sort_characters(string)
    char_class = compute_char_classes(string, order)
    length = 1
    while length < len(string):
        order = sort_doubled(string, length, order, char_class)
        char_class = update_classes(order, char_class, length)
        length *= 2
    return order


def PreprocessBWT(text, order):
    n = len(text)
    bwt = [''] * n
    for i in range(n):
        bwt[i] = text[(order[i] + n - 1) % n]
    counts = defaultdict(lambda: 0)
    occ_count_before = defaultdict(lambda: defaultdict(lambda: 0))
    for index, letter in enumerate(bwt):
        counts[letter] += 1
        for let, count in sorted(counts.items()):
            occ_count_before[let][index + 1] = count
    starts = defaultdict(lambda: 0)
    total = 0
    for letter, count in sorted(counts.items()):
        starts[letter] = total
        total += count
    return starts, occ_count_before


def readData():
    reads = sys.stdin.read().strip().split()
    # Don't remove duplicates as they might be important for assembly
    return reads


def hamming_distance(s1, s2):
    """Compute Hamming distance between two strings of equal length"""
    if len(s1) != len(s2):
        return float('inf')
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def find_occurrences_with_errors(text, patterns, max_error_rate=0.05):
    order = build_suffix_array(text)
    starts, counts = PreprocessBWT(text, order)
    l = len(text) - 1
    occs = defaultdict(lambda: [])
    k = 12
    for i, p in enumerate(patterns):
        pattern = p[:k]
        top = 0
        bottom = len(text) - 1
        while top <= bottom:
            if pattern:
                symbol = pattern[-1]
                pattern = pattern[:-1]
                if counts[symbol][bottom + 1] - counts[symbol][top] > 0:
                    top = starts[symbol] + counts[symbol][top]
                    bottom = starts[symbol] + counts[symbol][bottom + 1] - 1
                else:
                    break
            else:
                for j in range(top, bottom + 1):
                    if not order[j] in occs:
                        occs[order[j]] = []
                    occs[order[j]].append(i)
                break
    
    # Find the best overlap considering errors
    best_overlap = 0
    best_index = 0
    
    for pos, iList in sorted(occs.items()):
        for i in iList:
            suffix = text[pos:-1]
            prefix = patterns[i][:l - pos]
            
            if len(suffix) == len(prefix) and len(suffix) > 0:
                # Check if overlap is acceptable with error tolerance
                max_errors = int(len(suffix) * max_error_rate)
                if hamming_distance(suffix, prefix) <= max_errors:
                    if len(suffix) > best_overlap:
                        best_overlap = len(suffix)
                        best_index = i

    return best_index, best_overlap


def assembly_with_errors(reads, max_error_rate=0.05):
    if not reads:
        return ""
    
    genome = reads[0]
    currInd = 0
    firstRead = reads[currInd]
    
    while len(reads) > 1:
        currRead = reads[currInd]
        del reads[currInd]
        if not reads:  # If no reads left, break
            break
        currInd, overlap = find_occurrences_with_errors(currRead + '$', reads, max_error_rate)
        genome += reads[currInd][overlap:]
    
    # Handle circular genome - check overlap with first read
    if reads and firstRead:
        currInd, overlap = find_occurrences_with_errors(reads[0] + '$', [firstRead], max_error_rate)
        if overlap > 0:
            return genome[:-overlap]
    
    return genome


def Solution():
    reads = readData()
    genome = assembly_with_errors(reads, max_error_rate=0.05)
    print(genome)


if __name__ == '__main__':
    Solution()