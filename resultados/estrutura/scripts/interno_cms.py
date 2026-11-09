"""(09/11) Teste interno (C3 fixo) com CryptoMiniSat: XOR nativo + Gauss; produtos R*R como AND.
Uso: CLASSE=Q4a ARQ=cobertura_restrita_Q4a.json python interno_cms.py  (ou CONTROLE=1 para testemunhas)."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
from sat_n1 import confere
import pycryptosat


def interno(classe, c_pos, threads=1):
    w1, w2, ny = so.pencil(so.classes()[classe])
    fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
    zerar = set(so.pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    P = so.Pares(fixo, incog)
    c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    cs = set(c_pos)
    val = {var: (p in cs) for p, (m, var) in enumerate(c3v)}
    s = pycryptosat.Solver(threads=threads)
    n = len(incog)
    prox = n + 1
    nb = len(P.alvos)
    termos = [[] for _ in range(nb)]
    const = P.F0
    def add(v, var):
        nonlocal const
        h = 0
        while v:
            if v & 1:
                if var is None:
                    const ^= 1 << h
                else:
                    termos[h].append(var)
            v >>= 1; h += 1
    for k, v in enumerate(P.D1):
        var = k + 1
        if var in val:
            if val[var]: add(v, None)
        else:
            add(v, var)
    for (i, j), v in P.D2.items():
        a, b = i + 1, j + 1
        if a in val and b in val:
            if val[a] and val[b]: add(v, None)
        elif a in val:
            if val[a]: add(v, b)
        elif b in val:
            if val[b]: add(v, a)
        else:
            t = prox; prox += 1
            s.add_clause([-t, a]); s.add_clause([-t, b]); s.add_clause([t, -a, -b])
            add(v, t)
    for h in range(nb):
        vs = termos[h]
        # cancela repeticoes
        cnt = {}
        for x in vs: cnt[x] = cnt.get(x, 0) ^ 1
        vs = [x for x, c in cnt.items() if c]
        rhs = bool((const >> h) & 1)
        if vs:
            s.add_xor_clause(vs, rhs)
        elif rhs:
            return {"I6_extensivel": False, "motivo": "equacao constante 0=1"}
    for var, b in val.items():
        s.add_clause([var if b else -var])
    t0 = time.time()
    r, sol = s.solve()
    out = {"I6_extensivel": r, "tempo_s": round(time.time() - t0, 1)}
    if r:
        monos = [incog[k] for k in range(n) if sol[k + 1]]
        out["I6_conferido"] = bool(confere(fixo, monos, ny + 1)[0])
        out["anf_extra"] = monos
    return out


if __name__ == "__main__":
    classe = os.environ.get("CLASSE", "Q4a")
    if os.environ.get("CONTROLE"):
        from span_c3 import vetores
        vs, _ = vetores(classe)
        for v in vs[:2]:
            o = interno(classe, [p for p in range(48) if (v >> p) & 1])
            print("controle", {k: o[k] for k in o if k != "anf_extra"}, flush=True)
    else:
        c = json.load(open(os.environ.get("ARQ", "cobertura_restrita_Q4a.json")))["c"]
        o = interno(classe, c, int(os.environ.get("THREADS", 1)))
        print(json.dumps(o)[:800], flush=True)
