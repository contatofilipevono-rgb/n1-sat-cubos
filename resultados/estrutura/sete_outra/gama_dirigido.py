"""(10/11) Busca EXATA dirigida pelo grau 8 completo de I6 (caso misto, F4+F4).
Para um par (a,b) em N com a+b em N e beta(a,b)=0, e cada A12 com T∧A12 = phi_a∧phi_b (A12 percorre solução
particular + núcleo de T∧ em Λ²), as condições restantes do grau 8 são LINEARES em (x ∈ F2^40 [phi3 = anf(x)], A13, A23, B):
    T∧A13 = phi_a∧phi3,  T∧A23 = phi_b∧phi3,  T∧B + phi_a∧A23 + phi_b∧A13 + phi3∧A12 = 0.
Projeta o núcleo em x -> subespaço P; enumera P inteiro e testa c, c+a, c+b, c+a+b em N.
Achado = trio com grau 8 de I6 satisfeito e as 7 combinações sem isotrópico (candidato sério ao caso misto).
Uso: python gama_dirigido.py NPARES SEED"""
import sys, time, json, itertools
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
from sete_beta import anf, beta, em_N, T, L3, elim
from gama_massey import wedge, cub, DOIS, UM, nucleo_beta, soluvel

def wv(P, Q): return wedge(P, Q)
CUBX = [cub(anf(1 << k)) for k in range(40)]  # phi de cada vetor da base de L/G

def nucleo_int(cols, nvar):
    """núcleo do sistema homogêneo sum_j v_j cols[j] = 0; retorna base (ints sobre nvar bits)."""
    piv = {}  # h -> (col combinada, combinação de variáveis)
    base = []
    for j, c in enumerate(cols):
        comb = 1 << j
        while c:
            h = c.bit_length() - 1
            if h in piv:
                c ^= piv[h][0]; comb ^= piv[h][1]
            else:
                piv[h] = (c, comb); break
        if not c: base.append(comb)
    return base

def amostra_N(rng, gera, tent=4000):
    for _ in range(tent):
        xs = np.array([gera() for _ in range(256)], dtype=np.uint64)
        m = em_N(xs)
        if m.any(): return int(xs[np.nonzero(m)[0][0]])
    return None

B40 = None
def base_nucleo_beta(a):
    """base de {x: beta(a,x)=0} (subespaço de F2^40)."""
    fa = anf(a)
    linhas = [sum(beta(fa, anf(1 << j))[k] << j for j in range(40)) for k in range(10)]
    piv = {}
    for v in linhas:
        for h in sorted(piv, reverse=True):
            if v >> h & 1: v ^= piv[h]
        if v:
            h = v.bit_length() - 1
            for h2 in list(piv):
                if piv[h2] >> h & 1: piv[h2] ^= v
            piv[h] = v
    base = []
    for f in [j for j in range(40) if j not in piv]:
        w = 1 << f
        for h, v in piv.items():
            if v >> f & 1: w |= 1 << h
        base.append(w)
    return base

def solucoes_A12(pa, pb):
    cols = [wedge(T, [q]) for q in DOIS]
    rhs = wedge(pa, pb)
    # solução particular + núcleo
    piv = {}
    for j, c in enumerate(cols):
        comb = 1 << j
        while c:
            h = c.bit_length() - 1
            if h in piv: c ^= piv[h][0]; comb ^= piv[h][1]
            else: piv[h] = (c, comb); break
    r, sol = rhs, 0
    while r:
        h = r.bit_length() - 1
        if h not in piv: return None, None
        r ^= piv[h][0]; sol ^= piv[h][1]
    ker = nucleo_int(cols, 28)
    A = lambda s: [DOIS[k] for k in range(28) if s >> k & 1]
    return A(sol), [A(k) for k in ker]

def espaco_phi3(pa, pb, A12):
    # variáveis: x (40) | A13 (28) | A23 (28) | B (8); equações em blocos de 256 bits: E13 (Λ⁶), E23 (Λ⁶), E123 (Λ⁵)
    bl = lambda v, k: v << (256 * k)
    cols = []
    for k in range(40):
        p3 = CUBX[k]
        cols.append(bl(wedge(pa, p3), 0) ^ bl(wedge(pb, p3), 1) ^ bl(wedge(p3, A12), 2))
    for q in DOIS: cols.append(bl(wedge(T, [q]), 0) ^ bl(wedge(pb, [q]), 2))   # A13: T∧A13 em E13; phi_b∧A13 em E123
    for q in DOIS: cols.append(bl(wedge(T, [q]), 1) ^ bl(wedge(pa, [q]), 2))   # A23
    for q in UM:   cols.append(bl(wedge(T, [q]), 2))                           # B
    ker = nucleo_int(cols, len(cols))
    proj = [v & ((1 << 40) - 1) for v in ker]
    return elim(proj, 40)

if __name__ == "__main__":
    NP, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    r40 = lambda: int(rng.integers(1, 1 << 40, dtype=np.uint64))
    achados = []; stats = []; t0 = time.time()
    for par in range(NP):
        a = amostra_N(rng, r40)
        if a is None: continue
        BA = base_nucleo_beta(a)
        b = None
        for _ in range(400):
            sel = rng.integers(0, 2, (4096, len(BA))).astype(bool)
            Bm = np.array([[(v >> j) & 1 for j in range(40)] for v in BA], dtype=np.int64)
            bitsx = (sel.astype(np.int64) @ Bm) % 2
            xs = (bitsx.astype(np.uint64) << np.arange(40, dtype=np.uint64)[None, :]).sum(axis=1).astype(np.uint64)
            m = em_N(xs)
            cand = xs[m]
            if len(cand):
                ok = em_N(cand ^ np.uint64(a))
                cand = [int(v) for v in cand[ok] if int(v) not in (0, a)]
                if cand: b = cand[0]; break
        if b is None: continue
        pa, pb = cub(anf(a)), cub(anf(b))
        A0, KER = solucoes_A12(pa, pb)
        assert A0 is not None  # beta=0 garante solução
        # A12 = A0 + combinação do núcleo (dim 10); percorre todas (2^10)
        melhor = 0
        for s in range(1 << len(KER)):
            A12 = set(A0)
            for k in range(len(KER)):
                if s >> k & 1: A12 ^= set(KER[k])
            P = espaco_phi3(pa, pb, sorted(A12))
            d = len(P)
            if d > 24: raise SystemExit(f"dim P = {d} grande demais")
            # enumera P
            xs = np.zeros(1 << d, dtype=np.uint64)
            for k, v in enumerate(P): xs[(np.arange(1 << d) >> k) & 1 == 1] ^= np.uint64(v)
            vivo = xs[em_N(xs)]
            for sh in (a, b, a ^ b):
                if len(vivo): vivo = vivo[em_N(vivo ^ np.uint64(sh))]
            vivo = [int(v) for v in vivo if int(v) not in (0, a, b, a ^ b)]
            melhor = max(melhor, d)
            if vivo:
                achados.append({"a": a, "b": b, "A12": sorted(A12), "c": vivo[:5]})
                print("ACHADO", achados[-1], flush=True)
                break
        stats.append(melhor)
        print(f"par {par}: dim max P = {melhor}, achados acumulados {len(achados)} ({time.time()-t0:.0f}s)", flush=True)
    json.dump({"seed": seed, "pares": len(stats), "dimP": stats, "achados": achados},
              open(f"gama_dirigido_seed{seed}.json", "w"), indent=1)
    print("FIM pares", len(stats), "achados", len(achados))
