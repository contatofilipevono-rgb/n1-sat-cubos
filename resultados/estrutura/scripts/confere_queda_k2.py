"""(09/11) Conferencia independente da queda k=2 para o trio: acha UM subespaco U (dim 6 em F2^11) pela busca,
depois recalcula deg(Q|U) por SUBSTITUICAO SIMBOLICA (ANF booleana em 6 parametros, sem tabela-verdade),
e tambem por tabela-verdade de D completo com R=0. Mostra a base de U.
Controle negativo: o mesmo U com phi trocado por phi + (cubica aleatoria) normalmente perde a queda."""
import sys, json, re, random, itertools
import numpy as np
sys.argv = ["x"]
from queda_onze import tabela, grau_max_lote, subespacos, complemento, parse
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so

w1, w2, ny = so.pencil(so.classes()["F4+F4"])
_, _, _, Tq = so.modelo_nove(w1, w2, ny)
T = set(Tq)
tr = json.load(open(r"C:\Users\Valer\Downloads\analise adversarial\sete_restricoes_09nov\trio_s22_seed1.json"))["trios"][0]
phis = [parse(s) for s in tr["phi"]]


def monta(phis):
    Q = set(T)
    for i, ph in enumerate(phis):
        Q ^= {m | (1 << (8 + i)) for m in ph}
    return Q


def restringe_simbolico(Q, base):
    """Q como conjunto de monomios em 11 bits; ponto = sum t_j base_j. Coordenada i = XOR_{j: base_j tem bit i} t_j.
    Retorna ANF da restricao como conjunto de monomios em 6 bits (t)."""
    coord = [frozenset(j for j, b in enumerate(base) if (b >> i) & 1) for i in range(11)]
    tot = set()
    for m in Q:
        prod = {0}  # polinomio em t: conjunto de monomios (bitmask em j)
        for i in range(11):
            if (m >> i) & 1:
                lin = coord[i]
                novo = set()
                for a in prod:
                    for j in lin:
                        novo ^= {a | (1 << j)}
                prod = novo
        tot ^= prod
    return tot


Q = monta(phis)
tt = tabela(Q)
S4 = subespacos(8, 4)
iso4 = S4[~grau_max_lote(tt, S4)]
X = [1 << 8, 1 << 9, 1 << 10]
achado = None
for B in iso4:
    Bl = list(B); reps = complemento(Bl)
    for p1, p2 in [(X[0], X[1]), (X[0], X[2]), (X[1], X[2]), (X[0], X[1] ^ X[2]), (X[1], X[0] ^ X[2]), (X[2], X[0] ^ X[1]), (X[0] ^ X[1], X[0] ^ X[2])]:
        lote = np.array([Bl + [p1 ^ u1, p2 ^ u2] for u1 in reps for u2 in reps], dtype=np.int64)
        ok = np.where(~grau_max_lote(tt, lote))[0]
        if len(ok):
            achado = [int(v) for v in lote[ok[0]]]
            break
    if achado:
        break
print("U (base, 11 bits; bits 8..10 = x1..x3):", [format(b, "011b") for b in achado])
anf = restringe_simbolico(Q, achado)
print("grau de Q|U (substituicao simbolica):", max((bin(m).count('1') for m in anf), default=-1), "| monomios:", len(anf))
# posto da base (dimensao 6?)
piv = {}
for v in achado:
    while v:
        h = v.bit_length() - 1
        if h in piv: v ^= piv[h]
        else: piv[h] = v; break
print("dim U =", len(piv), "| codim em F2^11 =", 11 - len(piv))
# controle: projecao em X tem dim 2
proj = {(b >> 8) for b in achado}
print("projecao em X (vetores):", sorted(proj))
# controle negativo: perturbar phi1 aleatoriamente
rnd = random.Random(5)
cub = [sum(1 << i for i in c) for c in itertools.combinations(range(8), 3)]
for t in range(3):
    pert = set(rnd.sample(cub, 6))
    Q2 = monta([phis[0] ^ pert, phis[1], phis[2]])
    print("controle (phi1 perturbado):", "grau de Q2|U =", max((bin(m).count('1') for m in restringe_simbolico(Q2, achado)), default=-1))
