"""(09/11) Orbitas 1020/2040 de Q4: cada U encontra exatamente um W do espalhamento em dim 3 (W').
Afirmacao: a condicao 'C3|W' = 0' (1 linha) esta no espaco-linha de M_U (necessaria para isotropia).
Tambem: distribuicao de dim(U ∩ W) por U, e posto de M_U."""
import os, sys
from collections import Counter
from itertools import combinations
sys.argv = ["x"]
from analisa_testemunhas import contexto, rows_U, span
from sat_n1 import det3
from sat_n1_orbita import base
from espalhamento_255 import spread
from fecho_estrela import linhas, base_red, reduz
from feixe_255 import dimset


def base_de(S, d):
    b = []
    for v in sorted(S):
        if v and reduz(base_red(b), v):
            b.append(v)
    assert len(b) == d
    return b


def linha_cubica(b3, c3v, ny=8):
    r = 0
    for p, (m, var) in enumerate(c3v):
        idx = [j for j in range(ny) if (m >> j) & 1]
        if det3([[(b3[t] >> j) & 1 for j in idx] for t in range(3)]):
            r |= 1 << p
    return r


def main(classe):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    c3v = base(classe)[6]
    Ws, sps, orbs = spread(classe)
    for j in (1, 2):
        ok, dist, postos = 0, Counter(), Counter()
        for k in orbs[j]:
            U = sps[k]
            dims = sorted((dimset(W & U) for W in Ws), reverse=True)
            dist[tuple(Counter(dims).items())] += 1
            W = [W for W in Ws if dimset(W & U) == 3][0]
            Wp = W & U
            r = linha_cubica(base_de(Wp, 3), c3v)
            M = linhas(*dados[k])
            piv = base_red(M)
            postos[len(piv)] += 1
            if r and reduz(piv, r) == 0:
                ok += 1
        print(f"{classe} orbita {len(orbs[j])}: 'C3|W'=0' implicada por isotropia em {ok}/{len(orbs[j])}; postos M_U {dict(postos)}; dims(U∩W) {dict(dist)}")


if __name__ == "__main__":
    for c in ["Q4a", "Q4b", "Q4c"]:
        main(c)
