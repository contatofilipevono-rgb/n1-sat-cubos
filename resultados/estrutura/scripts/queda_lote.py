"""(09/11) Conjectura (caso de 3 lineares do Lema L, nivel C3): para phi1,phi2,phi3 com phi_i ∧ T = 0,
Q = T + sum x_i phi_i tem queda de grau em algum subespaco de codim 5 com projecao em X de dim 1 ou 2.
Testa: todos os trios do arquivo (N, todos os 7 em N) + NALEAT trios aleatorios em L. Para cada um: existe k=1? existe k=2?
(parada no primeiro achado). Classe via CLASSE (T critico)."""
import sys, json, os, random, itertools, time
import numpy as np
sys.argv = ["x"]
from queda_onze import tabela, grau_max_lote, subespacos, complemento, parse
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so

classe = os.environ.get("CLASSE", "F4+F4")
w1, w2, ny = so.pencil(so.classes()[classe])
_, _, _, Tq = so.modelo_nove(w1, w2, ny)
T = set(Tq)
cub = [sum(1 << i for i in c) for c in itertools.combinations(range(8), 3)]
# matriz da cunha: coluna p (monomio cubico) -> vetor de 8 bits
W = np.zeros((8, 56), dtype=np.uint8)
for p, m in enumerate(cub):
    for j in range(8):
        W[j, p] = sum(1 for t in T if (m & t) == 0 and (m | t) == 255 ^ (1 << j)) & 1


def nucleo(A):
    A = A.copy() % 2; r, piv = 0, []
    for c in range(A.shape[1]):
        k = next((i for i in range(r, A.shape[0]) if A[i, c]), None)
        if k is None: continue
        A[[r, k]] = A[[k, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, c]: A[i] ^= A[r]
        piv.append(c); r += 1
    base = []
    for f in [c for c in range(A.shape[1]) if c not in piv]:
        v = np.zeros(A.shape[1], dtype=np.uint8); v[f] = 1
        for i, c in enumerate(piv): v[c] = A[i, f]
        base.append(v)
    return np.array(base)


K = nucleo(W)
X = [1 << 8, 1 << 9, 1 << 10]
Xv = [v for v in (a ^ b ^ c for a, b, c in itertools.product((0, X[0]), (0, X[1]), (0, X[2]))) if v]
planos = []
for a, b in itertools.combinations(Xv, 2):
    s = frozenset({a, b, a ^ b})
    if s not in [frozenset({c, d, c ^ d}) for c, d in planos]:
        planos.append((a, b))
S5 = subespacos(8, 5); S4 = subespacos(8, 4)


def testa(phis):
    Q = set(T)
    for i, ph in enumerate(phis):
        Q ^= {m | (1 << (8 + i)) for m in ph}
    tt = tabela(Q)
    k1 = 0
    for B in S5[~grau_max_lote(tt, S5)]:
        reps = complemento(list(B))
        lote = np.array([list(B) + [p ^ u] for p in Xv for u in reps], dtype=np.int64)
        if (~grau_max_lote(tt, lote)).any():
            k1 = 1; break
    k2 = 0
    for B in S4[~grau_max_lote(tt, S4)]:
        Bl = list(B); reps = complemento(Bl)
        for p1, p2 in planos:
            lote = np.array([Bl + [p1 ^ u1, p2 ^ u2] for u1 in reps for u2 in reps], dtype=np.int64)
            if (~grau_max_lote(tt, lote)).any():
                k2 = 1; break
        if k2: break
    return k1, k2


out = []
arq = os.environ.get("TRIO", "")
if arq and os.path.exists(arq):
    for i, tr in enumerate(json.load(open(arq))["trios"]):
        t0 = time.time(); k1, k2 = testa([parse(s) for s in tr["phi"]])
        out.append({"fonte": f"trio {i}", "k1": k1, "k2": k2}); print(out[-1], f"{time.time()-t0:.0f}s", flush=True)
rnd = np.random.default_rng(int(os.environ.get("SEMENTE", 1)))
for t in range(int(os.environ.get("NALEAT", 10))):
    phis = []
    for i in range(3):
        v = (rnd.integers(0, 2, K.shape[0]) @ K) % 2
        phis.append({cub[p] for p in range(56) if v[p]})
    t0 = time.time(); k1, k2 = testa(phis)
    out.append({"fonte": f"aleatorio {t}", "k1": k1, "k2": k2}); print(out[-1], f"{time.time()-t0:.0f}s", flush=True)
print("RESUMO", classe, "casos:", len(out), "sem nenhuma queda (k1=k2=0):", sum(1 for o in out if not o["k1"] and not o["k2"]))
json.dump(out, open(f"queda_lote_{classe.replace('^','').replace('+','')}.json", "w"))
