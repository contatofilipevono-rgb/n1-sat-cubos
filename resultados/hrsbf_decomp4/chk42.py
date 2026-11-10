import csv,sys
rows=list(csv.DictReader(open(sys.argv[1]),delimiter="\t"))
b=1<<42
tot=[0,0];w=[0,0];reps=[0,0]
for r in rows:
    t=int(r["top"]);c=int(r["count"]);o=int(r["orbit_size"])
    if c==0: continue
    k=1 if t&b else 0
    reps[k]+=1; tot[k]+=c; w[k]+=c*o
print("reps com bent (sem/com orbita 42):",reps,"registros:",tot,"ponderado:",w, "max top", max(int(r["top"]) for r in rows).bit_length())
