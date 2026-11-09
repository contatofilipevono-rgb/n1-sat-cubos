"""Controles da codificacao de I7: testemunhas F4+F4 conhecidas (I7 sim / nao, por tabela-verdade) fixadas por
suposicoes no modelo base + I7; o solver deve aceitar exatamente as que tem I7. Tambem: D aleatorios do modelo."""
import json, sys, os, glob, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_n1_orbita import base
from sat_n1 import confere
from i7 import adiciona_I7
from pysat.solvers import Cadical153

B = r"C:\Users\Valer\Downloads\analise adversarial"
classe = "F4+F4"
fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
info = adiciona_I7(cnf, fixo, incog, ny + 1)
print("I7:", info, "| clausulas totais", len(cnf.cl), flush=True)
s = Cadical153(bootstrap_with=cnf.cl)
arqs = glob.glob(os.path.join(B, "q1_nuvem_08nov", "gh_F4F4_o012", "**", "cubo_*.json"), recursive=True) + \
       glob.glob(os.path.join(B, "q1_nuvem_08nov", "gh_42547926882", "**", "cubo_52.json"), recursive=True)
ok = True
for f in arqs:
    r = json.load(open(f))
    if r.get("resultado") != "SAT":
        continue
    monos = set(r["conferencia"]["anf_extra"])
    i6, i7 = confere(fixo, monos, ny + 1)
    assum = [k + 1 if m in monos else -(k + 1) for k, m in enumerate(incog)]
    sat = s.solve(assumptions=assum)
    print(os.path.basename(f), "tabela: I6", i6, "I7", i7, "| CNF(base+I7) aceita:", sat, flush=True)
    ok &= (sat == (i6 and i7))
# aleatorios: solucoes do modelo base (so I6), conferir que CNF+I7 aceita <=> I7 por tabela
sb = Cadical153(bootstrap_with=base(classe)[5].cl)
rnd = random.Random(3)
for t in range(6):
    assum = [rnd.choice([1, -1]) * (k + 1) for k in rnd.sample(range(len(incog)), 12)]
    if not sb.solve(assumptions=assum):
        continue
    mod = set(v for v in sb.get_model() if v > 0)
    monos = set(incog[k] for k in range(len(incog)) if (k + 1) in mod)
    i6, i7 = confere(fixo, monos, ny + 1)
    sat = s.solve(assumptions=[k + 1 if m in monos else -(k + 1) for k, m in enumerate(incog)])
    print("aleatoria", t, "tabela: I6", i6, "I7", i7, "| CNF aceita:", sat, flush=True)
    ok &= (sat == (i6 and i7))
print("CONTROLES I7:", "OK" if ok else "FALHA")
