import numpy as np, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
exec(open("resultados/hrsbf_decomp4/mecanismo_C.py", encoding="utf-8-sig").read().split("def analisa")[0])
for n, D in ((6, 3), (8, 4), (10, 3)):
    m = n // 2; M = 1 << m; B = rs_bent(n, D); y = np.arange(M)
    rotm = lambda v, j: ((v << j) | (v >> (m - j))) & (M - 1) if j % m else v
    cand = {}
    for j in range(m):
        for tipo in ("rot", "w+rot"):
            ok = True; usado = 0
            for w in range(M):
                if (bin(w).count("1") - m) % 2 == 0 or w == 0: continue
                e = rotm(w, j) if tipo == "rot" else w ^ rotm(w, j)
                if e == 0: ok = False; break
                G = B[:, y | ((y ^ w) << m)]
                if not np.all(G[:, y ^ e] != G): ok = False; break
                usado += 1
            cand[(tipo, j)] = ok
    print(f"n={n}: e universal (para todas as bent e todas as w proibidas !=0):", [k for k, v in cand.items() if v])
