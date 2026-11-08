"""Classificacao dos pencils (w1,w2) que violam K em grau 3, com os tres postos racionais >= 12.

defeito_d(V) = dim ker(T^ : L^d -> L^{d+4}) - dim(w1 L^{d-2} + w2 L^{d-2}),  T = w1^w2.
K (grau 3) <=> defeito_3 = 0. Com radical R de dim r:  defeito_3(V+R) = sum_j C(r,j) defeito_{3-j}(V).

Previsao teorica (nota CLASSIFICACAO_K_07NOV.md, sec. 2): com os tres postos racionais >= 12,
  defeito_0 = defeito_1 = defeito_2 = 0, e defeito_3 > 0  <=>  parte nao radical = F4+F4+F4 (defeito 16),
  e isso equivale a posto_F4(w1 + alfa w2) <= 6.
Testes:
 (A) controle: homologia de uma 2-forma em car. 2 tem serie (2z)^m (1+z)^r;
 (B) enumeracao exaustiva de multiconjuntos de blocos de Kronecker (sem L0) de dim 12..LIM com postos >= 12;
 (C) casos fora da hipotese (postos 10) e F4^3 + blocos, ate n = 20;
 (D) invariancia: conjugados GL aleatorios de F4^3 + radical; pencils aleatorios com postos >= 12.
"""
import itertools
import sys
import time
import random

LIM = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 16
random.seed(20261107)


def wedge(A, B):
    out = set()
    for a in A:
        for b in B:
            if a & b == 0:
                out ^= {a | b}
    return out


def rank_gf2(vs):
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


_comb = {}


def comb(n, k):
    if (n, k) not in _comb:
        _comb[(n, k)] = [sum(1 << i for i in c) for c in itertools.combinations(range(n), k)] if 0 <= k <= n else []
    return _comb[(n, k)]


def defeito(w1, w2, n, d):
    T = wedge(w1, w2)
    Ld = comb(n, d)
    Lt = comb(n, d + 4)
    it = {m: i for i, m in enumerate(Lt)}
    img = []
    for m in Ld:
        v = 0
        for t in T:
            if t & m == 0:
                v ^= 1 << it[t | m]
        img.append(v)
    ker = len(Ld) - rank_gf2(img)
    s = 0
    if d >= 2:
        idd = {m: i for i, m in enumerate(Ld)}
        sp = []
        for m in comb(n, d - 2):
            for w in (w1, w2):
                v = 0
                for p in w:
                    if p & m == 0:
                        v ^= 1 << idd[p | m]
                sp.append(v)
        s = rank_gf2(sp)
    return ker - s


def matriz(w, n):
    rows = [0] * n
    for p in w:
        i, j = [t for t in range(n) if (p >> t) & 1]
        rows[i] ^= 1 << j
        rows[j] ^= 1 << i
    return rows


def posto(w, n):
    return rank_gf2(matriz(w, n))


# GF(4): 0,1,2=alfa,3=alfa^2=alfa+1
MUL = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
INV = [None, 1, 3, 2]


