import numpy as np, sys, os, csv, zlib, struct, random
exec(open("fix_restricoes_n12.py", encoding="utf-8-sig").read().split("def periodicos")[0])
pts = np.arange(1 << N)
def tt(orbs_bits):
    t = np.zeros(1 << N, dtype=np.uint8)
    for o in orbs_bits:
        for q in o: t ^= ((pts & q) == q).astype(np.uint8)
    return t
def wht(v):
    a = v.astype(np.int64).copy(); h = 1
    while h < len(a):
        a = a.reshape(-1, 2, h); x = a[:, 0, :].copy(); y = a[:, 1, :]
        a[:, 0, :] = x + y; a[:, 1, :] = x - y; a = a.reshape(-1); h *= 2
    return a
d = sys.argv[1]; idx = [r for r in csv.DictReader(open(os.path.join(d, "catalog-index.tsv")), delimiter="\t") if int(r["count"])]
binf = open(os.path.join(d, "catalog.bin"), "rb"); rng = random.Random(5); ok = 0; tot = 0
for r in rng.sample(idx, 40):
    c = int(r["count"]); binf.seek(int(r["offset"])); codes = struct.unpack(f"<{c}I", zlib.decompress(binf.read(int(r["length"]))))
    top = int(r["top"])
    for low in rng.sample(codes, min(3, c)):
        orbs = [TOP[j] for j in range(43) if top >> j & 1] + [LOW[j] for j in range(25) if low >> j & 1]
        W = wht(1 - 2 * tt(orbs).astype(np.int64)); tot += 1; ok += bool(np.all(np.abs(W) == 64))
print(f"decodificação validada: {ok}/{tot} funções reconstruídas são bent")
