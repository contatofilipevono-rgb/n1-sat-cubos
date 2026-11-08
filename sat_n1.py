"""Lema N1 no modelo de 9 variaveis via SAT com XOR (CryptoMiniSat / pycryptosat).
D = q1 q2 + x*C3 + R3 + R2 em Y(8) + x, T = w1^w2 critico, C3 tomado modulo i_Y T (y -> y + x v).
I6: bits por contagem de pares (solver_pares.Pares): F0 + sum D1[k] u_k + sum D2[k,l] u_k u_l = 0,
    codificado com uma variavel AND por par (k,l) relevante e uma clausula XOR por conjunto S.
Nao-isotropia: todo U de codim 3 e U_Y + <e_x + v>, U_Y isotropico de codim 3 de T (iso_classes); exige-se,
    para cada U_Y, C3|U_Y fora de W_U = { i_v T|U_Y : v }  (OR de funcionais do anulador de W_U).
SAT  => contraexemplo a N1 (conferido: I6 por tabela-verdade, e isotropia exata por iso_nove);
UNSAT => N1 vale neste modelo para essa classe (certificado do resolvedor; nao conferido independentemente).
Controles: sem a nao-isotropia e SAT; produto F4^3 (12 var) e UNSAT; produto F4+F4 (8 var) e SAT."""
import itertools
import json
import os
import sys
import time
import numpy as np
import pycryptosat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver_pares import Pares  # noqa: E402
from classifica_K import bloco_reg, wedge  # noqa: E402
from iso_classes import rref_todos, restr_zero  # noqa: E402
from iso_nove import tem_iso3  # noqa: E402


def comb(idx, k):
    return [sum(1 << i for i in c) for c in itertools.combinations(idx, k)]


def produto_anf(w1, w2):
    """PARTE QUARTICA de q1*q2. CORRECAO 08/11: antes devolvia o produto inteiro (com 8-12 cubicos e ate 2
    quadraticos), e esses monomios saiam das incognitas, ficando presos em 1: modelo restrito. Agora todos os
    cubicos/quadraticos sao incognitas livres."""
    out = set()
    for a in w1:
        for b in w2:
            out ^= {a | b}
    return {m for m in out if bin(m).count("1") == 4}


def pencil(blocos):
    w1, w2, off = set(), set(), 0
    for f in blocos:
        a, b, d = f(off)
        w1 |= a
        w2 |= b
        off += d
    return w1, w2, off


def sistema_sat(P, s):
    """adiciona I6 ao solver s; variaveis 1..len(inc) = u; devolve proximo indice livre."""
    nv = len(P.inc)
    prox = nv + 1
    pv = {}
    for (i, j) in P.D2:
        p = prox
        prox += 1
        pv[(i, j)] = p
        a, b = i + 1, j + 1
        s.add_clause([-p, a])
        s.add_clause([-p, b])
        s.add_clause([p, -a, -b])
    nbits = len(P.alvos)
    por_bit = [[] for _ in range(nbits)]
    for k, v in enumerate(P.D1):
        while v:
            h = v.bit_length() - 1
            por_bit[h].append(k + 1)
            v ^= 1 << h
    for (i, j), v in P.D2.items():
        h = v.bit_length() - 1
        por_bit[h].append(pv[(i, j)])
    for h in range(nbits):
        rhs = bool((P.F0 >> h) & 1)
        if por_bit[h]:
            s.add_xor_clause(por_bit[h], rhs)
        elif rhs:
            s.add_clause([])  # impossivel
    return prox


def det3(M):
    return (M[0][0] & M[1][1] & M[2][2]) ^ (M[0][0] & M[1][2] & M[2][1]) ^ (M[0][1] & M[1][0] & M[2][2]) ^ \
           (M[0][1] & M[1][2] & M[2][0]) ^ (M[0][2] & M[1][0] & M[2][1]) ^ (M[0][2] & M[1][1] & M[2][0])


