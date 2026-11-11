# Exporta a base do espaco de pi (rotulos de 4 bits em 256 pontos) para o enumerador em C#.
# Uso: python exporta.py V1|V2
import pickle, os, sys
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
nome = sys.argv[1]
d = pickle.load(open(os.path.join(here, f"base_{nome}.pkl"), "rb"))
PH = d["PH"]; n = len(PH)
packb = lambda a: int.from_bytes(np.packbits(np.asarray(a, dtype=np.uint8).reshape(-1)).tobytes(), "big")
piv = {}; gens = []; ker = []
for i, (P, H) in enumerate(PH):
    r = packb(P); comb = 1 << i
    while r:
        c = r.bit_length() - 1
        if c in piv: r ^= piv[c][0]; comb ^= piv[c][1]
        else: piv[c] = (r, comb); gens.append(comb); break
    else: ker.append(comb)
def comb_arr(comb, k):
    out = np.zeros_like(PH[0][k])
    for i in range(n):
        if comb >> i & 1: out = out ^ PH[i][k]
    return out
lab = lambda P: (P.astype(np.int64) * (1 << np.arange(4))).sum(axis=1).astype(np.uint8)
# ordena: geradores com q1 = q2 = 0 primeiro (pi0), depois os que mexem em q
GP = [comb_arr(c, 0) for c in gens]
isq = [bool((P[64:128] ^ P[0:64]).any() or (P[128:192] ^ P[0:64]).any()) for P in GP]
# reduz para que exatamente dim(q) geradores tenham q != 0
qv = [packb(np.concatenate([P[64:128] ^ P[0:64], P[128:192] ^ P[0:64]])) for P in GP]
pv = {}; g0 = []; gq = []
for c, v in zip(gens, qv):
    comb = c
    while v:
        b = v.bit_length() - 1
        if b in pv: v ^= pv[b][0]; comb ^= pv[b][1]
        else: pv[b] = (v, comb); gq.append(comb); break
    else: g0.append(comb)
ordem = g0 + gq
GL = [lab(comb_arr(c, 0)) for c in ordem]; GH = [comb_arr(c, 1) for c in ordem]; KH = [comb_arr(c, 1) for c in ker]
print(f"{nome}: geradores de pi0: {len(g0)}, geradores de q: {len(gq)}, nucleo de H: {len(ker)}")
with open(os.path.join(here, f"gens_{nome}.bin"), "wb") as f:
    f.write(np.int32(len(ordem)).tobytes())
    for g in GL: f.write(g.tobytes())
pickle.dump({"GL": GL, "GH": GH, "KH": KH, "n0": len(g0), "nq": len(gq), "VB": d["VB"], "K": d["K"]}, open(os.path.join(here, f"gens_{nome}.pkl"), "wb"))
