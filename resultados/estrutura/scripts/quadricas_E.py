"""(09/11) Extrai as relacoes de grau <=2 (coords livres de L) que se anulam nas amostras de E (treino),
valida em amostras de teste (arquivos com semente >= TESTE_MIN), e testa N ∩ L ∩ V(relacoes) com CMS."""
import glob, json, sys, os, time
from itertools import combinations
sys.argv = ["x"]
from fecho_estrela import base_red, linhas
from linear_c3 import restricoes
from analisa_testemunhas import contexto
import pycryptosat

classe = os.environ.get("CLASSE", "Q4a")
nome = classe.replace("^", "").replace("+", "")
nc = 48
lin, _, TOP, _ = restricoes(classe)
pv = base_red([e & ((1 << nc) - 1) for e in lin])
livres = [i for i in range(nc) if i not in pv]
mon = [()] + [(i,) for i in livres] + list(combinations(livres, 2))


def carrega(filtro):
    out, vistos = [], set()
    for f in sorted(glob.glob(f"E_{nome}_s*.jsonl")):
        s = int(f.split("_s")[1].split(".")[0])
        if not filtro(s):
            continue
        for l in open(f):
            c = tuple(json.loads(l)["c"])
            if c not in vistos:
                vistos.add(c); out.append(set(c))
    return out


TESTE = int(os.environ.get("TESTE_SEM", 21))
treino = carrega(lambda s: s != TESTE)
teste = carrega(lambda s: s == TESTE)
# colunas (monomio) como bitvetores sobre amostras de treino; dependencias -> relacoes
colv = []
for m in mon:
    v = 0
    for k, c in enumerate(treino):
        if all(i in c for i in m):
            v |= 1 << k
    colv.append(v)
piv = {}  # bit -> (vetor, combinacao de monomios)
rels = []
for j, v in enumerate(colv):
    comb = 1 << j
    while v:
        h = v.bit_length() - 1
        if h in piv:
            pv_, pc = piv[h]; v ^= pv_; comb ^= pc
        else:
            piv[h] = (v, comb); break
    if not v:
        rels.append(comb)
print(f"treino {len(treino)} amostras, monomios {len(mon)}, relacoes {len(rels)}", flush=True)
# validacao no teste
def avalia(rel, c):
    t = 0; j = 0; r = rel
    while r:
        if r & 1:
            if all(i in c for i in mon[j]): t ^= 1
        r >>= 1; j += 1
    return t
falhas = [k for k, rel in enumerate(rels) if any(avalia(rel, c) for c in teste)]
print(f"teste {len(teste)} amostras: relacoes violadas {len(falhas)} de {len(rels)}", flush=True)
boas = [rel for k, rel in enumerate(rels) if k not in set(falhas)]
json.dump({"livres": livres, "monomios": mon, "relacoes": [[j for j in range(len(mon)) if (r >> j) & 1] for r in boas]},
          open(f"quadricas_E_{nome}.json", "w"))
# N ∩ L ∩ V(boas)
_, _, _, _, iso, orbs, dados = contexto(classe)
Ms = [linhas(*d) for d in dados]
s = pycryptosat.Solver(threads=4)
for e in lin:
    s.add_xor_clause([p + 1 for p in range(nc) if (e >> p) & 1], bool((e >> TOP) & 1))
prox = nc + 1
pv2 = {}
for (a, b) in [m for m in mon if len(m) == 2]:
    pv2[(a, b)] = prox
    s.add_clause([-prox, a + 1]); s.add_clause([-prox, b + 1]); s.add_clause([prox, -(a + 1), -(b + 1)])
    prox += 1
for rel in boas:
    vs = []; rhs = False
    for j in range(len(mon)):
        if (rel >> j) & 1:
            m = mon[j]
            if len(m) == 0: rhs = not rhs
            elif len(m) == 1: vs.append(m[0] + 1)
            else: vs.append(pv2[m])
    s.add_xor_clause(vs, rhs)
for M in Ms:
    auxs = []
    for r in M:
        s.add_xor_clause([p + 1 for p in range(nc) if (r >> p) & 1] + [prox], False)
        auxs.append(prox); prox += 1
    s.add_clause(auxs)
t0 = time.time()
r, sol = s.solve()
out = {"relacoes_validas": len(boas), "N∩L∩V": "SAT" if r else "UNSAT", "t": round(time.time() - t0, 1)}
if r:
    out["c"] = [p for p in range(nc) if sol[p + 1]]
print(json.dumps(out), flush=True)
json.dump(out, open(f"NLV_{nome}.json", "w"))
