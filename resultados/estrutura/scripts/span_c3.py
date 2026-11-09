"""(09/11) Span F2 das C3 (coords apos gauge) das testemunhas I6 conhecidas, por classe;
e se o C3 sem isotropico (cobertura_*.json) esta nesse span."""
import glob, json, os, sys
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1_orbita import base
from fecho_estrela import base_red, reduz

BASE = r"C:\Users\Valer\Downloads\analise adversarial"
FONTES = {"Q4a": ["gh_42521666326", "colab_Q4a_o1_cubo1_SAT.json"], "Q4b": ["gh_42521672988"],
          "Q4c": ["gh_42521679875", "colab_Q4c_o1_cubo0_SAT.json"]}


def vetores(classe):
    fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
    arqs = []
    for f in FONTES[classe]:
        p = os.path.join(BASE, "q1_nuvem_08nov", f)
        arqs += [p] if f.endswith(".json") else glob.glob(os.path.join(p, "**", "cubo_*.json"), recursive=True)
    arqs += glob.glob(os.path.join(BASE, "q1_tres_lineares", f"sat_orbita_{classe}_o*.json"))
    vs = []
    for f in arqs:
        r = json.load(open(f))
        if r.get("resultado", "SAT" if r.get("SAT") else "") != "SAT":
            continue
        monos = set(r["conferencia"]["anf_extra"] if "conferencia" in r else r["anf_extra"])
        vs.append(sum(1 << p for p, (m, var) in enumerate(c3v) if incog[var - 1] in monos))
    return vs, c3v


if __name__ == "__main__":
    for classe in ["Q4a", "Q4b", "Q4c"]:
        vs, c3v = vetores(classe)
        piv = base_red(vs)
        linha = f"{classe}: {len(vs)} testemunhas, dim span C3 = {len(piv)} de {len(c3v)}"
        f = f"cobertura_{classe}.json"
        if os.path.exists(f):
            c = sum(1 << p for p in json.load(open(f))["c"])
            linha += f"; C3 sem isotropico no span? {reduz(piv, c) == 0}"
        print(linha)
