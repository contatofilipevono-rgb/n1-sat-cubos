"""(09/11) Enumeracao EXAUSTIVA de RS bent (todas as combinacoes de orbitas de grau 1..DMAX, sem constante) em n,
e tipo da decomposicao em 4 no subespaco invariante V = {pares=0=impares}. Vetorizado em lotes.
Uso: python decomp4_exaust.py n DMAX"""
import numpy as np, itertools, sys, json, time
from collections import Counter

n, DMAX = int(sys.argv[1]), int(sys.argv[2])
N = 1 << n
rot = lambda m: ((m << 1) | (m >> (n - 1))) & (N - 1)
orbs = []
vistos = set()
for d in range(1, DMAX + 1):
    for c in itertools.combinations(range(n), d):
        m = sum(1 << i for i in c)
        if m in vistos: continue
        o = {m}; x = m
        for _ in range(n): x = rot(x); o.add(x)
        vistos |= o
        orbs.append((d, sorted(o)))
pts = np.arange(N)
OT = np.zeros((len(orbs), N), dtype=np.uint8)
for k, (d, o) in enumerate(orbs):
    for m in o: OT[k] ^= ((pts & m) == m).astype(np.uint8)
graus = np.array([d for d, _ in orbs])
E = sum(1 << i for i in range(0, n, 2)); O = sum(1 << i for i in range(1, n, 2))
pe = np.array([bin(x & E).count("1") & 1 for x in range(N)]); po = np.array([bin(x & O).count("1") & 1 for x in range(N)])
masc = [((pe == a) & (po == b)).astype(np.int32) for a, b in itertools.product((0, 1), repeat=2)]
K = len(orbs)
print(f"n={n}, orbitas de grau<= {DMAX}: {K} -> {2**K} funcoes", flush=True)

def wht_lote(S):  # S: (L, N) int32
    a = S.copy(); h = 1
    while h < N:
        a = a.reshape(a.shape[0], -1, 2, h); x = a[:, :, 0, :].copy(); y = a[:, :, 1, :]
        a[:, :, 0, :] = x + y; a[:, :, 1, :] = x - y; a = a.reshape(a.shape[0], N); h *= 2
    return a

def tipo(Wabs):
    v = set(np.unique(Wabs).tolist())
    if v == {2 ** ((n - 2) // 2)}: return "B"
    if v <= {0, 2 ** (n // 2)}: return "S"
    if v <= {0, 2 ** ((n - 2) // 2), 2 ** (n // 2)}: return "5"
    return "?"

t0 = time.time()
cont = Counter(); nbent = 0; L = 1 << 15
for i0 in range(0, 1 << K, L):
    idx = np.arange(i0, min(i0 + L, 1 << K))
    bits = ((idx[:, None] >> np.arange(K)[None, :]) & 1).astype(np.uint8)
    tt = (bits @ OT) & 1
    S = (1 - 2 * tt.astype(np.int32))
    W = wht_lote(S)
    bent = np.all(np.abs(W) == 2 ** (n // 2), axis=1)
    if not bent.any(): continue
    for j in np.nonzero(bent)[0]:
        nbent += 1
        gs = graus[bits[j].astype(bool)]
        gmax = int(gs.max())
        homog = "homog" if (gs == gmax).all() else ("so_topo+lin" if set(gs.tolist()) <= {1, gmax} else "misto")
        ts = "".join(tipo(np.abs(wht_lote((S[j] * mk)[None, :])[0])) for mk in masc)
        sinal = int(np.sign(W[j, 0]) * np.sign(W[j, N - 1]))
        cont[(gmax, homog, ts + f"|W0*W1:{sinal:+d}")] += 1
print(f"RS bent encontradas: {nbent} ({time.time()-t0:.0f}s)")
for k, v in sorted(cont.items()): print(f"   grau {k[0]}, {k[1]}, tipos {k[2]}: {v}")
json.dump({"n": n, "DMAX": DMAX, "rs_bent": nbent, "tipos": {f"g{k[0]}_{k[1]}_{k[2]}": v for k, v in cont.items()}},
          open(f"decomp4_exaust_n{n}_d{DMAX}.json", "w"), indent=1)
