"""(10/11) Confere (C'): RS bent g em n=2m => soma de (-1)^g sobre cada coclasse {x: x1+x2=w} de E é 0 quando wt(w) != m (mod 2)."""
import numpy as np, itertools, sys
sys.stdout.reconfigure(encoding="utf-8")
def testa(n, DMAX):
    N = 1 << n; m = n // 2; rot = lambda q: ((q << 1) | (q >> (n - 1))) & (N - 1)
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
    w = (pts & ((1 << m) - 1)) ^ (pts >> m)
    par = np.array([bin(int(v)).count("1") & 1 for v in w])
    K = len(orbs); L = 1 << 14; tot = 0; maxv = 0; outros = set()
    for s in range(0, 1 << K, L):
        idx = np.arange(s, min(s + L, 1 << K))
        bits = ((idx[:, None] >> np.arange(K)[None, :]) & 1).astype(np.uint8)
        tt = (bits @ OT) & 1; S = 1 - 2 * tt.astype(np.int32)
        a = S.copy(); hh = 1
        while hh < N:
            a = a.reshape(a.shape[0], -1, 2, hh); x0 = a[:, :, 0, :].copy(); y0 = a[:, :, 1, :]
            a[:, :, 0, :] = x0 + y0; a[:, :, 1, :] = x0 - y0; a = a.reshape(a.shape[0], N); hh *= 2
        Sb = S[np.all(np.abs(a) == 2 ** m, axis=1)]; tot += len(Sb)
        for wv in range(1 << m):
            sm = Sb[:, w == wv].sum(axis=1)
            if (bin(wv).count("1") - m) % 2: maxv = max(maxv, int(np.abs(sm).max(initial=0)))
            else: outros |= set(np.abs(sm).tolist())
    print(f"n={n}: RS bent {tot}; max |soma| nas coclasses de paridade != m: {maxv}; valores |soma| nas outras: {sorted(outros)}")
testa(6, 3); testa(8, 4); testa(10, 3)
