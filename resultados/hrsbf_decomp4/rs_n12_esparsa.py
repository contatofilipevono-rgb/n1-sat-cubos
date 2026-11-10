"""(09/11) RS bent em n=12 por busca semi-exaustiva: parte linear+quadratica arbitraria (2^7) + ate KMAX orbitas
de grau 3 e 4. Para cada bent: sinal W(0)W(1) (regra: +1), g(0)+g(1) (regra: 0) e tipo da decomposicao em 4."""
import numpy as np, itertools, json, time, sys
from collections import Counter
n = 12; N = 1 << n; KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 2
rot = lambda m: ((m << 1) | (m >> (n - 1))) & (N - 1)
def orbitas(d):
    out, vis = [], set()
    for c in itertools.combinations(range(n), d):
        mm = sum(1 << i for i in c)
        if mm in vis: continue
        o = {mm}; x = mm
        for _ in range(n): x = rot(x); o.add(x)
        vis |= o; out.append(sorted(o))
    return out
pts = np.arange(N)
def tt_orb(o):
    t = np.zeros(N, dtype=np.uint8)
    for mm in o: t ^= ((pts & mm) == mm).astype(np.uint8)
    return t
base_orbs = orbitas(1) + orbitas(2)            # 7
alto = [(3, o) for o in orbitas(3)] + [(4, o) for o in orbitas(4)]
TB = np.array([tt_orb(o) for o in base_orbs]); TA = [tt_orb(o) for _, o in alto]
print(f"orbitas base {len(base_orbs)}, altas {len(alto)}", flush=True)
E = sum(1 << i for i in range(0, n, 2)); O = sum(1 << i for i in range(1, n, 2))
pe = np.array([bin(x & E).count("1") & 1 for x in range(N)]); po = np.array([bin(x & O).count("1") & 1 for x in range(N)])
masc = [((pe == a) & (po == b)).astype(np.int32) for a, b in itertools.product((0, 1), repeat=2)]
def wht_lote(S):
    a = S.copy(); h = 1
    while h < N:
        a = a.reshape(a.shape[0], -1, 2, h); x = a[:, :, 0, :].copy(); y = a[:, :, 1, :]
        a[:, :, 0, :] = x + y; a[:, :, 1, :] = x - y; a = a.reshape(a.shape[0], N); h *= 2
    return a
def tipo(Wabs):
    v = set(np.unique(Wabs).tolist())
    if v == {32}: return "B"
    if v <= {0, 64}: return "S"
    if v <= {0, 32, 64}: return "5"
    return "?"
bits = ((np.arange(128)[:, None] >> np.arange(7)[None, :]) & 1).astype(np.uint8)
BASE = (bits @ TB) & 1                                  # 128 x N
cont = Counter(); t0 = time.time(); nb = 0
escolhas = [()] + [(i,) for i in range(len(alto))] + list(itertools.combinations(range(len(alto)), 2))
if KMAX < 2: escolhas = [e for e in escolhas if len(e) <= KMAX]
for e in escolhas:
    extra = np.zeros(N, dtype=np.uint8)
    for i in e: extra ^= TA[i]
    tt = BASE ^ extra[None, :]
    S = 1 - 2 * tt.astype(np.int32)
    W = wht_lote(S)
    bent = np.all(np.abs(W) == 64, axis=1)
    for j in np.nonzero(bent)[0]:
        nb += 1
        gmax = max([2 if bits[j, 1:].any() else (1 if bits[j, 0] else 0)] + [alto[i][0] for i in e])
        s = int(np.sign(W[j, 0]) * np.sign(W[j, N - 1]))
        g01 = int(tt[j, 0] ^ tt[j, N - 1])
        ts = "".join(tipo(np.abs(wht_lote((S[j] * mk)[None, :])[0])) for mk in masc)
        cont[(gmax, len(e), s, g01, ts)] += 1
print(f"RS bent encontradas: {nb} ({time.time()-t0:.0f}s)")
print("(grau, #orbitas altas, sinal W0W1, g(0)+g(1), tipos): contagem")
for k, v in sorted(cont.items(), key=str): print("  ", k, v)
json.dump({str(k): v for k, v in cont.items()}, open("rs_n12_esparsa.json", "w"), indent=1)
