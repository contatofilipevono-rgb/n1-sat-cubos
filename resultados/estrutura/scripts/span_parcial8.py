import json, sys
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
d = json.load(open("metades8_parcial.json"))
am, cubm = d["amostras"], d["cubicos"]
w1, w2, ny = so.pencil(so.classes()["F4+F4"])
_, _, _, Tq = so.modelo_nove(w1, w2, ny)
def red(rows):
    piv = {}
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; break
    return piv
gauge = []
for i in range(8):
    r = 0
    for t in Tq:
        if (t >> i) & 1: r ^= 1 << cubm.index(t ^ (1 << i))
    gauge.append(r)
difs = [a ^ am[0] for a in am[1:]]
print(len(am), "amostras; dim span difs:", len(red(difs)), "; com gauge:", len(red(difs + gauge)), "de 56")
