# Espaco das partes mistas (q1, q2, b) das funcoes RS de grau <= 4 afins nas classes de V, em complemento DUAL.
# V = ker r inter ker s; e_r, e_s duais (r(e_r)=1, s(e_r)=0, etc).  q1 = B_z(e_r,.)|V, q2 = B_z(e_s,.)|V, b = B_z(e_r,e_s).
# Compara com o espaco gerado pelas formas  theta_z ^ (R^k z), theta_z ^ 1,  theta_z = s(z) r + r(z) s,
# e pelas formas "diagonais"  g(z) * (r+s) ^ (R^k z)  etc.
# Uso: python espaco_q.py V1|V2      (leve; roda em segundos apos montar as 70 orbitas)
import itertools, sys
import numpy as np
from base4 import ORB, tt_orb, IDX, packb, elim_comb, N
nome = sys.argv[1]
par = lambda x: bin(x).count("1") & 1
CFG = {"V2": dict(VB=[5, 10, 20, 40], r=21, s=42, er=1, es=2),          # r = paridade par, s = paridade impar
       "V1": dict(VB=[7, 14, 28, 56], r=27, s=54, er=4, es=32)}          # e2: (27,54) -> (0,1)? ajustado abaixo
c = CFG[nome]; VB, rm, sm = c["VB"], c["r"], c["s"]
# complemento dual: procura e_r, e_s de menor indice
er = next(w for w in range(1, 64) if par(w & rm) == 1 and par(w & sm) == 0)
es = next(w for w in range(1, 64) if par(w & rm) == 0 and par(w & sm) == 1)
assert all(par(v & rm) == 0 and par(v & sm) == 0 for v in VB)
W = np.arange(N)
TT = [tt_orb(o) for o in ORB]
def conds(t):
    F = t[IDX]; out = []
    for u1, u2 in itertools.combinations(VB, 2): out.append(F ^ F[:, W ^ u1] ^ F[:, W ^ u2] ^ F[:, W ^ u1 ^ u2])
    return packb(np.concatenate([o.reshape(-1) for o in out]))
_, ker = elim_comb([conds(t) for t in TT])
def comb_tt(k):
    t = np.zeros(4096, dtype=np.uint8)
    for i in range(len(ORB)):
        if k >> i & 1: t ^= TT[i]
    return t
def polar_parts(t):
    F = t[IDX]
    B = lambda x, y: (F[:, 0] ^ F[:, x] ^ F[:, y] ^ F[:, x ^ y])          # B_z(x,y), independente de w por ser quadratica em w
    q1 = np.stack([B(er, v) for v in VB], axis=1); q2 = np.stack([B(es, v) for v in VB], axis=1); b = B(er, es)
    return q1, q2, b
parts = [polar_parts(comb_tt(k)) for k in ker]
vq = [packb(np.concatenate([q1.reshape(-1), q2.reshape(-1)])) for q1, q2, b in parts]
vqb = [packb(np.concatenate([q1.reshape(-1), q2.reshape(-1), b])) for q1, q2, b in parts]
ind_q, ker_q = elim_comb(vq); ind_qb, _ = elim_comb(vqb)
print(f"{nome}: e_r = {er}, e_s = {es}; dim (q1,q2) = {len(ind_q)}; dim (q1,q2,b) = {len(ind_qb)}; dim de b com q = 0: {len(ind_qb) - len(ind_q)}")
# base reduzida do espaco real de (q1,q2)
def span_basis(vs):
    piv = {}
    for v in vs:
        while v:
            cbit = v.bit_length() - 1
            if cbit in piv: v ^= piv[cbit]
            else: piv[cbit] = v; break
    return piv
real = span_basis(vq)
def in_span(piv, v):
    while v:
        cbit = v.bit_length() - 1
        if cbit in piv: v ^= piv[cbit]
        else: return False
    return True
# candidatas em forma fechada
R = lambda z, k: ((z << k) | (z >> (6 - k))) & 63 if k % 6 else z
res = lambda lam: [par(lam & v) for v in VB]
rr = lambda z: par(z & rm); ss = lambda z: par(z & sm)
def forma(f1, f2, mu):
    """q1(z) = f1(z) * mu(z)|V,  q2(z) = f2(z) * mu(z)|V"""
    q1 = [[x * f1(z) for x in res(mu(z))] for z in range(64)]; q2 = [[x * f2(z) for x in res(mu(z))] for z in range(64)]
    return packb(np.array(q1 + q2, dtype=np.uint8))
cands = {}
for k in range(6):
    cands[f"theta^R^{k}z"] = forma(ss, rr, lambda z, k=k: R(z, k))               # theta_z = s(z) r + r(z) s  ->  theta(e_r) = s(z), theta(e_s) = r(z)
    cands[f"(1+r+s)(r+s)^R^{k}z"] = forma(lambda z: 1 ^ rr(z) ^ ss(z), lambda z: 1 ^ rr(z) ^ ss(z), lambda z, k=k: R(z, k))
    cands[f"(1+r)(1+s)(r+s)^R^{k}z"] = forma(lambda z: (1 ^ rr(z)) & (1 ^ ss(z)), lambda z: (1 ^ rr(z)) & (1 ^ ss(z)), lambda z, k=k: R(z, k))
cands["theta^1"] = forma(ss, rr, lambda z: 63)
for nm_, mu in (("e0", 1), ("e1", 2), ("e2", 4), ("21", 21), ("42", 42), ("9", 9), ("18", 18), ("36", 36)):
    cands[f"theta^const({nm_})"] = forma(ss, rr, lambda z, mu=mu: mu)
okc = {nm_: v for nm_, v in cands.items() if v and in_span(real, v)}
print("candidatas nao nulas:", sum(1 for v in cands.values() if v), "| dentro do espaco real:", len(okc))
for nm_ in okc: print("   dentro:", nm_)
sp = span_basis(list(okc.values()))
print("dimensao gerada pelas candidatas que estao no espaco real:", len(sp), "de", len(real))
tudo = span_basis([v for v in cands.values() if v])
print("dimensao gerada por todas as candidatas:", len(tudo), "| contem o espaco real:", all(in_span(tudo, v) for v in real.values()))
