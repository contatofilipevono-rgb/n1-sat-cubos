"""Solver I6 simbolico por contagem de pares.
Para D de grau <= 4 com ANF {m}, c_S mod 4 (|S| >= 5) = 2 * #{pares {m, m'} : m u m' = S}; I6 <=> esses
contadores sao pares para todo |S| em {6,7,8}.  Com D = fixo + sum u_k m_k (m_k monomios incognitos distintos e
fora do fixo), os bits sao EXATAMENTE quadraticos em u:  F0 (pares no fixo), D1[k] (fixo x m_k), D2[k,l] (m_k x m_l).
Busca: branch-and-bound com linearizacao; restricao opcional 'algum u_k, k em G, e 1' por particao padrao
(subproblema j: u_{G[j]} = 1 e u_{G[i]} = 0 para i < j)."""
import itertools
import time


def popc(x):
    return bin(x).count("1")


class Pares:
    def __init__(self, fixo, incog, graus=(6, 7, 8)):
        self.fixo = list(fixo)
        self.inc = list(incog)
        assert not set(self.fixo) & set(self.inc)
        alvos = {}

        def idx(S):
            if S not in alvos:
                alvos[S] = len(alvos)
            return alvos[S]
        self.F0 = 0
        for a, b in itertools.combinations(self.fixo, 2):
            S = a | b
            if popc(S) in graus:
                self.F0 ^= 1 << idx(S)
        self.D1 = []
        for m in self.inc:
            v = 0
            for a in self.fixo:
                S = a | m
                if popc(S) in graus:
                    v ^= 1 << idx(S)
            self.D1.append(v)
        self.D2 = {}
        for i, j in itertools.combinations(range(len(self.inc)), 2):
            S = self.inc[i] | self.inc[j]
            if popc(S) in graus:
                self.D2[(i, j)] = 1 << idx(S)
        self.alvos = alvos
        self.viz = {i: [] for i in range(len(self.inc))}
        for (i, j) in self.D2:
            self.viz[i].append(j)
            self.viz[j].append(i)

    def avalia(self, u):
        v = self.F0
        for i in u:
            v ^= self.D1[i]
        for i, j in itertools.combinations(sorted(u), 2):
            v ^= self.D2.get((i, j), 0)
        return v


def resolve(cols, alvo):
    piv = {}
    for j, c in enumerate(cols):
        v, cb = c, 1 << j
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h][0]
                cb ^= piv[h][1]
            else:
                piv[h] = (v, cb)
                break
    v, cb = alvo, 0
    while v:
        h = v.bit_length() - 1
        if h not in piv:
            return None
        v ^= piv[h][0]
        cb ^= piv[h][1]
    return [j for j in range(len(cols)) if (cb >> j) & 1]


def busca(P, fixados=None, max_nos=10 ** 6, ordem=None):
    """procura u com F(u) = 0 respeitando fixados (dict k->bit). Devolve (u, nos) ou (None, nos)."""
    n = len(P.inc)
    fixados = dict(fixados or {})
    if ordem is None:
        ordem = sorted(range(n), key=lambda k: -len(P.viz[k]))
    ordem = [k for k in ordem if k not in fixados]
    # variaveis sem termos quadraticos nunca precisam de ramificacao
    ram = [k for k in ordem if P.viz[k]]
    lin = [k for k in ordem if not P.viz[k]]
    nos = [0]
    D2 = P.D2

    def d2(a, b):
        return D2.get((a, b) if a < b else (b, a), 0)

    def rec(fix, pos):
        nos[0] += 1
        if nos[0] > max_nos:
            raise RuntimeError("limite de nos")
        um = [k for k, b in fix.items() if b]
        livres = ram[pos:]
        rhs = P.F0
        for k in um:
            rhs ^= P.D1[k]
        for a, b in itertools.combinations(um, 2):
            rhs ^= d2(a, b)
        cols, rot = [], []
        for k in lin + livres:
            c = P.D1[k]
            for j in um:
                c ^= d2(k, j)
            cols.append(c)
            rot.append(k)
        nlin = len(cols)
        livres_set = set(livres)
        for a in livres:
            for b in P.viz[a]:
                if b in livres_set and a < b:
                    cols.append(d2(a, b))
                    rot.append(None)
        s = resolve(cols, rhs)
        if s is None:
            return None
        if not livres:
            return um + [rot[i] for i in s]
        k = livres[0]
        for b in (0, 1):
            f2 = dict(fix)
            f2[k] = b
            r = rec(f2, pos + 1)
            if r is not None:
                return r
        return None
    sol = rec(fixados, 0)
    if sol is not None:
        assert P.avalia(set(sol)) == 0
    return sol, nos[0]


def busca_nao_nulo(P, G, max_nos=10 ** 6, log=print):
    """existe solucao com algum u_k = 1, k em G?"""
    total = 0
    for j, g in enumerate(G):
        fx = {G[i]: 0 for i in range(j)}
        fx[g] = 1
        sol, nos = busca(P, fx, max_nos)
        total += nos
        if sol is not None:
            return sol, total
    return None, total
