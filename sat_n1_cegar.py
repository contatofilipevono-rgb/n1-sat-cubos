"""Lema N1, modelo de 9 variaveis, por CEGAR sobre CryptoMiniSat (mesma pergunta de sat_n1.py).
Diferencas em relacao a sat_n1.py:
 (a) quebra de simetria por translacao y -> y + a (a em Y): a parte cubica em Y de D muda exatamente por i_a T
     (a parte x*C3 so ganha termos de grau <= 2 em Y); como a -> i_a T e injetiva, pode-se zerar os coeficientes
     cubicos em Y nos monomios-pivo de span(i_Y T). Compativel com a normalizacao de C3 (y -> y + x v).
 (b) nao-isotropia preguicosa: resolve so I6; para a solucao achada, testa todos os U_Y; se nenhum U_Y da isotropia,
     a solucao e contraexemplo (conferido por tabela-verdade e por tem_iso3); senao acrescenta as clausulas dos U_Y
     violados e repete. UNSAT em qualquer rodada => N1 vale no modelo (certificado do resolvedor, nao conferido).
Saida incremental (flush) a cada iteracao; JSON por classe."""
import json
import os
import sys
import time
import pycryptosat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_n1 import (Pares, bloco_reg, rref_todos, restr_zero, tem_iso3, comb, pencil, modelo_nove, sistema_sat,
                    anulador, det3, confere, controles)  # noqa: E402
import itertools  # noqa: E402


def pivos_iT(Tq, ny):
    L3 = comb(range(ny), 3)
    i3 = {m: k for k, m in enumerate(L3)}
    piv = {}
    for i in range(ny):
        v = 0
        for t in Tq:
            if (t >> i) & 1:
                v ^= 1 << i3[t ^ (1 << i)]
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    return [L3[k] for k in piv]


def prepara_U(Tq, ny, c3_vars, iso):
    trip = list(itertools.combinations(range(5), 3))
    Tl = list(Tq)
    dados = []
    for B in iso:
        vecs = [sum(int(B[a, i]) << i for i in range(ny)) for a in range(5)]
        W = []
        for i in range(ny):
            w = 0
            for t_idx, (a, b, c) in enumerate(trip):
                val = 0
                for m in Tl:
                    if not (m >> i) & 1:
                        continue
                    rest = [j for j in range(ny) if (m >> j) & 1 and j != i]
                    val ^= det3([[(vecs[r] >> j) & 1 for j in rest] for r in (a, b, c)])
                w |= val << t_idx
            W.append(w)
        Ann = anulador(W, len(trip))
        coord = []
        for m, var in c3_vars:
            idx = [j for j in range(ny) if (m >> j) & 1]
            bits = 0
            for t_idx, (a, b, c) in enumerate(trip):
                bits |= det3([[(vecs[r] >> j) & 1 for j in idx] for r in (a, b, c)]) << t_idx
            coord.append((var, bits))
        dados.append((Ann, coord))
    return dados


def isotropico_em(sol, Ann, coord):
    v = 0
    for var, bits in coord:
        if sol[var]:
            v ^= bits
    return all(bin(v & f).count("1") % 2 == 0 for f in Ann)


def roda(nome, blocos, Us, max_iter):
    from n1_cegar_run import run
    return run("cms", nome, blocos, Us, max_iter, int(os.environ.get("N1_LOTE", 8)), globals())


if __name__ == "__main__":
    controles()
    classes = {"F4+F4": [bloco_reg(0b111, 1), bloco_reg(0b111, 1)], "F4^2": [bloco_reg(0b111, 2)],
               "Q4a": [bloco_reg(0b10011, 1)], "Q4b": [bloco_reg(0b11001, 1)], "Q4c": [bloco_reg(0b11111, 1)]}
    so = os.environ.get("N1_CLASSES", ",".join(classes)).split(",")
    Us = rref_todos(5, 8)
    res = {}
    arq = f"sat_cegar_{os.environ.get('N1_SUF', 'todas')}.json"
    for nome in so:
        res[nome] = roda(nome, classes[nome], Us, int(os.environ.get("N1_MAXIT", 100000)))
        json.dump(res, open(arq, "w"), indent=1)
