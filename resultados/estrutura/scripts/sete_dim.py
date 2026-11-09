"""(09/11) Teste das 7 restricoes (caso de 3 lineares do Lema L), nivel C3 + parte linear de I6.
Delta = T + x1 phi1 + x2 phi2 + x3 phi3 (T critico em 8 var). Restringindo (x1,x2,x3) a reta t*v (v != 0 em F2^3):
Delta| = T + t*(sum v_i phi_i). N1 falha nessa restricao <=> sum v_i phi_i nao tem U_Y isotropico (esta em N).
Pergunta: existem phi1, phi2, phi3 (coords de C3 apos gauge, cada um com phi_i âˆ§ T = 0) com as 7 combinacoes em N?
UNSAT => para a classe, alguma das 7 restricoes sempre tem isotropico (independente de R e de I7).
SAT => o triplo e candidato; precisa ainda de I6/I7 no modelo completo."""
import os, sys, json, time
from itertools import product
sys.argv = ["x"]
from linear_c3 import restricoes
from analisa_testemunhas import contexto
from fecho_estrela import linhas
import pycryptosat

classe = os.environ.get("CLASSE", "F4+F4")
DIM = int(os.environ.get("DIM", 3))
lin, nc, TOP, _ = restricoes(classe)
_, _, _, _, iso, orbs, dados = contexto(classe)
Ms = [linhas(*d) for d in dados]
s = pycryptosat.Solver(threads=int(os.environ.get("THREADS", 4)))
var = lambda i, p: i * nc + p + 1  # phi_i, coordenada p
for i in range(DIM):
    for e in lin:
        s.add_xor_clause([var(i, p) for p in range(nc) if (e >> p) & 1], bool((e >> TOP) & 1))
prox = 3 * nc + 1
vs = [v for v in product((0, 1), repeat=DIM) if any(v)]
for v in vs:
    for M in Ms:
        auxs = []
        for r in M:
            lits = [var(i, p) for i in range(DIM) if v[i] for p in range(nc) if (r >> p) & 1]
            s.add_xor_clause(lits + [prox], False)
            auxs.append(prox); prox += 1
        s.add_clause(auxs)  # combinacao v nao isotropica em U
# independencia (evita phi's dependentes/zero): cada combinacao nao nula precisa ser != 0 -> ja implicado por N (0 e isotropico)
CUBO = os.environ.get("CUBO")
assum = []
if CUBO is not None:
    KB = int(os.environ.get("KB", 3))
    assum = [var(0, j) if (int(CUBO) >> j) & 1 else -var(0, j) for j in range(KB)]
t0 = time.time()
r, sol = s.solve(assumptions=assum)
out = {"classe": classe, "SAT": r, "t": round(time.time() - t0, 1), "U": len(Ms)}
if r:
    out["phi"] = [[p for p in range(nc) if sol[var(i, p)]] for i in range(DIM)]
    # conferencia independente
    ok = True
    for v in vs:
        c = 0
        for i in range(DIM):
            if v[i]:
                c ^= sum(1 << p for p in out["phi"][i])
        ok &= all(any(bin(x & c).count("1") & 1 for x in M) for M in Ms)
    out["confere_7_sem_isotropico"] = ok
print(json.dumps(out), flush=True)
json.dump(out, open(f"sete_d{DIM}_c{CUBO}_{classe.replace('^','').replace('+','')}.json", "w"))

