"""Estrutura da orbita 255 de U_Y isotropicos (Q4) e das testemunhas [15,0,0] (09/11)."""
import glob, json, os, sys
from collections import Counter
sys.argv = ["x"]
from analisa_testemunhas import contexto, rows_U, span, popc
from sat_n1_cegar import isotropico_em

BASE = r"C:\Users\Valer\Downloads\analise adversarial"


def isos(classe, monos):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    s = set(monos)
    val = [False] * (len(incog) + 2)
    for k, m in enumerate(incog):
        val[k + 1] = m in s
    return [k for k in range(len(iso)) if isotropico_em(val, *dados[k])]


def dimset(S):
    return len(S).bit_length() - 1


def estudo_orbita(classe):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    o = sorted(orbs[0])
    sps = {k: frozenset(span(rows_U(iso[k]))) for k in o}
    cont = Counter()
    for k in o:
        for v in sps[k]:
            if v:
                cont[v] += 1
    # quantos U da orbita 255 contem cada vetor
    print(classe, "orbita", len(o), "| distribuicao 'v em quantos U':", Counter(cont.values()))
    # intersecoes duas a duas
    inter = Counter()
    for i, a in enumerate(o):
        for b in o[i + 1:]:
            inter[dimset(sps[a] & sps[b])] += 1
    print("   dim intersecao 2 a 2:", dict(inter))
    return o, sps


def main():
    out = {}
    for classe, pastas in [("Q4b", ["gh_42521672988"]), ("Q4c", ["gh_42521679875"]), ("Q4a", ["gh_42521666326"])]:
        o, sps = estudo_orbita(classe)
        so = set(o)
        for p in pastas:
            for f in sorted(glob.glob(os.path.join(BASE, "q1_nuvem_08nov", p, "**", "cubo_*.json"), recursive=True)):
                r = json.load(open(f))
                if r["resultado"] != "SAT":
                    continue
                viol = isos(classe, r["conferencia"]["anf_extra"])
                if not set(viol) <= so:
                    continue
                S = [sps[k] for k in viol]
                comum = frozenset.intersection(*S)
                soma = set()
                for sp in S:
                    soma |= sp
                # subespaco gerado pela uniao
                ger = span([v for v in soma if v])
                inter = Counter(dimset(a & b) for i, a in enumerate(S) for b in S[i + 1:])
                cont = Counter(v for sp in S for v in sp if v)
                top = Counter(cont.values())
                print(f"  {classe} cubo {r['cubo']}: n={len(viol)} dim(comum)={dimset(comum)} dim(soma)={dimset(ger)} inter2a2={dict(inter)} mult={dict(top)}")
                out[f"{classe}_{r['cubo']}"] = {"viol": viol, "dim_comum": dimset(comum), "inter": dict(inter)}
    json.dump(out, open(os.path.join(BASE, "q1_estrutura_09nov", "feixe_255.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
