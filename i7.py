"""Codificacao CNF de I7 (c_S = 0 mod 8 para |S| >= 7) no modelo N1 em 9 variaveis (09/11/2026).

Para f com ANF mod 2 de suporte M (monomios t_m): XOR_m t_m = sum_k (-2)^(k-1) e_k(t), logo
  c_S = N1(S) - 2 N2(S) + 4 N3(S) - ...   (Nk(S) = #k-subconjuntos de M com uniao exatamente S).
Como deg f <= 4, N1(S) = 0 para |S| >= 5. Modulo 8:  c_S = -2 N2 + 4 N3, e
  c_S = 0 mod 8  <=>  N2 = 0 mod 2 (I6)  e  (N2/2 = N3 mod 2),  isto e,  N2 = 2*N3 (mod 4).
Codificacao por S (|S| >= 7): contador mod 4 dos produtos de pares (s0, s1) e paridade dos produtos de triplas.
Monomios: fixo (presenca constante 1) e incog (variavel k+1). Produtos -> variaveis AND (cache)."""
from itertools import combinations


def popc(x):
    return bin(x).count("1")


class _Ctx:
    def __init__(self, cnf):
        self.cnf = cnf
        self.cache = {}

    def AND(self, vs):
        vs = tuple(sorted(set(vs)))
        if len(vs) == 1:
            return vs[0]
        if vs not in self.cache:
            p = self.cnf.novo()
            for v in vs:
                self.cnf.cl.append([-p, v])
            self.cnf.cl.append([p] + [-v for v in vs])
            self.cache[vs] = p
        return self.cache[vs]

    # literais: int (variavel/negacao) ou bool (constante)
    def XOR2(self, a, b):
        if isinstance(a, bool) and isinstance(b, bool):
            return a != b
        if isinstance(a, bool):
            a, b = b, a
        if isinstance(b, bool):
            return -a if b else a
        p = self.cnf.novo()
        self.cnf.cl += [[-p, a, b], [-p, -a, -b], [p, -a, b], [p, a, -b]]
        return p

    def AND2(self, a, b):
        if isinstance(a, bool):
            return b if a else False
        if isinstance(b, bool):
            return a if b else False
        return self.AND([a, b]) if a > 0 and b > 0 else self._and_lits(a, b)

    def _and_lits(self, a, b):
        p = self.cnf.novo()
        self.cnf.cl += [[-p, a], [-p, b], [p, -a, -b]]
        return p

    def fixa(self, lit, val):
        if isinstance(lit, bool):
            if lit != val:
                self.cnf.cl.append([])
            return
        self.cnf.cl.append([lit if val else -lit])


def adiciona_I7(cnf, fixo, incog, nbits=9):
    fixo = set(fixo)
    assert not (fixo & set(incog)), "fixo e incog devem ser disjuntos"
    univ = [(m, None) for m in sorted(fixo)] + [(m, k + 1) for k, m in enumerate(incog)]
    ctx = _Ctx(cnf)
    alvo_P = {}
    alvo_T = {}
    def prod(itens):
        vs = [v for (_, v) in itens if v is not None]
        return True if not vs else ctx.AND(vs)
    n = len(univ)
    for a, b in combinations(range(n), 2):
        u = univ[a][0] | univ[b][0]
        if popc(u) >= 7:
            alvo_P.setdefault(u, []).append(prod([univ[a], univ[b]]))
    for a, b in combinations(range(n), 2):
        uab = univ[a][0] | univ[b][0]
        if popc(uab) + 4 < 7:
            continue
        for c in range(b + 1, n):
            u = uab | univ[c][0]
            if popc(u) >= 7:
                alvo_T.setdefault(u, []).append(prod([univ[a], univ[b], univ[c]]))
    ns = 0
    for S in range(1 << nbits):
        if popc(S) < 7:
            continue
        P = alvo_P.get(S, [])
        T = alvo_T.get(S, [])
        s0, s1 = False, False
        for x in P:
            c = ctx.AND2(s0, x)
            s0 = ctx.XOR2(s0, x)
            s1 = ctx.XOR2(s1, c)
        ctx.fixa(s0, False)
        par = False
        for t in T:
            par = ctx.XOR2(par, t)
        # s1 == par
        ctx.fixa(ctx.XOR2(s1, par), False)
        ns += 1
    return {"conjuntos": ns, "pares": sum(len(v) for v in alvo_P.values()), "triplas": sum(len(v) for v in alvo_T.values()),
            "ANDs": len(ctx.cache)}
