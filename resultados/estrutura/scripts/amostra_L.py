"""(09/11) Amostragem vetorizada: C3 uniforme em L (nucleo das 8 restricoes lineares de I6) e em F2^48;
distribuicao do numero de U isotropicos; fracao sem nenhum (estimativa de |N ∩ L|)."""
import os, sys, json
import numpy as np
from collections import Counter
sys.argv = ["x"]
from analisa_testemunhas import contexto
from fecho_estrela import linhas
from linear_c3 import restricoes

classe = os.environ.get("CLASSE", "Q4a")
NS = int(os.environ.get("NS", 200000))
lin, nc, TOP, _ = restricoes(classe)
fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
Ms = [linhas(*d) for d in dados]
R = np.array([[(r >> p) & 1 for p in range(nc)] for M in Ms for r in M], dtype=np.uint8)  # (7U, 48)
nU = len(Ms)
# base do nucleo de L
A = np.array([[(e >> p) & 1 for p in range(nc)] for e in lin], dtype=np.uint8)
# nucleo via eliminacao
M = A.copy(); piv = []; r = 0
for c in range(nc):
    k = next((i for i in range(r, M.shape[0]) if M[i, c]), None)
    if k is None: continue
    M[[r, k]] = M[[k, r]]
    for i in range(M.shape[0]):
        if i != r and M[i, c]: M[i] ^= M[r]
    piv.append(c); r += 1
livres = [c for c in range(nc) if c not in piv]
K = []
for f in livres:
    v = np.zeros(nc, dtype=np.uint8); v[f] = 1
    for i, c in enumerate(piv):
        v[c] = M[i, f]
    K.append(v)
K = np.array(K)
assert ((A.astype(int) @ K.T.astype(int)) % 2 == 0).all()
rng = np.random.default_rng(int(os.environ.get("SEMENTE", 7)))
out = {"classe": classe, "dim_L": len(K)}
for nome, gera in [("L", lambda n: (rng.integers(0, 2, (n, len(K))).astype(int) @ K.astype(int)) % 2),
                   ("F2^48", lambda n: rng.integers(0, 2, (n, nc)))]:
    hist = Counter()
    zeros = 0
    for b in range(0, NS, 5000):
        C = gera(5000).astype(np.int32)
        S = (R.astype(np.int32) @ C.T) % 2          # (7U, n)
        S = S.reshape(nU, 7, -1).any(axis=1)        # True = nao isotropico
        n_iso = (~S).sum(axis=0)
        hist.update(n_iso.tolist())
    out[nome] = {"sem_isotropico": hist[0], "amostras": NS, "media": round(sum(k * v for k, v in hist.items()) / NS, 2), "min": min(hist),
                 "hist_baixo": {k: hist[k] for k in sorted(hist)[:8]}}
    print(nome, json.dumps(out[nome]), flush=True)
json.dump(out, open(f"amostra_L_{classe}.json", "w"))
