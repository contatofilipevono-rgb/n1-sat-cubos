"""Lema (2 lineares, 1 misto), teste por amostragem (09/11/2026).  Autocontido: so numpy >= 2.
  Delta = T + x1 phi1 + x2 phi2 + x1 x2 psi   em F2^10  (y0..y7 = bits 0..7, x1 = bit 8, x2 = bit 9)
  com  phi_i ^ T = 0  e  phi1 ^ phi2 + psi ^ T = 0  (parte de I6 com |S| = 8).
Pergunta: Delta sempre tem queda de grau (deg <= 3) em codimensao <= 4?  Subespacos testados:
  k=1: U_Y (dim 5) + <e_v + u>, v em {x1, x2, x1+x2}   -> conta = no. de U_Y isotropicos de phi1, phi2, phi1+phi2
  k=2: K (dim 4, T|K=0) + <e_x1 + u1, e_x2 + u2>       -> contado para TODOS os psi = psi0 + ker(T^) de uma vez
(codim 4 em F2^10; com x3 = 0 da codim 5 em F2^11.)  Contraexemplo = k1 = [0,0,0] e algum psi com k2 = 0.
Uso: python lema10.py CLASSE MODO SEMENTE NPARES [TEMPO_S]
  CLASSE: F4+F4 | F4^2 | Q4a | Q4b | Q4c      MODO: aleat (phi1 qualquer em L) | adv (phi1, phi2, phi1+phi2 em N)"""
import itertools
import json
import sys
import time
import numpy as np

n = 8
CLASSES = {
    "F4+F4": ("y0y2+y1y3+y4y6+y5y7", "y1y2+y0y3+y1y3+y5y6+y4y7+y5y7"),
    "F4^2": ("y0y4+y1y5+y2y6+y3y7", "y1y4+y2y5+y3y6+y0y7+y2y7"),
    "Q4a": ("y0y4+y1y5+y2y6+y3y7", "y1y4+y2y5+y3y6+y0y7+y1y7"),
    "Q4b": ("y0y4+y1y5+y2y6+y3y7", "y1y4+y2y5+y3y6+y0y7+y3y7"),
    "Q4c": ("y0y4+y1y5+y2y6+y3y7", "y1y4+y2y5+y3y6+y0y7+y1y7+y2y7+y3y7"),
}
N_ISO = {"F4+F4": 1275, "F4^2": 3195, "Q4a": 3315, "Q4b": 3315, "Q4c": 3315}


def poly(txt):
    out = set()
    for t in txt.replace(" ", "").split("+"):
        out ^= {sum(1 << int(c) for c in t.replace("y", ""))}
    return out


def comb(k):
    return [sum(1 << i for i in c) for c in itertools.combinations(range(n), k)]


L2, L3, L6 = comb(2), comb(3), comb(6)
I2, I3, I6 = ({m: k for k, m in enumerate(L)} for L in (L2, L3, L6))


def par(x):
    return bin(x).count("1") & 1


def elim_hist(vecs):
    """escalonamento com historico: devolve (piv: bit -> (vetor, combinacao), nucleo: lista de combinacoes)."""
    piv, ker = {}, []
    for k, v in enumerate(vecs):
        c = 1 << k
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h][0]
                c ^= piv[h][1]
            else:
                piv[h] = (v, c)
                break
        else:
            ker.append(c)
    return piv, ker


def reduz(piv, v):
    c = 0
    while v:
        h = v.bit_length() - 1
        if h not in piv:
            return v, c
        v ^= piv[h][0]
        c ^= piv[h][1]
    return 0, c


def residuo(piv, v):
    """residuo canonico de v modulo span(piv) (zera todos os bits-pivo)."""
    for h in sorted(piv, reverse=True):
        if (v >> h) & 1:
            v ^= piv[h][0]
    return v


def cunha33(a, b):
    """produto exterior de duas cubicas (vetores de 56 bits) -> vetor em L6 (28 bits)."""
    out = 0
    ma = [L3[k] for k in range(56) if (a >> k) & 1]
    mb = [L3[k] for k in range(56) if (b >> k) & 1]
    for x in ma:
        for y in mb:
            if x & y == 0:
                out ^= 1 << I6[x | y]
    return out


def pontos(gens):
    M, d = gens.shape
    pts = np.zeros((M, 1 << d), dtype=np.int32)
    idx = np.arange(1 << d)
    for k in range(d):
        pts[:, (idx >> k) & 1 == 1] ^= gens[:, k:k + 1]
    return pts


