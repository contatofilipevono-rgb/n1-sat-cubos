"""Busca DIRIGIDA de trios com beta=0 (caso misto do Lema L, F4+F4), 09/11.
Para cada par (a,b) em N com a+b em N e beta(a,b)=0 (obtidos de N∩S, S aleatorio de dim s), o terceiro vetor c
precisa de beta(a,c)=beta(b,c)=0: 20 condicoes LINEARES em c -> subespaco C_ab de L/G (dim ~20). Varre C_ab
exaustivamente: c em N, c+a em N, c+b em N, c+a+b em N (filtros em cascata, em blocos). Saida: trios + contagens.
Uso: python sete_beta2.py S SEED [max_pares] [max_trios]."""
import os, sys, json, time, itertools
import numpy as np
from sete_beta import F40, F56, comp, anf, beta, bits56, Bk, elim, L3, AQUI

def em_N_blocos(xs, bloco_u=48, bloco_x=1 << 16):
    out = np.zeros(len(xs), dtype=bool)
    for i0 in range(0, len(xs), bloco_x):
        x0 = xs[i0:i0 + bloco_x]
        vivo = np.arange(len(x0))
        for u0 in range(0, F40.shape[0], bloco_u):
            if not len(vivo): break
            x = x0[vivo]; F = F40[u0:u0 + bloco_u]
            z = np.ones((len(x), len(F)), dtype=bool)
            for j in range(7):
                z &= (np.bitwise_count(x[:, None] & F[None, :, j]) & 1) == 0
            vivo = vivo[~z.any(1)]
        out[i0 + vivo] = True
    return out

# beta em coordenadas de L/G (40): B40_k = C^T B_k C, C = imagens (56) da base canonica de L/G
C = np.array([bits56(anf(1 << k)) for k in range(40)], dtype=np.int64).T  # 56 x 40
B40 = np.stack([(C.T @ Bk[k].astype(np.int64) @ C) % 2 for k in range(10)])  # 10 x 40 x 40

def vec40(x):
    return np.array([(x >> k) & 1 for k in range(40)], dtype=np.int64)

def nucleo40(rows):
    """base (inteiros de 40 bits) de {c : <r,c>=0 para r em rows} sobre F2."""
    piv = {}
    for r in rows:
        v = int(r)
        for h, pv in piv.items():
            if (v >> h) & 1: v ^= pv
        if v:
            h = v.bit_length() - 1
            for h2 in list(piv):
                if (piv[h2] >> h) & 1: piv[h2] ^= v
            piv[h] = v
    base = []
    for f in [c for c in range(40) if c not in piv]:
        w = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1: w |= 1 << h
        base.append(w)
    return base

def span_arr(base):
    d = len(base); h = d // 2
    lo = np.zeros(1 << h, dtype=np.uint64); hi = np.zeros(1 << (d - h), dtype=np.uint64)
    for k in range(h): lo[(np.arange(1 << h) >> k) & 1 == 1] ^= np.uint64(base[k])
    for k in range(d - h): hi[(np.arange(1 << (d - h)) >> k) & 1 == 1] ^= np.uint64(base[h + k])
    return (lo[None, :] ^ hi[:, None]).ravel()

if __name__ == "__main__":
    s, seed = int(sys.argv[1]), int(sys.argv[2])
    maxp = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
    maxt = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    rng = np.random.default_rng(seed)
    while True:
        base = [int(x) for x in rng.integers(1, 1 << 40, size=s, dtype=np.uint64)]
        if len(elim(base, 40)) == s: break
    t0 = time.time()
    xs = span_arr(base)
    bm = em_N_blocos(xs); bm[0] = False
    I = np.nonzero(bm)[0]; P = len(I)
    Xv = xs[I]  # vetores 40-bit dos elementos de N∩S
    print(f"|N∩S| = {P} ({time.time()-t0:.0f}s)", flush=True)
    # pares (a,b) com a+b em N∩S e beta = 0
    pos = {int(v): k for k, v in enumerate(Xv)}
    pares = []
    Mcoord = np.array([vec40(b) for b in base], dtype=np.int64).T  # 40 x s
    BS = [(Mcoord.T @ B40[k] @ Mcoord) % 2 for k in range(10)]
    def bits_s(ix):
        return ((ix[:, None] >> np.arange(s)[None, :]) & 1).astype(np.int64)
    for a in range(P):
        sa = I[a]
        viz = np.nonzero(bm[I ^ sa])[0]
        viz = viz[viz > a]
        if not len(viz): continue
        va = bits_s(np.array([sa]))
        vb = bits_s(I[viz])
        bz = np.zeros(len(viz), dtype=bool)
        for k in range(10):
            bz |= ((vb @ (va @ BS[k]).T).ravel() % 2) == 1
        for b in viz[~bz]:
            pares.append((int(Xv[a]), int(Xv[b])))
        if len(pares) >= maxp: break
    print(f"pares com beta=0: {len(pares)} ({time.time()-t0:.0f}s)", flush=True)
    trios, stats = [], []
    for ip, (a, b) in enumerate(pares):
        va, vb = vec40(a), vec40(b)
        rows = [int(sum(int(x) << k for k, x in enumerate((va @ B40[kk]) % 2))) for kk in range(10)] + \
               [int(sum(int(x) << k for k, x in enumerate((vb @ B40[kk]) % 2))) for kk in range(10)]
        nb = nucleo40(rows)
        cs = span_arr(nb)
        m = em_N_blocos(cs); cs = cs[m]
        n1 = len(cs)
        for t in (a, b, a ^ b):
            if len(cs): cs = cs[em_N_blocos(cs ^ np.uint64(t))]
        cs = cs[(cs != np.uint64(a)) & (cs != np.uint64(b)) & (cs != np.uint64(a ^ b))]
        stats.append((len(nb), n1, len(cs)))
        if len(cs):
            c = int(cs[0])
            p = [anf(a), anf(b), anf(c)]
            combos = {}
            for v in range(1, 8):
                q = 0
                for k in range(3):
                    if (v >> k) & 1: q ^= p[k]
                combos[v] = int(((np.bitwise_count(np.uint64(q) & F56) & 1) == 0).all(1).sum())
            bet = [beta(p[0], p[1]), beta(p[0], p[2]), beta(p[1], p[2])]
            trios.append({"x40": [a, b, c], "phi_mascaras": [[L3[k] for k in range(56) if (q >> k) & 1] for q in p],
                          "isotropicos_por_combinacao": combos, "beta_pares": bet, "n_c": int(len(cs))})
            print(f"TRIO no par {ip}: n_c={len(cs)} isotropicos {combos} beta {bet}", flush=True)
            if len(trios) >= maxt: break
        if ip % 50 == 0:
            print(f"   par {ip}/{len(pares)}: dim C_ab={len(nb)}, c em N: {n1}, sobreviventes: {len(cs)} ({time.time()-t0:.0f}s)", flush=True)
    json.dump({"s": s, "seed": seed, "N_S": P, "pares_beta0": len(pares), "pares_varridos": len(stats),
               "stats_dimC_cN_sobrev": stats, "trios": trios},
              open(os.path.join(AQUI, f"trio_beta2_s{s}_seed{seed}.json"), "w"))
    print(f"FIM: pares varridos {len(stats)}, trios {len(trios)} ({time.time()-t0:.0f}s)", flush=True)
