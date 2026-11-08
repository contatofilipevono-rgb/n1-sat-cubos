"""Grupo G = { A em GL(8,2) : A^* T = T } para T = parte quartica de q1 q2 (4-forma alternada em Y = F_2^8).
Busca por retrocesso coluna a coluna (A e_j = c_j) com poda por invariantes:
  posto da 2-forma i_u i_v T (pares) e posto da aplicacao w -> i_w i_u T (vetores), e valores exatos de T nas
  quadras de colunas ja escolhidas.  Cada elemento achado e conferido: T(A e_i, A e_j, A e_k, A e_l) = T(e_..)
  para TODAS as quadras (70), o que equivale a A^* T = T.
Tambem: acao de G na parte C3 (cubicas em Y modulo i_Y T, coordenadas = monomios-complemento de modelo_nove)
e nas U_Y isotropicas (orbitas)."""
import itertools
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_n1 import bloco_reg, pencil, modelo_nove, rref_todos, restr_zero, comb  # noqa: E402

N = 8


def contrai(F, v):
    """i_v F para forma alternada F dada como conjunto de monomios (bitmasks)."""
    out = set()
    for m in F:
        x = m & v
        while x:
            b = x & -x
            out ^= {m ^ b}
            x ^= b
    return out


def avalia(F, vs):
    G = F
    for v in vs:
        G = contrai(G, v)
        if not G:
            return 0
    return 1 if G == {0} else 0


def posto2(F2):
    """posto da 2-forma (conjunto de pares)."""
    rows = [0] * N
    for m in F2:
        i, j = [k for k in range(N) if (m >> k) & 1]
        rows[i] ^= 1 << j
        rows[j] ^= 1 << i
    piv = {}
    r = 0
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                r += 1
                break
    return r


def grupo(T, limite=10 ** 6, log=True):
    t0 = time.time()
    vecs = range(1, 1 << N)
    iT = {u: frozenset(contrai(T, u)) for u in vecs}
    inv1 = {}
    for u in vecs:
        # posto da aplicacao w -> i_w i_u T (vetor de invariantes: multiconjunto de postos das 2-formas i_w i_u T)
        ps = sorted(posto2(contrai(iT[u], w)) for w in vecs)
        inv1[u] = tuple(ps)
    p2 = {}

    def par(u, v):
        k = (u, v) if u < v else (v, u)
        if k not in p2:
            p2[k] = posto2(contrai(iT[u], v))
        return p2[k]
    E = [1 << i for i in range(N)]
    alvo4 = {q: avalia(T, [E[i] for i in q]) for q in itertools.combinations(range(N), 4)}
    cand = [[u for u in vecs if inv1[u] == inv1[E[j]]] for j in range(N)]
    elems = []

    def rec(cols, span):
        if len(elems) >= limite:
            return
        j = len(cols)
        if j == N:
            elems.append(tuple(cols))
            return
        for u in cand[j]:
            if u in span:
                continue
            if any(par(cols[i], u) != par(E[i], E[j]) for i in range(j)):
                continue
            ok = True
            for q in itertools.combinations(range(j), 3):
                if avalia(T, [cols[q[0]], cols[q[1]], cols[q[2]], u]) != alvo4[q + (j,)]:
                    ok = False
                    break
            if ok:
                rec(cols + [u], span | {s ^ u for s in span})
    rec([], {0})
    # conferencia completa
    for A in elems:
        for q, val in alvo4.items():
            assert avalia(T, [A[i] for i in q]) == val
    if log:
        print(f"   |G| = {len(elems)}{' (limite)' if len(elems) >= limite else ''} ({time.time() - t0:.0f}s)",
              flush=True)
    return elems


def aplica(A, v):
    """A v, A dada por colunas."""
    r = 0
    i = 0
    while v:
        if v & 1:
            r ^= A[i]
        v >>= 1
        i += 1
    return r


def puxa_cubica(A, m):
    """parte cubica de (monomio m) o A, como forma alternada: coeficiente de e_i e_j e_k = det das linhas de m nas
    colunas A e_i, A e_j, A e_k."""
    idx = [k for k in range(N) if (m >> k) & 1]
    out = set()
    for i, j, k in itertools.combinations(range(N), 3):
        M = [[(A[c] >> r) & 1 for c in (i, j, k)] for r in idx]
        d = (M[0][0] & M[1][1] & M[2][2]) ^ (M[0][0] & M[1][2] & M[2][1]) ^ (M[0][1] & M[1][0] & M[2][2]) ^ \
            (M[0][1] & M[1][2] & M[2][0]) ^ (M[0][2] & M[1][0] & M[2][1]) ^ (M[0][2] & M[1][1] & M[2][0])
        if d:
            out ^= {(1 << i) | (1 << j) | (1 << k)}
    return out


