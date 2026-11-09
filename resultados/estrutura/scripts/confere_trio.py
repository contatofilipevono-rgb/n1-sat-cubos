"""(09/11) Conferencia independente do trio (phi1,phi2,phi3) de sete_restricoes_09nov/trio_s22_seed1.json:
 - phi_i ∧ T = 0 (8 coordenadas de Λ^7) ;
 - para cada v != 0: D = T + x*phi_v em 9 variaveis; forca bruta sobre os 788035 subespacos de codim 3 (queda de grau)."""
import json, sys, re
from itertools import product
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
from verifica_independente import tabela, isotropicos

w1, w2, ny = so.pencil(so.classes()["F4+F4"])
_, _, _, Tq = so.modelo_nove(w1, w2, ny)
T = list(Tq)


def parse(s):
    out = set()
    for termo in s.split("+"):
        bits = [int(d) for d in re.findall(r"y(\d)", termo)]
        out ^= {sum(1 << b for b in bits)}
    return out


tr = json.load(open(r"C:\Users\Valer\Downloads\analise adversarial\sete_restricoes_09nov\trio_s22_seed1.json"))["trios"][0]
phis = [parse(s) for s in tr["phi"]]
for i, ph in enumerate(phis):
    cunha = [sum(1 for a in ph for t in T if (a & t) == 0 and (a | t) == 255 ^ (1 << j)) % 2 for j in range(8)]
    print(f"phi{i+1}: {len(ph)} monomios cubicos: {all(bin(m).count('1') == 3 for m in ph)}; phi∧T = {cunha}")
X = 1 << 8
for v in product((0, 1), repeat=3):
    if not any(v):
        continue
    pv = set()
    for i in range(3):
        if v[i]:
            pv ^= phis[i]
    D = set(T) ^ {m | X for m in pv}
    tot, ns = isotropicos(tabela(D))
    print(f"v={v}: subespacos codim 3 com queda de grau: {tot} de {ns}", flush=True)