def rank_rows(rows):
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


def anulador(W, dim):
    """base do anulador (vetores f com <f,w> = 0) de span(W) em F2^dim."""
    piv = {}
    for v in W:
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
    for f in range(dim):
        if f in piv:
            continue
        x = 1 << f
        for h, v in piv.items():
            if (v >> f) & 1:
                x |= 1 << h
        base.append(x)
    return base


def nao_isotropia(s, prox, T, ny, c3_vars, iso):
    """c3_vars: lista de (monomio cubico em Y, var SAT). Adiciona clausulas; devolve prox."""
    trip = list(itertools.combinations(range(5), 3))
    Tl = list(T)
    triviais = 0
    for B in iso:
        vecs = [sum(int(B[a, i]) << i for i in range(ny)) for a in range(5)]
        # W_U: imagens de i_{e_i} T restritas (10 bits)
        W = []
        for i in range(ny):
            w = 0
            for t_idx, (a, b, c) in enumerate(trip):
                val = 0
                for m in Tl:
                    if not (m >> i) & 1:
                        continue
                    rest = [j for j in range(ny) if (m >> j) & 1 and j != i]
                    M = [[(vecs[r] >> j) & 1 for j in rest] for r in (a, b, c)]
                    val ^= det3(M)
                w |= val << t_idx
            W.append(w)
        Ann = anulador(W, len(trip))
        if not Ann:
            triviais += 1
            s.add_clause([])
            continue
        # coordenada t de C3|U = sum_k c_k * m_k(u_a,u_b,u_c)
        coord = []
        for m, var in c3_vars:
            idx = [j for j in range(ny) if (m >> j) & 1]
            bits = 0
            for t_idx, (a, b, c) in enumerate(trip):
                M = [[(vecs[r] >> j) & 1 for j in idx] for r in (a, b, c)]
                bits |= det3(M) << t_idx
            coord.append((var, bits))
        auxs = []
        for f in Ann:
            vs = [var for var, bits in coord if bin(bits & f).count("1") & 1]
            a = prox
            prox += 1
            auxs.append(a)
            s.add_xor_clause(vs + [a], False)   # a = XOR(vs)
        s.add_clause(auxs)
    return prox, triviais


def modelo_nove(w1, w2, ny):
    X = 1 << ny
    fixo = produto_anf(w1, w2)
    Y = list(range(ny))
    todos = list(range(ny + 1))
    L3 = comb(Y, 3)
    i3 = {m: k for k, m in enumerate(L3)}
    Tq = wedge(w1, w2)
    piv = {}
    for i in Y:
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
    compl = [L3[k] for k in range(len(L3)) if k not in piv]
    C3 = [X | m for m in compl]
    incog = [m for m in C3 + comb(todos, 3) + comb(todos, 2) if m not in fixo]
    return fixo, incog, C3, Tq


def confere(fixo, sol_monos, ny_total):
    N = 1 << ny_total
    iv = np.arange(N)
    tt = np.zeros(N, dtype=np.int64)
    for m in set(fixo) ^ set(sol_monos):
        tt ^= ((iv & m) == m).astype(np.int64)
    a = tt.copy()
    h = 1
    while h < N:
        a = a.reshape(-1, 2, h)
        a[:, 1, :] -= a[:, 0, :]
        a = a.reshape(-1)
        h *= 2
    pop = np.array([bin(i).count("1") for i in range(N)])
    return not np.count_nonzero(a[pop >= 6] % 4), not np.count_nonzero(a[pop >= 7] % 8)


