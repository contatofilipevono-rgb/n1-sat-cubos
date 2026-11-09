"""(09/11) Relacoes polinomiais (grau <= 2) que se anulam nas amostras de E (C3 extensiveis a I6).
Grau 1: dim do span afim. Grau 2: nucleo da matriz de avaliacao [1, c_i, c_i c_j]."""
import glob, json, sys, os
from itertools import combinations
sys.argv = ["x"]
from fecho_estrela import base_red, reduz

classe = os.environ.get("CLASSE", "Q4a")
nome = classe.replace("^", "").replace("+", "")
amostras = []
vistos = set()
for f in glob.glob(f"E_{nome}_s*.jsonl"):
    for l in open(f):
        c = tuple(json.loads(l)["c"])
        if c not in vistos:
            vistos.add(c); amostras.append(set(c))
nc = 48
print("amostras distintas:", len(amostras))
# grau 1 (afim): span de (1, c)
vs = [1 | sum(1 << (p + 1) for p in c) for c in amostras]
print("dim span afim (1,c):", len(base_red(vs)), "de", nc + 1)
# grau 2: colunas = monomios; linhas = amostras; queremos o nucleo (relacoes) -> posto da matriz
mon = [()] + [(i,) for i in range(nc)] + list(combinations(range(nc), 2))
cols = len(mon)
linhas = []
for c in amostras:
    r = 0
    for k, m in enumerate(mon):
        if all(i in c for i in m):
            r |= 1 << k
    linhas.append(r)
posto = len(base_red(linhas))
print(f"grau 2: monomios {cols}, posto da avaliacao {posto}, relacoes candidatas {cols - posto} (confiavel se amostras >> monomios)")
