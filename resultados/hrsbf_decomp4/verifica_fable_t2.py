import csv, os, sys, itertools, numpy as np
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
exec(open("fix_restricoes_n12.py", encoding="utf-8-sig").read().split("def periodicos")[0])
ix = lambda s: next(i for i, o in enumerate(TOP) if sum(1 << k for k in s) in o)
b1, b2, b3 = ix({0,1,6,7}), ix({0,2,6,8}), ix({0,3,6,9})
c = Counter()
for r in csv.DictReader(open(os.path.join(sys.argv[1], "catalog-index.tsv")), delimiter="\t"):
    if int(r["count"]) == 0: continue
    t = int(r["top"]); c[(t >> b1 & 1, t >> b2 & 1, t >> b3 & 1)] += 1
print("Teorema 2 no catálogo grau<=4 (b013=b023=0 lá): (b1,b2,b3) dos representantes com bent:", dict(c))
# Sêxticas do Astra: b1,b2,b3 no topo (col 1) e b013,b023 na máscara alta (col 0)
UP = []
def orbs(d):
    rem = set(sum(1 << i for i in cc) for cc in itertools.combinations(range(12), d)); out = []
    while rem:
        r0 = min(rem); o = {rot(r0, j) for j in range(12)}; out.append(o); rem -= o
    return out
UP = orbs(5) + orbs(6); iu = lambda s: next(i for i, o in enumerate(UP) if sum(1 << k for k in s) in o)
u013, u023 = iu({0,1,3,6,7,9}), iu({0,2,3,6,8,9})
c2 = Counter()
for l in open(os.path.join(sys.argv[1], "two-sextic-bent.tsv")):
    if not l.strip(): continue
    h, t = map(int, l.split()[:2])
    c2[((t >> b1 ^ t >> b2 ^ t >> b3) & 1) == ((h >> u013 ^ h >> u023) & 1)] += 1
print("Teorema 2 nas sêxticas (vale?):", dict(c2))
# (c): RS bent em 6 variáveis: b1+b2+b3+b013+b023
m = 6; M = 64; pts = np.arange(M); r6 = lambda q: ((q << 1) | (q >> 5)) & 63
def orb6(d):
    out, vis = [], set()
    for cc in itertools.combinations(range(6), d):
        q = sum(1 << i for i in cc)
        if q in vis: continue
        o = {q}; x = q
        for _ in range(6): x = r6(x); o.add(x)
        vis |= o; out.append((cc, sorted(o)))
    return out
O = orb6(1) + orb6(2) + orb6(3); nm = [cc for cc, _ in O]
cols = [np.bitwise_xor.reduce([((pts & q) == q).astype(np.int64) for q in o]) for _, o in O]
cnt = Counter(); nb = 0
for s in range(1 << len(O)):
    tt = np.zeros(M, np.int64)
    for k in range(len(O)):
        if s >> k & 1: tt ^= cols[k]
    a = 1 - 2 * tt; h = 1
    while h < M:
        a = a.reshape(-1, 2, h); x0 = a[:, 0, :].copy(); y0 = a[:, 1, :]; a[:, 0, :] = x0 + y0; a[:, 1, :] = x0 - y0; a = a.reshape(-1); h *= 2
    if np.all(np.abs(a) == 8):
        nb += 1; g = lambda cc: s >> nm.index(cc) & 1
        cnt[(g((0,1)) + g((0,2)) + g((0,3)) + g((0,1,3)) + g((0,1,4))) % 2] += 1
print(f"RS bent em 6 variáveis (sem constante): {nb}; b1+b2+b3+b013+b023 mod 2:", dict(cnt))

