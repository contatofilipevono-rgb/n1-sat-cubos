"""Certificado independente de UNSAT: CaDiCaL (python-sat, with_proof) -> prova DRAT -> drat-trim (compilado localmente
de github.com/marijnheule/drat-trim com zig cc, em ferramentas_externas/drat-trim).
Uso como biblioteca: certifica(clausulas, nome) -> dict(SAT, verificado, saida_drat).
Controles (main): F4^3 produto (UNSAT, prova deve VERIFICAR); prova truncada deve FALHAR; F4+F4 produto e SAT."""
import os
import subprocess
import sys
import time
from pysat.solvers import Solver

DRAT = os.environ.get("DRAT_TRIM", "./drat-trim")
PASTA = os.environ.get("CERT_DIR", "certificados")


def escreve_cnf(cl, arq):
    nv = max((abs(l) for c in cl for l in c), default=0)
    with open(arq, "w") as f:
        f.write(f"p cnf {nv} {len(cl)}\n")
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")


def drat(cnf_arq, prova_arq, timeout=36000):
    p = subprocess.run([DRAT, cnf_arq, prova_arq, "-t", str(timeout)], capture_output=True, text=True)
    out = p.stdout + p.stderr
    return ("s VERIFIED" in out), out


def certifica(cl, nome, truncar=False):
    os.makedirs(PASTA, exist_ok=True)
    cnf_arq = os.path.join(PASTA, f"{nome}.cnf")
    prova_arq = os.path.join(PASTA, f"{nome}.drat")
    escreve_cnf(cl, cnf_arq)
    t0 = time.time()
    with Solver(name="cadical195", bootstrap_with=cl, with_proof=True) as s:
        r = s.solve()
        prova = s.get_proof() if not r else None
        modelo = s.get_model() if r else None
    res = {"SAT": r, "tempo_solver_s": round(time.time() - t0, 1)}
    if r:
        res["modelo"] = modelo
        return res
    if truncar:
        prova = prova[: len(prova) // 3]
    with open(prova_arq, "w") as f:
        for linha in prova:
            f.write(linha.strip() + ("\n" if linha.strip().endswith("0") else " 0\n"))
    t1 = time.time()
    ok, out = drat(cnf_arq, prova_arq)
    res.update({"verificado": ok, "tempo_drat_s": round(time.time() - t1, 1), "linhas_prova": len(prova),
                "saida_drat": out[-600:]})
    return res


def cl_produto(blocos):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sat_n1 import pencil, produto_anf, comb, Pares
    from sat_cnf import CNF
    w1, w2, ny = pencil(blocos)
    fixo = produto_anf(w1, w2)
    inc = [m for m in comb(range(ny), 3) + comb(range(ny), 2) if m not in fixo]
    P = Pares(fixo, inc)
    c = CNF(len(inc) + 1)
    pb = [[] for _ in P.alvos]
    for k, v in enumerate(P.D1):
        while v:
            h = v.bit_length() - 1
            pb[h].append(k + 1)
            v ^= 1 << h
    for (i, j), v in P.D2.items():
        pb[v.bit_length() - 1].append(c.e(i + 1, j + 1))
    for h in range(len(pb)):
        c.xor(pb[h], (P.F0 >> h) & 1)
    return c.cl


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sat_n1 import bloco_reg
    r = certifica(cl_produto([bloco_reg(0b111, 1)] * 3), "controle_F4cubo")
    print("F4^3 produto:", {k: v for k, v in r.items() if k != "saida_drat"})
    assert r["SAT"] is False and r["verificado"]
    r = certifica(cl_produto([bloco_reg(0b111, 1)] * 3), "controle_F4cubo_truncado", truncar=True)
    print("F4^3 prova truncada:", {k: v for k, v in r.items() if k != "saida_drat"})
    assert r["SAT"] is False and not r["verificado"]
    r = certifica(cl_produto([bloco_reg(0b111, 1)] * 2), "controle_F4F4")
    print("F4+F4 produto: SAT =", r["SAT"])
    assert r["SAT"]
    print("controles de certificacao: ok")
