"""(10/11) Confere a redução do Fable: G(z)=g(z,z) tem ANF b_{S'} = a_{S' ∪ (S'+m)} (Lema 1), e (C) ⇔ D_1 G ≡ m,
sistema linear nos b (G RS em m variáveis, grau <= floor(m/2)).  Imprime as condições para m=4..7."""
import itertools, sys, random
sys.stdout.reconfigure(encoding="utf-8")
def orbitas(m, dmax):
    M = 1 << m; rot = lambda q: ((q << 1) | (q >> (m - 1))) & (M - 1)
    out, vis = [], set()
    for d in range(1, dmax + 1):
        for c in itertools.combinations(range(m), d):
            q = sum(1 << i for i in c)
            if q in vis: continue
            o = {q}; x = q
            for _ in range(m): x = rot(x); o.add(x)
            vis |= o; out.append(sorted(o))
    return out
def anf_de_tabela(t, m):
    a = list(t); h = 1
    while h < len(a):
        for i in range(len(a)):
            if i & h: a[i] ^= a[i ^ h]
        h <<= 1
    return a
for m in range(4, 8):
    M = 1 << m; O = orbitas(m, m // 2)
    # coluna de cada órbita: tabela de D_1 G
    cols = []
    for o in O:
        t = [sum(((x & q) == q) for q in o) & 1 for x in range(M)]
        cols.append([t[x] ^ t[x ^ (M - 1)] for x in range(M)])
    # D_1 G = soma b_o * cols[o]; deve ser a constante m mod 2. Escrever como sistema: para cada x, Σ b_o cols[o][x] = m.
    # eliminação: representar cada linha x como bitmask das órbitas
    linhas = {}
    for x in range(M):
        r = sum(cols[k][x] << k for k in range(len(O))) | ((m % 2) << len(O))  # bit extra = lado direito
        linhas.setdefault(r, x)
    # base reduzida
    base = []
    for r in linhas:
        for b in base:
            if r ^ b < r: r ^= b
        if r:
            base.append(r); base.sort(reverse=True)
    nome = lambda o: "{" + ",".join(str(i) for i in range(m) if (o[0] >> i) & 1) + "}"
    # normaliza: escrever cada relação como soma de b's
    rel = []
    for r in base:
        rel.append(" + ".join(f"b{nome(O[k])}" for k in range(len(O)) if (r >> k) & 1) + f" = {(r >> len(O)) & 1}")
    print(f"m={m} (n={2*m}): órbitas de grau ≤{m//2}: {len(O)}; relações independentes (= m mod 2 = {m%2}): {len(base)}")
    for s in rel: print("   ", s)
# conferência do Lema 1 em RS aleatórias de n=8, 12 (grau <= m)
for n in (8, 12):
    m = n // 2; N = 1 << n
    Og = orbitas(n, m)
    for _ in range(3):
        a = {q: 0 for o in Og for q in o}
        for o in Og:
            c = random.getrandbits(1)
            for q in o: a[q] = c
        t = [sum(c for q, c in a.items() if c and (x & q) == q) & 1 for x in [z | (z << m) for z in range(1 << m)]]
        anfG = anf_de_tabela(t, m)
        esperado = [a.get(s | (s << m), 0) if s else None for s in range(1 << m)]
        ok = all(anfG[s] == esperado[s] for s in range(1, 1 << m))
        print(f"Lema 1, n={n}: ANF de G = b_S' ? {ok}")
