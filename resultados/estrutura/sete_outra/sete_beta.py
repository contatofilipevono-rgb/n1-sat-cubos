"""Trios em L/G (F4+F4) com beta = 0 dois a dois e as 7 combinacoes em N, por enumeracao exata num subespaco
aleatorio S (dim s) de L/G. Base: sete.py / sete3.py da sessao 849f53da (N∩S exato, somas por XOR de indices).
Filtro novo (09/11, sessao d3ee3672): beta(a,b) = a∧b mod J, J = T∧Λ², 10 funcionais (Λ⁶/J), pares e trios.
Uso: python sete_beta.py S SEED [max_trios]. Saida: trio_beta_s<S>_seed<SEED>.json (com conferencias independentes)."""
import itertools, json, os, sys, time
import numpy as np
from sete import AQUI, L3, elim, T_BRIEF

D = np.load(os.path.join(AQUI, "base.npz"))
F40, F56, comp = D["F40"], D["F56"], [int(x) for x in D["comp"]]
pc = lambda x: bin(x).count("1")
T = sorted(T_BRIEF)
seis = [m for m in range(256) if pc(m) == 6]
i6 = {m: k for k, m in enumerate(seis)}
J = []
for q in (m for m in range(256) if pc(m) == 2):
    r = 0
    for t in T:
        if not (t & q):
            r ^= 1 << i6[t | q]
    J.append(r)
assert len(elim(J, 28)) == 18
# anulador de J em F2^28 (10 funcionais)
def anul(vecs, dim):
    rows = []
    for v in vecs:
        for r in rows:
            if v & (1 << (r.bit_length() - 1)): v ^= r
        if v: rows.append(v)
    # forma reduzida
    rows.sort(reverse=True)
    piv = {}
    for v in rows:
        for h, pv in list(piv.items()):
            if (v >> h) & 1: v ^= pv
        h = v.bit_length() - 1
        for h2 in list(piv):
            if (piv[h2] >> h) & 1: piv[h2] ^= v
        piv[h] = v
    out = []
    for f in [c for c in range(dim) if c not in piv]:
        w = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1: w |= 1 << h
        out.append(w)
    return out
FJ = anul(J, 28)
assert len(FJ) == 10 and all(pc(f & j) % 2 == 0 for f in FJ for j in J)
# matrizes B_k (56x56) de beta: B_k[p,q] = f_k(m_p ∪ m_q) se disjuntos (p != q)
Bk = np.zeros((10, 56, 56), dtype=np.uint8)
for p in range(56):
    for q in range(56):
        if p != q and not (L3[p] & L3[q]):
            for k in range(10):
                Bk[k, p, q] = (FJ[k] >> i6[L3[p] | L3[q]]) & 1
def bits56(v):
    return np.array([(v >> k) & 1 for k in range(56)], dtype=np.uint8)
def anf(x40):
    v = 0
    for k in range(40):
        if (x40 >> k) & 1: v ^= comp[k]
    return v
def beta(a56, b56):
    a, b = bits56(a56), bits56(b56)
    return [int(a @ Bk[k] @ b) % 2 for k in range(10)]
# controle: posto de beta em Λ²(L/G) = 10
base40 = [anf(1 << k) for k in range(40)]
img = [sum(v << k for k, v in enumerate(beta(base40[i], base40[j]))) for i, j in itertools.combinations(range(40), 2)]
assert len(elim(img, 10)) == 10, "controle posto beta"
print("controles: dim J = 18, posto beta = 10", flush=True)


def em_N(xs, bloco=48):
    vivo = np.arange(len(xs))
    for u0 in range(0, F40.shape[0], bloco):
        if not len(vivo): break
        x = xs[vivo]; F = F40[u0:u0 + bloco]
        z = np.ones((len(x), len(F)), dtype=bool)
        for j in range(7):
            z &= (np.bitwise_count(x[:, None] & F[None, :, j]) & 1) == 0
        vivo = vivo[~z.any(1)]
    m = np.zeros(len(xs), dtype=bool); m[vivo] = True
    return m


