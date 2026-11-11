# Verificador independente do lema das fibras de 16 pontos.
# Para P = 16 pontos distintos de F2^8, conta por forca bruta (2^16 escolhas) os sinais com
# |soma_{x em P} (-1)^{h(x) + alfa.x}| = 4 para todo alfa, e compara com:
#   0 se C nao e auto-ortogonal;  2^(15-k) - 128 se C e auto-ortogonal, k = dim C.
import random, itertools
import numpy as np
par = lambda x: bin(x).count("1") & 1
def rank(vs):
    piv = {}
    for v in vs:
        while v:
            c = v.bit_length() - 1
            if c in piv: v ^= piv[c]
            else: piv[c] = v; break
    return len(piv)
def codigo(P):
    gens = [(1 << 16) - 1] + [sum(((x >> j) & 1) << i for i, x in enumerate(P)) for j in range(8)]
    k = rank(gens)
    so = all(bin(a & b).count("1") % 2 == 0 for a in gens for b in gens)
    return k, so
H16 = np.arange(1 << 16, dtype=np.uint32)
BITS = ((H16[:, None] >> np.arange(16)) & 1).astype(np.int16)        # 65536 x 16
SG = 1 - 2 * BITS
def conta(P):
    ok = np.ones(1 << 16, dtype=bool)
    vistos = set()
    for alfa in range(256):
        ch = tuple(par(alfa & x) for x in P)
        if ch in vistos: continue
        vistos.add(ch)
        w = SG @ np.array([1 - 2 * c for c in ch], dtype=np.int16)
        ok &= (np.abs(w) == 4)
    return int(ok.sum())
def previsto(P):
    k, so = codigo(P)
    return (max(0, (1 << (15 - k)) - 128) if so else 0), k, so
random.seed(7)
casos = []
# flats de dimensao 4
for _ in range(3):
    while True:
        g = random.sample(range(1, 256), 4)
        if rank(g) == 4: break
    x0 = random.randrange(256)
    casos.append(("flat de dimensao 4", [x0 ^ (g[0] * a ^ g[1] * b ^ g[2] * c ^ g[3] * d) for a in (0, 1) for b in (0, 1) for c in (0, 1) for d in (0, 1)]))
# uniao de dois 3-flats paralelos? (dimensao afim 5): F x {0} uniao (F + t) com t fora -> ainda flat. Usa dois 3-flats nao paralelos:
def flat(x0, g):
    S = [x0]
    for v in g: S = S + [s ^ v for s in S]
    return S
casos.append(("dois 3-flats com direcoes independentes (dim 7, E8+E8)", flat(0, [1, 2, 4]) + flat(64, [8, 16, 32])))
casos.append(("dois 3-flats com direcoes que se cortam numa reta (dim 6)", flat(0, [1, 2, 4]) + flat(32, [1, 8, 16])))
casos.append(("quatro planos paralelos em posicao geral (dim 5)", flat(0, [1, 2]) + flat(4, [1, 2]) + flat(8, [1, 2]) + flat(16, [1, 2])))
casos.append(("quatro planos paralelos, translacoes independentes (dim 5 ou 6)", flat(0, [1, 2]) + flat(4, [1, 2]) + flat(8, [1, 2]) + flat(28, [1, 2])))
casos.append(("dois 3-flats com direcoes que se cortam num plano (dim 5)", flat(0, [1, 2, 4]) + flat(16, [1, 2, 8])))
casos.append(("quatro planos com direcoes independentes (dim 7)", flat(0, [1, 2]) + flat(64, [4, 8]) + flat(128, [16, 32]) + flat(192, [3, 12])))
casos.append(("quatro planos, direcoes em dimensao 6", flat(0, [1, 2]) + flat(16, [4, 8]) + flat(32, [1, 4]) + flat(48, [2, 8])))
# oito retas (pares) -- em geral nao auto-ortogonal
casos.append(("16 pontos aleatorios", random.sample(range(256), 16)))
casos.append(("8 pares com a mesma direcao (cilindro sobre 8 pontos)", [x ^ t for x in random.sample(range(0, 256, 2), 8) for t in (0, 1)]))
tudo = True
for nome, P in casos:
    prev, k, so = previsto(P); n = conta(P)
    tudo &= (n == prev)
    print(f"{nome}: k = {k}, auto-ortogonal = {so}, previsto = {prev}, forca bruta = {n}  {'ok' if n == prev else 'DIVERGE'}")
print("todos conferem:", tudo)
