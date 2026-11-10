import numpy as np, sys
exec(open(r"C:\Users\Valer\Downloads\analise adversarial\n1-sat-cubos\resultados\hrsbf_decomp4\mecanismo_C.py", encoding="utf-8-sig").read().split("def analisa")[0])
B = rs_bent(8, 4); m = 4; y = np.arange(16)
G = B[:, y | (y << 4)]
a = G.copy().astype(np.uint8); h = 1
while h < 16:
    a = a.reshape(a.shape[0], -1, 2, h); a[:, :, 1, :] ^= a[:, :, 0, :]; a = a.reshape(a.shape[0], 16); h *= 2
print("RS bent n=8:", len(B), "| b01 (y0y1) presente:", int(a[:, 3].sum()), "| b02 (y0y2) presente:", int(a[:, 5].sum()), "| grau de G <= 1 em todas:", bool(np.all(a[:, [3,5,6,9,10,12,7,11,13,14,15]] == 0)))
