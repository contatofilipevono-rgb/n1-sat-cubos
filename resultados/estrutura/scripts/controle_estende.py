import json, sys, os, glob
sys.argv = ["x"]
from estende_i6 import testa
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1_orbita import base

BASE = r"C:\Users\Valer\Downloads\analise adversarial"
for classe, f in [("Q4a", os.path.join(BASE, "q1_nuvem_08nov", "gh_42521666326", "res-0", "cubo_0.json")),
                  ("Q4a", os.path.join(BASE, "q1_tres_lineares", "sat_orbita_Q4a_o0.json"))]:
    r = json.load(open(f))
    monos = set(r["conferencia"]["anf_extra"] if "conferencia" in r else r["anf_extra"])
    fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
    c = [p for p, (m, var) in enumerate(c3v) if incog[var - 1] in monos]
    out = testa(classe, c)
    print("controle +", os.path.basename(f), "I6_extensivel =", out["I6_extensivel"], "conferido =", out.get("I6_conferido"), out["tempo_s"], "s")
