# Forma fechada dos seis pares (q1, q2) dos mapas exclusivos de V1 com fase.
#   q1(z) = B_z(e0, .)|V1,  q2(z) = B_z(e1, .)|V1,  V1 = {w : w.27 = w.54 = 0}.
#   q1 = r54(z) * mu(z),  q2 = r45(z) * mu(z),  com r_m(z) = z.m e mu(z) = M z + c*1 restrito a V1.
import json, os, collections
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, "V1_exclusivo_mapas.json")))
par = lambda x: bin(x).count("1") & 1
VB = [7, 14, 28, 56]
res = lambda lam: sum(par(lam & VB[i]) << i for i in range(4))
def conv(c, z):
    out = 0
    for j in range(6):
        if c >> j & 1: out ^= ((z << j) | (z >> (6 - j))) & 63
    return out
# (nome, polinomio circulante como mascara dos expoentes, constante c)
FAM = [("R^2(I+R^2), c=0", 0b010100, 0), ("R^2(I+R^2), c=1", 0b010100, 1), ("R(I+R^2), c=1", 0b001010, 1),
       ("I+R^2, c=1", 0b000101, 1), ("I+R, c=1", 0b000011, 1), ("R^2(I+R), c=1", 0b001100, 1)]
def par_q(M, c):
    mu = [res(conv(M, z) ^ (63 if c else 0)) for z in range(64)]
    return tuple([mu[z] if par(z & 54) else 0 for z in range(64)] + [mu[z] if par(z & 45) else 0 for z in range(64)])
inv = {par_q(M, c): nm for nm, M, c in FAM}
assert len(inv) == 6
cont = collections.Counter(); fun = collections.Counter()
for r in d:
    L = [int(ch, 16) for ch in r["rotulos"]]
    q = tuple([L[64 + z] ^ L[z] for z in range(64)] + [L[128 + z] ^ L[z] for z in range(64)])
    assert q in inv, "par (q1,q2) fora das familias"
    cont[inv[q]] += 1; fun[inv[q]] += r["fases"]
print("todos os 120 mapas tem (q1,q2) numa das 6 formas fechadas")
for nm, _, _ in FAM: print(f"  M = {nm}: {cont[nm]} mapas, {fun[nm]} funcoes")
print("total:", sum(cont.values()), "mapas,", sum(fun.values()), "funcoes")
