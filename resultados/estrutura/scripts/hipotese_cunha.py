"""(09/11) Hipotese: as 8 restricoes lineares de I6 sobre C3 sao 'C3 ∧ T = 0' em Λ^7 Y (8 coordenadas):
f_i(C3) = #{(a in C3, c in T) : a ⊔ c = [8] \\ {i}} mod 2. Compara spans com as restricoes de linear_c3."""
import sys
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from linear_c3 import restricoes
from sat_n1_orbita import base
from fecho_estrela import base_red, reduz

for classe in ["Q4a", "Q4b", "Q4c", "F4^2", "F4+F4"]:
    lin, nc, TOP, c3v = restricoes(classe)
    fixo, incog, C3, Tq, ny, cnf, _ = base(classe)
    T = list(Tq)
    full = (1 << 8) - 1
    fs = []
    for i in range(8):
        alvo = full ^ (1 << i)
        r = 0
        for p, (m, var) in enumerate(c3v):
            n = sum(1 for c in T if (m & c) == 0 and (m | c) == alvo)
            if n & 1:
                r |= 1 << p
        fs.append(r)
    L = [e & ((1 << nc) - 1) for e in lin]
    pL, pF = base_red(L), base_red(fs)
    iguais = len(pL) == len(pF) and all(reduz(pL, f) == 0 for f in fs)
    print(f"{classe}: posto(I6-lineares)={len(pL)}, posto(C3∧T)={len(pF)}, mesmo espaco: {iguais}")
