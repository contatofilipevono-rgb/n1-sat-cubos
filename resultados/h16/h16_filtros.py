"""H16: filtros 2-adicos para quarticas homogeneas RS em n=16 variaveis (08/11).
f_c = soma_{i<116} c_i g_i, g_i = soma da orbita de rotacao de um monomio de grau 4.
Fato (necessario): se f e bent em n=16, para todo subcubo coordenado V de codimensao k (coordenadas fixas F, |F|=k,
fixadas num padrao a) vale  sum_{x in a+V} (-1)^f(x) = 2^-k sum_{u in V^perp} (-1)^{u.a} W_f(u),  com W_f(u)=+-2^8;
logo a soma e 2^(8-k) * (soma de 2^k sinais) = multiplo de 2^(9-k)  (k>=1).  Com peso w = #{f=1} em a+V:
2^(16-k) - 2w = 0 mod 2^(9-k)  =>  w = 2^(15-k) mod 2^(8-k).   (k=0: w = 2^15 mod 2^8, isto e, w = 2^15 +- 2^7.)
Codificacao: t_x = f_c(x) e uma forma linear em c (XOR); agrupa pontos com a mesma forma (peso = multiplicidade);
soma ponderada mod 2^m por colunas (somadores completos), bits fixados.  Nada aqui testa bent: so condicoes necessarias.
Controles (main): (i) checagem direta == CNF em c aleatorios (unidades); (ii) a teoria: funcao bent quadratica
sum x_i x_{i+8} satisfaz as congruencias por avaliacao direta; quartica aleatoria em geral nao."""
import itertools
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from sat_cnf import CNF  # noqa: E402

N = 16


def rot(x, k=1):
    k %= N
    return ((x << k) | (x >> (N - k))) & ((1 << N) - 1)


def orbitas_quarticas():
    vistos, out = set(), []
    for t in itertools.combinations(range(N), 4):
        m = sum(1 << i for i in t)
        if m in vistos:
            continue
        orb = sorted({rot(m, k) for k in range(N)})
        vistos.update(orb)
        out.append(orb)
    assert len(out) == 116
    return out


ORB = orbitas_quarticas()


def forma(x, livres_mask=None):
    """bitmask (116 bits) da forma linear t_x = sum_i c_i * (#monomios da orbita i contidos em x mod 2)."""
    v = 0
    for i, orb in enumerate(ORB):
        par = 0
        for m in orb:
            if m & x == m:
                par ^= 1
        if par:
            v |= 1 << i
    return v


def subcubo_pontos(fixas, padrao):
    livres = [j for j in range(N) if j not in fixas]
    base = sum(1 << j for j, b in zip(fixas, padrao) if b)
    for bits in range(1 << len(livres)):
        x = base
        for t, j in enumerate(livres):
            if (bits >> t) & 1:
                x |= 1 << j
        yield x


def alvo(k):
    """(m, t): w = t mod 2^m.  k=0: W(0) = +-2^8 => w = 2^15 -+ 2^7 => w = 2^7 mod 2^8."""
    if k == 0:
        return 8, 1 << 7
    m = 8 - k
    return m, (1 << (15 - k)) % (1 << m)


_cache_forma = {}


def forma_c(x):
    if x not in _cache_forma:
        _cache_forma[x] = forma(x)
    return _cache_forma[x]


def peso_formas(fixas, padrao):
    """dict forma -> multiplicidade (pontos com t_x identica)."""
    d = {}
    for x in subcubo_pontos(fixas, padrao):
        f = forma_c(x)
        d[f] = d.get(f, 0) + 1
    return d


def avalia(cvec, fixas, padrao):
    """peso direto de f_c no subcubo."""
    w = 0
    for x in subcubo_pontos(fixas, padrao):
        w += bin(forma_c(x) & cvec).count("1") & 1
    return w


