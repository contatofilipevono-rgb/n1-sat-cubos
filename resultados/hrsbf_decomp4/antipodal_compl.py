"""(10/11) Conjectura: RS bent g em n variáveis => g(x)+g(x+1) = n/2 (mod 2) para todo x em Fix(rho^{n/2})
(vetores antipodais x_i = x_{i+n/2}).  Exaustivo: n=6 (grau<=3), n=8 (grau<=4), n=10 (grau<=3)."""
import numpy as np, itertools, sys
sys.stdout.reconfigure(encoding="utf-8")
def testa(n, DMAX):
    N = 1 << n; rot = lambda m: ((m << 1) | (m >> (n - 1))) & (N - 1)
    orbs, vis = [], set()
    for d in range(1, DMAX + 1):
        for c in itertools.combinations(range(n), d):
            m = sum(1 << i for i in c)
            if m in vis: continue
            o = {m}; x = m
            for _ in range(n): x = rot(x); o.add(x)
            vis |= o; orbs.append(sorted(o))
    pts = np.arange(N); h = n // 2
    OT = np.zeros((len(orbs), N), dtype=np.uint8)
    for k, o in enumerate(orbs):
        for m in o: OT[k] ^= ((pts & m) == m).astype(np.uint8)
    fix = [y | (y << h) for y in range(1 << h)]
    K = len(orbs); L = 1 << 14; tot = 0; Dset = {x: set() for x in fix}
    for s in range(0, 1 << K, L):
        idx = np.arange(s, min(s + L, 1 << K))
        bits = ((idx[:, None] >> np.arange(K)[None, :]) & 1).astype(np.uint8)
        tt = (bits @ OT) & 1
        a = (1 - 2 * tt.astype(np.int32)); hh = 1
        while hh < N:
            a = a.reshape(a.shape[0], -1, 2, hh); x0 = a[:, :, 0, :].copy(); y0 = a[:, :, 1, :]
            a[:, :, 0, :] = x0 + y0; a[:, :, 1, :] = x0 - y0; a = a.reshape(a.shape[0], N); hh *= 2
        bent = np.all(np.abs(a) == 2 ** h, axis=1)
        tb = tt[bent]; tot += len(tb)
        for x in fix:
            for v in np.unique(tb[:, x] ^ tb[:, x ^ (N - 1)]): Dset[x].add(int(v))
    viol = {f"{x:0{n}b}"[::-1]: sorted(v) for x, v in Dset.items() if v != {h % 2}}
    print(f"n={n} grau<={DMAX}: RS bent {tot}; pontos de Fix(rho^{h}): {len(fix)}; esperado D={h%2}; violações: {viol or 'nenhuma'}", flush=True)
testa(6, 3); testa(8, 4); testa(10, 3)
