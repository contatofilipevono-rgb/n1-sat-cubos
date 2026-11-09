"""(09/11) Queda de grau em codim <= 5 para Q = T + x1 phi1 + x2 phi2 + x3 phi3 em F2^11 (y0..y7 = bits 0..7, x1..x3 = bits 8..10).
Basta codim 5 exata (subespacos de dim 6; codim menor contem codim 5 com queda). Seja k = dim da projecao de U em X = <x1,x2,x3>.
 k=0: U ⊂ Y, dim 6: impossivel para T critico (testado aqui tambem por completude se FULL=1).
 k=1: as 7 restricoes (U_Y dim 5 + 1 direcao) -- incluido para controle.
 k=2: U = U_Y (dim 4) + <p1+u1, p2+u2>, P=<p1,p2> 2-subespaco de X (7), u_i em Y/U_Y.
 k=3: U = U_Y (dim 3) + <x1+u1, x2+u2, x3+u3>, u_i em Y/U_Y; poda: cada sub-U de dim 4 e 5 tambem precisa de queda.
Teste de queda: deg(Q|U) <= 3 via Mobius na restricao (64 pontos para dim 6)."""
import sys, json, re, itertools, time, os
import numpy as np
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so

NB = 11


def tabela(monos, n=NB):
    pts = np.arange(1 << n, dtype=np.int64)
    tt = np.zeros(1 << n, dtype=np.uint8)
    for m in monos:
        tt ^= ((pts & m) == m).astype(np.uint8)
    return tt


def grau_max_lote(tt, B):
    """B: (lote, d) bases (inteiros de NB bits). Retorna array bool: grau da restricao >= 4 (sem queda)."""
    lote, d = B.shape
    T = ((np.arange(1 << d)[:, None] >> np.arange(d)[None, :]) & 1).astype(np.int64)
    P = np.zeros((lote, 1 << d), dtype=np.int64)
    for i in range(d):
        P ^= T[:, i][None, :] * B[:, i][:, None]
    a = tt[P].copy()
    h = 1
    while h < (1 << d):
        a = a.reshape(lote, -1, 2, h); a[:, :, 1, :] ^= a[:, :, 0, :]; a = a.reshape(lote, 1 << d); h *= 2
    pop = np.array([bin(i).count("1") for i in range(1 << d)])
    return (a[:, pop >= 4] != 0).any(axis=1)


def subespacos(n, d):
    """bases RREF (d vetores de n bits) de todos os subespacos de dim d de F2^n."""
    out = []
    for P in itertools.combinations(range(n), d):
        livres = [(r, c) for r in range(d) for c in range(P[r] + 1, n) if c not in P]
        for bits in range(1 << len(livres)):
            B = [1 << p for p in P]
            for k, (r, c) in enumerate(livres):
                if (bits >> k) & 1:
                    B[r] |= 1 << c
            out.append(B)
    return np.array(out, dtype=np.int64)


def complemento(Bv, n=8):
    """representantes de F2^n / span(Bv) (inclui 0)."""
    span = {0}
    for b in Bv:
        span |= {s ^ b for s in span}
    reps, vistos = [], set()
    for v in range(1 << n):
        if v not in vistos:
            reps.append(v)
            vistos |= {v ^ s for s in span}
    return reps


