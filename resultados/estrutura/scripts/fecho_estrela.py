"""Lema candidato (09/11): para W do espalhamento, S_W(C3) = {v : W+<v> isotropico} U W e subespaco.
Isotropia em U e linear em C3: C3 em K_U = {M_U c = 0}. O fecho por soma vale para todo C3 sse
rowspace(M_{v1+v2}) contido em rowspace(M_{v1}) + rowspace(M_{v2}) para todos v1, v2 (mesmo W).
Teste exato (algebra linear F2) sobre as variaveis de C3 do modelo (apos fixar o gauge)."""
import os, sys, json
from itertools import combinations
sys.argv = ["x"]
from analisa_testemunhas import contexto, rows_U, span
from espalhamento_255 import spread
from feixe_255 import dimset


def linhas(Ann, coord):
    """linhas de M_U como bitmasks sobre o indice da variavel de C3 (posicao em coord)."""
    out = []
    for f in Ann:
        r = 0
        for p, (var, bits) in enumerate(coord):
            if bin(bits & f).count("1") & 1:
                r |= 1 << p
        out.append(r)
    return out


def base_red(rows):
    piv = {}
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    return piv


def reduz(piv, v):
    while v:
        h = v.bit_length() - 1
        if h not in piv:
            return v
        v ^= piv[h]
    return 0


def main(classe):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    Ws, sps, orbs = spread(classe)
    idx_por_span = {sps[k]: k for k in orbs[0]}
    nvars = len(dados[0][1])
    falhas = 0
    postos = []
    for wi, W in enumerate(Ws):
        Wl = sorted(W)
        reps = []  # representantes de Y/W
        vistos = set(W)
        for v in range(1, 256):
            if v not in vistos:
                reps.append(v)
                vistos |= {v ^ w for w in W}
        assert len(reps) == 15
        def U_de(v):
            return idx_por_span[frozenset(W | {v ^ w for w in W})]
        M = {v: linhas(*dados[U_de(v)]) for v in reps}
        cls = {}
        for v in reps:
            for w in W:
                cls[v ^ w] = v
        postos.append([len(base_red(M[v])) for v in reps])
        for a, b in combinations(reps, 2):
            c = cls[a ^ b]
            piv = base_red(M[a] + M[b])
            if any(reduz(piv, r) for r in M[c]):
                falhas += 1
        # posto conjunto: dim das condicoes de "toda a estrela isotropica"
        tot = base_red([r for v in reps for r in M[v]])
        if wi == 0:
            print(f"  {classe}: nvars C3={nvars}; posto de M_U por v: {postos[-1]}; posto da estrela inteira: {len(tot)}")
    print(f"{classe}: falhas do fecho (pares v1,v2 em 17 W): {falhas} de {17*105}")
    return falhas


if __name__ == "__main__":
    for c in ["Q4a", "Q4b", "Q4c"]:
        main(c)
