"""(09/11) C3 fixo: sistema I6 nas incognitas restantes (R). Produtos C3*R viram lineares em R; C3*C3 constantes;
R*R viram colunas livres. Relaxacao linear consistente? Tambem: posto e numero de colunas."""
import os, sys, json
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so


def relax(classe, c_pos):
    w1, w2, ny = so.pencil(so.classes()[classe])
    fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
    zerar = set(so.pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    P = so.Pares(fixo, incog)
    c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    val = {var: (p in set(c_pos)) for p, (m, var) in enumerate(c3v)}
    col = {}
    def cid(ch):
        if ch not in col:
            col[ch] = len(col)
        return col[ch]
    nb = len(P.alvos)
    eqs = [0] * nb
    const = P.F0
    def add(v, c=None):
        nonlocal const
        h = 0
        while v:
            if v & 1:
                if c is None:
                    const ^= 1 << h
                else:
                    eqs[h] ^= 1 << c
            v >>= 1; h += 1
    for k, v in enumerate(P.D1):
        var = k + 1
        if var in val:
            if val[var]: add(v)
        else:
            add(v, cid(("x", var)))
    for (i, j), v in P.D2.items():
        a, b = i + 1, j + 1
        if a in val and b in val:
            if val[a] and val[b]: add(v)
        elif a in val:
            if val[a]: add(v, cid(("x", b)))
        elif b in val:
            if val[b]: add(v, cid(("x", a)))
        else:
            add(v, cid(("p", a, b)))
    TOP = len(col)
    eqs = [e | (((const >> h) & 1) << TOP) for h, e in enumerate(eqs)]
    piv = {}
    inconsist = False
    for e in eqs:
        while e & ((1 << TOP) - 1):
            h = (e & ((1 << TOP) - 1)).bit_length() - 1
            if h in piv:
                e ^= piv[h]
            else:
                piv[h] = e
                break
        if not (e & ((1 << TOP) - 1)) and (e >> TOP) & 1:
            inconsist = True
    nlin = sum(1 for k in col if k[0] == "x")
    return {"inconsistente": inconsist, "colunas_R_simples": nlin, "colunas_RxR": len(col) - nlin, "posto": len(piv), "equacoes": nb}


if __name__ == "__main__":
    import glob
    classe = "Q4a"
    print("N∩L (cobertura restrita):", relax(classe, json.load(open("cobertura_restrita_Q4a.json"))["c"]))
    print("N fora de L:", relax(classe, json.load(open("cobertura_Q4a.json"))["c"]))
    from span_c3 import vetores
    vs, c3v = vetores(classe)
    for v in vs[:3]:
        print("testemunha (controle, deve ser consistente):", relax(classe, [p for p in range(48) if (v >> p) & 1]))
