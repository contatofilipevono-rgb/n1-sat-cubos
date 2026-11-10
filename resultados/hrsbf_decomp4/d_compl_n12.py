# D(x)=g(x)+g(x+1) em Fix6 ∪ Fix4: quais pontos têm D constante em todo o catálogo bent e em RS genérica
exec(open("fix_restricoes_n12.py", encoding="utf-8").read().split("NB = len(PTS)")[0])
import os, csv, zlib, struct, random
ALL1 = (1 << N) - 1
pos = {x: k for k, x in enumerate(PTS)}
def D(v):  # v: bitvector dos valores em PTS
    return {x: ((v >> pos[x]) ^ (v >> pos[x ^ ALL1])) & 1 for x in PTS}
dirn = sys.argv[1]
idx = list(csv.DictReader(open(os.path.join(dirn, "catalog-index.tsv")), delimiter="\t"))
binf = open(os.path.join(dirn, "catalog.bin"), "rb")
vals = {x: set() for x in PTS}
for r in idx:
    c = int(r["count"])
    if not c: continue
    binf.seek(int(r["offset"])); codes = struct.unpack(f"<{c}I", zlib.decompress(binf.read(int(r["length"]))))
    top = int(r["top"]); tv = 0
    for j in range(43):
        if (top >> j) & 1: tv ^= col[25 + j]
    for low in codes:
        v = tv; x = low
        while x:
            b = x & -x; v ^= col[b.bit_length() - 1]; x ^= b
        for p, d in D(v).items(): vals[p].add(d)
gen = {x: set() for x in PTS}
rng = random.Random(1)
for _ in range(3000):
    v = 0
    for cc in col:
        if rng.random() < .5: v ^= cc
    for p, d in D(v).items(): gen[p].add(d)
nome = lambda x: f"{x:012b}"[::-1]
for x in PTS:
    if len(vals[x]) == 1:
        print(nome(x), "Fix6" if x in F6 else "", "Fix4" if x in F4 else "", "D bent =", vals[x], "| genérico:", gen[x])
