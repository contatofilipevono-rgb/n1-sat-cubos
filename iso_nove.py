"""Isotropia exata de codim 3 para Delta = T + x^C3 em Y(8) + <x> (9 variaveis).
U de codim 3: U cap Y tem codim 2 + d em Y (d = 0 ou 1). d = 0 exigiria isotropico de codim 2 de T (nao existe,
iso_exato8). Logo U = U_Y + <e_x + v>, U_Y isotropico de codim 3 de T, e (C3 + i_v T)|U_Y = 0.
Le as testemunhas de n1_nove.json; testemunhas positivas de isotropia conferidas por avaliacao direta."""
import itertools
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classifica_K import bloco_reg, wedge  # noqa: E402
from iso_classes import rref_todos, restr_zero  # noqa: E402
from iso import isotropico  # noqa: E402

n = 8


def tensor4(T):
    t = np.zeros((n,) * 4, dtype=np.int64)
    for m in T:
        idx = [i for i in range(n) if (m >> i) & 1]
        for p in itertools.permutations(idx):
            t[p] = 1
    return t


def tensor3(C):
    t = np.zeros((n,) * 3, dtype=np.int64)
    for m in C:
        idx = [i for i in range(n) if (m >> i) & 1]
        for p in itertools.permutations(idx):
            t[p] = 1
    return t


def principal(arquivo):
    J = json.load(open(arquivo))
    for nome, r in J.items():
        if not r.get("testemunha_anf"):
            print(nome, "sem testemunha")
            continue
        ny = r["ny"]
        X = 1 << ny
        w1, w2 = set(r["w1"]), set(r["w2"])
        T = wedge(w1, w2)
        anf = set(r["testemunha_anf"])
        C3 = {m ^ X for m in anf if (m & X) and bin(m).count("1") == 4}
        Delta = set(T) ^ {m for m in anf if bin(m).count("1") == 4}
        print(f"{nome}: testemunha I6 com C3 de {len(C3)} monomios")
        # I6 da testemunha conferido por tabela-verdade
        N = 1 << (ny + 1)
        iv = np.arange(N)
        tt = np.zeros(N, dtype=np.int64)
        D = set(r["fixo"]) ^ anf
        for m in D:
            tt ^= ((iv & m) == m).astype(np.int64)
        a = tt.copy()
        h = 1
        while h < N:
            a = a.reshape(-1, 2, h)
            a[:, 1, :] -= a[:, 0, :]
            a = a.reshape(-1)
            h *= 2
        pop = np.array([bin(i).count("1") for i in range(N)])
        assert not np.count_nonzero(a[pop >= 6] % 4), "testemunha nao satisfaz I6"
        nz = a[pop >= 7]
        print(f"   I6 conferido por tabela-verdade; I7 (grau >= 7 mod 8) vale? {not np.count_nonzero(nz % 8)}")
        Us = rref_todos(5, n)
        iso = Us[restr_zero(T, Us)]
        r3 = tem_iso3(T, C3, iso)
        if r3 is None:
            print("   Delta SEM isotropico de codim 3  => Lema N1 FALSO (com I6)")
        else:
            B, v = r3
            base = [sum(int(B[a_, i]) << i for i in range(n)) for a_ in range(5)] + [X | v]
            assert isotropico(Delta, base)
            print("   Delta TEM isotropico de codim 3 (testemunha conferida)")


def tem_iso3(T, C3, Us_iso):
    t = tensor4(T)
    c = tensor3(C3)
    trip = list(itertools.combinations(range(5), 3))
    for B in Us_iso:
        B = B.astype(np.int64)
        cv = np.einsum("ijk,ai,bj,ck->abc", c, B, B, B) % 2
        alvo = np.array([cv[a, b, cc] for a, b, cc in trip])
        H = np.einsum("ijkl,aj,bk,cl->iabc", t, B, B, B) % 2   # i_v T|U = sum_i v_i H[i]
        M = np.array([[H[i, a, b, cc] for a, b, cc in trip] for i in range(n)])  # n x 10
        for v in range(1 << n):
            vv = np.array([(v >> i) & 1 for i in range(n)])
            if np.array_equal((vv @ M + alvo) % 2, np.zeros(len(trip), dtype=np.int64)):
                return B, v
    return None


if __name__ == "__main__":
    import os
    principal(os.environ["ISO_ARQ"])

