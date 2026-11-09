"""Filtro necessario para f = g + h com g,h bent (Lema 7 de Kepes et al., SEM supor simetria).

Se f=g+h, S=supp f, e T subconjunto com |T|=t<=m (n=2m):
    2^(m-t)  divide  N_T - 2 Z_T,   N_T=#{v in S: v>=T},  Z_T=#{v in S: v>=T, g(v)=1}.
O filtro pergunta se existe g|S em {0,1}^S satisfazendo TODAS essas congruencias (ILP via scipy.milp).
Infactivel  => f NAO e soma de duas bent.  Factivel => inconclusivo.
"""
import itertools, sys, random
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def subsets_upto(n, m):
    return [T for t in range(m + 1) for T in itertools.combinations(range(n), t)]

def feasible(tt, n, tmax=None, time_limit=20):
    m = n // 2; tmax = m if tmax is None else tmax
    S = np.nonzero(tt)[0]; ns = len(S)
    if ns == 0: return True
    Ts = [T for T in subsets_upto(n, tmax)]
    masks = np.array([sum(1 << i for i in T) for T in Ts])
    inc = ((S[None, :] & masks[:, None]) == masks[:, None]).astype(np.int64)      # |Ts| x ns
    N = inc.sum(1); mods = np.array([1 << (m - len(T)) for T in Ts])
    # variaveis: g_v (ns binarias) , k_T (inteiros)  ;  2*inc@g + mods*k = N
    nT = len(Ts)
    A = np.hstack([2 * inc, np.diag(mods)]).astype(float)
    ub_k = (N // mods) + 1
    lb = np.concatenate([np.zeros(ns), -ub_k]); ub = np.concatenate([np.ones(ns), ub_k])
    res = milp(c=np.zeros(ns + nT), constraints=LinearConstraint(A, N.astype(float), N.astype(float)),
               integrality=np.ones(ns + nT), bounds=Bounds(lb, ub), options={"time_limit": time_limit})
    if res.status == 0: return True
    if res.status == 2: return False
    return None   # tempo esgotado

# ---------- utilidades ----------
def anf_tt(n, monos):
    idx = np.arange(1 << n); tt = np.zeros(1 << n, dtype=np.uint8)
    for S in monos:
        mk = sum(1 << i for i in S); tt ^= ((idx & mk) == mk).astype(np.uint8)
    return tt

def walsh(tt):
    a = (1 - 2 * tt.astype(np.int64)); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h)
        a = np.stack([a[:, 0] + a[:, 1], a[:, 0] - a[:, 1]], 1).reshape(-1); h *= 2
    return a

def mm_bent(m, rng):
    n = 2 * m; N = 1 << m; pi = list(range(N)); rng.shuffle(pi)
    h = [rng.randint(0, 1) for _ in range(N)]; tt = np.zeros(1 << n, dtype=np.uint8)
    for v in range(1 << n):
        X, Y = v & (N - 1), v >> m
        tt[v] = (bin(Y & pi[X]).count("1") + h[X]) & 1
    return tt

def sigma(n, js):
    from math import comb
    w = np.array([bin(v).count("1") for v in range(1 << n)])
    out = np.zeros(1 << n, dtype=np.uint8)
    for j in js: out ^= np.array([comb(x, j) & 1 for x in range(n + 1)], dtype=np.uint8)[w]
    return out

def rot_orbits(n, d):
    seen, orbs = set(), []
    for S in itertools.combinations(range(n), d):
        if S in seen: continue
        orb = {tuple(sorted((i + r) % n for i in S)) for r in range(n)}
        seen |= orb; orbs.append(sorted(orb))
    return orbs

if __name__ == "__main__":
    rng = random.Random(5)
    # 1) validacao n=4 exaustiva: soma de bent => factivel (nunca infactivel)
    n = 4; N = 16
    def w4(t):
        return walsh(np.array([(t >> i) & 1 for i in range(N)], dtype=np.uint8))
    bent4 = [t for t in range(1 << N) if np.all(np.abs(w4(t)) == 4)]
    sums = {a ^ b for a in bent4 for b in bent4}
    bad = sum(1 for f in sums if feasible(np.array([(f >> i) & 1 for i in range(N)], dtype=np.uint8), 4) is False)
    print(f"[n=4] somas={len(sums)} infactiveis(deveria ser 0)={bad}")
    nao = [f for f in range(1 << N) if f not in sums]
    # o que o filtro pega entre os nao-somas de grau<=2?
    cnt = {True: 0, False: 0, None: 0}
    for f in random.Random(1).sample(nao, 400):
        cnt[feasible(np.array([(f >> i) & 1 for i in range(N)], dtype=np.uint8), 4)] += 1
    print(f"[n=4] nao-somas amostrados (400): factivel={cnt[True]} infactivel={cnt[False]} tempo={cnt[None]}")
    # 2) n=8: somas reais passam; Feng f8 e Kepes F8 devem ser barrados
    for _ in range(5):
        g, h = mm_bent(4, rng), mm_bent(4, rng)
    ok = [feasible(mm_bent(4, rng) ^ mm_bent(4, rng), 8) for _ in range(5)]
    print("[n=8] somas MM+MM (factivel esperado):", ok)
    f8 = anf_tt(8, [(0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7)])
    F8 = sigma(8, [0, 2, 4])
    print("[n=8] Feng f8 (nao-soma):", feasible(f8, 8), "| Kepes F8 (nao-soma):", feasible(F8, 8))
