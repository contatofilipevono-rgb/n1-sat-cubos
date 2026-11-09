"""(09/11) Consequencias de I6 que so envolvem C3 (simples e produtos C3xC3), por eliminacao gaussiana
(colunas de R e produtos com R sao eliminadas primeiro). Depois: cobertura restrita (CMS, produtos = AND)."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
from analisa_testemunhas import contexto
from fecho_estrela import linhas
import pycryptosat


def consequencias(classe):
    w1, w2, ny = so.pencil(so.classes()[classe])
    fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
    zerar = set(so.pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    P = so.Pares(fixo, incog)
    c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    c3pos = {var: p for p, (m, var) in enumerate(c3v)}
    nc = len(c3v)
    # colunas baixas: C3 simples (0..nc-1), depois produtos C3xC3; altas: o resto
    baixas = {}
    for p in range(nc):
        baixas[("s", p)] = p
    q = nc
    for (i, j) in P.D2:
        if (i + 1) in c3pos and (j + 1) in c3pos:
            a, b = sorted((c3pos[i + 1], c3pos[j + 1]))
            if ("q", a, b) not in baixas:
                baixas[("q", a, b)] = q; q += 1
    NB = q
    altas = {}
    prox = NB
    def col(ch):
        nonlocal prox
        if ch in baixas:
            return baixas[ch]
        if ch not in altas:
            altas[ch] = prox; prox += 1
        return altas[ch]
    nb = len(P.alvos)
    eqs = [0] * nb
    def add(v, c):
        h = 0
        while v:
            if v & 1:
                eqs[h] ^= 1 << c
            v >>= 1; h += 1
    for k, v in enumerate(P.D1):
        add(v, col(("s", c3pos[k + 1])) if (k + 1) in c3pos else col(("x", k + 1)))
    for (i, j), v in P.D2.items():
        if (i + 1) in c3pos and (j + 1) in c3pos:
            a, b = sorted((c3pos[i + 1], c3pos[j + 1]))
            add(v, col(("q", a, b)))
        else:
            add(v, col(("p", i, j)))
    TOP = prox + 1
    eqs = [e | (((P.F0 >> h) & 1) << TOP) for h, e in enumerate(eqs)]
    piv = {}
    for e in eqs:
        while e & ((1 << TOP) - 1):
            h = (e & ((1 << TOP) - 1)).bit_length() - 1
            if h in piv:
                e ^= piv[h]
            else:
                piv[h] = e
                break
        if not (e & ((1 << TOP) - 1)) and (e >> TOP) & 1:
            raise SystemExit("inconsistente")
    res = [e for h, e in piv.items() if h < NB]
    inv = {v: k for k, v in baixas.items()}
    return res, nc, NB, TOP, inv


def cobertura(classe, res, nc, NB, TOP, inv):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    Ms = [linhas(*d) for d in dados]
    s = pycryptosat.Solver()
    # variaveis: C3 em 1..nc; produtos (q) em variaveis novas = AND
    vq = {}
    prox = nc + 1
    for c in range(nc, NB):
        _, a, b = inv[c]
        vq[c] = prox
        s.add_clause([-prox, a + 1]); s.add_clause([-prox, b + 1]); s.add_clause([prox, -(a + 1), -(b + 1)])
        prox += 1
    for e in res:
        vs = [(c + 1) if c < nc else vq[c] for c in range(NB) if (e >> c) & 1]
        s.add_xor_clause(vs, bool((e >> TOP) & 1))
    for M in Ms:
        auxs = []
        for r in M:
            s.add_xor_clause([p + 1 for p in range(nc) if (r >> p) & 1] + [prox], False)
            auxs.append(prox); prox += 1
        s.add_clause(auxs)
    t0 = time.time()
    r, sol = s.solve()
    out = {"classe": classe, "consequencias": len(res), "lineares": sum(1 for e in res if not (e & (((1 << NB) - 1) ^ ((1 << nc) - 1)))),
           "SAT": r, "tempo_s": round(time.time() - t0, 1)}
    if r:
        out["c"] = [p for p in range(nc) if sol[p + 1]]
    return out


if __name__ == "__main__":
    classe = os.environ.get("CLASSE", "Q4a")
    res, nc, NB, TOP, inv = consequencias(classe)
    print(f"{classe}: colunas C3-simples {nc}, produtos C3xC3 {NB - nc}; consequencias so em C3: {len(res)}", flush=True)
    out = cobertura(classe, res, nc, NB, TOP, inv)
    print(json.dumps(out), flush=True)
    nome = classe.replace("^", "").replace("+", "")
    json.dump(out, open(f"cobertura_quad_{nome}.json", "w"))
