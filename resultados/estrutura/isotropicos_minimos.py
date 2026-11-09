"""Estrutura dos U_Y isotropicos das testemunhas de F4+F4 com poucos isotropicos (cubos 28 e 62 do GitHub).
Para cada U_Y (dim 5 em Y=F2^8): dim(U ∩ Y1), dim(U ∩ Y2) com Y1=<e0..e3>, Y2=<e4..e7> (blocos F4 do pencil),
dims das intersecoes duas a duas, dim da soma de todos, e T restrita (posto de forma) para referencia."""
import glob
import json
import os
import sys
from collections import Counter

sys.argv = ["x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analisa_testemunhas import contexto, isotropico_em, rows_U, span, BASE  # noqa: E402


def dim(s):
    return len(s).bit_length() - 1


Y1 = span([1 << i for i in range(4)])
Y2 = span([1 << i for i in range(4, 8)])

fixo, incog, Tq, ny, iso, orbs, dados = contexto("F4+F4")
print("T (F4+F4) monomios:", sorted(Tq))
for f in sorted(glob.glob(os.path.join(BASE, "q1_nuvem_08nov", "gh_F4F4_o012", "**", "cubo_*.json"), recursive=True)):
    r = json.load(open(f))
    if r.get("resultado") != "SAT":
        continue
    s = set(r["conferencia"]["anf_extra"])
    val = [False] * (len(incog) + 2)
    for k, m in enumerate(incog):
        val[k + 1] = m in s
    viol = [k for k in range(len(iso)) if isotropico_em(val, *dados[k])]
    Ss = [span(rows_U(iso[k])) for k in viol]
    print(f"\n== cubo {r['cubo']}: {len(viol)} isotropicos")
    print("  (dim U∩Y1, dim U∩Y2):", Counter((dim(S & Y1), dim(S & Y2)) for S in Ss))
    pares = Counter(dim(Ss[i] & Ss[j]) for i in range(len(Ss)) for j in range(i + 1, len(Ss)))
    print("  dims das intersecoes 2 a 2:", dict(sorted(pares.items())))
    tot = set()
    for S in Ss:
        tot |= S
    print("  dim da soma de todos:", dim(span(sorted(tot)[1:])))
    # vetores que aparecem em muitos U
    cont = Counter(v for S in Ss for v in S if v)
    top = cont.most_common(6)
    print("  vetores mais frequentes (vetor:qtd):", [(bin(v)[2:].zfill(8), c) for v, c in top])