def controles():
    print("controles:")
    # produto F4+F4 (8 var): SAT
    w1, w2, ny = pencil([bloco_reg(0b111, 1), bloco_reg(0b111, 1)])
    fixo = produto_anf(w1, w2)
    inc = [m for m in comb(range(ny), 3) + comb(range(ny), 2) if m not in fixo]
    s = pycryptosat.Solver()
    sistema_sat(Pares(fixo, inc), s)
    r, sol = s.solve()
    monos = [inc[k] for k in range(len(inc)) if sol[k + 1]]
    print("   F4+F4 produto (8 var): SAT =", r, "| I6 conferido:", confere(fixo, monos, ny)[0] if r else None)
    assert r and confere(fixo, monos, ny)[0]
    # produto F4^3 (12 var): UNSAT
    w1, w2, ny = pencil([bloco_reg(0b111, 1)] * 3)
    fixo = produto_anf(w1, w2)
    inc = [m for m in comb(range(ny), 3) + comb(range(ny), 2) if m not in fixo]
    s = pycryptosat.Solver()
    sistema_sat(Pares(fixo, inc), s)
    t0 = time.time()
    r, _ = s.solve()
    print(f"   F4^3 produto (12 var): SAT = {r} ({time.time() - t0:.0f}s)  [esperado UNSAT]")
    assert not r
    # Q4a + Ji (10 var): UNSAT pela classificacao (classe de posto minimo 8 fora da lista)
    w1, w2, ny = pencil([bloco_reg(0b10011, 1), bloco_reg(0b10, 1, inf=True)])
    fixo = produto_anf(w1, w2)
    inc = [m for m in comb(range(ny), 3) + comb(range(ny), 2) if m not in fixo]
    s = pycryptosat.Solver()
    sistema_sat(Pares(fixo, inc), s)
    r, _ = s.solve()
    print("   Q4a+Ji produto (10 var): SAT =", r, " [esperado UNSAT]")
    assert not r


if __name__ == "__main__":
    controles()
    classes = {"F4+F4": [bloco_reg(0b111, 1), bloco_reg(0b111, 1)], "F4^2": [bloco_reg(0b111, 2)],
               "Q4a": [bloco_reg(0b10011, 1)], "Q4b": [bloco_reg(0b11001, 1)], "Q4c": [bloco_reg(0b11111, 1)]}
    so = os.environ.get("N1_CLASSES", ",".join(classes)).split(",")
    res = {}
    Us = rref_todos(5, 8)
    for nome in so:
        t0 = time.time()
        w1, w2, ny = pencil(classes[nome])
        fixo, incog, C3, Tq = modelo_nove(w1, w2, ny)
        P = Pares(fixo, incog)
        iso = Us[restr_zero(Tq, Us)]
        # (i) sem nao-isotropia: SAT esperado
        s0 = pycryptosat.Solver()
        sistema_sat(P, s0)
        r0, _ = s0.solve()
        # (ii) com nao-isotropia
        s = pycryptosat.Solver()
        prox = sistema_sat(P, s)
        c3_vars = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
        prox, triv = nao_isotropia(s, prox, Tq, ny, c3_vars, iso)
        r, sol = s.solve()
        linha = {"sem_restricao_SAT": r0, "isotropicos_U_Y": int(len(iso)), "U_triviais": triv, "N1_contraexemplo": r}
        if r:
            monos = [incog[k] for k in range(len(incog)) if sol[k + 1]]
            i6, i7 = confere(fixo, monos, ny + 1)
            C3sol = {m ^ (1 << ny) for m in monos if (m >> ny) & 1 and bin(m).count("1") == 4}
            iso_check = tem_iso3(Tq, C3sol, iso)
            linha.update({"I6_conferido": i6, "I7": i7, "isotropico_codim3_encontrado": iso_check is not None,
                          "anf_extra": sorted(monos)})
            assert i6 and iso_check is None
        print(f"{nome}: sem restricao SAT={r0}; U_Y={len(iso)} (triviais {triv}); "
              f"CONTRAEXEMPLO A N1? {r} ({time.time() - t0:.0f}s)", flush=True)
        res[nome] = linha
        json.dump(res, open(f"sat_n1_{os.environ.get('N1_SUF', 'nove')}.json", "w"), indent=1)
