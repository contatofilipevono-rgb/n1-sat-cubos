"""Cube-and-conquer para as instancias de N1 restritas a orbitas (ver sat_n1_orbita.py).
  python cubo.py gera CLASSE AUTO_JSON ORB_K K SAIDA_DIR
      escreve SAIDA_DIR/base.cnf (DIMACS), meta.pkl (para conferir solucoes) e cubos.json
      (as 2^K combinacoes de sinais nas K primeiras variaveis de C3: cobertura completa por construcao).
  python cubo.py cnf_cubo SAIDA_DIR I ARQ      -> base.cnf + K clausulas unitarias do cubo I
  python cubo.py confere SAIDA_DIR MODELO_TXT  -> confere solucao SAT (I6 por tabela-verdade, nao isotropia em S)
UNSAT de todos os 2^K cubos (cada um com prova DRAT verificada) => base.cnf UNSAT (divisao de casos)."""
import json
import os
import pickle
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_n1 import rref_todos, restr_zero, confere  # noqa: E402
from sat_n1_cegar import prepara_U, isotropico_em  # noqa: E402
from sat_n1_orbita import base, orbitas, adiciona_U, popc  # noqa: E402


def gera(classe, auto, orb_k, K, out):
    os.makedirs(out, exist_ok=True)
    t0 = time.time()
    gens = [tuple(A) for A in json.load(open(auto))[classe]["geradores"]]
    Us = rref_todos(5, 8)
    fixo, incog, C3, Tq, ny, cnf, c3_vars = base(classe)
    iso = Us[restr_zero(Tq, Us)]
    orbs = orbitas(iso, gens)
    ks = [int(t) for t in str(orb_k).split(",")]
    S = sorted(k for i in ks for k in orbs[i])
    dados = prepara_U(Tq, ny, c3_vars, iso)
    for k in S:
        adiciona_U(cnf, *dados[k])
    nv = cnf.prox - 1
    with open(os.path.join(out, "base.cnf"), "w") as f:
        f.write(f"p cnf {nv} {len(cnf.cl)}\n")
        for c in cnf.cl:
            f.write(" ".join(map(str, c)) + " 0\n")
    vs = [v for _, v in c3_vars][:K]
    cubos = [[v if (i >> j) & 1 else -v for j, v in enumerate(vs)] for i in range(1 << K)]
    json.dump({"classe": classe, "orbitas": ks, "tamanhos": [len(o) for o in orbs], "S": len(S), "nv": nv,
               "ncl": len(cnf.cl), "K": K, "cubos": cubos}, open(os.path.join(out, "cubos.json"), "w"))
    pickle.dump({"fixo": fixo, "incog": incog, "ny": ny, "Tq": Tq, "c3_vars": c3_vars, "S": S,
                 "iso": iso, "dados": dados}, open(os.path.join(out, "meta.pkl"), "wb"))
    print(f"{classe} orbitas {ks} |S|={len(S)}: {nv} var, {len(cnf.cl)} clausulas, {1 << K} cubos "
          f"({time.time() - t0:.0f}s)")


def cnf_cubo(out, i, arq):
    cub = json.load(open(os.path.join(out, "cubos.json")))
    lits = cub["cubos"][int(i)]
    with open(os.path.join(out, "base.cnf")) as f:
        cab = f.readline().split()
        corpo = f.read()
    with open(arq, "w") as g:
        g.write(f"p cnf {cab[2]} {int(cab[3]) + len(lits)}\n")
        g.write(corpo)
        for l in lits:
            g.write(f"{l} 0\n")


def confere_sat(out, modelo):
    m = pickle.load(open(os.path.join(out, "meta.pkl"), "rb"))
    lits = [int(t) for ln in open(modelo) for t in ln.split()[1:] if ln.startswith("v")]
    val = [False] * (max(abs(l) for l in lits) + 2)
    for l in lits:
        if l:
            val[abs(l)] = l > 0
    viol_S = [k for k in m["S"] if isotropico_em(val, *m["dados"][k])]
    monos = [m["incog"][k] for k in range(len(m["incog"])) if val[k + 1]]
    i6, i7 = confere(m["fixo"], monos, m["ny"] + 1)
    viol = [k for k in range(len(m["iso"])) if isotropico_em(val, *m["dados"][k])]
    r = {"I6_conferido": bool(i6), "isotropicos_em_S": len(viol_S), "isotropicos_total": len(viol),
         "anf_extra": sorted(monos)}
    print(json.dumps(r))
    return r


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "gera":
        gera(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), sys.argv[6])
    elif cmd == "cnf_cubo":
        cnf_cubo(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "confere":
        confere_sat(sys.argv[2], sys.argv[3])
