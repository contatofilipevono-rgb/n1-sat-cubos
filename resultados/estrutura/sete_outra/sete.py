"""Lema das sete restricoes, F4+F4 (09/11). Script autocontido (so numpy).
Estagios:  python sete.py base | amostra N | quad | trio
  base    : T, 1275 U_Y, funcionais (7 por U) em coordenadas de L/G (40 bits); controles.
  amostra : sorteia phi em L/G, guarda os que estao em N (sem isotropico).
  quad    : procura polinomios de grau <= 2 em L/G que se anulam em N (criterio C2).
  trio    : procura a,b,c em N com as 7 combinacoes em N (contraexemplo ao lema).
"""
import itertools
import os
import sys
import time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
n = 8


def mono(s):
    return sum(1 << int(c) for c in s.replace("y", ""))


def poly(txt):
    out = set()
    for t in txt.replace(" ", "").split("+"):
        out ^= {mono(t)}
    return out


Q1 = poly("y0y2+y1y3+y4y6+y5y7")
Q2 = poly("y1y2+y0y3+y1y3+y5y6+y4y7+y5y7")
T_BRIEF = poly("y0y1y2y3 + y1y2y4y6 + y0y3y4y6 + y1y3y4y6 + y0y2y5y6 + y1y3y5y6 + y0y2y4y7 + y1y3y4y7 + "
               "y0y2y5y7 + y1y2y5y7 + y0y3y5y7 + y4y5y6y7")
PHI_F2 = poly("y0y1y4 + y0y2y4 + y0y3y4 + y1y3y4 + y2y4y5 + y0y1y6 + y0y2y6 + y1y2y6 + y0y3y6 + y0y1y7 + "
              "y1y2y7 + y2y3y7 + y1y6y7")
L3 = [sum(1 << i for i in c) for c in itertools.combinations(range(n), 3)]
I3 = {m: k for k, m in enumerate(L3)}


def vec3(P):
    return sum(1 << I3[m] for m in P)


def rref_todos(k):
    out = []
    for piv in itertools.combinations(range(n), k):
        livres = [(i, j) for i in range(k) for j in range(n) if j > piv[i] and j not in piv]
        base = np.zeros((k, n), dtype=np.uint8)
        for i in range(k):
            base[i, piv[i]] = 1
        bits = np.arange(1 << len(livres))
        M = np.broadcast_to(base, (len(bits), k, n)).copy()
        for t, (i, j) in enumerate(livres):
            M[:, i, j] = (bits >> t) & 1
        out.append(M)
    return np.concatenate(out)


def perm(A):
    """A: (N,d,d) uint8 -> permanente mod 2."""
    d = A.shape[1]
    s = np.zeros(A.shape[0], dtype=np.uint8)
    for p in itertools.permutations(range(d)):
        t = np.ones(A.shape[0], dtype=np.uint8)
        for r in range(d):
            t &= A[:, r, p[r]]
        s ^= t
    return s


def elim(rows, dim):
    """escalonamento reduzido; devolve dict pivo->vetor."""
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
    return piv


def anulador(W, dim):
    piv = elim(W, dim)
    base = []
    for f in range(dim):
        if f in piv:
            continue
        x = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1:
                x |= 1 << h
        base.append(x)
    return base


def nucleo(eqs, dim):
    """base de {x : <e,x>=0 para todo e em eqs}."""
    return anulador(eqs, dim)


def par(x):
    return bin(x).count("1") & 1