def posto_F4(w1, w2, n):
    """posto sobre F4 de w1 + alfa*w2."""
    M = [[0] * n for _ in range(n)]
    for w, c in ((w1, 1), (w2, 2)):
        for p in w:
            i, j = [t for t in range(n) if (p >> t) & 1]
            M[i][j] ^= c
            M[j][i] ^= c
    r = 0
    for col in range(n):
        p = next((i for i in range(r, n) if M[i][col]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        iv = INV[M[r][col]]
        M[r] = [MUL[iv][x] for x in M[r]]
        for i in range(n):
            if i != r and M[i][col]:
                f = M[i][col]
                M[i] = [x ^ MUL[f][y] for x, y in zip(M[i], M[r])]
        r += 1
    return r


# ---------- blocos de Kronecker ----------
def pmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def companheira(p):
    d = p.bit_length() - 1
    C = [[0] * d for _ in range(d)]
    for i in range(1, d):
        C[i][i - 1] = 1
    for i in range(d):
        C[i][d - 1] = (p >> i) & 1
    return C


par = lambda i, j: (1 << i) | (1 << j)


def bloco_reg(p, e, inf=False):
    """par duplicado com divisor elementar p^e: w1 = sum x_i y_i, w2 = sum M_ij x_i y_j."""
    q = 1
    for _ in range(e):
        q = pmul(q, p)
    M = companheira(q)
    d = len(M)

    def f(off):
        A = {par(off + i, off + d + i) for i in range(d)}
        B = {par(off + i, off + d + j) for i in range(d) for j in range(d) if M[i][j]}
        return (B, A, 2 * d) if inf else (A, B, 2 * d)
    return f


def bloco_L(k):
    def f(off):
        xs = [off + i for i in range(k + 1)]
        ys = [off + k + 1 + i for i in range(k)]
        return {par(xs[i], ys[i]) for i in range(k)}, {par(xs[i + 1], ys[i]) for i in range(k)}, 2 * k + 1
    return f


T_ = 0b10      # t
T1 = 0b11      # t+1
F4P = 0b111    # t^2+t+1
F8A, F8B = 0b1011, 0b1101
Q4A, Q4B, Q4C = 0b10011, 0b11001, 0b11111
MENU = {
    "L1": bloco_L(1), "L2": bloco_L(2), "L3": bloco_L(3), "L4": bloco_L(4),
    "J0": bloco_reg(T_, 1), "J1": bloco_reg(T1, 1), "Ji": bloco_reg(T_, 1, inf=True),
    "J0^2": bloco_reg(T_, 2), "J1^2": bloco_reg(T1, 2), "Ji^2": bloco_reg(T_, 2, inf=True),
    "J0^3": bloco_reg(T_, 3), "J1^3": bloco_reg(T1, 3), "Ji^3": bloco_reg(T_, 3, inf=True),
    "F4": bloco_reg(F4P, 1), "F4^2": bloco_reg(F4P, 2),
    "F8a": bloco_reg(F8A, 1), "F8b": bloco_reg(F8B, 1),
    "Q4a": bloco_reg(Q4A, 1), "Q4b": bloco_reg(Q4B, 1), "Q4c": bloco_reg(Q4C, 1),
}
DIM = {k: f(0)[2] for k, f in MENU.items()}


def monta(nomes):
    w1, w2, off = set(), set(), 0
    for nm in nomes:
        a, b, d = MENU[nm](off)
        w1 |= a
        w2 |= b
        off += d
    return w1, w2, off


def postos(w1, w2, n):
    return posto(w1, n), posto(w2, n), posto(w1 ^ w2, n)


if __name__ == "__main__":
    t0 = time.time()
    # (A) homologia de uma 2-forma
    print("(A) homologia de w^ em car. 2 vs (2z)^m (1+z)^r")
    okA = 0
    for n in range(4, 11):
        for _ in range(4):
            w = set()
            for _ in range(random.randint(2, 12)):
                i, j = random.sample(range(n), 2)
                w ^= {par(i, j)}
            m = posto(w, n) // 2
            r = n - 2 * m
            for d in range(n + 1):
                # ker(w : L^d -> L^{d+2}) e im(w : L^{d-2} -> L^d)
                Lt = {mm: k for k, mm in enumerate(comb(n, d + 2))}
                Ld = {mm: k for k, mm in enumerate(comb(n, d))}
                img = []
                for mm in comb(n, d):
                    v = 0
                    for p in w:
                        if p & mm == 0:
                            v ^= 1 << Lt[p | mm]
                    img.append(v)
                ker = len(comb(n, d)) - rank_gf2(img)
                im = []
                for mm in comb(n, d - 2):
                    v = 0
                    for p in w:
                        if p & mm == 0:
                            v ^= 1 << Ld[p | mm]
                    im.append(v)
                h = ker - rank_gf2(im)
                # coeficiente de z^d em (2z)^m (1+z)^r
                prev = 2 ** m * (len(comb(r, d - m)) if 0 <= d - m <= r else 0)
                assert h == prev, (n, w, d, h, prev)
            okA += 1
    print(f"   {okA} formas, todos os graus conferem")

    # (B) enumeracao exaustiva
    print(f"(B) multiconjuntos de blocos (sem L0), dim 12..{LIM}, tres postos >= 12")
    nomes = sorted(MENU, key=lambda k: (DIM[k], k))
    combos = []

    def rec(i, acc, dim):
        if dim >= 12:
            combos.append(tuple(acc))
        for j in range(i, len(nomes)):
            if dim + DIM[nomes[j]] <= LIM:
                acc.append(nomes[j])
                rec(j, acc, dim + DIM[nomes[j]])
                acc.pop()
    rec(0, [], 0)
    testados, viol, erros = 0, [], []
    for c in combos:
        w1, w2, n = monta(c)
        r = postos(w1, w2, n)
        if min(r) < 12:
            continue
        testados += 1
        defs = [defeito(w1, w2, n, d) for d in range(4)]
        rk4 = posto_F4(w1, w2, n)
        prev_viola = (sorted(c) == ["F4", "F4", "F4"])
        if defs[3] > 0:
            viol.append((c, r, defs, rk4))
        if defs[:3] != [0, 0, 0] or (defs[3] > 0) != prev_viola or (rk4 <= 6) != prev_viola:
            erros.append((c, r, defs, rk4))
        if testados % 200 == 0:
            print(f"   ... {testados} testados ({time.time() - t0:.0f}s)", flush=True)
    print(f"   combinacoes geradas {len(combos)}, com postos >= 12: {testados}")
    print(f"   violacoes de K: {viol}")
    print(f"   divergencias da previsao: {erros}")
    assert not erros and len(viol) == 1

    # (C) casos especificos ate n = 20
    print("(C) casos especificos (defeitos d=0..3; com radical r: defeito_3 = sum C(r,j) def_{3-j})")
    casos = [("F4","F4","L1"), ("F4","F4","J0"), ("F4","F4","F4"), ("F4","F4","F4","L1"), ("F4","F4","F4","J0"),
             ("F4","F4","F4","J1^2"), ("F4","F4","F4","F4"), ("F4","F4","F4","Ji","J0"), ("F4","F4","F4","L2"),
             ("F4","F4","F4","F8a"), ("F4","F4^2"), ("F4^2","F4^2"), ("F8a","F8a"), ("F8a","F8b"), ("F4","F4","F4","L1","J1")]
    for c in casos:
        w1, w2, n = monta(c)
        r = postos(w1, w2, n)
        defs = [defeito(w1, w2, n, d) for d in range(4)]
        print(f"   {'+'.join(c):26s} n={n:2d} postos={r} defeitos={defs} posto_F4(w1+a w2)={posto_F4(w1, w2, n)}", flush=True)
    # F4^3 + radical, direto em n = 20
    w1, w2, _ = monta(("F4", "F4", "F4"))
    d20 = defeito(w1, w2, 20, 3)
    print(f"   F4^3 + L0^8 direto em n=20: defeito_3 = {d20}")
    assert d20 == 16

    # (D) invariancia e aleatorios
    print("(D) conjugados GL aleatorios de F4^3 + L0^4 (n=16) e pencils aleatorios com postos >= 12")

    def conj(w, A, n):
        """w(Ax, Ay): matriz A^T M A."""
        M = matriz(w, n)
        cols = A  # A[j] = imagem do vetor basico j (bitmask)
        out = set()
        for i in range(n):
            for j in range(i + 1, n):
                # w(A e_i, A e_j) = sum_{a in A_i, b in A_j} M[a][b]
                s = 0
                for a in range(n):
                    if (cols[i] >> a) & 1:
                        s ^= bin(M[a] & cols[j]).count("1") & 1
                if s:
                    out.add(par(i, j))
        return out

    def gl(n):
        while True:
            A = [random.getrandbits(n) for _ in range(n)]
            if rank_gf2(list(A)) == n:
                return A
    for it in range(3):
        A = gl(16)
        c1, c2 = conj(w1, A, 16), conj(w2, A, 16)
        d = defeito(c1, c2, 16, 3)
        print(f"   conjugado {it}: postos={postos(c1, c2, 16)} defeito_3={d}", flush=True)
        assert d == 16
    ok = 0
    for n in (14, 15, 16):
        k = 0
        while k < 6:
            a = set()
            b = set()
            for _ in range(random.randint(10, 40)):
                a ^= {par(*random.sample(range(n), 2))}
            for _ in range(random.randint(10, 40)):
                b ^= {par(*random.sample(range(n), 2))}
            r = postos(a, b, n)
            if min(r) < 12:
                continue
            d = defeito(a, b, n, 3)
            assert d == 0, (n, r, d)
            k += 1
            ok += 1
    print(f"   {ok} pencils aleatorios com postos >= 12 (n=14,15,16): K vale em todos")
    print(f"TUDO OK ({time.time() - t0:.0f}s)")
