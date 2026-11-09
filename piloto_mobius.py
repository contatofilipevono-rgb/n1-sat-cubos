"""Bounded F4+F4 pilot. Reuses the repository's cube geometry and SAT checks."""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import cubo
from i7 import _Ctx
from sat_cnf import CNF

CUBES = (0, 17, 42, 63)
OUT = Path("pilot-results")
INSTANCE = Path("pilot-instance")


def neg(lit):
    return not lit if isinstance(lit, bool) else -lit


def subtract_mod8(ctx, a, b):
    borrow = False
    result = []
    for i, (left, right) in enumerate(zip(a, b)):
        parity = ctx.XOR2(left, right)
        result.append(ctx.XOR2(parity, borrow))
        if i < 2:
            generate = ctx.AND2(neg(left), right)
            propagate = ctx.AND2(neg(parity), borrow)
            borrow = ctx.XOR2(generate, propagate)
    return tuple(result)


def compact_cnf(fixed, unknown, n):
    cnf = CNF(len(unknown) + 1)
    ctx = _Ctx(cnf)
    truth = [False] * (1 << n)
    for m in fixed:
        truth[m] = True
    for i, m in enumerate(unknown, 1):
        truth[m] = i
    for k in range(n):
        bit = 1 << k
        for mask in range(1 << n):
            if mask & bit:
                truth[mask] = ctx.XOR2(truth[mask], truth[mask ^ bit])
    residues = [(v, False, False) for v in truth]
    for k in range(n):
        bit = 1 << k
        for mask in range(1 << n):
            if mask & bit:
                residues[mask] = subtract_mod8(ctx, residues[mask], residues[mask ^ bit])
    for mask, bits in enumerate(residues):
        # The low bit already vanishes above degree 4 by the ANF construction.
        if mask.bit_count() >= 6:
            ctx.fixa(bits[1], False)
        if mask.bit_count() >= 7:
            ctx.fixa(bits[2], False)
    return cnf


def generate():
    original_base = cubo.base

    def replacement(name):
        fixed, unknown, c3, top, ny, _, c3_vars = original_base(name)
        cnf = compact_cnf(fixed, unknown, ny + 1)
        cnf.cl.append([var for _, var in c3_vars])
        return fixed, unknown, c3, top, ny, cnf, c3_vars

    with patch.object(cubo, "base", replacement), patch.dict(os.environ, {"N1_I7": "0"}):
        cubo.gera("F4+F4", "automorfismos_F4F4.json", "0,1,2,3", 6, INSTANCE)
    manifest_path = INSTANCE / "cubos.json"
    manifest = json.loads(manifest_path.read_text())
    assert manifest["S"] == 1275 and len(manifest["cubos"]) == 64
    manifest.update(I7=True, encoding="zeta-mobius-mod8", selected_cubes=list(CUBES))
    (OUT / "instancia.json").write_text(json.dumps(manifest, indent=2) + "\n")


def solve(i, seconds):
    cnf = INSTANCE / f"cubo-{i}.cnf"
    log = OUT / f"cubo-{i}.log"
    proof = OUT / f"cubo-{i}.drat"
    cubo.cnf_cubo(INSTANCE, i, cnf)
    record = {"cubo": i, "limite_s": seconds, "resultado": "INDECISO"}
    started = time.monotonic()
    with log.open("w") as f:
        try:
            process = subprocess.run(["./cadical", "-t", str(seconds), cnf], stdout=f,
                                     stderr=subprocess.STDOUT, timeout=seconds + 20)
            record["codigo_solver"] = process.returncode
        except subprocess.TimeoutExpired:
            process = None
    record["tempo_solver_s"] = round(time.monotonic() - started, 3)
    if process and process.returncode == 10:
        check = cubo.confere_sat(INSTANCE, log)
        record["conferencia"] = check
        if check["I6_conferido"] and check["I7_conferido"] and check["isotropicos_total"] == 0:
            record["resultado"] = "SAT_CONFERIDO"
        else:
            record["resultado"] = "SAT_FALHA_CONFERENCIA"
    elif process and process.returncode == 20:
        record["resultado"] = "UNSAT_SEM_CERTIFICADO"
        # Replay only a decided UNSAT and cap the proof file at 256 MiB.
        try:
            with (OUT / f"cubo-{i}-prova.log").open("w") as f:
                replay = subprocess.run(
                    ["bash", "-c", 'ulimit -f 262144; exec "$@"', "_", "./cadical",
                     "-t", str(seconds), cnf, proof], stdout=f, stderr=subprocess.STDOUT,
                    timeout=seconds + 20)
            if replay.returncode == 20 and proof.exists():
                verified = subprocess.run(["./drat-trim", cnf, proof, "-t", "300"],
                                          capture_output=True, text=True, timeout=320)
                (OUT / f"cubo-{i}-drat.log").write_text(verified.stdout + verified.stderr)
                if verified.returncode == 0 and "s VERIFIED" in verified.stdout:
                    record["resultado"] = "UNSAT_VERIFICADO"
        except subprocess.TimeoutExpired:
            pass
        if record["resultado"] != "UNSAT_VERIFICADO":
            proof.unlink(missing_ok=True)
    elif process and process.returncode != 0:
        record["resultado"] = "ERRO_SOLVER"
    (OUT / f"cubo-{i}.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record), flush=True)
    return record


def main():
    seconds = int(sys.argv[1])
    OUT.mkdir(exist_ok=True)
    generate()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(solve, cube, seconds) for cube in CUBES]
        results = [future.result() for future in futures]
    (OUT / "resumo.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
