"""Missao termos mistos, passo 2 revisado (09/11). Mesmo modelo de ext_mobius.py (11 variaveis, phi fixo,
A_ij, B, R livres). (a) Relaxacao linear exata de I6 (pares; produtos = colunas): inconsistencia => certificado
de paridade (lista das equacoes S combinadas). (b) Se consistente: CryptoMiniSat com a tabela-verdade em XOR nativo
+ borboleta de Mobius mod 8 em clausulas (I6 ∧ I7 completos), com limite de tempo. SAT conferido nos 2048 pontos.
Uso: python ext_cms.py ENTRADA.json SAIDA_DIR [limite_s]"""
import sys, os, json, time
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_cnf import CNF
from lift_mobius import adiciona_lift_mobius
from ext_mobius import modelo, confere, N
import pycryptosat


class XCNF(CNF):
    def __init__(self, prox):
        super().__init__(prox)
        self.xors = []

    def xor(self, vs, rhs):
        self.xors.append((list(vs), bool(int(rhs) & 1)))


def relax_I6(fixo, incog):
    pc = lambda x: bin(x).count("1")
    univ = [(m, None) for m in fixo] + [(m, k + 1) for k, m in enumerate(incog)]
    eqs = {}
    for a, b in combinations(range(len(univ)), 2):
        u = univ[a][0] | univ[b][0]
        if pc(u) >= 6:
            vs = tuple(sorted(v for (_, v) in (univ[a], univ[b]) if v is not None))
            e = eqs.setdefault(u, {})
            e[vs] = e.get(vs, 0) ^ 1
    col = {(): 0}
    linhas = []
    for S, e in eqs.items():
        r = 0
        for vs, c in e.items():
            if c:
                if vs not in col: col[vs] = len(col)
                r ^= 1 << col[vs]
        linhas.append((r, S))
    piv = {}
    for r, S in linhas:
        comb = {S}
        while r:
            h = r.bit_length() - 1
            if h in piv:
                r ^= piv[h][0]; comb ^= piv[h][1]
            else:
                piv[h] = (r, comb); break
        if r == 1:
            return {"consistente": False, "certificado_S": sorted(comb)}
    return {"consistente": True, "equacoes": len(linhas), "colunas": len(col)}


if __name__ == "__main__":
    ent, out = sys.argv[1], sys.argv[2]
    lim = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
    os.makedirs(out, exist_ok=True)
    phis = json.load(open(ent))["phi"]
    phis = [list(p) for p in phis] + [[]] * (3 - len(phis))
    fixo, incog = modelo(phis)
    t0 = time.time()
    res = {"entrada": ent, "relax_I6": relax_I6(fixo, incog), "t_relax": round(time.time() - t0, 1)}
    print(json.dumps(res), flush=True)
    if res["relax_I6"]["consistente"]:
        cnf = XCNF(len(incog) + 1)
        adiciona_lift_mobius(cnf, fixo, incog, N, i6=True, i7=True)
        s = pycryptosat.Solver(time_limit=lim, threads=int(os.environ.get("THREADS", 2)))
        for c in cnf.cl:
            s.add_clause(c)
        for vs, rhs in cnf.xors:
            s.add_xor_clause(vs, rhs)
        t1 = time.time()
        r, sol = s.solve()
        res["t_sat"] = round(time.time() - t1, 1)
        if r is True:
            monos = [incog[k] for k in range(len(incog)) if sol[k + 1]]
            i6, i7, g = confere(fixo, monos)
            res.update({"resultado": "SAT", "I6_tabela": i6, "I7_tabela": i7, "grau": g, "anf_D": sorted(set(fixo) ^ set(monos))})
        elif r is False:
            res["resultado"] = "UNSAT (CMS, sem DRAT)"
        else:
            res["resultado"] = "INDECISO"
    else:
        res["resultado"] = "UNSAT (certificado de paridade em I6)"
    print(json.dumps({k: v for k, v in res.items() if k != "anf_D"}), flush=True)
    json.dump(res, open(f"{out}/resultado.json", "w"), indent=1)
