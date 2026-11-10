"""(10/11) RS bent-negabent de grau <= 4 em n=12, exato sobre o catálogo completo do Astra.
Critério: f negabent  <=>  f + s2 bent, s2 = soma de todos os x_i x_j (RS, grau 2, = as 6 órbitas de grau 2, máscara LOW 63).
Termos afins não alteram a bentness de f nem a de f + s2, logo a normalização afim do catálogo não atrapalha.
Para cada topo quártico t (todos os 67.647 com bent, expandidos das órbitas dos representantes pela mesma transformação do
lookup do Astra, aqui vetorizada), conta as partes baixas L com L ^ 63 também presente para t.
Previsão (Mandal–Singh–Gangopadhyay–Maitra–Vetrivel 2018; Mandal–Maitra–Stănică 2022, caso 4p^k): zero.
Controles: (i) amostra de (t, L) transformados reconstruída e conferida bent por Walsh nos 4096 pontos;
(ii) para a mesma amostra, f + s2 conferida por Walsh direto, comparando com o veredito por pertinência.
Uso: python negabent_n12.py DIR_ASTRA (com catalog/catalog-index.tsv e catalog.bin, e os .py do Astra)"""
import sys, os, csv, zlib, struct, json, time, random
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
ASTRA = sys.argv[1]
sys.path.insert(0, ASTRA)
from top_filters import N, SIZE, TOP, active_bits, orbits, masks_of_size
from top_quotient import quartic_map, transform_tables, action
from quartic_catalog import linear_generators, orbit_tree, LOW

S2 = 63
assert all(bin(m).count("1") == 2 for m, _ in LOW[:6]) and all(bin(m).count("1") == 3 for m, _ in LOW[6:])
rows = linear_generators()
ops = [transform_tables(quartic_map(r)) for r in rows]
x = np.arange(SIZE)
FWD = []
for r in rows:
    f = np.zeros(SIZE, dtype=np.int64)
    for k, row in enumerate(r):
        par = np.zeros(SIZE, dtype=np.int64)
        for b in active_bits(row): par ^= (x >> b) & 1
        f |= par << k
    FWD.append(f)
# estrutura para lower_columns vetorizado
X3 = np.array([v for v in range(SIZE) if bin(v).count("1") <= 3])
pos = {int(v): i for i, v in enumerate(X3)}
ORBS = [o for _, o in LOW] + [o for _, o in TOP]
SUP = np.array([u for o in ORBS for u in o], dtype=np.int64)
GRP = np.repeat(np.arange(len(ORBS)), [len(o) for o in ORBS])
Z = np.zeros((len(LOW), len(X3)), dtype=np.int64)  # subconjuntos x ⊆ m de cada m em LOW
for i, (m, _) in enumerate(LOW):
    s = m
    while True:
        Z[i, pos[s]] = 1
        if s == 0: break
        s = (s - 1) & m
def lower_columns_vec(points):
    p = points[X3]
    inc = ((p[:, None] & SUP[None, :]) == SUP[None, :]).astype(np.int64)      # 299 x 816
    C = np.zeros((len(X3), len(ORBS)), dtype=np.int64)
    np.add.at(C.T, GRP, inc.T)
    C &= 1
    M = (Z @ C) & 1                                                          # 25 x 68
    return [int(sum(int(M[i, j]) << i for i in range(len(LOW)))) for j in range(len(ORBS))]

def wht(v):
    a = v.copy(); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h); x0 = a[:, 0, :].copy(); y0 = a[:, 1, :]; a[:, 0, :] = x0 + y0; a[:, 1, :] = x0 - y0; a = a.reshape(-1); h *= 2
    return a
def tabela(top, low):
    t = np.zeros(SIZE, np.int64)
    for j in active_bits(top):
        for u in TOP[j][1]: t ^= ((x & u) == u)
    for j in active_bits(low):
        for u in LOW[j][1]: t ^= ((x & u) == u)
    return t
def eh_bent(t): return bool(np.all(np.abs(wht(1 - 2 * t)) == 64))

idx = [r for r in csv.DictReader(open(os.path.join(ASTRA, "catalog", "catalog-index.tsv")), delimiter="\t") if int(r["count"])]
binf = open(os.path.join(ASTRA, "catalog", "catalog.bin"), "rb")
rng = random.Random(12)
tot_topos = tot_reg = neg = 0; amostra = []; t0 = time.time()
for nr, r in enumerate(idx):
    rep, c = int(r["top"]), int(r["count"])
    binf.seek(int(r["offset"])); codes = np.array(struct.unpack(f"<{c}I", zlib.decompress(binf.read(int(r["length"])))), dtype=np.int64)
    tree = orbit_tree(rep, ops)
    assert len(tree) == int(r["orbit_size"])
    # relabel por BFS a partir do representante: relabel(filho) = relabel(pai)[FWD[op]]
    relabel = {rep: np.arange(SIZE)}
    ordem = [rep]
    for v in ordem:
        for i, op in enumerate(ops):
            w = action(op, v)
            if w in tree and tree[w] == (v, i) and w not in relabel:
                relabel[w] = relabel[v][FWD[i]]; ordem.append(w)
    assert len(relabel) == len(tree)
    for top, rl in relabel.items():
        if top == rep:
            lows = codes
        else:
            cols = lower_columns_vec(rl)
            const = 0
            for j in active_bits(rep): const ^= cols[len(LOW) + j]
            lows = np.full(len(codes), const, dtype=np.int64)
            for i in range(len(LOW)):
                lows ^= ((codes >> i) & 1) * cols[i]
        s = np.unique(lows); assert len(s) == len(lows)
        k = int(np.isin(lows ^ S2, s).sum())
        neg += k; tot_topos += 1; tot_reg += len(lows)
        if rng.random() < 3e-4 and len(amostra) < 25:
            amostra.append((top, int(lows[rng.randrange(len(lows))]), k))
    if (nr + 1) % 250 == 0: print(f"rep {nr+1}/{len(idx)}: topos {tot_topos}, registros {tot_reg}, negabent {neg} ({time.time()-t0:.0f}s)", flush=True)
print(f"TOTAL: topos {tot_topos}, registros normalizados {tot_reg}, f com f+s2 no catálogo (bent-negabent): {neg}")
ctrl = []
for top, low, _ in amostra:
    t = tabela(top, low); ts2 = tabela(top, low ^ S2)
    ctrl.append({"top": top, "low": low, "f_bent": eh_bent(t), "f_mais_s2_bent": eh_bent(ts2)})
print("controles:", sum(c["f_bent"] for c in ctrl), "/", len(ctrl), "reconstruídas bent;", sum(c["f_mais_s2_bent"] for c in ctrl), "com f+s2 bent")
json.dump({"topos": tot_topos, "registros_normalizados": tot_reg, "bent_negabent": neg,
           "esperado_registros": 77319680, "esperado_topos": 67647 + 1, "controles": ctrl},
          open("negabent_n12.json", "w"), indent=1)
