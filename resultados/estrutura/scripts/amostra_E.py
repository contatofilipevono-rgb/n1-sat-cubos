"""(09/11) Amostra o conjunto E = {C3 extensiveis a I6} (classe dada): CMS no modelo completo, com suposicoes
aleatorias em K bits de C3 (diversidade) e limite de tempo. Grava C3 e a ANF completa (para conferencia de I6)."""
import os, sys, json, time, random
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
import pycryptosat

classe = os.environ.get("CLASSE", "Q4a")
SEM = int(os.environ.get("SEMENTE", 1)); K = int(os.environ.get("K", 14)); N = int(os.environ.get("N", 400))
TL = float(os.environ.get("TL", 60))
rnd = random.Random(SEM)
w1, w2, ny = so.pencil(so.classes()[classe])
fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
zerar = set(so.pivos_iT(Tq, ny))
incog = [m for m in incog if m not in zerar]
P = so.Pares(fixo, incog)
c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
var_de = [var for (m, var) in c3v]
nc = len(var_de)


def novo():
    s = pycryptosat.Solver(time_limit=TL)
    n = len(incog); prox = n + 1
    termos = [[] for _ in range(len(P.alvos))]
    def add(v, var):
        h = 0
        while v:
            if v & 1: termos[h].append(var)
            v >>= 1; h += 1
    for k, v in enumerate(P.D1):
        add(v, k + 1)
    for (i, j), v in P.D2.items():
        t = prox; prox += 1
        s.add_clause([-t, i + 1]); s.add_clause([-t, j + 1]); s.add_clause([t, -(i + 1), -(j + 1)])
        add(v, t)
    for h, vs in enumerate(termos):
        s.add_xor_clause(vs, bool((P.F0 >> h) & 1))
    s.add_clause(var_de)  # C3 != 0
    return s


out = open(f"E_{classe.replace('^','').replace('+','')}_s{SEM}.jsonl", "a")
s = novo()
feitos = 0
while feitos < N:
    ps = rnd.sample(range(nc), K)
    assum = [var_de[p] * rnd.choice([1, -1]) for p in ps]
    t0 = time.time()
    r, sol = s.solve(assumptions=assum)
    if r is True:
        c = [p for p in range(nc) if sol[var_de[p]]]
        monos = [incog[k] for k in range(len(incog)) if sol[k + 1]]
        out.write(json.dumps({"c": c, "anf_extra": monos, "t": round(time.time() - t0, 1)}) + "\n"); out.flush()
        feitos += 1
    if time.time() - t0 > TL * 0.9:
        s = novo()  # reinicia apos limite
