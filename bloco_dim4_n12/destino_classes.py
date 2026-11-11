# Destino de cada classe de (q1,q2) com A = E (fatia z em V): quantos mapas auto-ortogonais, onde morrem, quantas funcoes.
# Uso: python destino_classes.py V2 fases_V2.pkl      ou      python destino_classes.py V1 <pasta dos json das fatias>
import pickle, os, sys, json, glob, collections
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
nome, fonte = sys.argv[1], sys.argv[2]
g = pickle.load(open(os.path.join(here, f"gens_{nome}.pkl"), "rb")); GL, n0, nq = g["GL"], g["n0"], g["nq"]
par = lambda x: bin(x).count("1") & 1
rm, sm, VB = ((21, 42, [5, 10, 20, 40]) if nome == "V2" else (27, 54, [7, 14, 28, 56]))
res = lambda lam: sum(par(lam & VB[i]) << i for i in range(4))
def conv(c, z):
    out = 0
    for j in range(6):
        if c >> j & 1: out ^= ((z << j) | (z >> (6 - j))) & 63
    return out
pol = lambda c: "+".join(("R^%d" % j if j else "I") for j in range(6) if c >> j & 1) or "0"
rr = lambda z: par(z & rm); ss = lambda z: par(z & sm)
Vs = [z for z in range(64) if not rr(z) and not ss(z)]
def dual(L):
    q1 = L[64:128] ^ L[0:64]; q2 = L[128:192] ^ L[0:64]
    return (q1, q2) if nome == "V2" else (q1, q1 ^ q2)
# nomes: theta ^ (M z + c 1), mais o termo de U em V2
forms = {}
for c in sorted(range(64), key=lambda c: (bin(c).count("1"), c)):
    for c0 in (0, 1):
        mu = [res(conv(c, z) ^ (63 if c0 else 0)) for z in range(64)]
        base = (tuple(mu[z] if ss(z) else 0 for z in range(64)), tuple(mu[z] if rr(z) else 0 for z in range(64)))
        forms.setdefault(base, f"theta^(({pol(c)})z" + ("+1)" if c0 else ")"))
        if nome == "V2":
            u = [res(z ^ conv(8, z)) if not (rr(z) ^ ss(z)) else 0 for z in range(64)]
            withu = (tuple(a ^ b for a, b in zip(base[0], u)), tuple(a ^ b for a, b in zip(base[1], u)))
            forms.setdefault(withu, f"theta^(({pol(c)})z" + ("+1)" if c0 else ")") + " + U")
cls = {}
for qc in range(1 << nq):
    L = np.zeros(256, dtype=np.uint8)
    for j in range(nq):
        if qc >> j & 1: L ^= GL[n0 + j]
    q1, q2 = dual(L)
    key = (tuple(int(x) for x in q1), tuple(int(x) for x in q2))
    AeqE = np.array_equal(q1[Vs], q2[Vs])
    cls[qc] = (forms.get(key, "A=E, fora das formas" if AeqE else "A!=E"), AeqE)
st = collections.defaultdict(collections.Counter)
if nome == "V2":
    codes = [int(l) for l in open(os.path.join(here, "mapas_V2.txt"))]
    resd = {r[0]: r for r in pickle.load(open(fonte, "rb"))}
    for c in codes:
        nm_ = cls[c >> n0][0]; r = resd[c]; st[nm_]["auto-ortogonais"] += 1
        if r[3] is None: st[nm_]["(q1=q2: fases nao contadas aqui)"] += 1
        elif max(r[2]) >= 8: st[nm_]["posto 8"] += 1
        elif r[3] == -1: st[nm_]["linear inconsistente"] += 1
        elif r[4] == 0: st[nm_]["quadratica"] += 1
        else: st[nm_]["com fase"] += 1; st[nm_]["funcoes"] += r[4]
else:
    for a in glob.glob(os.path.join(fonte, "**", "fases_V1_*.json"), recursive=True):
        for r in json.load(open(a))["res"]:
            nm_ = cls[r[0] >> n0][0]; st[nm_]["auto-ortogonais"] += 1
            ks = [k for k, _ in r[2]]
            if max(ks) >= 8: st[nm_]["posto 8"] += 1
            elif r[3] == -1: st[nm_]["linear inconsistente"] += 1
            elif r[4] == 0: st[nm_]["quadratica"] += 1
            else:
                nU = r[5] if len(r) > 5 else 0
                st[nm_]["com fase"] += 1; st[nm_]["funcoes exclusivas"] += r[4] - nU; st[nm_]["funcoes afins em U ou antipodais"] += nU
print(f"{nome}: classes de q = {1 << nq}; com A = E: {sum(1 for v in cls.values() if v[1])}; nomeadas: {sum(1 for v in cls.values() if v[0][0] == 't')}")
nomes_cls = collections.Counter(v[0] for v in cls.values())
for nm_ in sorted(nomes_cls, key=lambda s: (s[0] != "t", len(s), s)):
    if nm_ == "A!=E": print(f"  A != E: {nomes_cls[nm_]} classes; mapas auto-ortogonais: {st[nm_]['auto-ortogonais']}"); continue
    print(f"  {nm_}: {dict(st[nm_])}")