if __name__ == "__main__":
    s, seed = int(sys.argv[1]), int(sys.argv[2])
    maxt = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    rng = np.random.default_rng(seed)
    while True:
        base = [int(x) for x in rng.integers(1, 1 << 40, size=s, dtype=np.uint64)]
        if len(elim(base, 40)) == s: break
    h = s // 2
    lo = np.zeros(1 << h, dtype=np.uint64); hi = np.zeros(1 << (s - h), dtype=np.uint64)
    for k in range(h): lo[(np.arange(1 << h) >> k) & 1 == 1] ^= np.uint64(base[k])
    for k in range(s - h): hi[(np.arange(1 << (s - h)) >> k) & 1 == 1] ^= np.uint64(base[h + k])
    t0 = time.time()
    bm = np.zeros(1 << s, dtype=bool)
    for j in range(len(hi)):
        bm[(j << h):((j + 1) << h)] = em_N(lo ^ hi[j])
    bm[0] = False
    I = np.nonzero(bm)[0]; P = len(I)
    print(f"|N∩S| = {P} de 2^{s} ({time.time()-t0:.0f}s)", flush=True)
    # beta em coordenadas de S: B^S_k = M^T B_k M, M = matriz 56 x s das imagens da base de S
    Ms = np.array([bits56(anf(b)) for b in base], dtype=np.int64).T  # 56 x s
    BS = [(Ms.T @ Bk[k].astype(np.int64) @ Ms) % 2 for k in range(10)]  # s x s
    Ibits = ((I[:, None] >> np.arange(s)[None, :]) & 1).astype(np.int64)  # P x s
    def beta_S(ia, ib):  # vetores de indices (bits em S)
        va = ((ia[:, None] >> np.arange(s)[None, :]) & 1).astype(np.int64)
        vb = ((ib[:, None] >> np.arange(s)[None, :]) & 1).astype(np.int64)
        return np.stack([((va @ BS[k]) * vb).sum(1) % 2 for k in range(10)], 1)  # n x 10
    pos = np.full(1 << s, -1, dtype=np.int64); pos[I] = np.arange(P)
    sols, npares, npares_b = [], 0, 0
    for a in range(P):
        viz = np.nonzero(bm[I ^ I[a]])[0]
        viz = viz[viz > a]
        if not len(viz): continue
        npares += len(viz)
        bz = beta_S(np.full(len(viz), I[a]), I[viz]).any(1)
        viz = viz[~bz]
        npares_b += len(viz)
        for b in viz:
            ab = I[a] ^ I[b]
            # c com a+c, b+c, a+b+c em N e c em N
            cand = np.nonzero(bm[I ^ I[a]] & bm[I ^ I[b]] & bm[I ^ ab])[0]
            cand = cand[(cand != a) & (cand != b) & (cand != pos[ab])]
            if not len(cand): continue
            ok = ~(beta_S(np.full(len(cand), I[a]), I[cand]).any(1) | beta_S(np.full(len(cand), I[b]), I[cand]).any(1))
            for c in cand[ok][:1]:
                sols.append((int(I[a]), int(I[b]), int(I[c])))
        if len(sols) >= maxt: break
    print(f"pares em N com soma em N: {npares}; com beta=0: {npares_b}; trios com beta=0: {len(sols)} ({time.time()-t0:.0f}s)", flush=True)
    out = []
    for (ia, ib, ic) in sols[:maxt]:
        x = [int(lo[i & ((1 << h) - 1)] ^ hi[i >> h]) for i in (ia, ib, ic)]
        p = [anf(v) for v in x]
        combos = {}
        for v in range(1, 8):
            q = 0
            for k in range(3):
                if (v >> k) & 1: q ^= p[k]
            combos[v] = int(((np.bitwise_count(np.uint64(q) & F56) & 1) == 0).all(1).sum())
        bet = [beta(p[0], p[1]), beta(p[0], p[2]), beta(p[1], p[2])]
        out.append({"x40": x, "phi_56": p, "phi_mascaras": [[L3[k] for k in range(56) if (q >> k) & 1] for q in p],
                    "isotropicos_por_combinacao": combos, "beta_pares": bet})
        print("TRIO: isotropicos", combos, "beta", bet, flush=True)
    json.dump({"s": s, "seed": seed, "N_S": P, "pares": npares, "pares_beta0": npares_b, "trios": out},
              open(os.path.join(AQUI, f"trio_beta_s{s}_seed{seed}.json"), "w"), indent=1)
