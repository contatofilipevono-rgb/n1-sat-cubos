# Blocos de dimensao quatro (n = 12, grau <= 4): espaco RS afim nas classes de V, pi, H e as partes q1, q2.
# x = (a, b), z = a + b, w = b.  w = s1*K1 + s2*K2 + sum u_i V_i.  Ponto y = (z, s1, s2) -> indice z + 64*s1 + 128*s2.
# Uso: python base4.py V1|V2
import itertools, pickle, os, sys
import numpy as np
N = 64
rot12 = lambda x: ((x << 1) | (x >> 11)) & 4095
X = np.arange(4096)
def orbitas(maxdeg=4):
    seen = set(); out = []
    for d in range(maxdeg + 1):
        for c in itertools.combinations(range(12), d):
            m = sum(1 << i for i in c)
            if m in seen: continue
            o = set(); y = m
            for _ in range(12): o.add(y); y = rot12(y)
            seen |= o; out.append((d, min(o), sorted(o)))
    return out
ORB = orbitas()
def tt_orb(o):
    t = np.zeros(4096, dtype=np.uint8)
    for m in o[2]: t ^= ((X & m) == m).astype(np.uint8)
    return t
IDX = np.array([[(z ^ w) | (w << 6) for w in range(N)] for z in range(N)])
packb = lambda a: int.from_bytes(np.packbits(np.asarray(a, dtype=np.uint8).reshape(-1)).tobytes(), "big")
def elim_comb(vecs):
    piv = {}; ind = []; ker = []
    for i, r in enumerate(vecs):
        comb = 1 << i
        while r:
            c = r.bit_length() - 1
            if c in piv: r ^= piv[c][0]; comb ^= piv[c][1]
            else: piv[c] = (r, comb); ind.append(1 << i); break
        else: ker.append(comb)
    return ind, ker
BASES = {"V1": [7, 14, 28, 56], "V2": [5, 10, 20, 40]}
def complemento(VB):
    piv = {}
    def add(v):
        while v:
            c = v.bit_length() - 1
            if c in piv: v ^= piv[c]
            else: piv[c] = v; return True
        return False
    for v in VB: add(v)
    K = []
    for i in range(6):
        if add(1 << i): K.append(1 << i)
    return K
if __name__ == "__main__":
    nome = sys.argv[1]; VB = BASES[nome]; K = complemento(VB)
    assert len(K) == 2
    TT = [tt_orb(o) for o in ORB]
    W = np.arange(N)
    def conds(t):
        F = t[IDX]; out = []
        for u1, u2 in itertools.combinations(VB, 2):
            out.append(F ^ F[:, W ^ u1] ^ F[:, W ^ u2] ^ F[:, W ^ u1 ^ u2])
        return packb(np.concatenate([o.reshape(-1) for o in out]))
    _, ker = elim_comb([conds(t) for t in TT])
    V = []
    for k in ker:
        t = np.zeros(4096, dtype=np.uint8)
        for i in range(len(ORB)):
            if k >> i & 1: t ^= TT[i]
        V.append(t)
    def pi_H(t):
        F = t[IDX]; P = np.zeros((256, 4), dtype=np.uint8); H = np.zeros(256, dtype=np.uint8)
        for z in range(N):
            for s1 in (0, 1):
                for s2 in (0, 1):
                    w0 = (K[0] * s1) ^ (K[1] * s2); y = z + 64 * s1 + 128 * s2
                    H[y] = F[z][w0]
                    for i in range(4): P[y][i] = F[z][w0 ^ VB[i]] ^ F[z][w0]
        return P, H
    PH = [pi_H(t) for t in V]
    _, kpi = elim_comb([packb(P) for P, H in PH])
    # partes: pi(z,s) = pi0(z) + s1 q1(z) + s2 q2(z)
    def qs(P):
        q1 = P[64:128] ^ P[0:64]; q2 = P[128:192] ^ P[0:64]
        assert np.array_equal(P[192:256], P[0:64] ^ q1 ^ q2)
        return q1, q2
    Q = [qs(P) for P, H in PH]
    _, kq = elim_comb([packb(np.concatenate([q1, q2])) for q1, q2 in Q])
    _, kq12 = elim_comb([packb(q1 ^ q2) for q1, q2 in Q])
    print(f"{nome}: base {VB}, complemento {K}")
    print("  dim do espaco RS afim em V:", len(V), "| dim de pi:", len(V) - len(kpi), "| nucleo de H:", len(kpi))
    print("  dim da imagem de (q1,q2):", len(V) - len(kq), "| dim da imagem de q1+q2:", len(V) - len(kq12))
    pickle.dump({"nome": nome, "VB": VB, "K": K, "V": V, "PH": PH}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"base_{nome}.pkl"), "wb"))
