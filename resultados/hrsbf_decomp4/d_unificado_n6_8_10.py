import numpy as np, sys
sys.stdout.reconfigure(encoding="utf-8")
exec(open(r"C:\Users\Valer\Downloads\analise adversarial\n1-sat-cubos\resultados\hrsbf_decomp4\mecanismo_C.py", encoding="utf-8-sig").read().split("def analisa")[0])
from math import gcd
for n, D in ((6, 3), (8, 4), (10, 3)):
    N = 1 << n; B = rs_bent(n, D); x = np.arange(N)
    wt = np.array([bin(int(v)).count("1") & 1 for v in x])
    Dg = B ^ B[:, x ^ (N - 1)]
    alvo = (n // 2 + wt) & 1
    vale = np.all(Dg == alvo[None, :], axis=0)
    rot = lambda q: ((q << 1) | (q >> (n - 1))) & (N - 1)
    def periodo(v):
        p = 1; y = rot(v)
        while y != v: y = rot(y); p += 1
        return p
    per = np.array([periodo(int(v)) for v in x])
    print(f"n={n}: pontos onde D(x)=n/2+wt(x) para TODAS as {len(B)} bent: {int(vale.sum())}/{N}")
    for p in sorted(set(per.tolist())):
        s = per == p
        print(f"   período {p}: {int(vale[s].sum())}/{int(s.sum())}")
