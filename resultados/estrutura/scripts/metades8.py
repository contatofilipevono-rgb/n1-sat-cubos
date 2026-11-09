"""(09/11) Separacao em x: D = D0 + x C (9 var). D liftavel => D0 = D|x=0 e D1 = D|x=1 liftaveis em 8 variaveis,
ambas com parte quartica T. Logo C3 = (parte cubica de D1) - (parte cubica de D0).
Aqui: E8 = {R (graus 1..3 em Y) : T + R liftavel (I6 ∧ I7 em 8 var)}; amostra E8 com CaDiCaL e mede
W = span das diferencas das partes cubicas (+ gauge iota_u T). Se dim W < 56 - ..., C3 fica restrito a W.
Liftavel em 8 var: c_S = 0 mod 4 (|S| >= 6) e = 0 mod 8 (|S| >= 7), por tabela-verdade na conferencia."""
import os, sys, json, random, time
from itertools import combinations
import numpy as np
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\n1-sat-cubos")
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
from sat_cnf import CNF
from i7 import adiciona_I7
from pysat.solvers import Cadical153

classe = os.environ.get("CLASSE", "F4+F4")
w1, w2, ny = so.pencil(so.classes()[classe])
fixo9, incog9, C3, Tq = so.modelo_nove(w1, w2, ny)
X = 1 << ny
fixo = sorted(m for m in set(fixo9) if not m & X)
assert all(bin(m).count("1") <= 4 for m in fixo)
incog = [m for d in (1, 2, 3) for m in (sum(1 << i for i in c) for c in combinations(range(8), d)) if m not in set(fixo)]
nv = len(incog)
cnf = CNF(nv + 1)
# I6: para |S| >= 6, paridade dos produtos de pares com uniao S = 0
univ = [(m, None) for m in fixo] + [(m, k + 1) for k, m in enumerate(incog)]
pares = {}
for a, b in combinations(range(len(univ)), 2):
    u = univ[a][0] | univ[b][0]
    if bin(u).count("1") >= 6:
        vs = [v for (_, v) in (univ[a], univ[b]) if v is not None]
        pares.setdefault(u, []).append(vs)
for S, lst in pares.items():
    lits = []; c = 0
    for vs in lst:
        if not vs: c ^= 1
        elif len(vs) == 1: lits.append(vs[0])
        else: lits.append(cnf.e(vs[0], vs[1]))
    cnf.xor(lits, c)
info7 = adiciona_I7(cnf, fixo, incog, 8)


def lift_tabela(monos):
    N = 256; iv = np.arange(N)
    tt = np.zeros(N, dtype=np.int64)
    for m in set(fixo) ^ set(monos):
        tt ^= ((iv & m) == m).astype(np.int64)
    a = tt.copy(); h = 1
    while h < N:
        a = a.reshape(-1, 2, h); a[:, 1, :] -= a[:, 0, :]; a = a.reshape(-1); h *= 2
    pop = np.array([bin(i).count("1") for i in range(N)])
    return bool(np.all(a[pop >= 6] % 4 == 0)), bool(np.all(a[pop >= 7] % 8 == 0))


if __name__ == "__main__":
    s = Cadical153(bootstrap_with=cnf.cl)
    cub = [k for k, m in enumerate(incog) if bin(m).count("1") == 3]
    print(f"{classe}: 8 var, incognitas {nv} (cubicas {len(cub)}), I7 {info7}", flush=True)
    rnd = random.Random(int(os.environ.get("SEMENTE", 1)))
    amostras = []
    t0 = time.time()
    N = int(os.environ.get("N", 150))
    tent = 0
    t1 = time.time(); r0 = s.solve(); print("sem suposicoes:", r0, f"{time.time()-t1:.1f}s", flush=True)
    while len(amostras) < N:
        tent += 1
        t1 = time.time()
        if amostras:  # bloqueia a parte cubica anterior (novas solucoes, sem suposicoes)
            ult = amostras[-1]
            s.add_clause([-(cub[i] + 1) if (ult >> i) & 1 else (cub[i] + 1) for i in range(len(cub))])
        ok = s.solve()
        if tent <= 10 or tent % 20 == 0:
            print(f"tentativa {tent}: {ok} {time.time()-t1:.1f}s; amostras {len(amostras)}", flush=True)
        if not ok:
            continue
        mod = set(v for v in s.get_model() if v > 0)
        monos = [incog[k] for k in range(nv) if (k + 1) in mod]
        if len(amostras) < 5:
            i6, i7 = lift_tabela(monos)
            assert i6 and i7, "conferencia por tabela falhou"
        amostras.append(sum(1 << cub.index(k) for k in range(nv) if (k + 1) in mod and k in set(cub)))
        if len(amostras) % 10 == 0:
            json.dump({"cubicos": [incog[k] for k in cub], "amostras": amostras}, open("metades8_parcial.json", "w"))
    # span das diferencas + gauge iota_u T (em coordenadas cubicas)
    def red(rows):
        piv = {}
        for v in rows:
            while v:
                h = v.bit_length() - 1
                if h in piv: v ^= piv[h]
                else: piv[h] = v; break
        return piv
    difs = [a ^ amostras[0] for a in amostras[1:]]
    cubm = [incog[k] for k in cub]
    gauge = []
    for i in range(8):
        r = 0
        for t in Tq:
            if (t >> i) & 1:
                r ^= 1 << cubm.index(t ^ (1 << i))
        gauge.append(r)
    print(f"amostras {len(amostras)} ({time.time()-t0:.0f}s); dim span(diferencas) = {len(red(difs))}; "
          f"com gauge = {len(red(difs + gauge))} de {len(cub)}", flush=True)
    json.dump({"classe": classe, "cubicos": cubm, "amostras": amostras}, open(f"metades8_{classe.replace('^','').replace('+','')}.json", "w"))
