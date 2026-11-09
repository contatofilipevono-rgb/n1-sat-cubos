"""(09/11) Verificacao INDEPENDENTE de uma testemunha N1 (sem usar o modelo de orbitas/U_Y):
 (a) I6: c_S (ANF inteira, Mobius sobre Z na tabela-verdade de 512 pontos) == 0 mod 4 para |S| >= 6;
 (b) grau de D = 4;
 (c) forca bruta sobre TODOS os subespacos lineares de dimensao 6 (codim 3) de F2^9: existe U com deg(D|U) <= 3?
     (isotropia = queda de grau na restricao; translados nao importam para o grau maximo).
Controles: uma testemunha conhecida com isotropicos deve achar U; aleatoria de grau 4 tambem e testada."""
import sys, json, itertools, time
import numpy as np
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
from sat_n1_orbita import base

N = 9
pts = np.arange(1 << N)
POP = np.array([bin(i).count("1") for i in range(1 << N)])


def tabela(monos):
    tt = np.zeros(1 << N, dtype=np.int64)
    for m in monos:
        tt ^= ((pts & m) == m).astype(np.int64)
    return tt


def mobius_Z(tt, n):
    a = tt.astype(np.int64).copy()
    h = 1
    while h < (1 << n):
        a = a.reshape(-1, 2, h); a[:, 1, :] -= a[:, 0, :]; a = a.reshape(-1); h *= 2
    return a


def i6(tt):
    a = mobius_Z(tt, N)
    return bool(np.all(a[POP >= 6] % 4 == 0)), int(max(POP[a % 2 != 0]))


T6 = np.array([[(t >> i) & 1 for i in range(6)] for t in range(64)], dtype=np.int64)  # 64 x 6
POP6 = np.array([bin(i).count("1") for i in range(64)])


def subespacos6():
    """bases RREF 6x9 (linhas como inteiros de 9 bits), em lotes por conjunto de pivos."""
    for P in itertools.combinations(range(N), 6):
        livres = [(r, c) for r in range(6) for c in range(P[r] + 1, N) if c not in P]
        nf = len(livres)
        if nf == 0:
            yield np.array([[1 << p for p in P]], dtype=np.int64); continue
        bits = ((np.arange(1 << nf)[:, None] >> np.arange(nf)[None, :]) & 1).astype(np.int64)  # (2^nf, nf)
        B = np.tile(np.array([1 << p for p in P], dtype=np.int64), (1 << nf, 1))
        for k, (r, c) in enumerate(livres):
            B[:, r] |= bits[:, k] << c
        yield B


def isotropicos(tt, parar_no_primeiro=False):
    total = 0; n_sub = 0
    for B in subespacos6():
        # pontos: XOR das linhas selecionadas por t
        P = np.zeros((B.shape[0], 64), dtype=np.int64)
        for i in range(6):
            P ^= (T6[:, i][None, :] * B[:, i][:, None])
        f = tt[P]  # (lote, 64)
        a = f.copy()
        h = 1
        while h < 64:
            a = a.reshape(a.shape[0], -1, 2, h); a[:, :, 1, :] ^= a[:, :, 0, :]; a = a.reshape(a.shape[0], 64); h *= 2
        grau4 = (a[:, POP6 >= 4] != 0).any(axis=1)
        k = int((~grau4).sum())
        total += k; n_sub += B.shape[0]
        if parar_no_primeiro and k:
            return total, n_sub
    return total, n_sub


if __name__ == "__main__":
    classe = sys.argv_classe if False else "F4+F4"
    fixo = base(classe)[0]
    w = json.load(open(r"C:\Users\Valer\Downloads\analise adversarial\q1_nuvem_08nov\gh_42547926882\res-52\cubo_52.json"))
    D = set(fixo) ^ set(w["conferencia"]["anf_extra"])
    tt = tabela(D)
    t0 = time.time()
    ok6, grau = i6(tt)
    print("testemunha F4+F4 cubo 52: I6 =", ok6, "| grau =", grau, flush=True)
    tot, ns = isotropicos(tt)
    print(f"   subespacos de codim 3 testados: {ns} (esperado 788035); com queda de grau: {tot}  [{time.time()-t0:.0f}s]", flush=True)
    # controle positivo: testemunha F4+F4 conhecida com isotropicos [0,0,0,12] (cubo 28 da rodada 15+60+240)
    import glob
    f = glob.glob(r"C:\Users\Valer\Downloads\analise adversarial\q1_nuvem_08nov\gh_F4F4_o012\**\cubo_28.json", recursive=True)
    if f:
        w2 = json.load(open(f[0]))
        tt2 = tabela(set(fixo) ^ set(w2["conferencia"]["anf_extra"]))
        print("controle + (cubo 28, esperado 12 isotropicos): I6 =", i6(tt2)[0], "| queda de grau em", isotropicos(tt2)[0], flush=True)