def base():
    t0 = time.time()
    prod = set()
    for a in Q1:
        for b in Q2:
            prod ^= {a | b}
    T = {m for m in prod if bin(m).count("1") == 4}
    assert T == T_BRIEF, "T do brief difere de (q1 q2)_4"
    Us = rref_todos(5)
    assert len(Us) == 97155
    ok = np.ones(len(Us), dtype=bool)
    for q in itertools.combinations(range(5), 4):
        val = np.zeros(len(Us), dtype=np.uint8)
        sub = Us[:, list(q), :]
        for m in T:
            cols = [i for i in range(n) if (m >> i) & 1]
            val ^= perm(sub[:, :, cols])
        ok &= val == 0
    iso = Us[ok]
    print("U_Y isotropicos de T:", len(iso), flush=True)
    assert len(iso) == 1275
    trip = list(itertools.combinations(range(5), 3))
    # M[u, t, k] = coeficiente do trio t em (monomio L3[k])|U
    M = np.zeros((len(iso), 10, 56), dtype=np.uint8)
    for ti, t in enumerate(trip):
        sub = iso[:, list(t), :]
        for k, m in enumerate(L3):
            cols = [i for i in range(n) if (m >> i) & 1]
            M[:, ti, k] = perm(sub[:, :, cols])
    # gauge e L
    G = [vec3({t ^ (1 << i) for t in T if (t >> i) & 1}) for i in range(n)]
    eqs = []
    for i in range(n):
        S = 255 ^ (1 << i)
        eqs.append(vec3({m for m in L3 if (S ^ m) in T and (m & S) == m}))
    Lb = nucleo(eqs, 56)
    for g in G:
        assert all(par(g & e) == 0 for e in eqs), "gauge fora de L"
    pg = elim(G, 56)
    assert len(pg) == 8 and len(Lb) == 48
    # complemento de G em L: reduz base de L modulo G e escolhe 40 independentes
    comp, pv = [], dict(pg)
    for v in Lb:
        w = v
        for h in sorted(pv, reverse=True):
            if (w >> h) & 1:
                w ^= pv[h]
        if w:
            pv[w.bit_length() - 1] = w
            comp.append(v)
    assert len(comp) == 40
    # funcionais
    F56 = np.zeros((len(iso), 7), dtype=np.uint64)
    F40 = np.zeros((len(iso), 7), dtype=np.uint64)
    postos = {}
    for u in range(len(iso)):
        rows = [sum(int(M[u, t, k]) << k for k in range(56)) for t in range(10)]   # trio t como funcional em 56
        W = [sum(par(rows[t] & g) << t for t in range(10)) for g in G]
        Ann = anulador(W, 10)
        postos[10 - len(Ann)] = postos.get(10 - len(Ann), 0) + 1
        assert len(Ann) == 7, "posto de R_U diferente de 3"
        for j, f in enumerate(Ann):
            g56 = 0
            for t in range(10):
                if (f >> t) & 1:
                    g56 ^= rows[t]
            assert all(par(g56 & g) == 0 for g in G)
            F56[u, j] = g56
            F40[u, j] = sum(par(g56 & comp[k]) << k for k in range(40))
    print("posto de R_U:", postos, flush=True)
    # controle: phi de (F2) esta em L e em N
    p = vec3(PHI_F2)
    emL = all(par(p & e) == 0 for e in eqs)
    isoF2 = int(((np.bitwise_count(np.uint64(p) & F56) & 1) == 0).all(1).sum())
    print(f"controle F2: phi em L = {emL}; U_Y isotropicos = {isoF2} (esperado 0)", flush=True)
    postoA = [len(elim([int(x) for x in F40[u]], 40)) for u in range(len(iso))]
    print("codim de A_U em L/G:", sorted(set(postoA)), flush=True)
    np.savez(os.path.join(AQUI, "base.npz"), F40=F40, F56=F56, comp=np.array(comp, dtype=np.uint64), iso=iso,
             G=np.array(G, dtype=np.uint64))
    print(f"base ok ({time.time() - t0:.0f}s)")


def conta_iso(F40, xs, lote=1024):
    """numero de U isotropicos para cada x (40 bits)."""
    out = np.zeros(len(xs), dtype=np.int32)
    for a in range(0, len(xs), lote):
        x = xs[a:a + lote]
        z = np.ones((len(x), F40.shape[0]), dtype=bool)
        for j in range(7):
            z &= (np.bitwise_count(x[:, None] & F40[None, :, j]) & 1) == 0
        out[a:a + lote] = z.sum(1)
    return out


