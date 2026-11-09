"""Codificacao CNF da liftabilidade (I6 ∧ I7) por tabela-verdade + transformada de Mobius modulo 8 (09/11/2026).
f(x) = XOR_{m ⊆ x} a_m  (512 pontos);  c = Mobius_Z(f) mod 8 por borboleta de n estagios:
  para cada bit i, x com bit i: c[x] <- c[x] - c[x sem i]  (subtrator de 3 bits, complemento de 2).
Restricoes: |S| >= 6 => c_S = 0 mod 4 ; |S| >= 7 => c_S = 0 mod 8.  Constantes propagadas (estagios iniciais baratos)."""
from i7 import _Ctx


def _NOT(l):
    return (not l) if isinstance(l, bool) else -l


def _OR2(ctx, a, b):
    return _NOT(ctx.AND2(_NOT(a), _NOT(b)))


def _MAJ(ctx, a, b, c):
    return _OR2(ctx, ctx.AND2(a, b), ctx.AND2(c, ctx.XOR2(a, b)))


def _sub3(ctx, a, b):
    """a - b mod 8, com a, b = (b0, b1, b2) literais/constantes."""
    nb = [_NOT(x) for x in b]
    s = []
    c = True  # +1 do complemento de 2
    for i in range(3):
        s.append(ctx.XOR2(ctx.XOR2(a[i], nb[i]), c))
        if i < 2:
            c = _MAJ(ctx, a[i], nb[i], c)
    return s


def adiciona_lift_mobius(cnf, fixo, incog, nbits=9, i6=True, i7=True):
    ctx = _Ctx(cnf)
    N = 1 << nbits
    fixo = set(fixo)
    regs = []
    for x in range(N):
        vs = [k + 1 for k, m in enumerate(incog) if (m & x) == m]
        c = sum(1 for m in fixo if (m & x) == m) & 1
        if not vs:
            f = bool(c)
        elif len(vs) == 1:
            f = vs[0] if not c else -vs[0]
        else:
            f = cnf.novo()
            cnf.xor(vs + [f], c)
        regs.append([f, False, False])
    for i in range(nbits):
        for x in range(N):
            if (x >> i) & 1:
                regs[x] = _sub3(ctx, regs[x], regs[x ^ (1 << i)])
    for S in range(N):
        p = bin(S).count("1")
        if p >= 6 and i6:
            ctx.fixa(regs[S][0], False); ctx.fixa(regs[S][1], False)
        if p >= 7 and i7:
            ctx.fixa(regs[S][0], False); ctx.fixa(regs[S][1], False); ctx.fixa(regs[S][2], False)
