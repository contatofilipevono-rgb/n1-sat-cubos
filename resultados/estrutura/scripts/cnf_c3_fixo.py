"""(09/11) CNF do modelo I6 (Q4a) com C3 fixo (unidades) + 2^k cubos sobre as primeiras k variaveis de R.
Saida: c3fixo_Q4a.cnf e c3fixo_cubos.json."""
import os, sys, json
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1_orbita import base

classe = "Q4a"
K = int(os.environ.get("K", 4))
c = set(json.load(open("cobertura_restrita_Q4a.json"))["c"])
fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
cl = [list(x) for x in cnf.cl]
c3vars = set()
for p, (m, var) in enumerate(c3v):
    cl.append([var if p in c else -var])
    c3vars.add(var)
# variaveis de R: incognitas que nao sao C3, preferindo cubicas sem x (grau 3)
X = 1 << ny
rv = [k + 1 for k, m in enumerate(incog) if (k + 1) not in c3vars and not (m & X) and bin(m).count("1") == 3]
cubos = [[rv[i] if (b >> i) & 1 else -rv[i] for i in range(K)] for b in range(2 ** K)]
nv = max(abs(l) for x in cl for l in x)
open("c3fixo_Q4a.cnf", "w").write(f"p cnf {nv} {len(cl)}\n" + "".join(" ".join(map(str, x)) + " 0\n" for x in cl))
json.dump({"cubos": cubos, "c": sorted(c), "anf_incog": incog}, open("c3fixo_cubos.json", "w"))
print(nv, len(cl), len(cubos))