def amostra(alvo):
    F40 = np.load(os.path.join(AQUI, "base.npz"))["F40"]
    rng = np.random.default_rng(20261109)
    achados, tot, soma, t0 = [], 0, 0, time.time()
    while len(achados) < alvo:
        xs = rng.integers(1, 1 << 40, size=1 << 15, dtype=np.uint64)
        c = conta_iso(F40, xs)
        tot += len(xs)
        soma += int(c.sum())
        achados += [int(x) for x in xs[c == 0]]
        print(f"   {tot} amostras, {len(achados)} em N ({100 * len(achados) / tot:.3f}%), media iso "
              f"{soma / tot:.2f} ({time.time() - t0:.0f}s)", flush=True)
    np.save(os.path.join(AQUI, "N_amostras.npy"), np.array(sorted(set(achados)), dtype=np.uint64))


def quad():
    Ns = np.load(os.path.join(AQUI, "N_amostras.npy"))
    rng = np.random.default_rng(1)
    rng.shuffle(Ns)
    k = len(Ns) * 2 // 3
    tr, va = Ns[:k], Ns[k:]
    pares = list(itertools.combinations(range(40), 2))

    def feats(xs):
        B = ((xs[:, None] >> np.arange(40, dtype=np.uint64)[None, :]) & 1).astype(np.uint8)
        cols = [np.ones(len(xs), dtype=np.uint8)] + [B[:, i] for i in range(40)] + [B[:, i] & B[:, j] for i, j in pares]
        return np.stack(cols, 1)

    A = feats(tr)
    rows = [int("".join(map(str, r[::-1])), 2) for r in A]
    ker = anulador(rows, A.shape[1])
    print(f"treino {len(tr)}, validacao {len(va)}; polinomios grau<=2 nulos no treino: {len(ker)}")
    V = feats(va)
    vrows = [int("".join(map(str, r[::-1])), 2) for r in V]
    vivos = [f for f in ker if all(par(f & r) == 0 for r in vrows)]
    print("   sobrevivem a validacao:", len(vivos), "| com termo constante 1:", sum(f & 1 for f in vivos))
    # so grau 1
    A1 = [r & ((1 << 41) - 1) for r in rows]
    print("   afins nulos em N:", len(anulador(A1, 41)))


def trio(maxpool):
    F40 = np.load(os.path.join(AQUI, "base.npz"))["F40"]
    Ns = np.load(os.path.join(AQUI, "N_amostras.npy"))[:maxpool]
    P = len(Ns)
    t0 = time.time()
    adj = [set() for _ in range(P)]
    ne = 0
    for a in range(P - 1):
        s = Ns[a] ^ Ns[a + 1:]
        c = conta_iso(F40, s)
        for b in np.nonzero(c == 0)[0]:
            adj[a].add(a + 1 + int(b))
            ne += 1
        if a % 200 == 0:
            print(f"   a={a}/{P}, arestas {ne} ({time.time() - t0:.0f}s)", flush=True)
    print(f"pool {P}: arestas (a+b em N) = {ne}; densidade {ne / (P * (P - 1) / 2):.5f}", flush=True)
    ntri, sol = 0, []
    for a in range(P):
        for b in adj[a]:
            for c in adj[a] & adj[b]:
                ntri += 1
                x = np.array([Ns[a] ^ Ns[b] ^ Ns[c]], dtype=np.uint64)
                if conta_iso(F40, x)[0] == 0:
                    sol.append((int(Ns[a]), int(Ns[b]), int(Ns[c])))
    print(f"triangulos: {ntri}; com a+b+c em N: {len(sol)}", flush=True)
    np.save(os.path.join(AQUI, "trios.npy"), np.array(sol, dtype=np.uint64))
    for s in sol[:5]:
        print("   TRIO:", s)


if __name__ == "__main__":
    est = sys.argv[1]
    if est == "base":
        base()
    elif est == "amostra":
        amostra(int(sys.argv[2]))
    elif est == "quad":
        quad()
    elif est == "trio":
        trio(int(sys.argv[2]))
