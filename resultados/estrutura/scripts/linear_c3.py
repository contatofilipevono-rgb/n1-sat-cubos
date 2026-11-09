"""(09/11) Consequencias LINEARES de I6 sobre C3 (relaxacao: cada produto x_i x_j vira coluna livre).
Sistema I6: para cada bit-alvo h, XOR_k D1[k]_h x_k + XOR_{(i,j)} D2[i,j]_h x_i x_j = F0_h.
Elimina colunas que nao sao variaveis simples de C3; linhas restantes so em C3 => validas para toda solucao de I6.
Depois: cobertura restrita a esse subespaco afim (CryptoMiniSat). UNSAT => N1 para a classe."""
import os, sys, json, time
sys.argv = ["x"]
sys.path.insert(0, r"C:\Users\Valer\Downloads\analise adversarial\q1_tres_lineares")
import sat_n1_orbita as so
from analisa_testemunhas import contexto
from fecho_estrela import linhas
import pycryptosat


def restricoes(classe):
    w1, w2, ny = so.pencil(so.classes()[classe])
    fixo, incog, C3, Tq = so.modelo_nove(w1, w2, ny)
    zerar = set(so.pivos_iT(Tq, ny))
    incog = [m for m in incog if m not in zerar]
    P = so.Pares(fixo, incog)
    c3v = [(m ^ (1 << ny), incog.index(m) + 1) for m in C3]
    c3pos = {var: p for p, (m, var) in enumerate(c3v)}
    nc = len(c3v)
    # colunas: C3 simples -> bits 0..nc-1 (baixos, eliminados por ultimo); demais -> bits altos
    col = {}
    prox = nc
    def colde(chave):
        nonlocal prox
        if chave not in col:
            col[chave] = prox; prox += 1
        return col[chave]
    nb = len(P.alvos)
    eqs = [0] * nb
    for k, v in enumerate(P.D1):
        var = k + 1
        c = c3pos[var] if var in c3pos else colde(("x", var))
        h = 0
        while v:
            if v & 1:
                eqs[h] ^= 1 << c
            v >>= 1; h += 1
    for (i, j), v in P.D2.items():
        c = colde(("p", i, j))
        h = 0
        while v:
            if v & 1:
                eqs[h] ^= 1 << c
            v >>= 1; h += 1
    # constante como bit extra no topo
    TOP = prox + 1
    eqs = [e | (((P.F0 >> h) & 1) << TOP) for h, e in enumerate(eqs)]
    # eliminacao gaussiana com pivo no bit mais alto abaixo de TOP
    piv = {}
    for e in eqs:
        while True:
            m = e & ((1 << TOP) - 1)
            if not m:
                break
            h = m.bit_length() - 1
            if h in piv:
                e ^= piv[h]
            else:
                piv[h] = e
                break
        else:
            pass
        if not (e & ((1 << TOP) - 1)) and (e >> TOP) & 1:
            raise SystemExit("relaxacao linear inconsistente?!")
    lin = [e for h, e in piv.items() if h < nc]
    return lin, nc, TOP, c3v


def cobertura(classe, lin, nc, TOP):
    fixo, incog, Tq, ny, iso, orbs, dados = contexto(classe)
    Ms = [linhas(*d) for d in dados]
    s = pycryptosat.Solver()
    for e in lin:
        vs = [p + 1 for p in range(nc) if (e >> p) & 1]
        s.add_xor_clause(vs, bool((e >> TOP) & 1))
    prox = nc + 1
    for M in Ms:
        auxs = []
        for r in M:
            vs = [p + 1 for p in range(nc) if (r >> p) & 1]
            s.add_xor_clause(vs + [prox], False)
            auxs.append(prox); prox += 1
        s.add_clause(auxs)
    t0 = time.time()
    r, sol = s.solve()
    out = {"classe": classe, "restricoes_lineares": len(lin), "dim_afim": nc - len(lin), "SAT": r, "tempo_s": round(time.time() - t0, 1)}
    if r:
        cb = sum(1 << p for p in range(nc) if sol[p + 1])
        out["c"] = [p for p in range(nc) if (cb >> p) & 1]
        out["confere"] = all(any(bin(x & cb).count("1") & 1 for x in M) for M in Ms) and \
            all((bin(e & cb & ((1 << nc) - 1)).count("1") & 1) == ((e >> TOP) & 1) for e in lin)
    return out


if __name__ == "__main__":
    classe = os.environ.get("CLASSE", "Q4a")
    lin, nc, TOP, c3v = restricoes(classe)
    print(f"{classe}: {len(lin)} restricoes lineares sobre C3 implicadas por I6 (relaxacao)", flush=True)
    # o C3 sem isotropico da cobertura viola alguma?
    nome = classe.replace("^", "").replace("+", "")
    if os.path.exists(f"cobertura_{nome}.json"):
        cb = sum(1 << p for p in json.load(open(f"cobertura_{nome}.json"))["c"])
        viol = sum(1 for e in lin if (bin(e & cb & ((1 << nc) - 1)).count("1") & 1) != ((e >> TOP) & 1))
        print(f"   C3 sem isotropico viola {viol} delas", flush=True)
    out = cobertura(classe, lin, nc, TOP)
    print(json.dumps(out), flush=True)
    json.dump({"restricoes": [[p for p in range(nc) if (e >> p) & 1] + [int((e >> TOP) & 1)] for e in lin], **out},
              open(f"cobertura_restrita_{nome}.json", "w"))
