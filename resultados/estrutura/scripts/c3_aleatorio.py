"""(09/11) Fracao de C3 aleatorios (espaco de 48 variaveis apos gauge) SEM nenhum U isotropico, por classe.
Se for 0 em muitas amostras: candidata a 'toda C3 tem U isotropico' (N1 sem usar I6)."""
import os, sys, random
from collections import Counter
sys.argv = ["x"]
from analisa_testemunhas import contexto
from fecho_estrela import linhas

random.seed(int(os.environ.get("SEMENTE", 1)))
N = int(os.environ.get("AMOSTRAS", 2000))
for classe in ["Q4a", "Q4b", "Q4c", "F4+F4", "F4^2"]:
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    nv = len(dados[0][1])
    Ms = [linhas(*d) for d in dados]
    orb_de = {}
    for j, o in enumerate(orbs):
        for k in o:
            orb_de[k] = j
    sem = 0
    hist = Counter()
    for _ in range(N):
        c = random.getrandbits(nv)
        n_iso = [0] * len(orbs)
        for k, M in enumerate(Ms):
            if all(bin(r & c).count("1") % 2 == 0 for r in M):
                n_iso[orb_de[k]] += 1
        if sum(n_iso) == 0:
            sem += 1
        hist[sum(n_iso)] += 1
    media = sum(k * v for k, v in hist.items()) / N
    print(f"{classe}: nvars C3={nv}, #U={len(Ms)}, postos={sorted(Counter(len(M) for M in Ms).items())}; "
          f"C3 sem isotropico: {sem}/{N}; media de isotropicos {media:.2f}; min {min(hist)}", flush=True)
