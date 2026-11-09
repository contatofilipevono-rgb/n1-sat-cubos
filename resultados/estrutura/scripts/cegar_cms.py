"""(09/11) CEGAR sobre C3 com interno em CryptoMiniSat (XOR nativo). Ver cegar_c3.py.
Interno: modelo I6 completo (todos os produtos como AND), C3 por suposicoes; UNSAT -> get_conflict() -> clausula."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
from sat_n1 import confere
from linear_c3 import restricoes
from analisa_testemunhas import contexto
from fecho_estrela import linhas
import pycryptosat

classe = os.environ.get("CLASSE", "Q4a")
nome = classe.replace("^", "").replace("+", "")
lin, nc, TOP, _ = restricoes(classe)
_, _, _, _, iso, orbs, dados = contexto(classe)
Ms = [linhas(*d) for d in dados]

# interno
w1, w2, ny = so.pencil(so.classes()[classe])
fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
zerar = set(so.pivos_iT(Tq, ny))
incog = [m for m in incog if m not in zerar]
P = so.Pares(fixo, incog)
c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
var_de = [var for (m, var) in c3v]
inn = pycryptosat.Solver(threads=int(os.environ.get("THREADS", 2)))
n = len(incog); prox = n + 1
termos = [[] for _ in range(len(P.alvos))]
def add(v, var):
    h = 0
    while v:
        if v & 1: termos[h].append(var)
        v >>= 1; h += 1
for k, v in enumerate(P.D1):
    add(v, k + 1)
for (i, j), v in P.D2.items():
    t = prox; prox += 1
    inn.add_clause([-t, i + 1]); inn.add_clause([-t, j + 1]); inn.add_clause([t, -(i + 1), -(j + 1)])
    add(v, t)
for h, vs in enumerate(termos):
    inn.add_xor_clause(vs, bool((P.F0 >> h) & 1))

# externo
ext = pycryptosat.Solver()
for e in lin:
    ext.add_xor_clause([p + 1 for p in range(nc) if (e >> p) & 1], bool((e >> TOP) & 1))
pe = nc + 1
for M in Ms:
    auxs = []
    for r in M:
        ext.add_xor_clause([p + 1 for p in range(nc) if (r >> p) & 1] + [pe], False)
        auxs.append(pe); pe += 1
    ext.add_clause(auxs)

pos = {var: p for p, var in enumerate(var_de)}
log = open(f"cegar_cms_{nome}.jsonl", "a")
it = 0
while True:
    it += 1
    t0 = time.time(); r, sol = ext.solve(); te = time.time() - t0
    if not r:
        m = {"it": it, "externo": "UNSAT", "conclusao": f"N1 para {classe}, condicional a certificar clausulas"}
        print(json.dumps(m), flush=True); log.write(json.dumps(m) + "\n"); break
    assum = [var_de[p] if sol[p + 1] else -var_de[p] for p in range(nc)]
    t1 = time.time(); ok, isol = inn.solve(assumptions=assum); ti = time.time() - t1
    if ok:
        monos = [incog[k] for k in range(n) if isol[k + 1]]
        m = {"it": it, "CONTRAEXEMPLO_N1": True, "I6_conferido": bool(confere(fixo, monos, ny + 1)[0]), "anf_extra": monos,
             "c": [p for p in range(nc) if sol[p + 1]]}
        print(json.dumps(m), flush=True); log.write(json.dumps(m) + "\n"); break
    conf = inn.get_conflict()  # literais (negados) das suposicoes responsaveis
    lits = [l for l in conf if abs(l) in pos]
    clausula = [(pos[abs(l)] + 1) * (1 if l > 0 else -1) for l in lits]
    if clausula and any((l > 0) == bool(sol[abs(l)]) for l in clausula):
        clausula = [-l for l in clausula]  # convencao de sinal invertida
        assert not any((l > 0) == bool(sol[abs(l)]) for l in clausula)
    if not clausula:
        clausula = [-(p + 1) if sol[p + 1] else (p + 1) for p in range(nc)]
    ext.add_clause(clausula)
    m = {"it": it, "tam_clausula": len(clausula), "t_ext": round(te, 1), "t_int": round(ti, 1), "clausula": clausula}
    print(json.dumps(m), flush=True); log.write(json.dumps(m) + "\n"); log.flush()
