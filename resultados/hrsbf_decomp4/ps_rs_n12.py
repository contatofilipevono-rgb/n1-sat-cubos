"""(09/11) RS bent PS⁻ em n=12 (Dillon) via base normal de F_4096: f = indicadora de uma uniao de 32 classes de
F_64^* em F_4096^* (classes indexadas por k mod 65, com y = g^k), escolhida fechada por k -> 2k (Frobenius),
f(0)=0. Em coordenadas de base normal, Frobenius = rotacao ciclica, logo f e RS. Testa: bent, RS, grau,
sinal W(0)W(1) (regra (-1)^{n/2} = +1), g(0)+g(1) (regra: = n/2 mod 2 = 0) e tipo da decomposicao em 4."""
import numpy as np, itertools, random, json

n, m = 12, 6
POLY = 0b1000001010011  # x^12+x^6+x^4+x+1 (primitivo para F_4096)
def mul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a >> n: a ^= POLY
    return r
def pw(a, e):
    r = 1
    while e:
        if e & 1: r = mul(r, a)
        a = mul(a, a); e >>= 1
    return r
# verificar primitividade de x (=2): ordem 4095
g = 2
assert pw(g, 4095) == 1 and all(pw(g, 4095 // q) != 1 for q in (3, 5, 7, 13))
logt = {}; x = 1
for k in range(4095): logt[x] = k; x = mul(x, g)
# elemento normal: beta com conjugados linearmente independentes
def posto(vs):
    piv = {}
    for v in vs:
        for h, pv in piv.items():
            if (v >> h) & 1: v ^= pv
        if v: piv[v.bit_length() - 1] = v
    return len(piv)
beta = next(b for b in range(2, 4096) if posto([pw(b, 2 ** i) for i in range(n)]) == n)
conj = [pw(beta, 2 ** i) for i in range(n)]
# vetor x (bits) -> elemento sum x_i beta^{2^i}
elem = np.zeros(1 << n, dtype=np.int64)
for v in range(1 << n):
    e = 0
    for i in range(n):
        if (v >> i) & 1: e ^= conj[i]
    elem[v] = e
assert elem[(1 << n) - 1] == 1, "vetor de uns deveria ser o elemento 1 (traco de beta = 1)"
classe = np.array([-1 if e == 0 else logt[int(e)] % 65 for e in elem])
# orbitas de k -> 2k em Z/65
orbs, vis = [], set()
for c in range(65):
    if c in vis: continue
    o = []; x = c
    while x not in o: o.append(x); x = 2 * x % 65
    vis |= set(o); orbs.append(o)
tam = [len(o) for o in orbs]
def wht(v):
    a = v.astype(np.int64).copy(); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h); x0 = a[:, 0, :].copy(); y0 = a[:, 1, :]
        a[:, 0, :] = x0 + y0; a[:, 1, :] = x0 - y0; a = a.reshape(-1); h *= 2
    return a
def grau(tt):
    a = tt.astype(np.uint8).copy(); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h); a[:, 1, :] ^= a[:, 0, :]; a = a.reshape(-1); h *= 2
    return max(bin(i).count("1") for i in np.nonzero(a)[0]) if a.any() else -1
N = 1 << n; pts = np.arange(N)
rot = ((pts << 1) | (pts >> (n - 1))) & (N - 1)
E = sum(1 << i for i in range(0, n, 2)); O = sum(1 << i for i in range(1, n, 2))
pe = np.array([bin(x & E).count("1") & 1 for x in range(N)]); po = np.array([bin(x & O).count("1") & 1 for x in range(N)])
def tipo(Wabs):
    v = set(np.unique(Wabs).tolist())
    if v == {2 ** ((n - 2) // 2)}: return "B"
    if v <= {0, 2 ** (n // 2)}: return "S"
    if v <= {0, 2 ** ((n - 2) // 2), 2 ** (n // 2)}: return "5"
    return "?"
# subconjuntos de orbitas somando 32 classes
rng = random.Random(3)
alvos = []
# todas as somas exatas: busca por DP aleatoria
idx = list(range(len(orbs)))
tent = 0
while len(alvos) < 60 and tent < 200000:
    tent += 1
    rng.shuffle(idx); tot = 0; S = []
    for i in idx:
        if tot + tam[i] <= 32: S.append(i); tot += tam[i]
        if tot == 32: break
    if tot == 32:
        key = tuple(sorted(S))
        if key not in alvos: alvos.append(key)
res = []
from collections import Counter
cont = Counter()
for key in alvos:
    sup = set(c for i in key for c in orbs[i])
    tt = np.isin(classe, list(sup)).astype(np.uint8); tt[0] = 0
    assert np.all(tt[rot] == tt), "nao RS"
    W = wht(1 - 2 * tt.astype(np.int64))
    bent = bool(np.all(np.abs(W) == 64))
    s = int(np.sign(W[0]) * np.sign(W[N - 1]))
    g01 = int(tt[0] ^ tt[N - 1])
    S_ = 1 - 2 * tt.astype(np.int64)
    ts = "".join(tipo(np.abs(wht(S_ * ((pe == a) & (po == b))))) for a, b in itertools.product((0, 1), repeat=2))
    dg = grau(tt)
    cont[(bent, dg, 0 in sup, s, g01, ts)] += 1
print("orbitas de x->2x em Z/65 (tamanhos):", sorted(tam))
print("(bent, grau, classe0 no suporte, sinal W0W1, f(0)+f(1), tipos): contagem")
for k, v in sorted(cont.items(), key=str): print("  ", k, v)
json.dump({str(k): v for k, v in cont.items()}, open("ps_rs_n12.json", "w"), indent=1)
