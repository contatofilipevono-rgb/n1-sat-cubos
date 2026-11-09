"""Controle da codificacao de ext_cms.py com solucao conhecida (09/11): testemunha F4+F4 cubo 62 (I6 ∧ I7 em 9 var;
x = bit 8 = x1), mergulhada em 11 variaveis (x2, x3 ausentes => continua liftavel). phi1 = sua C3, phi2 = phi3 = 0.
(1) com todas as incognitas fixadas na solucao: CMS deve dar SAT; (2) com UMA incognita trocada: deve dar UNSAT
(ou SAT com outra extensao: entao conferimos pela tabela); (3) conferencia direta pela tabela de 2048 pontos."""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_mobius import modelo, confere, N
from ext_cms import XCNF
from lift_mobius import adiciona_lift_mobius
from sat_n1_orbita import base
import pycryptosat

fixo9 = base("F4+F4")[0]
w = json.load(open("resultados/github_cubos/F4F4_o012/cubo_62.json"))
assert w["resultado"] == "SAT"
D = set(fixo9) ^ set(w["conferencia"]["anf_extra"])
X1 = 1 << 8
phi1 = sorted(m ^ X1 for m in D if m & X1 and bin(m).count("1") == 4)
fixo, incog = modelo([phi1, [], []])
print("conferencia direta (I6, I7, grau):", confere(fixo, sorted(set(D) ^ set(fixo))))
sol = set(D) ^ set(fixo)
assert sol <= set(incog), "monomio fora do modelo: " + str(sorted(sol - set(incog))[:5])
cnf = XCNF(len(incog) + 1)
adiciona_lift_mobius(cnf, fixo, incog, N, i6=True, i7=True)
s = pycryptosat.Solver(threads=2)
for c in cnf.cl: s.add_clause(c)
for vs, rhs in cnf.xors: s.add_xor_clause(vs, rhs)
assum = [k + 1 if m in sol else -(k + 1) for k, m in enumerate(incog)]
print("(1) solucao conhecida aceita:", s.solve(assumptions=assum)[0])
k0 = next(k for k, m in enumerate(incog) if bin(m).count("1") == 3 and not (m >> 8))
assum2 = list(assum); assum2[k0] = -assum2[k0]
print("(2) com um monomio cubico trocado:", s.solve(assumptions=assum2)[0], "| tabela:", confere(fixo, sol ^ {incog[k0]}))
