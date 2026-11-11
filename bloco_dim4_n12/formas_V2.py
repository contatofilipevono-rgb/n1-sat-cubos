# Forma fechada dos oito pares (q1, q2) dos mapas exclusivos de V2 com fase.
#   q1(z) = B_z(e0, .)|V2,  q2(z) = B_z(e1, .)|V2,  V2 = {w : s_e(w) = s_o(w) = 0}.
# Familias (N = I + R^3, s_e e s_o = paridades das coordenadas pares e impares, s = s_e + s_o):
#   C_k:  q1 = s_o(z) R^k z,       q2 = s_e(z) R^k z,       k = 1, 2, 4, 5
#   A_j:  q1 = s_o(z) R^j N z,     q2 = s_e(z) R^j N z,     j = 1, 2
#   B_j:  A_j + U,  com U: q1 = q2 = (1 + s(z)) N z   (o tipo de peso 24 do bloco U)
import json, os, collections
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, "V2_exclusivo_mapas.json")))
par = lambda x: bin(x).count("1") & 1
VB = [5, 10, 20, 40]; E, O = 21, 42
res = lambda lam: sum(par(lam & VB[i]) << i for i in range(4))
R = lambda z, k=1: ((z << k) | (z >> (6 - k))) & 63 if k % 6 else z
N = lambda z: z ^ R(z, 3)
se = lambda z: par(z & E); so = lambda z: par(z & O)
def par_q(M, U=False):
    q1 = [res(M(z)) if so(z) else 0 for z in range(64)]; q2 = [res(M(z)) if se(z) else 0 for z in range(64)]
    if U:
        u = [res(N(z)) if not (se(z) ^ so(z)) else 0 for z in range(64)]
        q1 = [a ^ b for a, b in zip(q1, u)]; q2 = [a ^ b for a, b in zip(q2, u)]
    return tuple(q1 + q2)
FAM = {}
for k in (1, 2, 4, 5): FAM[f"C_{k}"] = par_q(lambda z, k=k: R(z, k))
for j in (1, 2):
    FAM[f"A_{j}"] = par_q(lambda z, j=j: R(N(z), j))
    FAM[f"B_{j}"] = par_q(lambda z, j=j: R(N(z), j), U=True)
assert len(set(FAM.values())) == 8
inv = {v: k for k, v in FAM.items()}
cont = collections.Counter(); fun = collections.Counter()
for r in d:
    L = [int(ch, 16) for ch in r["rotulos"]]
    q = tuple([L[64 + z] ^ L[z] for z in range(64)] + [L[128 + z] ^ L[z] for z in range(64)])
    assert q in inv, "par (q1,q2) fora das familias"
    cont[inv[q]] += 1; fun[inv[q]] += r["fases"]
print("todos os 768 mapas tem (q1,q2) numa das 8 formas fechadas")
for k in sorted(cont): print(f"  {k}: {cont[k]} mapas, {fun[k]} funcoes")
print("total:", sum(cont.values()), "mapas,", sum(fun.values()), "funcoes")
