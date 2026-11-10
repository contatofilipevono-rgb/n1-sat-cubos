import numpy as np, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
exec(open("resultados/hrsbf_decomp4/mecanismo_C.py", encoding="utf-8-sig").read().split("def analisa")[0])
def grau_lote(T):
    a = T.copy(); h = 1; Mx = a.shape[1]
    while h < Mx:
        a = a.reshape(a.shape[0], -1, 2, h); a[:, :, 1, :] ^= a[:, :, 0, :]; a = a.reshape(a.shape[0], Mx); h *= 2
    pc = np.array([bin(i).count("1") for i in range(Mx)])
    return np.where(a.any(axis=1), (a * pc[None, :]).max(axis=1), -1)
for n, D in ((6, 3), (8, 4), (10, 3)):
    m = n // 2; M = 1 << m; B = rs_bent(n, D); y = np.arange(M)
    cp, ca = Counter(), Counter()
    for w in range(M):
        dg = grau_lote(B[:, y | ((y ^ w) << m)])
        (cp if (bin(w).count("1") - m) % 2 else ca).update(dg.tolist())
    print(f"n={n}: grau de g_w nas coclasses proibidas: {dict(sorted(cp.items()))}; nas permitidas: {dict(sorted(ca.items()))}")
