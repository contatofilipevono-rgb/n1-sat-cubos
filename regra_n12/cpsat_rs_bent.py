"""(10/11) RS bent em n=12, grau <= 6, por CP-SAT (OR-Tools).
Incógnitas: a_O (coeficiente da órbita de monômios O, graus 1..6; constante = 0 sem perda: troca o sinal de W).
Tabela-verdade nos representantes r das órbitas de pontos: t_r = XOR_O a_O * [#{m in O: m ⊆ r} ímpar]  (AddBoolXOr).
Walsh no representante u: W(u) = Σ_r S(u,r)(1 − 2 t_r), S(u,r) = Σ_{x ∈ órbita(r)} (−1)^{u·x};  W(u) = 64 − 128 s_u.
(Espectro de RS é RS, então basta u nos representantes.)
Regra em n=12: g(0)+g(1) = a_{x0x3x6x9} (só órbitas ímpares de grau ≤ 6). Contraexemplo ⇔ RS bent com a_585 = 1.
Uso: python cpsat_rs_bent.py MODO [limite_s] [workers]
  MODO = livre        (controle positivo: qualquer RS bent)
         b1          (controle positivo não trivial: força a órbita x0x1x6x7, que ocorre no catálogo)
         grau6       (controle: força alguma órbita de grau 6 presente)
         regra       (alvo: força a órbita x0x3x6x9)
         c_b12       (alvo de (C): b1 != b2)
Toda solução é conferida por Walsh direto nos 4096 pontos."""
import sys, itertools, time, json
import numpy as np
from ortools.sat.python import cp_model

N = 12; M = 1 << N; MASK = M - 1
rot = lambda m: ((m << 1) | (m >> (N - 1))) & MASK
def orb(m):
    o = {m}; x = m
    for _ in range(N): x = rot(x); o.add(x)
    return sorted(o)
def orbitas_grau(d):
    rem = set(sum(1 << i for i in c) for c in itertools.combinations(range(N), d)); out = []
    while rem:
        r = min(rem); o = orb(r); out.append(o); rem -= set(o)
    return out
import os; DMAX = int(os.environ.get("DMAX", 6))
ORB = [o for d in range(1, DMAX + 1) for o in orbitas_grau(d)]
GRAU = [bin(o[0]).count("1") for o in ORB]
# órbitas de pontos
vis = set(); REP = []
for x in range(M):
    if x in vis: continue
    o = orb(x); vis |= set(o); REP.append(o)
print(f"órbitas de monômios (grau 1..6): {len(ORB)}; órbitas de pontos: {len(REP)}", flush=True)
pc = lambda v: bin(v).count("1")
# matriz de incidência: coef[r][O] = paridade de #{m in O : m ⊆ rep(r)}
inc = [[sum(1 for m in O if (R[0] & m) == m) & 1 for O in ORB] for R in REP]
# S(u, r)
S = [[sum(1 - 2 * (pc(U[0] & x) & 1) for x in R) for R in REP] for U in REP]
idx = lambda s: next(i for i, o in enumerate(ORB) if sum(1 << k for k in s) in o)

def modelo(modo):
    md = cp_model.CpModel()
    a = [md.NewBoolVar(f"a{k}") for k in range(len(ORB))]
    t = []
    for r, R in enumerate(REP):
        ts = md.NewBoolVar(f"t{r}")
        termos = [a[k] for k in range(len(ORB)) if inc[r][k]]
        if termos: md.AddBoolXOr(termos + [ts.Not()])   # XOR(termos) = ts  <=>  XOR(termos, ¬ts) = 1
        else: md.Add(ts == 0)
        t.append(ts)
    for u in range(len(REP)):
        s = md.NewBoolVar(f"s{u}")
        md.Add(sum(S[u][r] * (1 - 2 * t[r]) for r in range(len(REP))) == 64 - 128 * s)
    if modo == "b1": md.Add(a[idx({0, 1, 6, 7})] == 1)
    if modo == "grau6": md.AddBoolOr([a[k] for k in range(len(ORB)) if GRAU[k] == 6])
    if modo == "grau4": md.AddBoolOr([a[k] for k in range(len(ORB)) if GRAU[k] == 4])
    if modo == "regra": md.Add(a[idx({0, 3, 6, 9})] == 1)
    if modo == "c_b12": md.Add(a[idx({0, 1, 6, 7})] != a[idx({0, 2, 6, 8})])
    return md, a

def confere(sol):
    pts = np.arange(M); tt = np.zeros(M, np.int64)
    for k in sol:
        for m in ORB[k]: tt ^= ((pts & m) == m).astype(np.int64)
    w = 1 - 2 * tt; h = 1
    while h < M:
        w = w.reshape(-1, 2, h); x0 = w[:, 0, :].copy(); y0 = w[:, 1, :]; w[:, 0, :] = x0 + y0; w[:, 1, :] = x0 - y0; w = w.reshape(-1); h *= 2
    return bool(np.all(np.abs(w) == 64)), int(tt[0] ^ tt[M - 1])

if __name__ == "__main__":
    modo = sys.argv[1]; lim = float(sys.argv[2]) if len(sys.argv) > 2 else 600; wk = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    md, a = modelo(modo)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = lim; sv.parameters.num_workers = wk
    t0 = time.time(); st = sv.Solve(md); dt = time.time() - t0
    nome = sv.StatusName(st); res = {"modo": modo, "status": nome, "segundos": round(dt, 1), "workers": wk, "limite": lim}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [k for k in range(len(ORB)) if sv.Value(a[k])]
        bent, g01 = confere(sol)
        res.update({"orbitas_ativas": [ORB[k][0] for k in sol], "graus": sorted(GRAU[k] for k in sol),
                    "bent_conferido_4096": bent, "g0_mais_g1": g01})
    print(json.dumps(res), flush=True)
    json.dump(res, open(f"res_{modo}.json", "w"), indent=1)
