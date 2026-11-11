# Base explicita do espaco real de (q1, q2) em termos de monomios  m(z) * R^k z  e  m(z) * const,
# com m em {1, r, s, rs} (grau total <= 2).  Uso: python espaco_q2.py V1|V2
import sys, itertools
import numpy as np
exec(open("espaco_q.py", encoding="utf-8").read().split("# candidatas em forma fechada")[0].replace("nome = sys.argv[1]", "nome = sys.argv[1]"))
R = lambda z, k: ((z << k) | (z >> (6 - k))) & 63 if k % 6 else z
res = lambda lam: [par(lam & v) for v in VB]
rr = lambda z: par(z & rm); ss = lambda z: par(z & sm)
MULT = {"1": lambda z: 1, "r": rr, "s": ss, "rs": lambda z: rr(z) & ss(z)}
# constantes: representantes de F2^6 / V^perp
reps = []; seen = set()
for cst in range(64):
    key = tuple(res(cst))
    if any(key) and key not in seen: seen.add(key); reps.append(cst)
basec = [c0 for c0 in reps if bin(sum(res(c0)[i] << i for i in range(4))).count("1") == 1]
gens = {}
def vec(slot, f, mu):
    q = [[x * f(z) for x in res(mu(z))] for z in range(64)]; zero = [[0] * 4] * 64
    return packb(np.array((q + zero) if slot == 1 else (zero + q), dtype=np.uint8))
for slot in (1, 2):
    for mn in ("1", "r", "s"):
        for k in range(6): gens[f"q{slot}: {mn}*R^{k}z"] = vec(slot, MULT[mn], lambda z, k=k: R(z, k))
    for mn in ("1", "r", "s", "rs"):
        for c0 in basec: gens[f"q{slot}: {mn}*c{c0}"] = vec(slot, MULT[mn], lambda z, c0=c0: c0)
names = list(gens); vs = [gens[n_] for n_ in names]
piv = {}
for i, v in enumerate(vs):
    comb = 1 << i
    while v:
        cb = v.bit_length() - 1
        if cb in piv: v ^= piv[cb][0]; comb ^= piv[cb][1]
        else: piv[cb] = (v, comb); break
def expr(v):
    comb = 0
    while v:
        cb = v.bit_length() - 1
        if cb not in piv: return None
        v ^= piv[cb][0]; comb ^= piv[cb][1]
    return comb
def forma(f1, f2, mu):
    q1 = [[x * f1(z) for x in res(mu(z))] for z in range(64)]; q2 = [[x * f2(z) for x in res(mu(z))] for z in range(64)]
    return packb(np.array(q1 + q2, dtype=np.uint8))
print(f"{nome}: geradores monomiais {len(names)}, posto {len(piv)}; constantes de base {basec}")
theta = [forma(ss, rr, lambda z, k=k: R(z, k)) for k in range(6)] + [forma(ss, rr, lambda z: 63)]
quo = span_basis([t for t in theta if t])
extras = []
for v in real.values():
    w = v
    # reduz modulo as formas theta
    while True:
        cb = w.bit_length() - 1 if w else -1
        if cb in quo: w ^= quo[cb]
        else: break
    if w and not in_span(span_basis([t for t in theta if t] + extras), w): extras.append(w)
print("dimensao do espaco real:", len(real), "| formas theta:", len(quo), "| extras:", len(extras))
# procura, em cada classe extra + <theta>, o representante com menos termos monomiais
thl = list(quo.values())
for e in extras:
    best = None
    for mask in range(1 << len(thl)):
        w = e
        for j in range(len(thl)):
            if mask >> j & 1: w ^= thl[j]
        cmb = expr(w)
        if cmb is None: continue
        nt = bin(cmb).count("1")
        if best is None or nt < best[0]: best = (nt, cmb)
    if best is None: print("   extra NAO expresso em monomios"); continue
    print("   extra:", " + ".join(names[i] for i in range(len(names)) if best[1] >> i & 1))