class Codificador:
    def __init__(self):
        self.cnf = CNF(117)              # variaveis 1..116 = c_0..c_115
        self.cache_xor = {}

    def lit_forma(self, f):
        """literal para XOR_{i in f} c_i (com cache)."""
        if f in self.cache_xor:
            return self.cache_xor[f]
        vs = [i + 1 for i in range(116) if (f >> i) & 1]
        if len(vs) == 1:
            lit = vs[0]
        else:
            lit = self.cnf.novo()
            self.cnf.xor(vs + [lit], 0)
        self.cache_xor[f] = lit
        return lit

    def fa(self, a, b, c):
        """somador completo: devolve (s, carry)."""
        s = self.cnf.novo()
        self.cnf.xor([a, b, c, s], 0)
        cy = self.cnf.novo()
        cl = self.cnf.cl
        cl += [[-a, -b, cy], [-a, -c, cy], [-b, -c, cy], [a, b, -cy], [a, c, -cy], [b, c, -cy]]
        return s, cy

    def ha(self, a, b):
        s = self.cnf.novo()
        self.cnf.xor([a, b, s], 0)
        cy = self.cnf.e(a, b)
        return s, cy

    def soma_mod(self, colunas, m):
        """colunas[j] = lista de literais de peso 2^j; devolve bits 0..m-1 da soma."""
        cols = [list(colunas[j]) if j < len(colunas) else [] for j in range(m)]
        bits = []
        for j in range(m):
            col = cols[j]
            while len(col) > 1:
                if len(col) >= 3:
                    a, b, c = col.pop(), col.pop(), col.pop()
                    s, cy = self.fa(a, b, c)
                else:
                    a, b = col.pop(), col.pop()
                    s, cy = self.ha(a, b)
                col.insert(0, s)
                if j + 1 < m:
                    cols[j + 1].append(cy)
            bits.append(col[0] if col else None)
        return bits

    def filtro(self, fixas, padrao):
        k = len(fixas)
        m, t = alvo(k)
        d = peso_formas(fixas, padrao)
        colunas = [[] for _ in range(m)]
        for f, mult in d.items():
            if f == 0:
                continue
            lit = self.lit_forma(f)
            for j in range(m):
                if (mult >> j) & 1:
                    colunas[j].append(lit)
        bits = self.soma_mod(colunas, m)
        for j, b in enumerate(bits):
            want = (t >> j) & 1
            if b is None:
                if want:
                    self.cnf.cl.append([])        # contradicao estrutural
            else:
                self.cnf.cl.append([b] if want else [-b])
        return m, t


def familias(ks, padroes="zero", amostra=None, semente=1):
    """subcubos ate rotacao: conjuntos de coordenadas fixas F (|F|=k) modulo rotacao; padrao zero ou todos."""
    out = []
    for k in ks:
        vistos = set()
        for F in itertools.combinations(range(N), k):
            mask = sum(1 << j for j in F)
            can = min(rot(mask, r) for r in range(N))
            if can in vistos:
                continue
            vistos.add(can)
            pads = [tuple([0] * k)] if padroes == "zero" else list(itertools.product((0, 1), repeat=k))
            for p in pads:
                out.append((F, p))
    if amostra and len(out) > amostra:
        out = random.Random(semente).sample(out, amostra)
    return out


def controles():
    from pysat.solvers import Solver
    rnd = random.Random(3)
    # (ii) teoria: bent quadratica sum x_i x_{i+8} satisfaz todas as congruencias (avaliacao direta, sem c)
    def f_quad(x):
        return sum(((x >> i) & 1) * ((x >> (i + 8)) & 1) for i in range(8)) & 1
    for k in range(0, 7):
        for F in [tuple(sorted(rnd.sample(range(N), k))) for _ in range(6)]:
            for p in [tuple(rnd.randint(0, 1) for _ in range(k)) for _ in range(3)]:
                w = sum(f_quad(x) for x in subcubo_pontos(F, p))
                m, t = alvo(k)
                assert w % (1 << m) == t, ("teoria falhou para bent quadratica", k, F, p, w)
    print("controle teoria: bent quadratica satisfaz as congruencias (k=0..6, amostra)", flush=True)
    # (i) CNF == checagem direta
    fams = familias([4, 5, 6], padroes="todos", amostra=30, semente=5) + familias([0, 1, 2], padroes="zero")
    for rodada in range(12):
        c = rnd.getrandbits(116) if rodada else 0
        enc = Codificador()
        ok_direto = True
        for F, p in fams:
            enc.filtro(F, p)
            m, t = alvo(len(F))
            if avalia(c, F, p) % (1 << m) != t:
                ok_direto = False
        units = [[i + 1] if (c >> i) & 1 else [-(i + 1)] for i in range(116)]
        with Solver(name="cadical195", bootstrap_with=enc.cnf.cl + units) as s:
            r = s.solve()
        assert r == ok_direto, ("CNF diverge da checagem direta", rodada, r, ok_direto)
    print("controle codificacao: CNF == checagem direta em 12 vetores c (inclui c=0)", flush=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["controles"]:
        controles()
        sys.exit()
    ks = [int(t) for t in os.environ.get("H16_KS", "4").split(",")]
    pad = os.environ.get("H16_PAD", "zero")
    t0 = time.time()
    enc = Codificador()
    fams = familias(ks, padroes=pad)
    for F, p in fams:
        enc.filtro(F, p)
    print(f"H16 ks={ks} padroes={pad}: {len(fams)} subcubos, {enc.cnf.prox - 1} var, {len(enc.cnf.cl)} clausulas "
          f"({time.time() - t0:.0f}s)", flush=True)
    out = os.environ.get("H16_CNF")
    if out:
        with open(out, "w") as f:
            f.write(f"p cnf {enc.cnf.prox - 1} {len(enc.cnf.cl)}\n")
            for c in enc.cnf.cl:
                f.write(" ".join(map(str, c)) + " 0\n")
        print("CNF escrita em", out)
    else:
        from pysat.solvers import Solver
        with Solver(name="cadical195", bootstrap_with=enc.cnf.cl) as s:
            r = s.solve()
            print("SAT" if r else "UNSAT", f"({time.time() - t0:.0f}s)")
            if r:
                mod = s.get_model()
                c = sum(1 << i for i in range(116) if mod[i] > 0)
                print("c =", hex(c))