def moebius(f):
    M, N = f.shape
    f = f.copy()
    h = 1
    while h < N:
        g = f.reshape(M, -1, 2, h)
        g[:, :, 1, :] ^= g[:, :, 0, :]
        h *= 2
    return f


PESO = {d: np.array([bin(i).count("1") for i in range(1 << d)]) for d in (4, 5, 6)}


def sem_quartico(tt, gens):
    d = gens.shape[1]
    return ~moebius(tt[pontos(gens)])[:, PESO[d] >= 4].any(1)


def tabela(monos, nb=10):
    z = np.arange(1 << nb)
    tt = np.zeros(1 << nb, dtype=np.uint8)
    for m in monos:
        tt ^= ((z & m) == m).astype(np.uint8)
    return tt


class Base:
    def __init__(self, nome):
        t0 = time.time()
        q1, q2 = (poly(s) for s in CLASSES[nome])
        prod = set()
        for a in q1:
            for b in q2:
                prod ^= {a | b}
        self.T = T = {m for m in prod if bin(m).count("1") == 4}
        ttT = tabela(T, 8)
        # L = {phi : phi ^ T = 0}
        eqs = []
        for i in range(n):
            S = 255 ^ (1 << i)
            eqs.append(sum(1 << I3[m] for m in L3 if (m & S) == m and (S ^ m) in T))
        cols = [sum(((eqs[i] >> k) & 1) << i for i in range(n)) for k in range(56)]
        _, ker = elim_hist(cols)
        self.L = ker                                        # base de L (vetores de 56 bits)
        self.G = [sum(1 << I3[t ^ (1 << i)] for t in T if (t >> i) & 1) for i in range(n)]
        # T^ : L2 -> L6
        img = []
        for m in L2:
            v = 0
            for t in T:
                if t & m == 0:
                    v ^= 1 << I6[t | m]
            img.append(v)
        self.pivT, kerT = elim_hist(img)
        self.ker2 = [{L2[k] for k in range(28) if (c >> k) & 1} for c in kerT]
        # U_Y isotropicos (dim 5) e funcionais
        iso = []
        for piv in itertools.combinations(range(n), 5):
            R = self._rref(piv, 5)
            iso.append(R[sem_quartico(ttT, R)])
        iso = np.concatenate(iso)
        assert len(iso) == N_ISO[nome], len(iso)
        trip = list(itertools.combinations(range(5), 3))
        F = []
        for B in iso:
            pts = pontos(B[None, :])[0]
            rows = []                                       # trio t como funcional em 56 coordenadas
            cm = np.zeros((56, 32), dtype=np.uint8)
            for k, m in enumerate(L3):
                cm[k] = (pts & m) == m
            cm = moebius(cm)
            for (a, b, c) in trip:
                idx = (1 << a) | (1 << b) | (1 << c)
                rows.append(sum(int(cm[k, idx]) << k for k in range(56)))
            W = [sum(par(rows[t] & g) << t for t in range(10)) for g in self.G]
            pv, _ = elim_hist(W)
            assert len(pv) == 3, "posto de R_U != 3"
            # anulador de span(W) em F2^10
            colsW = [sum(((W[i] >> t) & 1) << i for i in range(len(W))) for t in range(10)]
            _, ann = elim_hist(colsW)
            fs = []
            for f in ann:
                g = 0
                for t in range(10):
                    if (f >> t) & 1:
                        g ^= rows[t]
                fs.append(g)
            F.append(fs)
        self.F56 = np.array(F, dtype=np.uint64)             # (nU, 7)
        # K de dim 4 com T|K = 0, agrupados por pivos (para os representantes de Y/K)
        Ks, reps = [], []
        for piv in itertools.combinations(range(n), 4):
            R = self._rref(piv, 4)
            R = R[sem_quartico(ttT, R)]
            np_ = [j for j in range(n) if j not in piv]
            rp = np.array([sum(((a >> t) & 1) << np_[t] for t in range(4)) for a in range(16)], dtype=np.int32)
            Ks.append(R)
            reps.append(np.broadcast_to(rp, (len(R), 16)))
        self.K = np.concatenate(Ks)
        self.reps = np.concatenate(reps)
        print(f"base {nome}: dim L = {len(self.L)}, posto T^ = {len(self.pivT)}, dim ker(T^) = {len(self.ker2)}, "
              f"U_Y = {len(iso)}, K(dim 4, T|K=0) = {len(self.K)} ({time.time() - t0:.0f}s)", flush=True)

    @staticmethod
    def _rref(piv, k):
        livres = [(i, j) for i in range(k) for j in range(n) if j > piv[i] and j not in piv]
        bits = np.arange(1 << len(livres))
        rows = np.zeros((len(bits), k), dtype=np.int32)
        for i in range(k):
            rows[:, i] = 1 << piv[i]
        for t, (i, j) in enumerate(livres):
            rows[:, i] |= ((bits >> t) & 1) << j
        return rows

    def n_iso(self, xs, bloco=64):
        """numero de U_Y isotropicos para cada cubica (56 bits)."""
        xs = np.asarray(xs, dtype=np.uint64)
        out = np.zeros(len(xs), dtype=np.int32)
        for u0 in range(0, len(self.F56), bloco):
            F = self.F56[u0:u0 + bloco]
            z = np.ones((len(xs), len(F)), dtype=bool)
            for j in range(F.shape[1]):
                z &= (np.bitwise_count(xs[:, None] & F[None, :, j]) & 1) == 0
            out += z.sum(1)
        return out

    def em_N(self, xs, bloco=64):
        xs = np.asarray(xs, dtype=np.uint64)
        vivo = np.arange(len(xs))
        for u0 in range(0, len(self.F56), bloco):
            if not len(vivo):
                break
            F = self.F56[u0:u0 + bloco]
            x = xs[vivo]
            z = np.ones((len(x), len(F)), dtype=bool)
            for j in range(F.shape[1]):
                z &= (np.bitwise_count(x[:, None] & F[None, :, j]) & 1) == 0
            vivo = vivo[~z.any(1)]
        m = np.zeros(len(xs), dtype=bool)
        m[vivo] = True
        return m

    def sorteia(self, rng, base, B):
        """B combinacoes aleatorias de 'base' (lista de inteiros de 56 bits)."""
        x = np.zeros(B, dtype=np.uint64)
        for b in base:
            x ^= np.where(rng.integers(0, 2, B).astype(bool), np.uint64(b), np.uint64(0))
        return x

    def compat(self, p1):
        """base de {phi2 em L : phi1 ^ phi2 em T ^ L2}."""
        res = [residuo(self.pivT, cunha33(p1, b)) for b in self.L]
        _, ker = elim_hist(res)
        out = []
        for c in ker:
            v = 0
            for k in range(len(self.L)):
                if (c >> k) & 1:
                    v ^= self.L[k]
            out.append(v)
        return out

    def psi0(self, p1, p2):
        r, c = reduz(self.pivT, cunha33(p1, p2))
        assert r == 0
        return {L2[k] for k in range(28) if (c >> k) & 1}

    def quedas_k2(self, p1, p2):
        """numero de W (k=2) com queda, para cada psi = psi0 + sum eps_j ker2[j]; devolve array de 2^dimker."""
        X1, X2 = 256, 512
        mon = lambda v, x: {L3[k] | x for k in range(56) if (v >> k) & 1}
        tt0 = tabela(set(self.T) | mon(p1, X1) | mon(p2, X2) | {m | X1 | X2 for m in self.psi0(p1, p2)})
        cands = []
        for a in range(0, len(self.K), 4096):
            R, rp = self.K[a:a + 4096], self.reps[a:a + 4096]
            ok = []
            for X in (X1, X2):
                G = np.concatenate([np.repeat(R, 16, 0), (rp.reshape(-1) | X)[:, None]], 1)
                ok.append(sem_quartico(tt0, G).reshape(len(R), 16))
            i, u1, u2 = np.nonzero(ok[0][:, :, None] & ok[1][:, None, :])
            if len(i):
                cands.append(np.concatenate([R[i], (rp[i, u1] | X1)[:, None], (rp[i, u2] | X2)[:, None]], 1))
        if not cands:
            return np.zeros(1 << len(self.ker2), dtype=np.int64), 0
        W = np.concatenate(cands).astype(np.int32)
        pts = pontos(W)
        sel = PESO[6] >= 4

        def codigo(tt):
            c = moebius(tt[pts])[:, sel]                    # 22 coeficientes de peso >= 4
            return np.packbits(c, axis=1, bitorder="little")
        A0 = codigo(tt0)
        Aj = [codigo(tabela({m | X1 | X2 for m in eta})) for eta in self.ker2]
        nk = len(Aj)
        out = np.zeros(1 << nk, dtype=np.int64)
        cur, eps = A0.copy(), 0
        out[0] = int((~cur.any(1)).sum())
        for g in range(1, 1 << nk):                         # codigo de Gray
            j = (g & -g).bit_length() - 1
            cur ^= Aj[j]
            eps ^= 1 << j
            out[eps] = int((~cur.any(1)).sum())
        return out, len(W)


