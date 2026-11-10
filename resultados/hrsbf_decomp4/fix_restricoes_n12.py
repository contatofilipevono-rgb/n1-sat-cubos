"""(10/11) RS bent n=12 (catálogo grau<=4 do Astra): restrição aos subespaços fixos Fix(rho^d), d | 12.
Pergunta: que relações GF(2)-afins entre os valores g(x), x em Fix(rho^6) ∪ Fix(rho^4), valem para TODA RS bent
do catálogo mas não para RS genérica de grau <= 4?  (Relações genéricas = identidades de grau; as extras vêm de bent.)
Uso: python -I fix_restricoes_n12.py <dir com catalog-index.tsv e catalog.bin>"""
import sys, os, csv, zlib, struct, itertools
sys.stdout.reconfigure(encoding="utf-8")
N = 12; MASK = (1 << N) - 1
rot = lambda m, j=1: ((m << j) | (m >> (N - j))) & MASK if j % N else m

def orbits(d):
    # ordem do Astra (top_filters/higher_filter): representante = menor máscara restante (CORRIGIDO 10/11;
    # antes usava a ordem lexicográfica das combinações, que difere nos graus 3 e 4)
    rem = set(sum(1 << i for i in c) for c in itertools.combinations(range(N), d)); out = []
    while rem:
        r = min(rem); o = sorted({rot(r, j) for j in range(N)}); out.append(o); rem -= set(o)
    return out
LOW = orbits(2) + orbits(3); TOP = orbits(4)
assert len(LOW) == 25 and len(TOP) == 43 and 585 in TOP[42]

def periodicos(p):  # vetores de período p
    return [sum(((y >> (i % p)) & 1) << i for i in range(N)) for y in range(1 << p)]
F6, F4 = periodicos(6), periodicos(4)
PTS = sorted(set(F6) | set(F4))
col = []
for o in LOW + TOP:
    v = 0
    for k, x in enumerate(PTS):
        if sum((x & m) == m for m in o) & 1: v |= 1 << k
    col.append(v)

def reduz(basis, v):
    for h in sorted(basis, reverse=True):
        if (v >> h) & 1: v ^= basis[h]
    return v
def add(basis, v):
    v = reduz(basis, v)
    if v: basis[v.bit_length() - 1] = v; return True
    return False
def kernel(basis, nb):
    # relações c (vetor sobre nb bits) com c·v = 0 para todo v no span
    rows = list(basis.values()); piv = {}
    M = []
    for r in rows:
        for p, (pr) in piv.items():
            if (r >> p) & 1: r ^= pr
        if r:
            p = r.bit_length() - 1
            for q in list(piv):
                if (piv[q] >> p) & 1: piv[q] ^= r
            piv[p] = r
    livres = [j for j in range(nb) if j not in piv]
    ker = []
    for f in livres:
        c = 1 << f
        for p, r in piv.items():
            if (r >> f) & 1: c |= 1 << p
        ker.append(c)
    return ker

NB = len(PTS) + 1   # bit extra = constante 1 (relações afins)
ONE = 1 << len(PTS)
gen = {}
for v in col: add(gen, v)
add(gen, ONE)  # constante livre (o catálogo normaliza afins; genérico inclui constante)
dirn = sys.argv[1]
bent = {}; vistos = set(); nrec = 0
idx = list(csv.DictReader(open(os.path.join(dirn, "catalog-index.tsv")), delimiter="\t"))
binf = open(os.path.join(dirn, "catalog.bin"), "rb")
for r in idx:
    c = int(r["count"])
    if not c: continue
    binf.seek(int(r["offset"])); codes = struct.unpack(f"<{c}I", zlib.decompress(binf.read(int(r["length"]))))
    top = int(r["top"]); tv = 0
    for j in range(43):
        if (top >> j) & 1: tv ^= col[25 + j]
    for low in codes:
        v = tv
        x = low
        while x:
            b = x & -x; v ^= col[b.bit_length() - 1]; x ^= b
        nrec += 1
        v |= ONE        # vetor afim (1, valores)
        if v not in vistos:
            vistos.add(v); add(bent, v)
print(f"registros {nrec}, vetores distintos em Fix6∪Fix4: {len(vistos)}, pontos {len(PTS)}")
print(f"dim span genérico (com constante): {len(gen)}; dim span afim bent: {len(bent)}")
kg = kernel(gen, NB); kb = kernel(bent, NB)
# relações extras: kernel de bent módulo kernel genérico
base_g = {}
for c in kg: add(base_g, c)
extras = []
for c in kb:
    if add(base_g, c): extras.append(c)
print(f"relações genéricas: {len(kg)}; relações bent: {len(kb)}; extras (só bent): {len(extras)}")
nome = lambda x: f"{x:012b}"[::-1]
for c in extras:
    termos = [nome(PTS[k]) for k in range(len(PTS)) if (c >> k) & 1]
    print(("1 + " if (c >> len(PTS)) & 1 else "") + " + ".join(f"g({t})" for t in termos), "= 0")
