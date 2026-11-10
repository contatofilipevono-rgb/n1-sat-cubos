import numpy as np, itertools, sys
sys.stdout.reconfigure(encoding="utf-8")
def orbs(m, dmax):
    M = 1 << m; rot = lambda q: ((q << 1) | (q >> (m - 1))) & (M - 1)
    out, vis = [], set()
    for d in range(1, dmax + 1):
        for c in itertools.combinations(range(m), d):
            q = sum(1 << i for i in c)
            if q in vis: continue
            o = {q}; x = q
            for _ in range(m): x = rot(x); o.add(x)
            vis |= o; out.append((c, sorted(o)))
    return out
def walsh_em(tt, w):
    M = len(tt); return sum((-1) ** (int(tt[x]) ^ (bin(x & w).count("1") & 1)) for x in range(M))
# n=12: G RS grau <=3 em 6 variáveis; W_G(1) ≡ 0 mod 8  <=>  b012 = b024 ?
m = 6; O = orbs(m, 3); M = 1 << m; pts = np.arange(M)
cols = [np.bitwise_xor.reduce([((pts & q) == q).astype(np.uint8) for q in o]) for _, o in O]
nome = [c for c, _ in O]; i012 = nome.index((0, 1, 2)); i024 = nome.index((0, 2, 4))
viol = 0
for s in range(1 << len(O)):
    tt = np.zeros(M, np.uint8)
    for k in range(len(O)):
        if s >> k & 1: tt ^= cols[k]
    W = walsh_em(tt, M - 1)
    if ((W % 8 == 0) != ((s >> i012 & 1) == (s >> i024 & 1))): viol += 1
print(f"n=12 (m=6): {1 << len(O)} funções G; violações de [W_G(1)≡0 mod 8 <=> b012=b024]: {viol}")
# n=8: G RS grau <=2 em 4 variáveis; W_G(1) ≡ 0 mod 16 <=> b02 = 0 ?
m = 4; O = orbs(m, 2); M = 1 << m; pts = np.arange(M)
cols = [np.bitwise_xor.reduce([((pts & q) == q).astype(np.uint8) for q in o]) for _, o in O]
nome = [c for c, _ in O]; i02 = nome.index((0, 2)); viol = 0
for s in range(1 << len(O)):
    tt = np.zeros(M, np.uint8)
    for k in range(len(O)):
        if s >> k & 1: tt ^= cols[k]
    W = walsh_em(tt, M - 1)
    if ((W % 16 == 0) != ((s >> i02 & 1) == 0)): viol += 1
print(f"n=8 (m=4): {1 << len(O)} funções G; violações de [W_G(1)≡0 mod 16 <=> b02=0]: {viol}")
# passo 1: órbitas na classe w=1 de n=12 e n=8
for n in (8, 12):
    N = 1 << n; m = n // 2; rot = lambda q: ((q << 1) | (q >> (n - 1))) & (N - 1)
    C = [x for x in range(N) if (x ^ ((x >> m) | ((x & ((1 << m) - 1)) << m))) == N - 1]
    vis, tam = set(), []
    for x in C:
        if x in vis: continue
        o = {x}; y = x
        for _ in range(n): y = rot(y); o.add(y)
        vis |= o; tam.append(len(o))
    print(f"n={n}: classe w=1 tem {len(C)} pontos, órbitas de tamanhos {sorted(tam)}")