def acao_C3(T, A, compl):
    """matriz (lista de colunas como bitmask sobre indices de compl) da acao C3 -> A^* C3 modulo i_Y T."""
    L3 = comb(range(N), 3)
    i3 = {m: k for k, m in enumerate(L3)}
    piv = {}
    for i in range(N):
        v = 0
        for t in contrai(T, 1 << i):
            v ^= 1 << i3[t]
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    ic = {i3[m]: k for k, m in enumerate(compl)}
    cols = []
    for m in compl:
        v = 0
        for t in puxa_cubica(A, m):
            v ^= 1 << i3[t]
        # reduz modulo span(i_Y T): elimina bits-pivo
        for h in sorted(piv, reverse=True):
            if (v >> h) & 1:
                v ^= piv[h]
        col = 0
        while v:
            h = v.bit_length() - 1
            col |= 1 << ic[h]
            v ^= 1 << h
        cols.append(col)
    return cols


def compoe(A, B):
    """(A B) e_i = A (B e_i)."""
    return tuple(aplica(A, b) for b in B)


def geradores(G):
    """conjunto pequeno de geradores: acrescenta elementos ate o fecho ter |G| elementos."""
    import random
    rnd = random.Random(1)
    Gs = set(G)
    ident = tuple(1 << i for i in range(N))
    gens, fecho = [], {ident}
    while len(fecho) < len(Gs):
        A = rnd.choice(G)
        if A in fecho:
            continue
        gens.append(A)
        fila = list(fecho)
        while fila:
            X = fila.pop()
            for g in gens:
                Y = compoe(g, X)
                if Y not in fecho:
                    fecho.add(Y)
                    fila.append(Y)
    assert fecho == Gs
    return gens


def classes():
    return {"F4+F4": [bloco_reg(0b111, 1), bloco_reg(0b111, 1)], "F4^2": [bloco_reg(0b111, 2)],
            "Q4a": [bloco_reg(0b10011, 1)], "Q4b": [bloco_reg(0b11001, 1)], "Q4c": [bloco_reg(0b11111, 1)]}


if __name__ == "__main__":
    Us = rref_todos(5, 8)
    res = {}
    for nome, bl in classes().items():
        if nome not in os.environ.get("N1_CLASSES", nome):
            continue
        w1, w2, ny = pencil(bl)
        fixo, incog, C3, Tq = modelo_nove(w1, w2, ny)
        T = set(Tq)
        print(nome, flush=True)
        lim = int(os.environ.get("AUTO_LIMITE", 10 ** 6))
        G = grupo(T, limite=lim)
        if len(G) < lim:
            gens = geradores(G)
            print(f"   {len(gens)} geradores (fecho conferido = |G|)", flush=True)
        else:
            import random
            gens = random.Random(1).sample(G, 12)
            print("   grupo truncado: 12 elementos aleatorios como 'geradores' (orbitas = do subgrupo gerado)",
                  flush=True)
        # orbitas nas U_Y isotropicas
        iso = Us[restr_zero(Tq, Us)]

        def chave(B):
            rows = [sum(int(B[a, i]) << i for i in range(N)) for a in range(B.shape[0])]
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
            return tuple(sorted(piv.values()))
        idx = {chave(B): k for k, B in enumerate(iso)}
        rowsU = [list(chave(B)) for B in iso]
        visto = [-1] * len(iso)
        orb = 0
        tam = []
        for k in range(len(iso)):
            if visto[k] >= 0:
                continue
            fila = [k]
            visto[k] = orb
            cnt = 0
            while fila:
                a = fila.pop()
                cnt += 1
                for A in gens:
                    img = [aplica(A, v) for v in rowsU[a]]
                    piv = {}
                    for v in img:
                        for h in sorted(piv, reverse=True):
                            if (v >> h) & 1:
                                v ^= piv[h]
                        if v:
                            h = v.bit_length() - 1
                            for kk in list(piv):
                                if (piv[kk] >> h) & 1:
                                    piv[kk] ^= v
                            piv[h] = v
                    b = idx[tuple(sorted(piv.values()))]   # G preserva isotropia => imagem esta na lista
                    if visto[b] < 0:
                        visto[b] = orb
                        fila.append(b)
            tam.append(cnt)
            orb += 1
        print(f"   U_Y: {len(iso)} em {orb} orbitas, tamanhos {sorted(tam, reverse=True)}", flush=True)
        res[nome] = {"ordem": len(G), "geradores": gens, "elementos": G, "orbitas_U": orb,
                     "tamanhos_orbitas_U": sorted(tam)}
    json.dump(res, open(f"automorfismos_{os.environ.get('N1_SUF', 'todas')}.json", "w"))
