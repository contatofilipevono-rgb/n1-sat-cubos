"""(09/11) Consequencias de I6 ∧ I7 que so envolvem C3 (monomios de grau <= 2 em C3), por eliminacao:
colunas com variaveis de R vao para o topo (eliminadas); ficam constante, C3 simples e C3xC3."""
import os, sys, json
sys.argv = ["x"]
from linear_c3_i7 import equacoes

classe = os.environ.get("CLASSE", "F4+F4")
eqs, c3v = equacoes(classe, True)
c3vars = {var for (m, var) in c3v}
baixos = {frozenset(): 0}
for t in sorted({t for e in eqs for t in e if t and t <= c3vars and len(t) <= 2}, key=lambda t: (len(t), sorted(t))):
    baixos[t] = len(baixos)
NB = len(baixos)
col = dict(baixos)
prox = NB
linhas = []
for e in eqs:
    r = 0
    for t in e:
        if t not in col:
            col[t] = prox; prox += 1
        r ^= 1 << col[t]
    linhas.append(r)
piv = {}
for r in linhas:
    while r:
        h = r.bit_length() - 1
        if h in piv: r ^= piv[h]
        else: piv[h] = r; break
res = [r for h, r in piv.items() if h < NB]
inv = {v: k for k, v in baixos.items()}
nl = sum(1 for r in res if all(len(inv[i]) <= 1 for i in range(NB) if (r >> i) & 1))
print(f"{classe}: colunas so-C3 (grau<=2) {NB}; consequencias so em C3: {len(res)} (lineares {nl}, com termo quadratico {len(res) - nl})")
json.dump([[sorted(inv[i]) for i in range(NB) if (r >> i) & 1] for r in res], open(f"quad_i7_{classe.replace('^','').replace('+','')}.json", "w"))