def texto3(v):
    return " + ".join("".join(f"y{i}" for i in range(8) if (L3[k] >> i) & 1) for k in range(56) if (v >> k) & 1)


def texto2(P):
    return " + ".join("".join(f"y{i}" for i in range(8) if (m >> i) & 1) for m in sorted(P))


def no_span(v, vecs):
    piv, _ = elim_hist(vecs)
    return reduz(piv, v)[0] == 0


if __name__ == "__main__":
    nome, modo, semente, npares = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    tmax = float(sys.argv[5]) if len(sys.argv) > 5 else 1e18
    B = Base(nome)
    rng = np.random.default_rng([semente, sum(map(ord, nome + modo))])
    t0, res, tent = time.time(), [], 0
    arq = f"lema10_{nome.replace('+', '').replace('^', '')}_{modo}_{semente}.json"
    while len(res) < npares and time.time() - t0 < tmax:
        # phi1
        if modo == "adv":
            xs = B.sorteia(rng, B.L, 1 << 13)
            xs = xs[B.em_N(xs)]
            if not len(xs):
                continue
            p1 = int(xs[0])
        else:
            p1 = int(B.sorteia(rng, B.L, 1)[0])
        if no_span(p1, B.G):
            continue
        cb = B.compat(p1)
        # phi2
        p2 = None
        for _ in range(60):
            tent += 1
            ys = B.sorteia(rng, cb, 1 << 14 if modo == "adv" else 4)
            if modo == "adv":
                ys = ys[B.em_N(ys)]
                if len(ys):
                    ys = ys[B.em_N(ys ^ np.uint64(p1))]
            ys = [int(y) for y in ys if not no_span(int(y), B.G + [p1])]
            if ys:
                p2 = ys[0]
                break
        if p2 is None:
            print(f"   phi1 sem phi2 compativel em N apos 60 lotes (dim compat {len(cb)})", flush=True)
            continue
        k1 = B.n_iso([p1, p2, p1 ^ p2]).tolist()
        t1 = time.time()
        k2, ncand = B.quedas_k2(p1, p2)
        zeros = np.nonzero(k2 == 0)[0].tolist()
        r = {"phi1": texto3(p1), "phi2": texto3(p2), "psi0": texto2(B.psi0(p1, p2)), "dim_compat": len(cb), "k1": k1,
             "cand_k2": ncand, "k2_min": int(k2.min()), "k2_max": int(k2.max()), "k2_media": float(k2.mean()),
             "psi_com_k2_zero": len(zeros), "eps_zero": zeros[:20],
             "CONTRAEXEMPLO": bool(sum(k1) == 0 and zeros)}
        res.append(r)
        print(f"par {len(res)}: k1={k1} cand={ncand} k2 min/media/max = {r['k2_min']}/{r['k2_media']:.0f}/{r['k2_max']} "
              f"psi com k2=0: {len(zeros)}{'  <<< CONTRAEXEMPLO' if r['CONTRAEXEMPLO'] else ''} "
              f"({time.time() - t1:.0f}s; total {time.time() - t0:.0f}s)", flush=True)
        json.dump({"classe": nome, "modo": modo, "semente": semente, "ker2": [texto2(e) for e in B.ker2], "pares": res},
                  open(arq, "w"), indent=1)
    mins = [r["k2_min"] for r in res]
    print(f"RESUMO {nome} {modo} semente {semente}: pares {len(res)}; menor k2 = {min(mins) if mins else None}; "
          f"pares com algum psi sem queda k=2: {sum(1 for r in res if r['psi_com_k2_zero'])}; "
          f"CONTRAEXEMPLOS (k1=0 e k2=0): {sum(1 for r in res if r['CONTRAEXEMPLO'])}", flush=True)
