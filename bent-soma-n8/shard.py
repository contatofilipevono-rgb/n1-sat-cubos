"""Fatia do varrido RS n=8 com o filtro de soma de duas bent.
uso: python shard.py {4|42} i nshards   -> res/shard_<which>_<i>.jsonl  (linhas [c, resultado])
resultado: false = filtro INFACTIVEL (f nao e soma de duas bent); true = factivel (inconclusivo); null = tempo/memoria
"""
import sys, os, json
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from filtro_soma_bent import rot_orbits, anf_tt, feasible

n = 8
O4, O2 = rot_orbits(n, 4), rot_orbits(n, 2)

def work(a):
    which, c = a
    orbs = O4 if which == "4" else O4 + O2
    f = anf_tt(n, [S for j in range(len(orbs)) if (c >> j) & 1 for S in orbs[j]])
    try:
        return c, feasible(f, n, time_limit=20)
    except MemoryError:
        return c, None

if __name__ == "__main__":
    which, i, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    norb = 10 if which == "4" else 14
    cs = [c for c in range(1, 1 << norb) if c % k == i]
    os.makedirs("res", exist_ok=True)
    out = open(f"res/shard_{which}_{i}.jsonl", "w")
    with Pool(os.cpu_count()) as p:
        for c, r in p.imap_unordered(work, [(which, c) for c in cs], chunksize=2):
            out.write(json.dumps([c, r]) + "\n"); out.flush()
