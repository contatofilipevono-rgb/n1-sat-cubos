"""CNF puro (sem XOR nativo) para CaDiCaL/Kissat via python-sat.
XOR longo -> cadeia: x1+x2+x3 = t (aux), t+x4+x5 = t', ... (blocos de 3 entradas, 2^3 clausulas por bloco).
AND -> 3 clausulas.  Conferido em controles(): todas as atribuicoes de XOR de ate 7 variaveis."""
import itertools


class CNF:
    def __init__(self, prox):
        self.prox = prox
        self.cl = []

    def novo(self):
        v = self.prox
        self.prox += 1
        return v

    def xor_direto(self, vs, rhs):
        n = len(vs)
        for sinais in itertools.product((0, 1), repeat=n):
            # proibe atribuicoes com paridade errada: atribuicao a com sum a != rhs
            if sum(sinais) % 2 != rhs:
                self.cl.append([-v if a else v for v, a in zip(vs, sinais)])

    def xor(self, vs, rhs):
        vs = list(vs)
        rhs = int(rhs) & 1
        if not vs:
            if rhs:
                self.cl.append([])
            return
        while len(vs) > 4:
            t = self.novo()
            self.xor_direto(vs[:3] + [t], 0)      # t = x1+x2+x3
            vs = [t] + vs[3:]
        self.xor_direto(vs, rhs)

    def e(self, a, b):
        p = self.novo()
        self.cl += [[-p, a], [-p, b], [p, -a, -b]]
        return p


def controles():
    from pysat.solvers import Solver
    for n in range(1, 8):
        for rhs in (0, 1):
            c = CNF(n + 1)
            c.xor(list(range(1, n + 1)), rhs)
            for a in itertools.product((0, 1), repeat=n):
                with Solver(name="cadical195", bootstrap_with=c.cl) as s:
                    ok = s.solve(assumptions=[i + 1 if b else -(i + 1) for i, b in enumerate(a)])
                assert ok == (sum(a) % 2 == rhs), (n, rhs, a)
    print("controle XOR->CNF: ok (n<=7)")


if __name__ == "__main__":
    controles()
