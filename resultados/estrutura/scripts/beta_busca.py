"""(09/11) Missao "quarticas com termos mistos", passo 1 (F4+F4, bits y0..y7).
L = ker(T∧: Λ³→Λ⁷), G = ι_Y T, J = T∧Λ² ⊂ Λ⁶. β([a],[b]) = a∧b mod J (10 funcionais).
Coordenadas: as 48 variaveis de C3 do modelo (gauge fixo = complemento de G) com as 8 restricoes de L -> L/G (dim 40).
Busca (CryptoMiniSat): DIM cubicas phi_1..phi_DIM em L/G com β(phi_i,phi_j)=0 para i<j e TODAS as combinacoes
nao nulas sem U_Y isotropico (em N). Controles: dim J=18, posto de β em Λ²(L/G)=10 (exato).
Saida: candidatos em beta_DIM<d>_<seed>.json (phi como listas de mascaras cubicas)."""
import os, sys, json, time, random
from itertools import combinations, product
sys.argv = ["x"]
from linear_c3 import restricoes
from analisa_testemunhas import contexto
from fecho_estrela import linhas, base_red, reduz
import pycryptosat

classe = "F4+F4"
lin, nc, TOP, c3v = restricoes(classe)
fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
T = list(Tq)
pc = lambda x: bin(x).count("1")
# Λ⁶: 6-subconjuntos de 8 -> indice
seis = [m for m in range(256) if pc(m) == 6]
i6 = {m: k for k, m in enumerate(seis)}
# J = span{T ∧ q : q monomio quadratico}
J = []
for q in (m for m in range(256) if pc(m) == 2):
    r = 0
    for t in T:
        if not (t & q):
            r ^= 1 << i6[t | q]
    J.append(r)
pJ = base_red(J)
assert len(pJ) == 18, len(pJ)
# funcionais que anulam J: base do anulador (vetores f com <f, j> = 0 para j em J)
def anulador(vecs, n):
    # resolve sistema: f · v = 0 para todo v
    rows = list(base_red(vecs).values())
    # eliminacao reduzida
    piv = {}
    for v in rows:
        for h, pv in piv.items():
            if (v >> h) & 1: v ^= pv
        if v:
            h = v.bit_length() - 1
            for h2 in list(piv):
                if (piv[h2] >> h) & 1: piv[h2] ^= v
            piv[h] = v
    livres = [c for c in range(n) if c not in piv]
    out = []
    for f in livres:
        w = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1: w |= 1 << h
        out.append(w)
    return out
F = anulador(J, 28)
assert len(F) == 10 and all(bin(f & j).count("1") % 2 == 0 for f in F for j in J)
cm = [m for (m, var) in c3v]  # mascaras cubicas (bits y; c3v ja vem sem o bit de x)
assert all(m < 256 and pc(m) == 3 for m in cm)
# tensor de β: para cada funcional k, conjunto de pares (p,q) (p<q) com f_k(m_p ∪ m_q)=1 e disjuntos (a∧b alterna: a∧a=0)
Bk = [[(p, q) for p in range(nc) for q in range(p + 1, nc) if not (cm[p] & cm[q]) and (F[k] >> i6[cm[p] | cm[q]]) & 1] for k in range(10)]
# posto de β em Λ²(L/G): base de L/G em coords, avaliar β em pares da base
def base_L():
    # nucleo das restricoes lineares nas 48 coords
    rows = [e & ((1 << nc) - 1) for e in lin]
    piv = {}
    for v in rows:
        for h, pv in piv.items():
            if (v >> h) & 1: v ^= pv
        if v:
            h = v.bit_length() - 1
            for h2 in list(piv):
                if (piv[h2] >> h) & 1: piv[h2] ^= v
            piv[h] = v
    out = []
    for f in [c for c in range(nc) if c not in piv]:
        w = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1: w |= 1 << h
        out.append(w)
    return out
BL = base_L()
assert len(BL) == 40
def beta(a, b):
    r = 0
    for k in range(10):
        s = 0
        for p, q in Bk[k]:
            s ^= (((a >> p) & 1) & ((b >> q) & 1)) ^ (((a >> q) & 1) & ((b >> p) & 1))
        r |= s << k
    return r
img = [beta(BL[i], BL[j]) for i, j in combinations(range(40), 2)]
pb = len(base_red(img))
print("dim J = 18 ok; posto de β em Λ²(L/G) =", pb, flush=True)
assert pb == 10, "controle do posto de beta falhou"
if os.environ.get("SO_CONTROLE"):
    sys.exit(0)

DIM = int(os.environ.get("DIM", 2))
SEED = int(os.environ.get("SEED", 1))
Ms = [linhas(*d) for d in dados]
s = pycryptosat.Solver(threads=int(os.environ.get("THREADS", 2)))
var = lambda i, p: i * nc + p + 1
for i in range(DIM):
    for e in lin:
        s.add_xor_clause([var(i, p) for p in range(nc) if (e >> p) & 1], bool((e >> TOP) & 1))
prox = DIM * nc + 1
ands = {}
def AND(a, b):
    global prox
    k = (min(a, b), max(a, b))
    if k not in ands:
        ands[k] = prox
        s.add_clause([-prox, a]); s.add_clause([-prox, b]); s.add_clause([prox, -a, -b]); prox += 1
    return ands[k]
for i, j in combinations(range(DIM), 2):
    for k in range(10):
        lits = []
        for p, q in Bk[k]:
            lits.append(AND(var(i, p), var(j, q))); lits.append(AND(var(i, q), var(j, p)))
        s.add_xor_clause(lits, False)
vs = [v for v in product((0, 1), repeat=DIM) if any(v)]
for v in vs:
    for M in Ms:
        auxs = []
        for r in M:
            s.add_xor_clause([var(i, p) for i in range(DIM) if v[i] for p in range(nc) if (r >> p) & 1] + [prox], False)
            auxs.append(prox); prox += 1
        s.add_clause(auxs)
rnd = random.Random(SEED)
assum = [var(0, p) * rnd.choice([1, -1]) for p in rnd.sample(range(nc), int(os.environ.get("K", 0)))]
t0 = time.time()
r, sol = s.solve(assumptions=assum)
out = {"DIM": DIM, "SEED": SEED, "SAT": r, "t": round(time.time() - t0, 1)}
if r:
    phis = [sum(1 << p for p in range(nc) if sol[var(i, p)]) for i in range(DIM)]
    # conferencias independentes
    out["beta_pares"] = [beta(phis[i], phis[j]) for i, j in combinations(range(DIM), 2)]
    sem_iso = []
    for v in vs:
        c = 0
        for i in range(DIM):
            if v[i]: c ^= phis[i]
        sem_iso.append(all(any(bin(x & c).count("1") & 1 for x in M) for M in Ms))
    out["todas_sem_isotropico"] = all(sem_iso)
    out["phi_mascaras"] = [[cm[p] for p in range(nc) if (ph >> p) & 1] for ph in phis]
print(json.dumps(out), flush=True)
json.dump(out, open(f"beta_DIM{DIM}_{SEED}.json", "w"))
