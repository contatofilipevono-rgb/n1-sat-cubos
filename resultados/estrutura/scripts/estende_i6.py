"""(09/11) Dado C3 fixo (sem U isotropico), existe R com I6? (C3 fixado por unidades no modelo base).
UNSAT para todo C3 em N (= C3 sem isotropico) <=> N1 para a classe."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1_orbita import base
from sat_n1 import confere
from pysat.solvers import Cadical153


def testa(classe, c_pos, limite=None):
    fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
    s = Cadical153(bootstrap_with=cnf.cl)
    c = set(c_pos)
    assum = [var if p in c else -var for p, (m, var) in enumerate(c3v)]
    t0 = time.time()
    r = s.solve(assumptions=assum)
    out = {"classe": classe, "c": sorted(c_pos), "I6_extensivel": r, "tempo_s": round(time.time() - t0, 1)}
    if r:
        mod = set(v for v in s.get_model() if v > 0)
        monos = [incog[k] for k in range(len(incog)) if (k + 1) in mod]
        out["I6_conferido"] = bool(confere(fixo, monos, ny + 1)[0])
        out["anf_extra"] = monos
    return out


if __name__ == "__main__":
    classe = os.environ.get("CLASSE", "Q4a")
    nome = classe.replace("^", "").replace("+", "")
    c = json.load(open(f"cobertura_{nome}.json"))["c"]
    print(json.dumps(testa(classe, c))[:600])
