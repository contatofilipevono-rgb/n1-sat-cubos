"""Estrutura das testemunhas SAT de N1 restrito a orbitas (09/11).
Para cada testemunha D = q1q2 + x C3 + R (ANF em 9 variaveis, x = bit 8):
  - I6 e I7 (confere): I7 e a 2a condicao de liftabilidade (Lema L usa I6 E I7; N1 so usa I6);
  - C3: numero de monomios, 'posto' = dim do span de {i_v C3 : v em Y} (= numero de variaveis essenciais),
        e se C3 e degenerado (fatora com linear) etc.;
  - isotropicos: U_Y isotropicos por orbita; intersecao comum de todos (subespaco contido em todos);
  - R: grau-3 sem x, grau-2 com x etc. (contagens)."""
import glob
import json
import os
import sys

sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1 import rref_todos, restr_zero, confere  # noqa: E402
from sat_n1_cegar import prepara_U, isotropico_em  # noqa: E402
from sat_n1_orbita import base, orbitas  # noqa: E402

BASE = r"C:\Users\Valer\Downloads\analise adversarial"
CLASSE_AUTO = {"F4^2": "automorfismos_F42.json", "F4+F4": "automorfismos_F4F4.json", "Q4a": "automorfismos_Q4a.json",
               "Q4b": "automorfismos_Q4b.json", "Q4c": "automorfismos_Q4c.json"}


def popc(x):
    return bin(x).count("1")


def contrai(F, v):
    """i_v F para forma F (conjunto de monomios bitmask) no sentido exterior: soma sobre i em supp(v) de d/dx_i."""
    out = set()
    for m in F:
        for i in range(8):
            if (v >> i) & 1 and (m >> i) & 1:
                out ^= {m ^ (1 << i)}
    return out


def posto_formas(lista):
    """dim do span F2 de uma lista de conjuntos de monomios."""
    idx = {}
    vecs = []
    for s in lista:
        v = 0
        for m in s:
            if m not in idx:
                idx[m] = len(idx)
            v |= 1 << idx[m]
        vecs.append(v)
    piv = {}
    for v in vecs:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    return len(piv)


def rows_U(B):
    return [sum(int(B[a, i]) << i for i in range(8)) for a in range(B.shape[0])]


def span(rows):
    s = {0}
    for r in rows:
        s |= {x ^ r for x in s}
    return s


cache = {}


def contexto(classe):
    if classe not in cache:
        fixo, incog, C3, Tq, ny, cnf, c3v = base(classe)
        Us = rref_todos(5, 8)
        iso = Us[restr_zero(Tq, Us)]
        gens = [tuple(A) for A in json.load(open(os.path.join(BASE, "q1_tres_lineares", CLASSE_AUTO[classe])))[classe]["geradores"]]
        orbs = orbitas(iso, gens)
        dados = prepara_U(Tq, ny, c3v, iso)
        cache[classe] = (fixo, incog, Tq, ny, iso, orbs, dados)
    return cache[classe]


def analisa(nome, classe, monos):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    s = set(monos)
    assert s <= set(incog), "monomio fora do modelo"
    i6, i7 = confere(fixo, monos, ny + 1)
    val = [False] * (len(incog) + 2)
    for k, m in enumerate(incog):
        val[k + 1] = m in s
    viol = [k for k in range(len(iso)) if isotropico_em(val, *dados[k])]
    por_orb = [sum(1 for k in viol if k in set(o)) for o in orbs]
    X = 1 << ny
    C3 = {m ^ X for m in s if m & X and popc(m) == 4}
    Rx2 = sum(1 for m in s if m & X and popc(m) == 3)
    R3 = sum(1 for m in s if not m & X and popc(m) == 3)
    R2 = sum(1 for m in s if popc(m) <= 2)
    der = [contrai(C3, 1 << i) for i in range(8)]
    posto = posto_formas(der)
    # intersecao comum dos U_Y isotropicos
    if viol:
        comum = None
        for k in viol:
            sp = span(rows_U(iso[k]))
            comum = sp if comum is None else (comum & sp)
        dim_comum = (len(comum)).bit_length() - 1
    else:
        dim_comum = None
    return {"nome": nome, "classe": classe, "I6": bool(i6), "I7": bool(i7), "C3_monomios": len(C3),
            "C3_posto": posto, "x*quadraticos": Rx2, "cubicos_sem_x": R3, "grau<=2": R2,
            "isotropicos_por_orbita": por_orb, "tamanhos_orbitas": [len(o) for o in orbs],
            "dim_intersecao_comum_isotropicos": dim_comum}


def testemunhas():
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, "q1_tres_lineares", "sat_orbita_*.json"))):
        r = json.load(open(f))
        if r.get("SAT") and "anf_extra" in r:
            out.append((os.path.basename(f)[11:-5], r["classe"], r["anf_extra"]))
    for f, classe in [(os.path.join(BASE, "q1_nuvem_08nov", "F42_o3_cubo7_SAT.json"), "F4^2")] + \
            [(g, "F4+F4") for g in glob.glob(os.path.join(BASE, "q1_nuvem_08nov", "gh_F4F4_o012", "**", "cubo_*.json"), recursive=True)]:
        r = json.load(open(f))
        if r.get("resultado") == "SAT":
            nome = os.path.basename(os.path.dirname(f)) + "_" + os.path.basename(f)[:-5] if "gh_" in f else "F42_o3_nuvem"
            out.append((nome, classe, r["conferencia"]["anf_extra"]))
    return out


if __name__ == "__main__":
    res = []
    for nome, classe, monos in testemunhas():
        a = analisa(nome, classe, monos)
        res.append(a)
        print(json.dumps(a), flush=True)
    json.dump(res, open(os.path.join(BASE, "q1_estrutura_09nov", "invariantes_testemunhas.json"), "w"), indent=1)
