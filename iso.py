"""Subespacos isotropicos de uma 4-forma T (T|U = 0).
Extensao: se T|U = 0, entao T|(U+v) = 0 <=> T(u_i,u_j,u_k,v) = 0 para todo triplo da base de U (condicao LINEAR em v).
max_iso: buscas gulosas aleatorias (limite inferior da dimensao maxima, com testemunha conferida).
exato_codim(T, n, c): busca exaustiva de U de codimensao c (via anuladores de dimensao c), para n pequeno."""
import itertools
import random


def avalia4(T, vs):
    """T(v1,v2,v3,v4) = sum_{monomios} det 4x4 (car. 2: permanente)."""
    s = 0
    for m in T:
        idx = [i for i in range(64) if (m >> i) & 1]
        # det sobre F2 da matriz [v_a(idx_b)]
        M = [[(v >> i) & 1 for i in idx] for v in vs]
        # eliminacao
        d = 1
        M = [r[:] for r in M]
        for c in range(4):
            p = next((r for r in range(c, 4) if M[r][c]), None)
            if p is None:
                d = 0
                break
            M[c], M[p] = M[p], M[c]
            for r in range(c + 1, 4):
                if M[r][c]:
                    M[r] = [x ^ y for x, y in zip(M[r], M[c])]
        s ^= d
    return s


def nucleo(rows, n):
    piv = {}
    for v in rows:
        for h in sorted(piv, reverse=True):
            if (v >> h) & 1:
                v ^= piv[h]
        if v:
            h = v.bit_length() - 1
            for k in list(piv):
                if (piv[k] >> h) & 1:
                    piv[k] ^= v
            piv[h] = v
    base = []
    for f in range(n):
        if f in piv:
            continue
        x = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1:
                x |= 1 << h
        base.append(x)
    return base


def rank(vs):
    piv = {}
    r = 0
    for v in vs:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                r += 1
                break
    return r


def isotropico(T, U):
    return all(avalia4(T, list(q)) == 0 for q in itertools.combinations(U, 4))


def max_iso(T, n, trials=200, seed=1):
    random.seed(seed)
    melhor = []
    for _ in range(trials):
        U = []
        while True:
            cond = []
            for tri in itertools.combinations(U, 3):
                row = 0
                for i in range(n):
                    if avalia4(T, list(tri) + [1 << i]):
                        row |= 1 << i
                cond.append(row)
            cand = [v for v in nucleo(cond, n)]
            # combinacao aleatoria do espaco admissivel, fora de span(U)
            ok = None
            for _ in range(30):
                v = 0
                for b in cand:
                    if random.random() < 0.5:
                        v ^= b
                if v and rank(U + [v]) > len(U):
                    ok = v
                    break
            if ok is None:
                # tenta cada vetor da base
                ok = next((b for b in cand if rank(U + [b]) > len(U)), None)
            if ok is None:
                break
            U.append(ok)
        if len(U) > len(melhor):
            melhor = U
    assert isotropico(T, melhor)
    return len(melhor), melhor
