"""(09/11) XL / Nullstellensatz de grau 3 sobre F2 (aneis booleanos, x^2=x) para o sistema I6 com C3 fixo.
Equacoes: polinomios de grau <=2 nas 112 incognitas de R. Multiplica cada uma por 1 e por cada variavel;
lineariza nos monomios (conjuntos de variaveis); eliminacao gaussiana com o monomio vazio (constante) como ultima coluna.
Se aparece a linha '1 = 0' => sistema sem solucao (certificado algebrico)."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so


def sistema(classe, c_pos):
    w1, w2, ny = so.pencil(so.classes()[classe])
    fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
    zerar = set(so.pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    P = so.Pares(fixo, incog)
    c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    cs = set(c_pos)
    val = {var: (p in cs) for p, (m, var) in enumerate(c3v)}
    livres = sorted(k + 1 for k in range(len(incog)) if (k + 1) not in val)
    ix = {v: i for i, v in enumerate(livres)}
    eqs = [set() for _ in range(len(P.alvos))]  # cada eq: conjunto de monomios (frozenset de indices); frozenset() = 1
    def add(v, mono):
        h = 0
        while v:
            if v & 1: eqs[h] ^= {mono}
            v >>= 1; h += 1
    for h in range(len(P.alvos)):
        if (P.F0 >> h) & 1: eqs[h] ^= {frozenset()}
    for k, v in enumerate(P.D1):
        var = k + 1
        if var in val:
            if val[var]: add(v, frozenset())
        else:
            add(v, frozenset([ix[var]]))
    for (i, j), v in P.D2.items():
        a, b = i + 1, j + 1
        if a in val and b in val:
            if val[a] and val[b]: add(v, frozenset())
        elif a in val:
            if val[a]: add(v, frozenset([ix[b]]))
        elif b in val:
            if val[b]: add(v, frozenset([ix[a]]))
        else:
            add(v, frozenset([ix[a], ix[b]]))
    return [e for e in eqs if e], len(livres)


def xl(eqs, n, grau=3):
    col = {frozenset(): 0}
    def cid(m):
        if m not in col: col[m] = len(col)
        return col[m]
    linhas = []
    mult = [frozenset()] + ([frozenset([i]) for i in range(n)] if grau >= 3 else [])
    for e in eqs:
        for u in mult:
            r = 0
            for m in e:
                r ^= 1 << cid(m | u)
            if r: linhas.append(r)
    # eliminacao: pivo no bit mais alto; constante = bit 0 (eliminado por ultimo)
    piv = {}
    t0 = time.time()
    for k, r in enumerate(linhas):
        while r:
            h = r.bit_length() - 1
            if h in piv:
                r ^= piv[h]
            else:
                piv[h] = r
                break
        if r == 1:
            return {"UNSAT_certificado": True, "linhas": len(linhas), "colunas": len(col), "linha_k": k, "t": round(time.time() - t0, 1)}
    return {"UNSAT_certificado": False, "linhas": len(linhas), "colunas": len(col), "posto": len(piv), "t": round(time.time() - t0, 1)}


if __name__ == "__main__":
    classe = os.environ.get("CLASSE", "Q4a")
    grau = int(os.environ.get("GRAU", 3))
    alvos = []
    if os.environ.get("CONTROLE"):
        from span_c3 import vetores
        vs, _ = vetores(classe)
        alvos = [("testemunha", [p for p in range(48) if (vs[0] >> p) & 1])]
    alvos.append(("N∩L", json.load(open("cobertura_restrita_Q4a.json"))["c"]))
    alvos.append(("N fora de L", json.load(open("cobertura_Q4a.json"))["c"]))
    for nome, c in alvos:
        eqs, n = sistema(classe, c)
        print(nome, f"n={n} eqs={len(eqs)}", xl(eqs, n, grau), flush=True)
