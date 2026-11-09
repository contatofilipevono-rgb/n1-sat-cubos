"""(09/11) Gera varios C3 distintos em N ∩ L (sem isotropico e C3∧T=0) com bloqueio, CMS. Saida NL_<classe>.jsonl."""
import os, sys, json, time, random
sys.argv = ["x"]
from linear_c3 import restricoes
from analisa_testemunhas import contexto
from fecho_estrela import linhas
import pycryptosat

classe = os.environ.get("CLASSE", "Q4a")
QTD = int(os.environ.get("QTD", 6))
lin, nc, TOP, _ = restricoes(classe)
_, _, _, _, iso, orbs, dados = contexto(classe)
Ms = [linhas(*d) for d in dados]
out = open(f"NL_{classe}.jsonl", "a")
for q in range(QTD):
    s = pycryptosat.Solver()
    for e in lin:
        s.add_xor_clause([p + 1 for p in range(nc) if (e >> p) & 1], bool((e >> TOP) & 1))
    pe = nc + 1
    for M in Ms:
        auxs = []
        for r in M:
            s.add_xor_clause([p + 1 for p in range(nc) if (r >> p) & 1] + [pe], False)
            auxs.append(pe); pe += 1
        s.add_clause(auxs)
    # diversificar: fixa 6 bits aleatorios de C3
    rnd = random.Random(q)
    assum = [(p + 1) * rnd.choice([1, -1]) for p in rnd.sample(range(nc), 6)]
    t0 = time.time()
    r, sol = s.solve(assumptions=assum)
    if r:
        c = [p for p in range(nc) if sol[p + 1]]
        cb = sum(1 << p for p in c)
        okc = all(any(bin(x & cb).count("1") & 1 for x in M) for M in Ms)
        out.write(json.dumps({"c": c, "confere": okc, "t": round(time.time() - t0, 1)}) + "\n"); out.flush()
        print(q, "ok", okc, round(time.time() - t0, 1), flush=True)
    else:
        print(q, "UNSAT com suposicoes", flush=True)
