import numpy as np, sys, itertools
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
exec(open("resultados/hrsbf_decomp4/afim_coclasse.py", encoding="utf-8-sig").read().split("for n, D in")[0])
# controle: RS genéricas de grau <= 4 em n=8 (todas as 2^22), grau de g_w e existência de e anti nas coclasses proibidas
n, m, M = 8, 4, 16
N = 1 << n; rot = lambda q: ((q << 1) | (q >> (n - 1))) & (N - 1)
orbs, vis = [], set()
for d in range(1, 5):
    for c in itertools.combinations(range(n), d):
        q = sum(1 << i for i in c)
        if q in vis: continue
        o = {q}; x = q
        for _ in range(n): x = rot(x); o.add(x)
        vis |= o; orbs.append(sorted(o))
pts = np.arange(N); OT = np.zeros((len(orbs), N), dtype=np.uint8)
for k, o in enumerate(orbs):
    for q in o: OT[k] ^= ((pts & q) == q).astype(np.uint8)
rng = np.random.default_rng(0); bits = rng.integers(0, 2, (20000, len(orbs))).astype(np.uint8)
T = (bits @ OT) & 1; y = np.arange(M); cg = Counter(); anti_ok = 0; tot = 0
for w in range(M):
    if bin(w).count("1") % 2 == 0: continue
    G = T[:, y | ((y ^ w) << m)]
    cg.update(grau_lote(G).tolist())
    A = np.zeros(len(G), bool)
    for e in range(1, M): A |= np.all(G[:, y ^ e] != G, axis=1)
    anti_ok += int(A.sum()); tot += len(G)
print("RS genérica grau<=4, n=8: grau de g_w nas proibidas:", dict(sorted(cg.items())), "| com e anti:", anti_ok, "de", tot)
