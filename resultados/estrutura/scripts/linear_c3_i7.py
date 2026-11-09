"""(09/11) Relaxacao linear de I6 ∧ I7 sobre C3.
Representacao: cada equacao e um polinomio booleano nas incognitas (termos = frozenset de variaveis; frozenset() = 1).
 - I6 (todas as |S|>=6): N2(S) = 0 mod 2  (pares de monomios com uniao S).
 - I7 nos S com |S| in {8, 9} (exata): N2 = 2 N3 mod 4  <=>  [N2 par] e  e2(pares) + N3 = 0 mod 2,
   onde e2(pares) = sum_{i<j} p_i p_j (bit 1 da contagem, dado N2 par) e N3 = paridade das triplas com uniao S.
   (Os S com |S| = 7 ficam de fora: o bit 1 tem muitos termos; a relaxacao fica valida, so mais fraca.)
Eliminacao gaussiana: colunas = monomios nas incognitas; ficam por ultimo as variaveis simples de C3 e a constante.
Saida: restricoes lineares (afins) sobre C3 implicadas por I6 ∧ I7(|S|>=8)."""
import os, sys, json
from itertools import combinations
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so


def popc(x):
    return bin(x).count("1")


def modelo(classe):
    w1, w2, ny = so.pencil(so.classes()[classe])
    fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
    zerar = set(so.pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    return fixo, incog, c3v, ny


def equacoes(classe, com_i7=True):
    fixo, incog, c3v, ny = modelo(classe)
    nb = ny + 1
    univ = [(m, frozenset()) for m in sorted(set(fixo))] + [(m, frozenset([k + 1])) for k, m in enumerate(incog)]
    n = len(univ)
    pares = {}
    for a, b in combinations(range(n), 2):
        u = univ[a][0] | univ[b][0]
        if popc(u) >= 6:
            pares.setdefault(u, []).append(univ[a][1] | univ[b][1])
    eqs = []
    def soma(termos):
        e = {}
        for t in termos:
            e[t] = e.get(t, 0) ^ 1
        return frozenset(t for t, c in e.items() if c)
    for S, ps in pares.items():
        eqs.append(soma(ps))  # I6: N2(S) par
    if com_i7:
        triplas = {}
        SMIN = int(os.environ.get("SMIN", 8))
        for a, b in combinations(range(n), 2):
            uab = univ[a][0] | univ[b][0]
            if popc(uab) + 4 < SMIN:
                continue
            for c in range(b + 1, n):
                u = uab | univ[c][0]
                if popc(u) >= SMIN:
                    triplas.setdefault(u, []).append(univ[a][1] | univ[b][1] | univ[c][1])
        for S in range(1 << nb):
            if popc(S) < SMIN:
                continue
            ps = pares.get(S, [])
            e2 = [ps[i] | ps[j] for i, j in combinations(range(len(ps)), 2)]
            eqs.append(soma(e2 + triplas.get(S, [])))
    return [e for e in eqs if e], c3v


def restricoes(classe, com_i7=True):
    eqs, c3v = equacoes(classe, com_i7)
    c3set = {var: p for p, (m, var) in enumerate(c3v)}
    nc = len(c3v)
    # colunas: 0 = constante; 1..nc = C3 simples (ordem p); demais acima
    col = {frozenset(): 0}
    for var, p in c3set.items():
        col[frozenset([var])] = p + 1
    prox = nc + 1
    linhas = []
    for e in eqs:
        r = 0
        for t in e:
            if t not in col:
                col[t] = prox; prox += 1
            r ^= 1 << col[t]
        linhas.append(r)
    piv = {}
    inconsist = False
    for r in linhas:
        while r:
            h = r.bit_length() - 1
            if h in piv:
                r ^= piv[h]
            else:
                piv[h] = r
                break
        if r == 1:
            inconsist = True
    lin = [r for h, r in piv.items() if 1 <= h <= nc]
    return lin, nc, c3v, inconsist, len(col)


if __name__ == "__main__":
    for classe in os.environ.get("CLASSES", "F4+F4,F4^2,Q4a,Q4b,Q4c").split(","):
        l6, nc, _, i6, _ = restricoes(classe, False)
        l7, nc, c3v, i7, ncol = restricoes(classe, True)
        print(f"{classe}: so I6 -> {len(l6)} restricoes; I6+I7(|S|>=8) -> {len(l7)} restricoes "
              f"(inconsistente: {i7}; colunas {ncol})", flush=True)
        nome = classe.replace("^", "").replace("+", "")
        json.dump({"classe": classe, "nc": nc, "restricoes": [[p for p in range(nc) if (r >> (p + 1)) & 1] + [r & 1] for r in l7]},
                  open(f"linear_i7_{nome}.json", "w"))
