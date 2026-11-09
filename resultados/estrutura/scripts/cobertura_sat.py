"""(09/11) Pergunta de cobertura, SEM I6: existe C3 (48 variaveis apos gauge) com M_U c != 0 para todo U isotropico?
UNSAT => toda D = q1q2 + x C3 + R tem U isotropico, logo N1 vale para a classe independentemente de I6.
Codificacao: para cada U e cada linha r de M_U, aux_{U,r} = <r,c> (XOR); clausula OR_r aux_{U,r}.
Resolve com CryptoMiniSat (XOR nativo) e grava tambem CNF pura (XOR em cadeia de Tseitin) para CaDiCaL+DRAT."""
import os, sys, json, time
sys.argv = ["x"]
from analisa_testemunhas import contexto
from fecho_estrela import linhas
import pycryptosat

classe = os.environ.get("CLASSE", "Q4a")
fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
nv = len(dados[0][1])
Ms = [linhas(*d) for d in dados]

s = pycryptosat.Solver()
prox = nv + 1
cnf = []  # CNF pura
def xor_cnf(vs, aux):
    """aux = XOR(vs) em CNF por cadeia."""
    global prox
    cur = vs[0]
    for v in vs[1:]:
        t = prox; prox += 1
        cnf.extend([[-t, cur, v], [-t, -cur, -v], [t, -cur, v], [t, cur, -v]])
        cur = t
    cnf.extend([[-aux, cur], [aux, -cur]])

for M in Ms:
    auxs = []
    for r in M:
        vs = [p + 1 for p in range(nv) if (r >> p) & 1]
        a = prox; prox += 1
        s.add_xor_clause(vs + [a], False)
        xor_cnf(vs, a)
        auxs.append(a)
    s.add_clause(auxs)
    cnf.append(auxs)
nome = classe.replace("^", "").replace("+", "")
if os.environ.get("SO_CNF"):
    open(f"cobertura_{nome}.cnf", "w").write(f"p cnf {prox - 1} {len(cnf)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cnf))
    sys.exit(0)
t0 = time.time()
r, sol = s.solve()
dt = time.time() - t0
out = {"classe": classe, "nvars_C3": nv, "U": len(Ms), "SAT": r, "tempo_s": round(dt, 1)}
if r:
    c = [p for p in range(nv) if sol[p + 1]]
    out["c"] = c
    # conferencia independente
    cb = sum(1 << p for p in c)
    out["confere_sem_isotropico"] = all(any(bin(x & cb).count("1") & 1 for x in M) for M in Ms)
print(json.dumps(out), flush=True)
nome = classe.replace("^", "").replace("+", "")
open(f"cobertura_{nome}.cnf", "w").write(f"p cnf {prox - 1} {len(cnf)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cnf))
json.dump(out, open(f"cobertura_{nome}.json", "w"))
