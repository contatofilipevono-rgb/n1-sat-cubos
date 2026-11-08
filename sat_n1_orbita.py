"""N1 restrito a uma orbita de U_Y (08/11).
Afirmacao testada, para a classe T e um conjunto S de U_Y isotropicos (uma orbita do grupo gerado pelos 'geradores'
de automorfismos_*.json; para grupos truncados e orbita de um subgrupo, o que nao importa):
   (*)  I6(D) e C3 != 0 e, para todo U_Y em S, C3 nao isotropico em U_Y + <e_x + v>   e INSATISFAZIVEL?
UNSAT de (*) implica N1 para T (todo D com I6 tem U isotropico de codim 3, com U_Y em S).  Nenhuma quebra de
simetria e usada: o certificado DRAT vale sem argumento de grupo.  Normalizacoes usadas (as mesmas do CEGAR):
C3 modulo i_Y T (y -> y + x v) e pivos cubicos de span(i_Y T) zerados (translacao y -> y + a).
SAT: confere I6 por tabela-verdade (confere) e a nao isotropia em S por isotropico_em; conta isotropicos no total.
Env: N1_CLASSES, AUTO_ARQ, ORB_K (indice da orbita em ordem crescente de tamanho), N1_SUF."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_n1 import Pares, rref_todos, restr_zero, tem_iso3, pencil, modelo_nove, confere  # noqa: E402
from sat_n1_cegar import pivos_iT, prepara_U, isotropico_em  # noqa: E402
from sat_cnf import CNF  # noqa: E402
from automorfismos import aplica, classes  # noqa: E402
from certifica import certifica  # noqa: E402


def popc(x):
    return bin(x).count("1")


def reduz(rows):
    piv = {}
    for v in rows:
        for h in sorted(piv, reverse=True):
            if (v >> h) & 1:
                v ^= piv[h]
        if v:
            h = v.bit_length() - 1
            for k in list(piv):
                if (piv[k] >> h) & 1:
                    piv[k] ^= v
            piv[h] = v
    return tuple(sorted(piv.values()))


def orbitas(iso, gens, n=8):
    rows = [reduz([sum(int(B[a, i]) << i for i in range(n)) for a in range(B.shape[0])]) for B in iso]
    idx = {r: k for k, r in enumerate(rows)}
    visto = [-1] * len(iso)
    orbs = []
    for k in range(len(iso)):
        if visto[k] >= 0:
            continue
        o, fila = [], [k]
        visto[k] = len(orbs)
        while fila:
            a = fila.pop()
            o.append(a)
            for A in gens:
                b = idx[reduz([aplica(A, v) for v in rows[a]])]
                if visto[b] < 0:
                    visto[b] = len(orbs)
                    fila.append(b)
        orbs.append(sorted(o))
    # controle: cada orbita e fechada sob os geradores
    for o in orbs:
        so = set(o)
        for a in o:
            for A in gens:
                assert idx[reduz([aplica(A, v) for v in rows[a]])] in so
    return sorted(orbs, key=len)


def base(nome):
    w1, w2, ny = pencil(classes()[nome])
    fixo, incog, C3, Tq = modelo_nove(w1, w2, ny)
    zerar = set(pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    P = Pares(fixo, incog)
    nv = len(incog)
    cnf = CNF(nv + 1)
    por_bit = [[] for _ in range(len(P.alvos))]
    for k, v in enumerate(P.D1):
        while v:
            h = v.bit_length() - 1
            por_bit[h].append(k + 1)
            v ^= 1 << h
    for (i, j), v in P.D2.items():
        por_bit[v.bit_length() - 1].append(cnf.e(i + 1, j + 1))
    for h in range(len(por_bit)):
        cnf.xor(por_bit[h], (P.F0 >> h) & 1)
    c3_vars = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    cnf.cl.append([var for _, var in c3_vars])
    return fixo, incog, C3, Tq, ny, cnf, c3_vars


def adiciona_U(cnf, Ann, coord):
    auxs = []
    for f in Ann:
        vs = [var for var, bits in coord if popc(bits & f) & 1]
        a = cnf.novo()
        auxs.append(a)
        cnf.xor(vs + [a], 0)
    cnf.cl.append(auxs)


if __name__ == "__main__":
    nome = os.environ["N1_CLASSES"]
    k_orb = [int(t) for t in os.environ["ORB_K"].split(",")]   # uma ou varias orbitas (uniao)
    suf = os.environ.get("N1_SUF", f"{nome}_o{k_orb}")
    t0 = time.time()
    auto = json.load(open(os.environ["AUTO_ARQ"]))[nome]
    gens = [tuple(A) for A in auto["geradores"]]
    Us = rref_todos(5, 8)
    fixo, incog, C3, Tq, ny, cnf, c3_vars = base(nome)
    iso = Us[restr_zero(Tq, Us)]
    orbs = orbitas(iso, gens)
    S = sorted(k for i in k_orb for k in orbs[i])
    print(f"{nome}: orbitas {[len(o) for o in orbs]}; testando orbita {k_orb} (|S|={len(S)})", flush=True)
    dados = prepara_U(Tq, ny, c3_vars, iso)
    for k in S:
        adiciona_U(cnf, *dados[k])
    print(f"   {cnf.prox - 1} var, {len(cnf.cl)} clausulas; preparo {time.time() - t0:.0f}s", flush=True)
    if os.environ.get("N1_PROVA", "1") == "0":
        # economia de memoria: resolve sem prova; so se der UNSAT refaz com prova DRAT (certifica)
        from pysat.solvers import Solver
        t1 = time.time()
        with Solver(name="cadical195", bootstrap_with=cnf.cl) as s0:
            sat0 = s0.solve()
            mod0 = s0.get_model() if sat0 else None
        print(f"   sem prova: {'SAT' if sat0 else 'UNSAT'} ({time.time() - t1:.0f}s)", flush=True)
        if sat0:
            r = {"SAT": True, "tempo_solver_s": round(time.time() - t1, 1), "modelo": mod0}
        else:
            print("   refazendo com prova DRAT...", flush=True)
            r = certifica(cnf.cl, f"N1_orbita_{suf}")
    else:
        r = certifica(cnf.cl, f"N1_orbita_{suf}")
    out = {"classe": nome, "orbita": k_orb, "tamanho": len(S), "tamanhos": [len(o) for o in orbs],
           "SAT": r["SAT"], "tempo_solver_s": r["tempo_solver_s"]}
    if r["SAT"]:
        val = [False] * (cnf.prox + 1)
        for lit in r["modelo"]:
            if abs(lit) < len(val):
                val[abs(lit)] = lit > 0
        viol_S = [k for k in S if isotropico_em(val, *dados[k])]
        viol = [k for k in range(len(iso)) if isotropico_em(val, *dados[k])]
        monos = [incog[k] for k in range(len(incog)) if val[k + 1]]
        i6, i7 = confere(fixo, monos, ny + 1)
        C3sol = {m ^ (1 << ny) for m in monos if (m >> ny) & 1 and popc(m) == 4}
        out.update({"I6_conferido": i6, "isotropicos_em_S": len(viol_S), "isotropicos_total": len(viol),
                    "orbitas_dos_isotropicos": [sum(1 for k in viol if k in set(o)) for o in orbs],
                    "tem_iso3": tem_iso3(Tq, C3sol, iso) is not None, "anf_extra": sorted(monos)})
        print(f"   SAT ({r['tempo_solver_s']}s): I6 conferido={i6}, isotropicos em S={len(viol_S)} (deve ser 0), "
              f"total={len(viol)}, por orbita={out['orbitas_dos_isotropicos']}", flush=True)
    else:
        out.update({"verificado_DRAT": r["verificado"], "tempo_drat_s": r["tempo_drat_s"],
                    "linhas_prova": r["linhas_prova"]})
        print(f"   UNSAT ({r['tempo_solver_s']}s); DRAT verificado={r['verificado']} ({r['tempo_drat_s']}s, "
              f"{r['linhas_prova']} linhas) => N1 vale para {nome}", flush=True)
    json.dump(out, open(f"sat_orbita_{suf}.json", "w"), indent=1)
