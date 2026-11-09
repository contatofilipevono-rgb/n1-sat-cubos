"""Orbita 255 = estrelas de um espalhamento (spread) de 17 subespacos W de dim 4? (09/11)
Para cada testemunha Q4, distribui os U_Y isotropicos da orbita 255 pelos W, e conta
tambem quantos U das orbitas 1020/2040 contem cada W."""
import glob, json, os, sys
from collections import Counter
from itertools import combinations
sys.argv = ["x"]
from analisa_testemunhas import contexto, rows_U, span
from feixe_255 import isos, dimset

BASE = r"C:\Users\Valer\Downloads\analise adversarial"


def spread(classe):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    o = sorted(orbs[0])
    sps = {k: frozenset(span(rows_U(iso[k]))) for k in range(len(iso))}
    Ws = set()
    for a, b in combinations(o, 2):
        I = sps[a] & sps[b]
        if dimset(I) == 4:
            Ws.add(I)
    Ws = sorted(Ws, key=lambda s: sorted(s))
    # controles: 17 W, disjuntos dois a dois (fora do 0), cobrem Y
    uni = Counter(v for W in Ws for v in W if v)
    assert len(Ws) == 17 and set(uni.values()) == {1} and len(uni) == 255, (len(Ws), Counter(uni.values()))
    # cada U da orbita 255 contem exatamente um W
    for k in o:
        assert sum(1 for W in Ws if W <= sps[k]) == 1
    # U das outras orbitas: quantos W contem
    for j, orb in enumerate(orbs[1:], 1):
        c = Counter(sum(1 for W in Ws if W <= sps[k]) for k in orb)
        cw = Counter(dimset(W & sps[k]) for k in orb for W in Ws)
        print(f"   {classe}: orbita {len(orb)}: #W contidos -> {dict(c)}; dim(W∩U) -> {dict(cw)}")
    return Ws, sps, orbs


def main():
    res = {}
    fontes = {"Q4a": ["gh_42521666326", "colab_Q4a_o1_cubo1_SAT.json"],
              "Q4b": ["gh_42521672988"],
              "Q4c": ["gh_42521679875", "colab_Q4c_o1_cubo0_SAT.json"]}
    for classe, fs in fontes.items():
        Ws, sps, orbs = spread(classe)
        o0 = set(orbs[0])
        print(classe, ": orbita 255 = 17 estrelas de 15 (espalhamento confirmado)")
        arqs = []
        for f in fs:
            p = os.path.join(BASE, "q1_nuvem_08nov", f)
            arqs += [p] if f.endswith(".json") else glob.glob(os.path.join(p, "**", "cubo_*.json"), recursive=True)
        # testemunhas antigas da orbita 255 (isotropicos so em 1020/2040)
        for g in glob.glob(os.path.join(BASE, "q1_tres_lineares", f"sat_orbita_{classe}_o0*.json")):
            arqs.append(g)
        for f in sorted(arqs):
            r = json.load(open(f))
            if r.get("resultado", "SAT" if r.get("SAT") else "") != "SAT":
                continue
            monos = r["conferencia"]["anf_extra"] if "conferencia" in r else r["anf_extra"]
            viol = isos(classe, monos)
            por_W = [sum(1 for k in viol if k in o0 and Ws[i] <= sps[k]) for i in range(17)]
            outros = [k for k in viol if k not in o0]
            # para U fora da orbita 255: dimensao maxima de W∩U
            dmax = Counter(max(dimset(W & sps[k]) for W in Ws) for k in outros)
            nome = os.path.basename(os.path.dirname(f)) + "/" + os.path.basename(f)
            print(f"  {nome}: por W = {sorted([x for x in por_W if x], reverse=True)}, fora da 255: {len(outros)} (max dim W∩U: {dict(dmax)})")
            res[nome] = {"classe": classe, "por_W": por_W, "fora_255": len(outros)}
    json.dump(res, open(os.path.join(BASE, "q1_estrutura_09nov", "espalhamento_255.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
