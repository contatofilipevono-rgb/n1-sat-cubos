"""Missao termos mistos, passo 2 (09/11): dado phi_1..phi_3 (mascaras cubicas em y), existe
D = T + sum x_i phi_i + sum_{i<j} x_i x_j A_ij + x1 x2 x3 B + R  (deg R <= 3)  com I6 ∧ I7 em 11 variaveis?
Bits: y0..y7 = 0..7, x1..x3 = 8..10. Fixos: T (F4+F4) e x_i*phi_i. Incognitas: A_ij (x_i x_j * quadratico em y),
B (x1x2x3 * linear em y) e R de graus 2 e 3 (termos lineares nao afetam I6/I7; constante idem).
Codificacao: tabela-verdade + Mobius mod 8 (lift_mobius.py). Saida: CNF DIMACS; com CaDiCaL: SAT conferido nos
2048 pontos (I6, I7 por tabela inteira) ou UNSAT com prova DRAT verificada por drat-trim.
Uso: python ext_mobius.py ENTRADA.json SAIDA_DIR [cadical] [drat-trim]
ENTRADA.json: {"phi": [[mascaras de phi1], [..phi2], [..phi3]]}  (phi vazio = controle positivo)."""
import sys, os, json, subprocess, time
from itertools import combinations
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_cnf import CNF
from lift_mobius import adiciona_lift_mobius

T = [15, 86, 89, 90, 101, 106, 149, 154, 165, 166, 169, 240]
N = 11
X = [1 << 8, 1 << 9, 1 << 10]


def modelo(phis):
    fixo = set(T)
    for i, ph in enumerate(phis):
        for m in ph:
            fixo ^= {m | X[i]}
    incog = []
    for i, j in combinations(range(3), 2):
        incog += [X[i] | X[j] | (1 << a) | (1 << b) for a, b in combinations(range(8), 2)]
    incog += [X[0] | X[1] | X[2] | (1 << a) for a in range(8)]
    incog += [sum(1 << b for b in c) for d in (2, 3) for c in combinations(range(N), d)]
    incog = [m for m in dict.fromkeys(incog) if m not in fixo]
    return sorted(fixo), incog


def confere(fixo, monos):
    pts = np.arange(1 << N)
    tt = np.zeros(1 << N, dtype=np.int64)
    for m in set(fixo) ^ set(monos):
        tt ^= ((pts & m) == m).astype(np.int64)
    a = tt.copy(); h = 1
    while h < (1 << N):
        a = a.reshape(-1, 2, h); a[:, 1, :] -= a[:, 0, :]; a = a.reshape(-1); h *= 2
    pop = np.array([bin(i).count("1") for i in range(1 << N)])
    return bool(np.all(a[pop >= 6] % 4 == 0)), bool(np.all(a[pop >= 7] % 8 == 0)), int(max(pop[a % 2 != 0]))


if __name__ == "__main__":
    ent, out = sys.argv[1], sys.argv[2]
    cad = sys.argv[3] if len(sys.argv) > 3 else None
    dt = sys.argv[4] if len(sys.argv) > 4 else None
    os.makedirs(out, exist_ok=True)
    phis = json.load(open(ent))["phi"]
    phis = [list(p) for p in phis] + [[]] * (3 - len(phis))
    fixo, incog = modelo(phis)
    cnf = CNF(len(incog) + 1)
    t0 = time.time()
    adiciona_lift_mobius(cnf, fixo, incog, N, i6=True, i7=True)
    nv = cnf.prox - 1
    with open(f"{out}/ext.cnf", "w") as f:
        f.write(f"p cnf {nv} {len(cnf.cl)}\n")
        for c in cnf.cl:
            f.write(" ".join(map(str, c)) + " 0\n")
    res = {"entrada": ent, "incognitas": len(incog), "variaveis": nv, "clausulas": len(cnf.cl), "t_cnf": round(time.time() - t0, 1)}
    if cad:
        t1 = time.time()
        p = subprocess.run([cad, "-q", f"{out}/ext.cnf", f"{out}/ext.drat"], capture_output=True, text=True) if False else \
            subprocess.run([cad, f"{out}/ext.cnf", f"{out}/ext.drat"], capture_output=True, text=True)
        res["t_sat"] = round(time.time() - t1, 1)
        if p.returncode == 10:
            lits = [int(t) for ln in p.stdout.splitlines() if ln.startswith("v") for t in ln.split()[1:]]
            pos = {l for l in lits if l > 0}
            monos = [incog[k] for k in range(len(incog)) if (k + 1) in pos]
            i6, i7, g = confere(fixo, monos)
            res.update({"resultado": "SAT", "I6_tabela": i6, "I7_tabela": i7, "grau": g, "anf_D": sorted(set(fixo) ^ set(monos))})
        elif p.returncode == 20:
            v = subprocess.run([dt, f"{out}/ext.cnf", f"{out}/ext.drat", "-t", "20000"], capture_output=True, text=True) if dt else None
            res.update({"resultado": "UNSAT", "drat_verificado": bool(v and "s VERIFIED" in v.stdout)})
            if os.path.exists(f"{out}/ext.drat") and res["drat_verificado"]:
                res["bytes_prova"] = os.path.getsize(f"{out}/ext.drat")
        else:
            res["resultado"] = f"rc{p.returncode}"
    print(json.dumps({k: v for k, v in res.items() if k != "anf_D"}))
    json.dump(res, open(f"{out}/resultado.json", "w"), indent=1)
