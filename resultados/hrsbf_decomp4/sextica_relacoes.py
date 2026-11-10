import itertools, sys, os
sys.stdout.reconfigure(encoding="utf-8")
N = 12; MASK = (1 << N) - 1
rot = lambda m, j=1: ((m << j) | (m >> (N - j))) & MASK if j % N else m
def orbs(d):
    rem = set(sum(1 << i for i in c) for c in itertools.combinations(range(N), d)); out = []
    while rem:
        r = min(rem); o = {rot(r, j) for j in range(N)}; out.append(o); rem -= o
    return out
UPPER = orbs(5) + orbs(6); TOP = orbs(4)
ix = lambda L, s: next(i for i, o in enumerate(L) if sum(1 << k for k in s) in o)
b012, b024, b013, b023 = (ix(UPPER, s) for s in ({0,1,2,6,7,8}, {0,2,4,6,8,10}, {0,1,3,6,7,9}, {0,2,3,6,8,9}))
b03 = ix(TOP, {0,3,6,9}); assert b03 == 42
print("índices UPPER:", b012, b024, b013, b023, "de", len(UPPER))
d = sys.argv[1]
for f in ("two-sextic-bent.tsv", "su6-bent.tsv"):
    L = [l.split() for l in open(os.path.join(d, f)) if l.strip()]
    if f == "su6-bent.tsv": print(f, "(2 colunas: sem máscara alta; pular)"); continue
    from collections import Counter
    c = Counter()
    for r in L:
        h, t = int(r[0]), int(r[1]); bit = lambda v, i: v >> i & 1
        c[(bit(t, 42), bit(h, b012) ^ bit(h, b024), bit(h, b013) ^ bit(h, b023), bit(h, b012), bit(h, b013))] += 1
    print(f, len(L), "linhas; (b03, b012+b024, b013+b023, b012, b013):", dict(c))