def busca(Q, log=print):
    tt = tabela(Q)
    res = {}
    X = [1 << 8, 1 << 9, 1 << 10]
    Xv = [a ^ b ^ c for a, b, c in itertools.product((0, X[0]), (0, X[1]), (0, X[2]))]
    Xv = [v for v in Xv if v]
    # k=1 (controle): U_Y dim 5 + p+u
    t0 = time.time()
    S5 = subespacos(8, 5)
    semq5 = grau_max_lote(tt, S5)  # T|U_Y (x=0) tem grau >=4 ?
    iso5 = S5[~semq5]
    n1 = 0
    for B in iso5:
        reps = complemento(list(B))
        lote = np.array([list(B) + [p ^ u] for p in Xv for u in reps], dtype=np.int64)
        n1 += int((~grau_max_lote(tt, lote)).sum())
    res["k1"] = n1
    log(f"k=1: U_Y isotropicos de T: {len(iso5)}; subespacos com queda: {n1} ({time.time()-t0:.0f}s)")
    # k=2
    t0 = time.time()
    S4 = subespacos(8, 4)
    semq4 = grau_max_lote(tt, S4)
    iso4 = S4[~semq4]
    planos = [(a, b) for a, b in itertools.combinations(Xv, 2) if a < b and (a ^ b) not in (a, b)]
    pl = []
    for a, b in planos:
        s = frozenset({a, b, a ^ b})
        if s not in [frozenset({c, d, c ^ d}) for c, d in pl]:
            pl.append((a, b))
    n2 = 0
    for B in iso4:
        reps = complemento(list(B))
        Bl = list(B)
        for (p1, p2) in pl:
            # poda: direcoes individuais (dim 5) precisam de queda
            l1 = np.array([Bl + [p1 ^ u] for u in reps], dtype=np.int64)
            ok1 = [reps[i] for i in np.where(~grau_max_lote(tt, l1))[0]]
            if not ok1:
                continue
            l2 = np.array([Bl + [p2 ^ u] for u in reps], dtype=np.int64)
            ok2 = [reps[i] for i in np.where(~grau_max_lote(tt, l2))[0]]
            if not ok2:
                continue
            lote = np.array([Bl + [p1 ^ u1, p2 ^ u2] for u1 in ok1 for u2 in ok2], dtype=np.int64)
            n2 += int((~grau_max_lote(tt, lote)).sum())
    res["k2"] = n2
    log(f"k=2: U_Y dim4 com T de grau<=3: {len(iso4)}; subespacos com queda: {n2} ({time.time()-t0:.0f}s)")
    # k=3
    t0 = time.time()
    S3 = subespacos(8, 3)
    n3 = 0
    for idx, B in enumerate(S3):
        Bl = list(B)
        reps = complemento(Bl)
        oks = []
        for p in X:
            l = np.array([Bl + [p ^ u] for u in reps], dtype=np.int64)
            oks.append([reps[i] for i in np.where(~grau_max_lote(tt, l))[0]])
        if not all(oks):
            continue
        # pares (dim 5)
        par12 = [(u1, u2) for u1 in oks[0] for u2 in oks[1]]
        l = np.array([Bl + [X[0] ^ u1, X[1] ^ u2] for u1, u2 in par12], dtype=np.int64)
        par12 = [par12[i] for i in np.where(~grau_max_lote(tt, l))[0]]
        if not par12:
            continue
        cand = [(u1, u2, u3) for (u1, u2) in par12 for u3 in oks[2]]
        l = np.array([Bl + [X[0] ^ a, X[1] ^ b, X[2] ^ c] for a, b, c in cand], dtype=np.int64)
        n3 += int((~grau_max_lote(tt, l)).sum())
        if idx % 10000 == 0:
            log(f"   k=3: {idx}/{len(S3)} U_Y, achados {n3} ({time.time()-t0:.0f}s)")
    res["k3"] = n3
    log(f"k=3: U_Y dim 3: {len(S3)}; subespacos com queda: {n3} ({time.time()-t0:.0f}s)")
    return res


def parse(s):
    out = set()
    for termo in s.split("+"):
        out ^= {sum(1 << int(d) for d in re.findall(r"y(\d)", termo))}
    return out


if __name__ == "__main__":
    w1, w2, ny = so.pencil(so.classes()["F4+F4"])
    _, _, _, Tq = so.modelo_nove(w1, w2, ny)
    T = set(Tq)
    modo = os.environ.get("MODO", "trio")
    if modo == "controle":
        # controle positivo: phi_i = iota_{u_i} T (gauge puro) -> queda garantida em toda parte
        def iota(u):
            out = set()
            for t in T:
                for i in range(8):
                    if (u >> i) & 1 and (t >> i) & 1:
                        out ^= {t ^ (1 << i)}
            return out
        phis = [iota(1), iota(2), iota(4)]
    else:
        tr = json.load(open(os.environ.get("TRIO", r"C:\Users\Valer\Downloads\analise adversarial\sete_restricoes_09nov\trio_s22_seed1.json")))["trios"][int(os.environ.get("IDX", 0))]
        phis = [parse(s) for s in tr["phi"]]
    Q = set(T)
    for i, ph in enumerate(phis):
        Q ^= {m | (1 << (8 + i)) for m in ph}
    r = busca(Q)
    print(json.dumps({"modo": modo, **r}))
