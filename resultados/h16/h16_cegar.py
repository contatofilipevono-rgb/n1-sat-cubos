"""CEGAR sobre os filtros 2-adicos do H16 (08/11).
Comeca com os subcubos de H16_KS (padrao zero) e repete:
  resolve -> se UNSAT: nao existe quartica homogenea RS bent em 16 variaveis (os filtros sao necessarios).
          -> se SAT: calcula o espectro de Walsh completo de f_c (2^16 pontos, exato);
               bent?  => registra a TESTEMUNHA (refutaria a conjectura em n=16; conferir de novo antes de qualquer conclusao)
               nao   => procura subcubo (codim 1..6, padrao qualquer) cuja congruencia f_c viola, acrescenta o filtro;
                        se nenhum violado for achado na amostra, bloqueia c (clausula) e registra como sobrevivente.
Sem certificado DRAT aqui (pysat); um UNSAT final deve ser refeito com prova (certifica.py/drat-trim)."""
import json
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h16_filtros import Codificador, familias, alvo, avalia, forma_c, N  # noqa: E402
from pysat.solvers import Solver  # noqa: E402


def tabela(c):
    t = np.zeros(1 << N, dtype=np.int8)
    for x in range(1 << N):
        t[x] = bin(forma_c(x) & c).count("1") & 1
    return t


def walsh(t):
    a = (1 - 2 * t.astype(np.int64))
    h = 1
    while h < len(a):
        a = a.reshape(-1, 2 * h)
        x, y = a[:, :h].copy(), a[:, h:].copy()
        a[:, :h], a[:, h:] = x + y, x - y
        a = a.reshape(-1)
        h *= 2
    return a


def viola(c, t, rnd, tentativas=4000):
    """procura subcubo violado (codim 1..6, padrao aleatorio)."""
    for _ in range(tentativas):
        k = rnd.randint(1, 6)
        F = tuple(sorted(rnd.sample(range(N), k)))
        p = tuple(rnd.randint(0, 1) for _ in range(k))
        livres = [j for j in range(N) if j not in F]
        base = sum(1 << j for j, b in zip(F, p) if b)
        idx = np.full(1, base, dtype=np.int64)
        for j in livres:
            idx = np.concatenate([idx, idx | (1 << j)])
        w = int(t[idx].sum())
        m, alv = alvo(k)
        if w % (1 << m) != alv:
            return F, p
    return None


if __name__ == "__main__":
    ks = [int(x) for x in os.environ.get("H16_KS", "4").split(",")]
    rnd = random.Random(int(os.environ.get("H16_SEMENTE", "1")))
    t0 = time.time()
    enc = Codificador()
    for F, p in familias(ks, padroes="zero"):
        enc.filtro(F, p)
    s = Solver(name="cadical195", bootstrap_with=enc.cnf.cl)
    log = {"ks": ks, "iteracoes": [], "sobreviventes": [], "testemunhas_bent": []}
    for it in range(1, int(os.environ.get("H16_MAXIT", "400")) + 1):
        t1 = time.time()
        r = s.solve()
        if not r:
            log["resultado"] = "UNSAT"
            print(f"it {it}: UNSAT ({time.time() - t1:.0f}s) => nenhuma quartica RS homogenea passa os filtros "
                  f"(total {time.time() - t0:.0f}s)", flush=True)
            break
        mod = s.get_model()
        c = sum(1 << i for i in range(116) if mod[i] > 0)
        t = tabela(c)
        W = walsh(t)
        bent = bool(np.all(np.abs(W) == 256))
        if bent:
            log["testemunhas_bent"].append(hex(c))
            print(f"it {it}: SAT e BENT! c={hex(c)}  (conferir de novo)", flush=True)
            s.add_clause([-(i + 1) if (c >> i) & 1 else (i + 1) for i in range(116)])
            continue
        v = viola(c, t, rnd)
        if v:
            F, p = v
            n0 = len(enc.cnf.cl)
            prox0 = enc.cnf.prox
            enc.filtro(F, p)
            for cl in enc.cnf.cl[n0:]:
                s.add_clause(cl)
            log["iteracoes"].append({"it": it, "k": len(F), "max|W|": int(np.abs(W).max())})
            print(f"it {it}: SAT ({time.time() - t1:.0f}s), nao bent (max|W|={int(np.abs(W).max())}); "
                  f"filtro novo codim {len(F)}", flush=True)
        else:
            log["sobreviventes"].append(hex(c))
            s.add_clause([-(i + 1) if (c >> i) & 1 else (i + 1) for i in range(116)])
            print(f"it {it}: SAT, nao bent, SEM filtro violado na amostra -> sobrevivente bloqueado", flush=True)
        json.dump(log, open(os.environ.get("H16_LOG", "h16_cegar_log.json"), "w"), indent=1)
    json.dump(log, open(os.environ.get("H16_LOG", "h16_cegar_log.json"), "w"), indent=1)
