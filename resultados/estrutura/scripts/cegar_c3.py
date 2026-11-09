"""(09/11) CEGAR sobre C3 para N1 (classe dada).
Externo (CryptoMiniSat, 48 vars de C3): sem U isotropico + restricoes lineares de I6 + clausulas aprendidas.
Interno (CaDiCaL, modelo I6 completo): C3 fixado por suposicoes; se UNSAT, o core (subconjunto das suposicoes)
vira clausula 'not(core)' no externo, minimizada por remocao gulosa.
Externo UNSAT => toda solucao de I6 tem U isotropico (N1 para a classe), condicionado a certificar cada clausula
(cada uma e 'I6 ∧ core UNSAT', instancia pequena, certificavel por DRAT depois).
Saida incremental em cegar_c3_<classe>.jsonl."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1_orbita import base
from sat_n1 import confere
from linear_c3 import restricoes
from analisa_testemunhas import contexto
from fecho_estrela import linhas
from pysat.solvers import Cadical153
import pycryptosat

classe = os.environ.get("CLASSE", "Q4a")
nome = classe.replace("^", "").replace("+", "")
MINIM = int(os.environ.get("MINIM", 1))
lin, nc, TOP, _ = restricoes(classe)
fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
_, _, _, _, iso, orbs, dados = contexto(classe)
Ms = [linhas(*d) for d in dados]

ext = pycryptosat.Solver()
for e in lin:
    ext.add_xor_clause([p + 1 for p in range(nc) if (e >> p) & 1], bool((e >> TOP) & 1))
prox = nc + 1
for M in Ms:
    auxs = []
    for r in M:
        ext.add_xor_clause([p + 1 for p in range(nc) if (r >> p) & 1] + [prox], False)
        auxs.append(prox); prox += 1
    ext.add_clause(auxs)

inn = Cadical153(bootstrap_with=cnf.cl)
var_de = [var for (m, var) in c3v]
log = open(f"cegar_c3_{nome}.jsonl", "a")
it = 0
while True:
    it += 1
    t0 = time.time()
    r, sol = ext.solve()
    te = time.time() - t0
    if not r:
        msg = {"it": it, "externo": "UNSAT", "conclusao": f"N1 vale para {classe} (condicional a certificar as clausulas)", "t_ext": round(te, 1)}
        print(json.dumps(msg), flush=True); log.write(json.dumps(msg) + "\n"); break
    c = [bool(sol[p + 1]) for p in range(nc)]
    assum = [var_de[p] if c[p] else -var_de[p] for p in range(nc)]
    t1 = time.time()
    ok = inn.solve(assumptions=assum)
    ti = time.time() - t1
    if ok:
        mod = set(v for v in inn.get_model() if v > 0)
        monos = [incog[k] for k in range(len(incog)) if (k + 1) in mod]
        msg = {"it": it, "CONTRAEXEMPLO_N1": True, "I6_conferido": bool(confere(fixo, monos, ny + 1)[0]), "anf_extra": monos}
        print(json.dumps(msg), flush=True); log.write(json.dumps(msg) + "\n"); break
    core = list(inn.get_core() or assum)
    n0 = len(core)
    if MINIM:
        i = 0
        while i < len(core):
            tent = core[:i] + core[i + 1:]
            if not inn.solve(assumptions=tent):
                core = list(inn.get_core() or tent)
            else:
                i += 1
    pos = {var: p for p, var in enumerate(var_de)}
    clausula = [-(pos[abs(l)] + 1) if l > 0 else (pos[abs(l)] + 1) for l in core]
    ext.add_clause(clausula)
    msg = {"it": it, "core": len(core), "core0": n0, "t_ext": round(te, 1), "t_int": round(ti, 2), "t_tot": round(time.time() - t0, 1),
           "clausula_c3": clausula}
    print(json.dumps(msg), flush=True); log.write(json.dumps(msg) + "\n"); log.flush()
