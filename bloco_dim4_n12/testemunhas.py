# Testemunhas: para um mapa de cada familia, escolhe uma fase, reconstroi f em F2^12 e confere
# RS, grau exatamente 4, os 4096 coeficientes de Walsh, afinidade em V e nao afinidade em U.
# Uso: python testemunhas.py V2 <codigo> [<codigo> ...]     (precisa de gens_<V>.pkl, gerado por base4.py + exporta.py)
import pickle, os, sys, json
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
nome = sys.argv[1]
g = pickle.load(open(os.path.join(here, f"gens_{nome}.pkl"), "rb"))
GL, GH, KH, VB, K = g["GL"], g["GH"], g["KH"], g["VB"], g["K"]
n = len(GL); nk = len(KH); KHm = np.array(KH, dtype=np.uint8)
par = lambda x: bin(x).count("1") & 1
rot12 = lambda x: ((x << 1) | (x >> 11)) & 4095
def fwht(a):
    a = np.array(a, dtype=np.int64); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h); x = a[:, 0, :].copy(); y = a[:, 1, :].copy()
        a[:, 0, :] = x + y; a[:, 1, :] = x - y; a = a.reshape(-1); h *= 2
    return a
def anf(t):
    a = np.array(t, dtype=np.uint8).copy(); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h); a[:, 1, :] ^= a[:, 0, :]; a = a.reshape(-1); h *= 2
    return a
# coordenadas de w na base (K1, K2, V1..V4)
coord = {}
for s1 in (0, 1):
    for s2 in (0, 1):
        for u in range(16):
            w = (K[0] * s1) ^ (K[1] * s2)
            for i in range(4):
                if u >> i & 1: w ^= VB[i]
            coord[w] = (s1, s2, u)
assert len(coord) == 64
out = []
for c in map(int, sys.argv[2:]):
    L = np.zeros(256, dtype=np.uint8); H0 = np.zeros(256, dtype=np.uint8)
    for j in range(n):
        if c >> j & 1: L ^= GL[j]; H0 ^= GH[j]
    fib = [np.nonzero(L == l)[0] for l in range(16)]
    achou = None
    rng = np.random.default_rng(c)
    for _ in range(200000):
        t = rng.integers(0, 2, nk, dtype=np.uint8)
        H = H0 ^ ((t.astype(np.int32) @ KHm.astype(np.int32)) & 1).astype(np.uint8)
        if all(int(H[P].sum()) % 4 == 2 for P in fib):
            ok = True
            for P in fib:
                for i in range(8):
                    sel = P[((P >> i) & 1) == 1]
                    if (int(H[sel].sum()) & 1) != ((len(sel) // 2) & 1): ok = False
            if ok: achou = H; break
    assert achou is not None, "nenhuma fase encontrada por sorteio"
    H = achou
    tt = np.zeros(4096, dtype=np.uint8)
    for z in range(64):
        for w in range(64):
            s1, s2, u = coord[w]; y = z + 64 * s1 + 128 * s2
            tt[(z ^ w) | (w << 6)] = par(int(L[y]) & u) ^ int(H[y])
    W = fwht(1 - 2 * tt.astype(np.int64))
    assert np.all(np.abs(W) == 64), "nao bent"
    assert all(tt[rot12(x)] == tt[x] for x in range(4096)), "nao RS"
    a = anf(tt); deg = max(bin(m).count("1") for m in range(4096) if a[m]); assert deg == 4
    F = lambda z, w: int(tt[(z ^ w) | (w << 6)])
    d2 = lambda x1, x2: any(F(z, w) ^ F(z, w ^ x1) ^ F(z, w ^ x2) ^ F(z, w ^ x1 ^ x2) for z in range(64) for w in range(64))
    assert not any(d2(VB[i], VB[j]) for i in range(4) for j in range(i))
    UB = [(1 << i) | 32 for i in range(5)]
    afimU = not any(d2(UB[i], UB[j]) for i in range(5) for j in range(i))
    print(f"codigo {c}: bent (4096 coeficientes +-64), RS, grau 4, afim em V; afim em U: {afimU}")
    out.append({"codigo": c, "anf_monomios": [int(m) for m in range(4096) if a[m]], "afim_em_U": afimU})
json.dump(out, open(os.path.join(here, f"testemunhas_{nome}.json"), "w"))
