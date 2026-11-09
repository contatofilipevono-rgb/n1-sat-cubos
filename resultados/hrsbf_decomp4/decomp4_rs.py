"""(09/11) Decomposicao em 4 (Canteaut-Charpin) de RS bent no subespaco invariante por rotacao
V = {x : sum_{i par} x_i = 0 = sum_{i impar} x_i} (codim 2), V^perp = <u, w>, u = (1,0,1,0,...), w = (0,1,0,1,...).
Para cada f: tipo das 4 restricoes f_{ab} (a,b = paridades par/impar): 'B' bent, 'S' {0, ±2^{n/2}}, '5' cinco valores,
e o tipo previsto pelo dual: D_u D_w f~ = 1 (todas bent), = 0 (todas S), senao (5 valores) -- controle do teorema.
Familias: (i) quadraticas RS homogeneas bent; (ii) Tang/MM: f = x.y + gamma(x+y) com x = primeira metade,
y = segunda metade (r = n/2), gamma RS em r variaveis aleatoria de grau dado. Saida: tabela por (n, familia, grau)."""
import numpy as np, itertools, random, json, sys

def wht(v):
    a = v.astype(np.int64).copy(); h = 1; n = len(a)
    while h < n:
        a = a.reshape(-1, 2, h); x = a[:, 0, :].copy(); y = a[:, 1, :]
        a[:, 0, :] = x + y; a[:, 1, :] = x - y; a = a.reshape(-1); h *= 2
    return a

def anf_tt(monos, n):
    pts = np.arange(1 << n); tt = np.zeros(1 << n, dtype=np.uint8)
    for m in monos: tt ^= ((pts & m) == m).astype(np.uint8)
    return tt

def rot(m, n):  # rotacao ciclica de um monomio (bitmask)
    return ((m << 1) | (m >> (n - 1))) & ((1 << n) - 1)

def orbita(m, n):
    o = {m}; x = m
    for _ in range(n): x = rot(x, n); o.add(x)
    return o

def tipo_espectro(vals, n):
    a = set(np.abs(vals).tolist())
    if a == {2 ** ((n - 2) // 2)}: return "B"
    if a <= {0, 2 ** (n // 2)}: return "S"
    if a <= {0, 2 ** ((n - 2) // 2), 2 ** (n // 2)}: return "5"
    return "?" + str(sorted(a))[:40]

def analisa(tt, n):
    s = (-1.0) ** tt
    W = wht(s)
    bent = np.all(np.abs(W) == 2 ** (n // 2))
    if not bent: return None
    pts = np.arange(1 << n)
    E = sum(1 << i for i in range(0, n, 2)); O = sum(1 << i for i in range(1, n, 2))
    pe = np.array([bin(x & E).count("1") & 1 for x in range(1 << n)]); po = np.array([bin(x & O).count("1") & 1 for x in range(1 << n)])
    tipos = []
    for a, b in itertools.product((0, 1), repeat=2):
        C = (pe == a) & (po == b)
        Wc = wht(s * C)  # restricao estendida por zero: valores = espectro da restricao (cada classe 4x)
        tipos.append(tipo_espectro(Wc, n))
    # dual e D_u D_w
    dual = (W < 0).astype(np.uint8)
    u, w = E, O
    dd = dual ^ dual[pts ^ u] ^ dual[pts ^ w] ^ dual[pts ^ (u ^ w)]
    prev = "B" if np.all(dd == 1) else ("S" if np.all(dd == 0) else "5")
    return "".join(tipos), prev

def familia_tang(n, grau, rng):
    r = n // 2
    # x.y com x_i = bit i (i<r), y_i = bit i+r: monomios x_i y_i  -> orbita de x_0 x_r (RS)
    monos = set();
    for i in range(r): monos ^= {(1 << i) | (1 << (i + r))}
    # gamma RS em r variaveis z_i = x_i + y_i; escolher orbitas aleatorias de grau <= grau, incluindo uma de grau exato
    orbs = {}
    for d in range(1, grau + 1):
        for c in itertools.combinations(range(r), d):
            m = sum(1 << i for i in c); key = min(orbita(m, r))
            orbs.setdefault(d, set()).add(key)
    escolhidas = [rng.choice(sorted(orbs[grau]))] + [o for d in range(1, grau) for o in orbs[d] if rng.random() < 0.5]
    # gamma(z) com z_i = x_i + x_{i+r}: tabela-verdade direta
    pts = np.arange(1 << n)
    z = (pts & ((1 << r) - 1)) ^ (pts >> r)
    gtt = np.zeros(1 << n, dtype=np.uint8)
    for o in escolhidas:
        for m in orbita(o, r):
            gtt ^= ((z & m) == m).astype(np.uint8)
    return anf_tt(monos, n) ^ gtt

def quad_rs_homog(n):
    """todas as quadraticas RS homogeneas bent: somas de orbitas x_i x_{i+k}, k=1..n/2."""
    out = []
    ks = list(range(1, n // 2 + 1))
    for sub in itertools.product((0, 1), repeat=len(ks)):
        monos = set()
        for k, s_ in zip(ks, sub):
            if s_:
                for m in orbita((1 << 0) | (1 << k), n): monos.add(m)
        if monos:
            tt = anf_tt(monos, n)
            r = analisa(tt, n)
            if r: out.append((tuple(k for k, s_ in zip(ks, sub) if s_), r))
    return out

if __name__ == "__main__":
    rng = random.Random(1)
    res = {}
    for n in (8, 10, 12, 14):
        q = quad_rs_homog(n)
        tab = {}
        for _, (t, p) in q: tab[(t, p)] = tab.get((t, p), 0) + 1
        print(f"n={n} quadraticas RS homogeneas bent: {len(q)}; (tipos, previsto pelo dual): {tab}", flush=True)
        res[f"n{n}_quad"] = {str(k): v for k, v in tab.items()}
        for grau in range(2, n // 2 + 1):
            tab = {}; nb = 0
            for t in range(12 if n <= 12 else 6):
                tt = familia_tang(n, grau, rng)
                r = analisa(tt, n)
                if r: nb += 1; tab[r] = tab.get(r, 0) + 1
            print(f"   n={n} Tang/MM grau {grau}: bent {nb}; (tipos, previsto): {tab}", flush=True)
            res[f"n{n}_tang_g{grau}"] = {str(k): v for k, v in tab.items()}
    json.dump(res, open("decomp4_rs.json", "w"), indent=1)
