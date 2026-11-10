"""(10/11) Obstrução secundária do caso misto (Lema L, F4+F4).
Para phi1,phi2,phi3 em L (phi∧T=0) com beta=0 dois a dois, o grau 8 de I6 é o sistema LINEAR em (A12,A13,A23 ∈ Λ², B ∈ Λ¹):
    T∧A_ij = phi_i∧phi_j   (Λ⁶),        T∧B + phi1∧A23 + phi2∧A13 + phi3∧A12 = 0   (Λ⁵).
gamma(phi) := [sistema insolúvel]  (produto triplo tipo Massey).  Os certificados de paridade dos 4 trios conhecidos usam
só essas equações.  Pergunta: gamma=0 (solúvel) ⇒ alguma das 7 combinações tem subespaço isotrópico (não está em N)?
Uso: python gama_massey.py NTRIOS SEED"""
import sys, itertools, time, json
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
from sete_beta import anf, beta, em_N, T, L3, elim
from collections import Counter

pc = lambda x: bin(x).count("1")
UM = [1 << i for i in range(8)]
DOIS = [m for m in range(256) if pc(m) == 2]
idx = {}
def coord(m):  # índice global de monômio em y (por grau)
    return m
def wedge(A, B):
    out = 0
    for a in A:
        for b in B:
            if not (a & b): out ^= 1 << (a | b)
    return out  # bitset sobre 256 monômios
def cub(x56):
    return [L3[k] for k in range(56) if x56 >> k & 1]

# colunas (incógnitas): A12 (28), A13 (28), A23 (28), B (8) -> 92
def sistema(ph):
    p1, p2, p3 = ph
    cols, rhs = [], 0
    # cada coluna = vetor de equações; equações indexadas em blocos: E12 (Λ⁶ 256 bits), E13, E23, E123 (Λ⁵)
    def bloco(v, k): return v << (256 * k)
    for q in DOIS: cols.append(bloco(wedge(T, [q]), 0) ^ bloco(wedge(p3, [q]), 3))   # A12: T∧A12 em E12; phi3∧A12 em E123
    for q in DOIS: cols.append(bloco(wedge(T, [q]), 1) ^ bloco(wedge(p2, [q]), 3))   # A13
    for q in DOIS: cols.append(bloco(wedge(T, [q]), 2) ^ bloco(wedge(p1, [q]), 3))   # A23
    for q in UM:   cols.append(bloco(wedge(T, [q]), 3))                              # B
    rhs = bloco(wedge(p1, p2), 0) ^ bloco(wedge(p1, p3), 1) ^ bloco(wedge(p2, p3), 2)
    return cols, rhs
def soluvel(cols, rhs):
    piv = {}
    for c in cols:
        while c:
            h = c.bit_length() - 1
            if h in piv: c ^= piv[h]
            else: piv[h] = c; break
    r = rhs
    while r:
        h = r.bit_length() - 1
        if h not in piv: return False
        r ^= piv[h]
    return True
def beta_zero(a, b): return not any(beta(anf(a), anf(b)))

def nucleo_beta(fixos, rng):
    """vetor aleatório x em F2^40 com beta(f,x)=0 para todo f em fixos (condições lineares em x)."""
    linhas = []
    for f in fixos:
        fa = anf(f)
        for k in range(10):
            linhas.append(sum(beta(fa, anf(1 << j))[k] << j for j in range(40)))
    # núcleo
    piv = {}
    for v in linhas:
        for h in sorted(piv, reverse=True):
            if v >> h & 1: v ^= piv[h]
        if v:
            h = v.bit_length() - 1
            for h2 in list(piv):
                if piv[h2] >> h & 1: piv[h2] ^= v
            piv[h] = v
    livres = [j for j in range(40) if j not in piv]
    base = []
    for f in livres:
        w = 1 << f
        for h, v in piv.items():
            if v >> f & 1: w |= 1 << h
        base.append(w)
    x = 0
    for b in base:
        if rng.random() < .5: x ^= b
    return x, len(base)

if __name__ == "__main__":
    NT, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    # controles: os 4 trios conhecidos devem dar gamma insolúvel
    ctrl = []
    for i in range(3):
        ph = json.load(open(fr"..\trios_beta2_seed111\trio{i}.json"))["phi"]
        ctrl.append(soluvel(*sistema(ph)))
    print("controle (3 trios seed111, esperado False):", ctrl, flush=True)
    cont = Counter(); t0 = time.time(); exemplos = []
    for t in range(NT):
        a = int(rng.integers(1, 1 << 40, dtype=np.uint64))
        b, _ = nucleo_beta([a], rng)
        c, dimc = nucleo_beta([a, b], rng)
        if not (a and b and c) or len(elim([a, b, c], 40)) < 3: continue
        assert beta_zero(a, b) and beta_zero(a, c) and beta_zero(b, c)
        combs = [a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c]
        nN = int(em_N(np.array(combs, dtype=np.uint64)).sum())
        ph = [cub(anf(a)), cub(anf(b)), cub(anf(c))]
        g = soluvel(*sistema(ph))
        cont[(g, nN)] += 1
        if g and nN == 7: exemplos.append([a, b, c])
        if (t + 1) % 200 == 0: print(t + 1, dict(sorted(cont.items())), f"{time.time()-t0:.0f}s", flush=True)
    print("FIM (gamma_soluvel, #combinacoes em N): contagem", dict(sorted(cont.items())))
    print("CONTRAEXEMPLOS a 'gamma=0 => algum isotropico':", len(exemplos), exemplos[:5])
