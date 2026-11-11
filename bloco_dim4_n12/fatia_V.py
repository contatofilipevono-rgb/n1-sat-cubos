# Condicao necessaria na fatia z em V, a partir apenas das somas de funcoes de grau <= 2 nas fibras.
# Para z = x em V os quatro pontos (x, s) tem rotulos g(x) + s_r A(x) + s_s E(x)  (complemento dual), g = pi0|V.
# De m = (1+r)(1+s), (1+r)s_r, (1+s)s_s e (1+r) z_i sai, para cada rotulo:
#   (P1) as quatro contagens a^s = #{x em V : g + s_r A + s_s E = rotulo} tem a mesma paridade;
#   (P2) a soma dos x sobre as quatro pre-imagens e zero.
# Este script percorre todas as classes de q e todos os g possiveis e diz quais classes passam.
# Uso: python fatia_V.py V1|V2      (precisa de gens_<V>.pkl; leve)
import pickle, os, sys, collections
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
nome = sys.argv[1]
g = pickle.load(open(os.path.join(here, f"gens_{nome}.pkl"), "rb")); GL, n0, nq = g["GL"], g["n0"], g["nq"]
par = lambda x: bin(x).count("1") & 1
rm, sm = (21, 42) if nome == "V2" else (27, 54)
Vs = [z for z in range(64) if par(z & rm) == 0 and par(z & sm) == 0]
assert len(Vs) == 16
def partes(L):
    """rotulos em V nas quatro fatias de s, no complemento dual"""
    g0 = L[0:64][Vs]; k1 = L[64:128][Vs] ^ g0; k2 = L[128:192][Vs] ^ g0
    A = k1; E = k2 if nome == "V2" else (k1 ^ k2)
    return g0, A, E
# espaco das restricoes g = pi0|V
G = []
piv = {}
for j in range(n0):
    g0, A, E = partes(GL[j]); assert not A.any() and not E.any()
    v = int.from_bytes(bytes(g0), "big"); w = v
    while w:
        c = w.bit_length() - 1
        if c in piv: w ^= piv[c]
        else: piv[c] = w; G.append(g0.copy()); break
dV = len(G)
print(f"{nome}: dimensao do espaco de g = pi0|V: {dV}")
allg = np.zeros((1, 16), dtype=np.uint8)
for gg in G: allg = np.concatenate([allg, allg ^ gg], axis=0)
xs = np.array(Vs, dtype=np.int64)
res = collections.Counter(); passam = []
for qc in range(1 << nq):
    L = np.zeros(256, dtype=np.uint8)
    for j in range(nq):
        if qc >> j & 1: L ^= GL[n0 + j]
    g0, A, E = partes(L)
    tipo = "A=E=0" if not A.any() and not E.any() else ("A=E" if np.array_equal(A, E) else "A!=E")
    base = allg ^ g0                                    # todos os g desta classe
    ok = np.ones(len(base), dtype=bool)
    par_cnt = []; mom = np.zeros((len(base), 16), dtype=np.int64)
    for (sr, ss_) in ((0, 0), (1, 0), (0, 1), (1, 1)):
        lab = base ^ (A if sr else 0) ^ (E if ss_ else 0)
        onehot = (lab[:, :, None] == np.arange(16)[None, None, :])           # g x ponto x rotulo
        par_cnt.append(onehot.sum(axis=1) & 1)
        m = np.zeros((len(base), 16), dtype=np.int64)
        for i in range(16): m ^= np.where(onehot[:, i, :], xs[i], 0)
        mom ^= m
    for k in range(1, 4): ok &= (par_cnt[k] == par_cnt[0]).all(axis=1)
    p1 = int(ok.sum())
    ok &= (mom == 0).all(axis=1)
    p2 = int(ok.sum())
    res[(tipo, p1 > 0, p2 > 0)] += 1
    if p2: passam.append(qc)
print("(tipo de (A,E), algum g passa em P1, algum g passa em P1 e P2): numero de classes de q")
for k, v in sorted(res.items()): print("  ", k, v)
