"""Executor generico (Kaggle / Colab / qualquer Linux): N1 em 64 cubos com CaDiCaL + DRAT verificado.
uso: python plataformas/executor.py CLASSE AUTO_JSON ORBITAS [PASTA_SAIDA]
Salva res/cubo_*.json, inst/cubos.json e o log em PASTA_SAIDA (padrao /kaggle/working/n1 se existir /kaggle).
Imprime o placar a cada 5 min (SAT com conferencia; UNSAT so conta com DRAT verificado)."""
import glob
import json
import os
import shutil
import subprocess
import sys
import time

CL, AUTO, ORB = sys.argv[1], sys.argv[2], sys.argv[3]
SAIDA = sys.argv[4] if len(sys.argv) > 4 else ("/kaggle/working/n1" if os.path.isdir("/kaggle") else "/tmp/n1_saida")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(SAIDA, exist_ok=True)

SH = r'''set -u
cd "%s"
pip -q install python-sat pycryptosat numpy > /dev/null 2>&1
[ -x cadical ] || { git clone -q --depth 1 https://github.com/arminbiere/cadical.git cad && (cd cad && ./configure -q && make -s -j$(nproc)) && cp cad/build/cadical ./cadical; }
[ -x drat-trim ] || { curl -sL https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c -o drat-trim.c && gcc -O2 -o drat-trim drat-trim.c; }
python - <<'EOF'
n, m = 7, 6
v = lambda i, j: i * m + j + 1
cl = [[v(i, j) for j in range(m)] for i in range(n)] + [[-v(i, j), -v(k, j)] for j in range(m) for i in range(n) for k in range(i + 1, n)]
open("php.cnf", "w").write(f"p cnf {n*m} {len(cl)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cl))
EOF
./cadical php.cnf php.drat > /dev/null; ./drat-trim php.cnf php.drat | grep -q "s VERIFIED" && echo "controle DRAT: VERIFIED" || { echo "controle DRAT FALHOU"; exit 1; }
[ -f inst/cubos.json ] || python cubo.py gera "%s" %s %s 6 inst
seq 0 63 | xargs -P $(nproc) -I{} bash -c '[ -f res/cubo_{}.json ] && grep -q SAT res/cubo_{}.json || bash resolve_lote.sh inst {} 1 172800 86400 > /dev/null'
echo FIM
''' % (REPO, CL, AUTO, ORB)

open(os.path.join(SAIDA, "run.sh"), "w").write(SH)
log = os.path.join(SAIDA, "run.log")
subprocess.Popen(["bash", os.path.join(SAIDA, "run.sh")], stdout=open(log, "w"), stderr=subprocess.STDOUT,
                 start_new_session=True)
while True:
    fs = glob.glob(os.path.join(REPO, "res", "cubo_*.json"))
    r = [json.load(open(f)) for f in fs]
    os.makedirs(os.path.join(SAIDA, "res"), exist_ok=True)
    for f in fs:
        shutil.copy(f, os.path.join(SAIDA, "res"))
    if os.path.exists(os.path.join(REPO, "inst", "cubos.json")):
        shutil.copy(os.path.join(REPO, "inst", "cubos.json"), SAIDA)
    est = subprocess.run("nproc; tail -3 '%s'; echo cadical: $(pgrep -c -x cadical)" % log, shell=True,
                         capture_output=True, text=True).stdout
    uns = sum(1 for x in r if x["resultado"] == "UNSAT" and x.get("drat_verificado"))
    sat = [x["cubo"] for x in r if x["resultado"] == "SAT"]
    ind = sum(1 for x in r if x["resultado"] == "INDECISO")
    print(time.strftime("%H:%M:%S UTC"), est.replace("\n", " | "), flush=True)
    print(f"PLACAR {CL} orbitas {ORB}: UNSAT_ver={uns} SAT={sat} INDEC={ind} de 64 | saida {SAIDA}", flush=True)
    for x in r:
        if x["resultado"] == "SAT":
            print("SAT", x["cubo"], json.dumps(x["conferencia"]), flush=True)
    if os.path.exists(os.path.join(SAIDA, "FIM")) or "FIM" in open(log).read().splitlines()[-1:]:
        print("FIM", flush=True)
        break
    time.sleep(300)
