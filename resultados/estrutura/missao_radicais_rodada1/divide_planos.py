"""Consolida rank-*.json, deduplica planos {a,b,a+b} e escreve lotes no formato sampled_pair_rank (para radical_grau8.py)."""
import json, sys, glob, os
from collections import Counter
pasta, nlotes = sys.argv[1], int(sys.argv[2])
planos = {}; por_semente = {}
for f in sorted(glob.glob(os.path.join(pasta, "rank-*.json"))):
    d = json.load(open(f)); s = d["seed"]; n = 0
    for row in d["sampled_pair_rank"]:
        for hit in row["pairs_in_N"]:
            k = tuple(sorted((row["a"], hit["b"], row["a"] ^ hit["b"])))
            planos.setdefault(k, s); n += 1
    por_semente[s] = {"cubicas": len(d["sampled_pair_rank"]), "pares_em_N": n}
lista = sorted(planos)
print(f"sementes {len(por_semente)}, pares em N {sum(v['pares_em_N'] for v in por_semente.values())}, planos distintos {len(lista)}")
for i in range(nlotes):
    lote = lista[i::nlotes]
    rows = [{"a": x, "b_candidates_with_rank_deficiency": None, "pairs_in_N": [{"b": y}]} for x, y, _ in lote]
    json.dump({"sampled_pair_rank": rows}, open(os.path.join(pasta, f"lote-{i:02d}.json"), "w"))
json.dump({"por_semente": por_semente, "planos_distintos": len(lista), "planos": [list(p) for p in lista]},
          open(os.path.join(pasta, "consolidado.json"), "w"), indent=1)
