"""Compara duas codificacoes de I7 (pares/triplas `i7.py` vs Mobius mod 8 `lift_mobius.py`) no mesmo problema:
 (1) controles: testemunhas F4+F4 (cubo 62 com I7: aceitar; cubos 28 e 52 sem I7: rejeitar);
 (2) tamanho; (3) tempo ate SAT no cubo 62 de F4+F4 orbitas 0,1,2, k=6 (ha solucao com I7 nesse cubo).
Uso: python compara_codificacoes.py [limite_s]"""
import sys, os, json, glob, time, threading, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_n1 import rref_todos, restr_zero, confere
from sat_n1_cegar import prepara_U
from sat_n1_orbita import base, orbitas, adiciona_U
from i7 import adiciona_I7
from lift_mobius import adiciona_lift_mobius
from pysat.solvers import Cadical195

B = r"C:\Users\Valer\Downloads\analise adversarial\q1_nuvem_08nov"
LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 1800
classe = "F4+F4"


def monta(cod, com_U):
    fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
    if com_U:
        gens = [tuple(A) for A in json.load(open("automorfismos_F4F4.json"))[classe]["geradores"]]
        Us = rref_todos(5, 8); iso = Us[restr_zero(Tq, Us)]
        orbs = orbitas(iso, gens)
        dados = prepara_U(Tq, ny, c3v, iso)
        for k in sorted(k for i in (0, 1, 2) for k in orbs[i]):
            adiciona_U(cnf, *dados[k])
    if cod == "pares":
        adiciona_I7(cnf, fixo, incog, ny + 1)
    else:
        adiciona_lift_mobius(cnf, fixo, incog, ny + 1, i6=False, i7=True)
    return fixo, incog, ny, cnf, c3v


def resolve(cl, assum, lim):
    s = Cadical195(bootstrap_with=cl)
    t = threading.Timer(lim, s.interrupt); t.start()
    t0 = time.time()
    r = s.solve_limited(assumptions=assum, expect_interrupt=True)
    t.cancel()
    m = s.get_model() if r else None
    s.delete()
    return r, time.time() - t0, m


if __name__ == "__main__":
    for cod in ("mobius", "pares"):
        fixo, incog, ny, cnf, c3v = monta(cod, False)
        print(f"[{cod}] sem isotropia: {len(cnf.cl)} clausulas, {cnf.prox - 1} variaveis", flush=True)
        ok = True
        for f in glob.glob(B + r"\gh_F4F4_o012\**\cubo_*.json", recursive=True) + [B + r"\gh_42547926882\res-52\cubo_52.json"]:
            r = json.load(open(f))
            if r.get("resultado") != "SAT":
                continue
            ms = set(r["conferencia"]["anf_extra"])
            i6, i7 = confere(fixo, ms, ny + 1)
            ac, _, _ = resolve(cnf.cl, [k + 1 if m in ms else -(k + 1) for k, m in enumerate(incog)], 120)
            print(f"   controle {os.path.basename(f)}: tabela I6={i6} I7={i7} | aceita={ac}", flush=True)
            ok &= (ac == (i6 and i7))
        print(f"[{cod}] CONTROLES {'OK' if ok else 'FALHA'}", flush=True)
    cubo = [[v if (62 >> j) & 1 else -v for j, v in enumerate([v for _, v in base(classe)[6]][:6])]][0]
    for cod in ("mobius", "pares"):
        fixo, incog, ny, cnf, c3v = monta(cod, True)
        r, t, m = resolve(cnf.cl, cubo, LIM)
        extra = ""
        if r:
            ms = [incog[k] for k in range(len(incog)) if m[k] > 0]
            extra = f" I6,I7 por tabela = {confere(fixo, ms, ny + 1)}"
        print(f"[{cod}] cubo 62 (orbitas 0,1,2, k=6): {len(cnf.cl)} clausulas; resultado {r} em {t:.0f}s{extra}", flush=True)
