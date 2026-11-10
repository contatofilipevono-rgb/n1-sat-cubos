"""(10/11) Mecanismo de (C'): para RS bent g em n=2m e coclasse w (wt(w) != m mod 2), g_w(y)=g(y, y+w) em F^m.
Pergunta: existe e com g_w(y+e) = g_w(y)+1 para todo y?  Quais e (dependem só de w?)."""
import numpy as np, itertools, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
def rs_bent(n, DMAX):
    N = 1 << n; rot = lambda q: ((q << 1) | (q >> (n - 1))) & (N - 1)
    orbs, vis = [], set()
    for d in range(1, DMAX + 1):
        for c in itertools.combinations(range(n), d):
            q = sum(1 << i for i in c)
            if q in vis: continue
            o = {q}; x = q
            for _ in range(n): x = rot(x); o.add(x)
            vis |= o; orbs.append(sorted(o))
    pts = np.arange(N)
    OT = np.zeros((len(orbs), N), dtype=np.uint8)
    for k, o in enumerate(orbs):
        for q in o: OT[k] ^= ((pts & q) == q).astype(np.uint8)
    K = len(orbs); L = 1 << 14; out = []
    for s in range(0, 1 << K, L):
        idx = np.arange(s, min(s + L, 1 << K))
        bits = ((idx[:, None] >> np.arange(K)[None, :]) & 1).astype(np.uint8)
        tt = (bits @ OT) & 1; a = 1 - 2 * tt.astype(np.int32); hh = 1
        while hh < N:
            a = a.reshape(a.shape[0], -1, 2, hh); x0 = a[:, :, 0, :].copy(); y0 = a[:, :, 1, :]
            a[:, :, 0, :] = x0 + y0; a[:, :, 1, :] = x0 - y0; a = a.reshape(a.shape[0], N); hh *= 2
        out.append(tt[np.all(np.abs(a) == 2 ** (n // 2), axis=1)])
    return np.concatenate(out)
def analisa(n, DMAX):
    m = n // 2; M = 1 << m; B = rs_bent(n, DMAX)
    y = np.arange(M)
    falhas = 0; tot = 0; Es = defaultdict(Counter); sempre = {}
    for w in range(M):
        if (bin(w).count("1") - m) % 2 == 0: continue
        idx = y | ((y ^ w) << m)               # x = (y, y+w): bits 0..m-1 = x1 = y, bits m.. = x2
        G = B[:, idx]                           # (#bent, M)
        cand = None
        for row in G:
            es = frozenset(e for e in range(1, M) if np.all(row[y ^ e] != row))
            tot += 1
            if not es: falhas += 1
            Es[w][es] += 1
            cand = es if cand is None else cand & es
        sempre[w] = sorted(cand)
    print(f"n={n}: bent {len(B)}; pares (g,w) proibidos {tot}; sem e anti-invariante: {falhas}")
    fmt = lambda v: f"{v:0{m}b}"[::-1]
    for w in sorted(sempre):
        print(f"  w={fmt(w)}: e comuns a todas as bent: {[fmt(e) for e in sempre[w]]}; nº de conjuntos distintos {len(Es[w])}")
analisa(6, 3); analisa(8, 4); analisa(10, 3)
