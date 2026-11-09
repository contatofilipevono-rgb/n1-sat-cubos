"""Controle do filtro: somas reais de duas bent passam; f8 (Feng) e F8 (Kepes) sao barradas."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from filtro_soma_bent import *

rng = random.Random(5)
ok = [feasible(mm_bent(4, rng) ^ mm_bent(4, rng), 8, time_limit=60) for _ in range(3)]
f8 = anf_tt(8, [(0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7)])
F8 = sigma(8, [0, 2, 4])
bf, bF = feasible(f8, 8, time_limit=60), feasible(F8, 8, time_limit=60)
print("somas MM+MM (esperado True):", ok, "| f8:", bf, "| F8:", bF)
assert all(x is True for x in ok) and bf is False and bF is False
print("CONTROLE OK")
