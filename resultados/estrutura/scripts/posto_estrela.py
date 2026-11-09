"""Funcao posto r(S) = posto das condicoes de isotropia de {W+v : v em S} para S contido em Y/W (09/11)."""
import os, sys, json, random
from itertools import combinations
sys.argv = ["x"]
from analisa_testemunhas import contexto
from espalhamento_255 import spread
from fecho_estrela import linhas, base_red
from feixe_255 import isos

BASE = r"C:\Users\Valer\Downloads\analise adversarial"


def prep(classe):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    Ws, sps, orbs = spread(classe)
    idx_por_span = {sps[k]: k for k in orbs[0]}
    estrelas = []
    for W in Ws:
        reps, vistos = [], set(W)
        for v in range(1, 256):
            if v not in vistos:
                reps.append(v)
                vistos |= {v ^ w for w in W}
        cls = {v ^ w: v for v in reps for w in W}
        M = {v: linhas(*dados[idx_por_span[frozenset(W | {v ^ w for w in W})]]) for v in reps}
        estrelas.append((W, reps, cls, M))
    return estrelas, sps, orbs


def r(M, S):
    return len(base_red([x for v in S for x in M[v]]))


def main(classe):
    estrelas, sps, orbs = prep(classe)
    W, reps, cls, M = estrelas[0]
    # pares, retas (3 pontos), planos (7 pontos), conjuntos aleatorios
    pares = sorted({r(M, [a, b]) for a, b in combinations(reps, 2)})
    retas = sorted({r(M, [a, b, cls[a ^ b]]) for a, b in combinations(reps, 2)})
    planos = set()
    for a, b, c in combinations(reps, 3):
        if cls[a ^ b] == c:
            continue
        P = {a, b, c, cls[a ^ b], cls[a ^ c], cls[b ^ c], cls[a ^ b ^ c]}
        planos.add(r(M, P))
    tres_gen = sorted({r(M, [a, b, c]) for a, b, c in combinations(reps, 3) if cls[a ^ b] != c})
    print(f"{classe}: r(1)=7; r(par)={pares}; r(reta,3pts)={retas}; r(3 pts gerais)={tres_gen}; r(plano,7pts)={sorted(planos)}; r(tudo)={r(M, reps)}")
    return estrelas


def testemunha_plano():
    estrelas, sps, orbs = prep("Q4a")
    rj = json.load(open(os.path.join(BASE, "q1_nuvem_08nov", "colab_Q4a_o1_cubo1_SAT.json")))
    viol = set(isos("Q4a", rj["conferencia"]["anf_extra"]))
    for W, reps, cls, M in estrelas:
        S = [v for v in reps if any(k in viol and sps[k] == frozenset(W | {v ^ w for w in W}) for k in orbs[0])]
        if S:
            fech = all(cls[a ^ b] in S for a, b in combinations(S, 2))
            print("Q4a Colab cubo 1: pontos isotropicos na estrela:", len(S), "fechado por soma (plano):", fech)


if __name__ == "__main__":
    for c in ["Q4a", "Q4b", "Q4c"]:
        main(c)
    testemunha_plano()
