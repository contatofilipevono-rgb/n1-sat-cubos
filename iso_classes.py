"""(1) Todos os subespacos de codimensao 3 isotropicos para T nas 5 classes criticas de 8 variaveis
    (F4+F4, F4^2, Q4a, Q4b, Q4c): enumeracao exaustiva das 97155 formas escalonadas, vetorizada.
(2) Nucleo de T^ em L^2 (span(w1,w2) + extras). Para cada eta do nucleo (2^dim), existe U isotropico de codim 3
    com eta|U = 0?  Se sim, Delta = T + (x r) eta tem isotropico de codim 3 (U + <x, r>)."""
import itertools
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classifica_K import bloco_reg, wedge, comb, rank_gf2  # noqa: E402

n = 8


def rref_todos(k, n):
    """todas as matrizes k x n em forma escalonada reduzida (subespacos de dim k)."""
    out = []
    for piv in itertools.combinations(range(n), k):
        livres = [(i, j) for i in range(k) for j in range(n) if j > piv[i] and j not in piv]
        for bits in range(1 << len(livres)):
            M = np.zeros((k, n), dtype=np.uint8)
            for i in range(k):
                M[i, piv[i]] = 1
            for t, (i, j) in enumerate(livres):
                if (bits >> t) & 1:
                    M[i, j] = 1
            out.append(M)
    return np.array(out)


def det4(A):
    """A: (N,4,4) uint8 -> det mod 2 (permanente)."""
    s = np.zeros(A.shape[0], dtype=np.uint8)
    for p in itertools.permutations(range(4)):
        s ^= A[:, 0, p[0]] & A[:, 1, p[1]] & A[:, 2, p[2]] & A[:, 3, p[3]]
    return s


def restr_zero(T, Us):
    """Us: (N,k,n). True onde T|U = 0."""
    N, k, _ = Us.shape
    ok = np.ones(N, dtype=bool)
    for q in itertools.combinations(range(k), 4):
        val = np.zeros(N, dtype=np.uint8)
        sub = Us[:, list(q), :]
        for m in T:
            cols = [i for i in range(n) if (m >> i) & 1]
            val ^= det4(sub[:, :, cols])
        ok &= (val == 0)
    return ok


def forma_restr_zero(eta, Us):
    """eta 2-forma; True onde eta|U = 0."""
    N, k, _ = Us.shape
    ok = np.ones(N, dtype=bool)
    for a, b in itertools.combinations(range(k), 2):
        val = np.zeros(N, dtype=np.uint8)
        for m in eta:
            i, j = [t for t in range(n) if (m >> t) & 1]
            val ^= (Us[:, a, i] & Us[:, b, j]) ^ (Us[:, a, j] & Us[:, b, i])
        ok &= (val == 0)
    return ok


def nucleo_L2(T):
    L2, L6 = comb(n, 2), comb(n, 6)
    i6 = {m: k for k, m in enumerate(L6)}
    piv, ker = {}, []
    for k, m in enumerate(L2):
        img, ide = 0, 1 << k
        for t in T:
            if t & m == 0:
                img ^= 1 << i6[t | m]
        while img:
            h = img.bit_length() - 1
            if h in piv:
                img ^= piv[h][0]
                ide ^= piv[h][1]
            else:
                piv[h] = (img, ide)
                break
        else:
            ker.append({L2[j] for j in range(len(L2)) if (ide >> j) & 1})
    return ker


if __name__ == "__main__":
    Us = rref_todos(5, n)
    print("subespacos de dim 5 em F2^8:", len(Us))
    classes = {"F4+F4": [bloco_reg(0b111, 1), bloco_reg(0b111, 1)], "F4^2": [bloco_reg(0b111, 2)],
               "Q4a": [bloco_reg(0b10011, 1)], "Q4b": [bloco_reg(0b11001, 1)], "Q4c": [bloco_reg(0b11111, 1)]}
    res = {}
    for nome, bl in classes.items():
        w1, w2, off = set(), set(), 0
        for f in bl:
            a, b, d = f(off)
            w1 |= a
            w2 |= b
            off += d
        T = wedge(w1, w2)
        iso = Us[restr_zero(T, Us)]
        ker = nucleo_L2(T)
        assert w1 in [k for k in ker] or True
        nk = len(ker)
        mortos, vivos = 0, []
        for c in range(1, 1 << nk):
            eta = set()
            for j in range(nk):
                if (c >> j) & 1:
                    eta ^= ker[j]
            if forma_restr_zero(eta, iso).any():
                mortos += 1
            else:
                vivos.append(sorted(eta))
        print(f"{nome}: {len(iso)} isotropicos de codim 3; dim ker(T^ em L^2) = {nk}; "
              f"eta != 0 anulado por algum deles: {mortos}/{(1 << nk) - 1}; sem: {len(vivos)}", flush=True)
        res[nome] = {"n_iso": int(len(iso)), "dim_ker2": nk, "vivos": vivos[:50], "n_vivos": len(vivos)}
    json.dump(res, open("iso_classes.json", "w"), indent=1)
