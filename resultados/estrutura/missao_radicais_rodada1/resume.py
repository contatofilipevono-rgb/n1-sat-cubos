import json, glob
from collections import Counter
P = []; [P.extend(json.load(open(f))["pairs"]) for f in sorted(glob.glob("rodada1/rad-*.json"))]
dimC = Counter(p["dimension_C"] for p in P); hist = Counter()
for p in P:
    for k, v in p["radical_dimension_histogram"].items(): hist[int(k)] += v
hits = [p for p in P if p["hits"]]
hi = sum(len(p["directly_verified_radicals_of_dimension_at_least_seven"]) for p in P)
cc = sum(p["cross_checks"] for p in P)
print("planos:", len(P), "| dim C/G:", dict(sorted(dimC.items())), "| escolhas de A12:", 1024 * len(P))
print("histograma dos radicais:", dict(sorted(hist.items())), "| radicais dim>=7 conferidos:", hi, "| controles cruzados:", cc)
print("planos com trio:", len(hits))
json.dump({"planos": len(P), "dimC": dimC, "hist_radicais": hist, "trios": hits, "cross_checks": cc, "radicais_ge7": hi},
          open("rodada1/resumo_rodada1.json", "w"), indent=1, default=lambda o: dict(o))
