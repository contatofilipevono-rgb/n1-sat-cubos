# Fases dos mapas auto-ortogonais: sistema linear (h.c = wt(c)/2) + condicao quadratica (wt(h) = 2 mod 4) por fibra.
# Uso: python fases.py V1|V2     (le mapas_<V>.txt; grava fases_<V>.pkl)
import pickle, os, sys, collections, time
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
nome = sys.argv[1]
g = pickle.load(open(os.path.join(here, f"gens_{nome}.pkl"), "rb"))
GL, GH, KH = g["GL"], g["GH"], g["KH"]
n = len(GL); nk = len(KH)
codes = [int(l) for l in open(os.path.join(here, f"mapas_{nome}.txt"))]
SH = int(sys.argv[2]) if len(sys.argv) > 3 else 0; NSH = int(sys.argv[3]) if len(sys.argv) > 3 else 1      # fatia SH de NSH
codes = codes[SH::NSH]
def rank(vs):
    piv = {}
    for v in vs:
        while v:
            c = v.bit_length() - 1
            if c in piv: v ^= piv[c]
            else: piv[c] = v; break
    return len(piv)
KHm = np.array(KH, dtype=np.uint8)                       # nk x 256
COORD = np.array([[(y >> i) & 1 for y in range(256)] for i in range(8)], dtype=np.uint8)
res = []; t0 = time.time(); hist = collections.Counter(); extra = collections.Counter()
for idx, c in enumerate(codes):
    L = np.zeros(256, dtype=np.uint8); H0 = np.zeros(256, dtype=np.uint8)
    for j in range(n):
        if c >> j & 1: L ^= GL[j]; H0 ^= GH[j]
    q1 = L[64:128] ^ L[0:64]; q2 = L[128:192] ^ L[0:64]
    if nome == "V2":
        tipo = "antipodal" if not q1.any() and not q2.any() else ("U" if not (q1 ^ q2).any() else "exclusivo")
    else:
        # V1: afim em U <=> q1, q2 com valores em {0, 1111} e b = t1 + t2 (b = coeficiente de s1 s2 em H); decide-se por fase
        tipo = "talvez-U" if all(int(x) in (0, 15) for x in q1) and all(int(x) in (0, 15) for x in q2) else "exclusivo"
    fib = [np.nonzero(L == l)[0] for l in range(16)]
    ks = tuple(1 + rank([int(y) ^ int(P[0]) for y in P[1:]]) for P in fib)
    if nome == "V2" and tipo != "exclusivo" and "--todos" not in sys.argv:
        res.append((c, tipo, ks, None, None)); continue
    if max(ks) >= 8:
        res.append((c, tipo, ks, -1, 0)); hist[(tipo, "k=8")] += 1; continue
    # sistema linear nas nk fases
    piv = {}; ok = True
    for P in fib:
        for gi in range(9):
            sel = P if gi == 8 else P[COORD[gi][P] == 1]
            wt = len(sel)
            m = 0
            col = KHm[:, sel].sum(axis=1) & 1
            for j in range(nk):
                if col[j]: m |= 1 << j
            r = ((wt // 2) & 1) ^ (int(H0[sel].sum()) & 1)
            while m:
                b = m.bit_length() - 1
                if b in piv: m ^= piv[b][0]; r ^= piv[b][1]
                else: piv[b] = (m, r); break
            else:
                if r: ok = False
        if not ok: break
    if not ok:
        res.append((c, tipo, ks, -1, 0)); hist[(tipo, "linear inconsistente")] += 1; continue
    # solucao particular e base do nucleo
    sol = 0
    for b in sorted(piv):
        m, r = piv[b]
        if r ^ (bin(sol & (m ^ (1 << b))).count("1") & 1): sol |= 1 << b
    free = [b for b in range(nk) if b not in piv]
    base = []
    for fb in free:
        v = 1 << fb
        for b in sorted(piv):
            m, r = piv[b]
            if bin(v & (m ^ (1 << b))).count("1") & 1: v |= 1 << b
        base.append(v)
    d = len(free)
    Hp = H0.copy()
    for j in range(nk):
        if sol >> j & 1: Hp ^= KHm[j]
    Bv = np.zeros((d, 256), dtype=np.uint8)
    for i, v in enumerate(base):
        for j in range(nk):
            if v >> j & 1: Bv[i] ^= KHm[j]
    # enumeracao das 2^d fases: peso em cada fibra = 2 mod 4
    alive = np.ones(1 << d, dtype=bool)
    T = (np.arange(1 << d, dtype=np.uint32)[:, None] >> np.arange(d)) & 1 if d else np.zeros((1, 0), dtype=np.uint32)
    for P in fib:
        hv = (T.astype(np.int32) @ Bv[:, P].astype(np.int32)) & 1 if d else np.zeros((1, 16), dtype=np.int32)
        wt = (hv ^ Hp[P].astype(np.int32)).sum(axis=1)
        alive &= (wt % 4 == 2)
        if not alive.any(): break
    cnt = int(alive.sum())
    if tipo == "talvez-U" and cnt:
        A = np.nonzero(alive)[0]
        Hf = ((T[A].astype(np.int32) @ Bv.astype(np.int32)) & 1).astype(np.uint8) ^ Hp if d else Hp[None, :]
        b = Hf[:, 0:64] ^ Hf[:, 64:128] ^ Hf[:, 128:192] ^ Hf[:, 192:256]
        alvo = ((q1 != 0) ^ (q2 != 0)).astype(np.uint8)
        nU = int((b == alvo).all(axis=1).sum())
        ant = (not q1.any()) and (not q2.any())
        extra[("antipodal" if ant else "U")] += nU; extra["exclusivo (mapa talvez-U)"] += cnt - nU
        res.append((c, tipo, ks, d, cnt, nU)); hist[(tipo, tuple(sorted(collections.Counter(ks).items())), d, cnt, nU)] += 1
        continue
    res.append((c, tipo, ks, d, cnt)); hist[(tipo, tuple(sorted(collections.Counter(ks).items())), d, cnt)] += 1
    if idx % 2000 == 0: print(f"  {idx}/{len(codes)}  {time.time() - t0:.0f}s", flush=True)
tot = collections.Counter()
for r_ in res:
    if r_[4]: tot[r_[1]] += r_[4]
print("V1, mapas talvez-U, por fase:", dict(extra))
print("histograma (tipo, postos das fibras, dim linear, numero de fases): mapas")
for k, v in sorted(hist.items(), key=str): print("  ", v, k)
print("funcoes bent por tipo:", dict(tot))
import json
json.dump({"bloco": nome, "fatia": SH, "fatias": NSH, "mapas": len(codes), "extra": dict(extra), "total": dict(tot),
           "res": [[r_[0], r_[1], sorted(collections.Counter(r_[2]).items()), r_[3], r_[4]] + list(r_[5:]) for r_ in res]},
          open(os.path.join(here, f"fases_{nome}_{SH}de{NSH}.json"), "w"))
