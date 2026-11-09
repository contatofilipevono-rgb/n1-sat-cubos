"""(09/11) Para W do espalhamento (17 subespacos de dim 4, totalmente singulares para o pencil q1,q2):
 (1) verifica que as 4 condicoes 'C3|W = 0' (coef. dos 4 monomios cubicos em coords de W) estao no
     espaco-linha de M_U para todo U = W+<v> (deducao: T|_{W+v} tem grau <=3 e iota_u T|W = 0);
 (2) para cada testemunha Q4, conta quantos W tem C3|W = 0 e compara com os isotropicos."""
import glob, json, os, sys
from itertools import combinations
sys.argv = ["x"]
from analisa_testemunhas import contexto
from sat_n1 import det3
from posto_estrela import prep
from fecho_estrela import base_red, reduz
from feixe_255 import isos

BASE = r"C:\Users\Valer\Downloads\analise adversarial"


def base_W(W):
    b = []
    for v in sorted(W):
        if v and all(v not in {0} for _ in [0]):
            piv = base_red(b)
            if reduz(piv, v):
                b.append(v)
    assert len(b) == 4
    return b


def cond_W(W, coord, ny=8):
    """4 linhas (bitmask sobre posicao em coord) = coeficientes de C3|W."""
    b = base_W(W)
    out = []
    for (a, bb, c) in combinations(range(4), 3):
        r = 0
        for p, (var, m) in enumerate(coord):
            pass
        out.append((a, bb, c))
    return b, out


def linhas_C3W(W, c3v, ny=8):
    b = base_W(W)
    rows = []
    for (a, bb, c) in combinations(range(4), 3):
        r = 0
        for p, (m, var) in enumerate(c3v):
            idx = [j for j in range(ny) if (m >> j) & 1]
            if det3([[(b[t] >> j) & 1 for j in idx] for t in (a, bb, c)]):
                r |= 1 << p
        rows.append(r)
    return rows


def main():
    res = {}
    fontes = {"Q4a": ["gh_42521666326", "colab_Q4a_o1_cubo1_SAT.json"], "Q4b": ["gh_42521672988"],
              "Q4c": ["gh_42521679875", "colab_Q4c_o1_cubo0_SAT.json"]}
    for classe, fs in fontes.items():
        fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
        # c3v na mesma ordem de coord em dados (coord = [(var,bits)] na ordem de c3_vars)
        from sat_n1_orbita import base
        _, _, _, _, _, _, c3v = base(classe)
        estrelas, sps, orbs = prep(classe)
        ok = True
        CW = []
        for (W, reps, cls, M) in estrelas:
            L = linhas_C3W(W, c3v)
            assert len(base_red(L)) == 4
            CW.append(L)
            for v in reps:
                piv = base_red(M[v])
                if any(reduz(piv, x) for x in L):
                    ok = False
            # intersecao V_a ∩ V_b = span(L)?  (dim 4 medida antes)
        print(f"{classe}: 'C3|W=0' contido nas condicoes de cada U da estrela: {ok}")
        arqs = []
        for f in fs:
            p = os.path.join(BASE, "q1_nuvem_08nov", f)
            arqs += [p] if f.endswith(".json") else glob.glob(os.path.join(p, "**", "cubo_*.json"), recursive=True)
        arqs += glob.glob(os.path.join(BASE, "q1_tres_lineares", f"sat_orbita_{classe}_o*.json"))
        for f in sorted(arqs):
            r = json.load(open(f))
            if r.get("resultado", "SAT" if r.get("SAT") else "") != "SAT":
                continue
            monos = set(r["conferencia"]["anf_extra"] if "conferencia" in r else r["anf_extra"])
            # vetor c (bitmask) das variaveis de C3 presentes
            c = 0
            for p, (m, var) in enumerate(c3v):
                if incog[var - 1] in monos:
                    c |= 1 << p
            nulos = [i for i, L in enumerate(CW) if all(bin(x & c).count("1") % 2 == 0 for x in L)]
            viol = isos(classe, list(monos))
            por = [sum(1 for k in viol if k in set(o)) for o in orbs]
            nome = os.path.basename(os.path.dirname(f)) + "/" + os.path.basename(f)
            print(f"  {nome}: #W com C3|W=0: {len(nulos)}  isotropicos {por}")
            res[nome] = {"classe": classe, "W_nulos": nulos, "isotropicos": por}
    json.dump(res, open(os.path.join(BASE, "q1_estrutura_09nov", "c3_nas_retas.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
