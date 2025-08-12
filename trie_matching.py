# python3
import sys

NA = -1

def build_trie(patterns):
    # Map A,C,G,T to 0..3
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    class Node:
        def __init__(self):
            self.next = [NA] * 4
            self.patternEnd = False

    trie = [Node()]
    for pattern in patterns:
        current = 0
        for ch in pattern:
            idx = mapping[ch]
            if trie[current].next[idx] == NA:
                trie[current].next[idx] = len(trie)
                trie.append(Node())
            current = trie[current].next[idx]
        trie[current].patternEnd = True
    return trie

def prefix_trie_matching(text, trie):
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    idx = 0
    current = 0
    while True:
        if trie[current].patternEnd:
            return True
        if idx < len(text):
            symbol = text[idx]
            next_index = trie[current].next[mapping[symbol]]
            if next_index != NA:
                current = next_index
                idx += 1
            else:
                return False
        else:
            return False

def solve(text, n, patterns):
    result = []
    trie = build_trie(patterns)
    for i in range(len(text)):
        if prefix_trie_matching(text[i:], trie):
            result.append(i)
    return result

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    n = int(sys.stdin.readline().strip())
    patterns = [sys.stdin.readline().strip() for _ in range(n)]
    ans = solve(text, n, patterns)
    sys.stdout.write(' '.join(map(str, ans)) + '\n')
