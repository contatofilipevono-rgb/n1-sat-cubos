"""(09/11) Q4: o grupo Aut(T) tem elemento de ordem 17 permutando ciclicamente os 17 W do espalhamento?
Gera o grupo a partir dos geradores (matrizes 8x8 sobre F2 como listas de colunas/linhas em automorfismos_*.json)."""
import json, sys, random
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from automorfismos import aplica
from espalhamento_255 import spread

for classe in ["Q4a", "Q4b", "Q4c"]:
    gens = [tuple(A) for A in json.load(open(rf"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares\automorfismos_{classe}.json"))[classe]["geradores"]]
    # representa elemento do grupo pela permutacao de F2^8
    def perm(A):
        return tuple(aplica(A, v) for v in range(256))
    P = [perm(A) for A in gens]
    comp = lambda p, q: tuple(p[q[v]] for v in range(256))
    ident = tuple(range(256))
    grupo = {ident}; fila = [ident]
    while fila:
        g = fila.pop()
        for p in P:
            h = comp(p, g)
            if h not in grupo:
                grupo.add(h); fila.append(h)
    def ordem(g):
        k, h = 1, g
        while h != ident:
            h = comp(g, h); k += 1
        return k
    ords = {}
    for g in grupo:
        o = ordem(g); ords[o] = ords.get(o, 0) + 1
    Ws, sps, orbs = spread(classe)
    idx = {W: i for i, W in enumerate(Ws)}
    g17 = next(g for g in grupo if ordem(g) == 17) if 17 in ords else None
    ciclo = None
    if g17:
        img = [idx[frozenset(g17[v] for v in W)] for W in Ws]
        # comprimento dos ciclos da permutacao induzida nos 17 W
        vis, ciclos = set(), []
        for i in range(17):
            if i not in vis:
                c, j = 0, i
                while j not in vis:
                    vis.add(j); j = img[j]; c += 1
                ciclos.append(c)
        ciclo = ciclos
        # pontos fixos em F2^8
        fixos = sum(1 for v in range(256) if g17[v] == v)
    print(f"{classe}: |Aut(T)| = {len(grupo)}; ordens presentes: {sorted(ords)}; elementos de ordem 17: {ords.get(17, 0)}; "
          f"acao nos 17 W: ciclos {ciclo}; pontos fixos em F2^8: {fixos if g17 else None}")
