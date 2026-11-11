# Agrega as fatias fases_<V>_<i>de<n>.json (artefatos do workflow bloco-dim4).
# Uso: python agrega.py V1 <pasta com os json>
import json, glob, os, sys, collections
nome, pasta = sys.argv[1], sys.argv[2]
arqs = sorted(glob.glob(os.path.join(pasta, "**", f"fases_{nome}_*.json"), recursive=True))
fat = set(); mapas = 0; extra = collections.Counter(); tot = collections.Counter(); hist = collections.Counter(); bent_maps = 0
for a in arqs:
    d = json.load(open(a)); fat.add((d["fatia"], d["fatias"])); mapas += d["mapas"]
    for k, v in d["extra"].items(): extra[k] += v
    for k, v in d["total"].items(): tot[k] += v
    for r in d["res"]:
        c, tipo, ks, dl, cnt = r[:5]
        if cnt:
            bent_maps += 1
            hist[(tipo, tuple(map(tuple, ks)), dl, cnt, r[5] if len(r) > 5 else None)] += 1
print("fatias lidas:", len(fat), "de", {n for _, n in fat}, "| mapas:", mapas, "| mapas com fase:", bent_maps)
print("total de funcoes bent por tipo de mapa:", dict(tot))
print("mapas talvez-U, por fase:", dict(extra))
if nome == "V1":
    excl = tot.get("exclusivo", 0) + extra.get("exclusivo (mapa talvez-U)", 0)
    print("V1 exclusivo (fora de U e do antipodal):", excl)
    print("bloco U dentro de V1:", extra.get("U", 0), "| antipodal dentro de V1:", extra.get("antipodal", 0))
print("familias (tipo, postos das fibras, dim linear, fases, fases afins em U): mapas")
for k, v in sorted(hist.items(), key=str): print("  ", v, k)
