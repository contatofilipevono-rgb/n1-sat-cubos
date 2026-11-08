#!/bin/bash
# Script de inicializacao da VM (roda como root a cada boot; idempotente: cubos ja resolvidos sao pulados).
# Parametros via metadados: classe, auto, orbitas, k, tempo_cadical, tempo_drat, paralelo
set -u
M() { curl -s -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/attributes/$1"; }
CLASSE=$(M classe); AUTO=$(M auto); ORB=$(M orbitas); K=$(M k); TC=$(M tempo_cadical); TD=$(M tempo_drat); P=$(M paralelo)
W=/opt/n1; mkdir -p $W; cd $W
exec >> $W/startup.log 2>&1
echo "=== boot $(date -u)"
if [ ! -x $W/ferr/cadical ]; then
  apt-get update -qq && apt-get install -y -qq build-essential git python3-venv curl > /dev/null
  mkdir -p ferr && cd ferr
  git clone -q --depth 1 https://github.com/arminbiere/cadical.git && (cd cadical && ./configure -q && make -s -j"$(nproc)") && cp cadical/build/cadical cadical-bin
  curl -sL https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c -o drat-trim.c && gcc -O2 -o drat-trim drat-trim.c
  mv cadical-bin cadical-tmp && rm -rf cadical && mv cadical-tmp cadical
  cd $W
fi
if [ ! -d $W/repo ]; then git clone -q https://github.com/contatofilipevono-rgb/n1-sat-cubos.git repo; fi
cd $W/repo
if [ ! -d venv ]; then python3 -m venv venv && venv/bin/pip install -q python-sat pycryptosat numpy; fi
export PATH=$W/repo/venv/bin:$PATH
cp $W/ferr/cadical ./cadical; cp $W/ferr/drat-trim ./drat-trim
# controle UNSAT com prova verificada (pombos 7 em 6)
python - <<'EOF'
n, m = 7, 6
v = lambda i, j: i * m + j + 1
cl = [[v(i, j) for j in range(m)] for i in range(n)] + [[-v(i, j), -v(k, j)] for j in range(m) for i in range(n) for k in range(i + 1, n)]
open("php.cnf", "w").write(f"p cnf {n*m} {len(cl)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cl))
EOF
./cadical php.cnf php.drat > /dev/null; ./drat-trim php.cnf php.drat | grep -q "s VERIFIED" && echo "controle DRAT: VERIFIED" || { echo "controle DRAT FALHOU"; exit 1; }
[ -f inst/cubos.json ] || python cubo.py gera "$CLASSE" "$AUTO" "$ORB" "$K" inst
N=$(python -c "import json;print(len(json.load(open('inst/cubos.json'))['cubos']))")
mkdir -p res
pendentes=$(for ((i=0;i<N;i++)); do f=res/cubo_$i.json; if [ -f $f ] && grep -q '"SAT"\|"UNSAT"' $f; then :; else echo $i; fi; done)
echo "pendentes: $(echo $pendentes | wc -w) de $N"
echo $pendentes | tr ' ' '\n' | xargs -P "$P" -I{} bash resolve_lote.sh inst {} 1 "$TC" "$TD"
echo "=== fim $(date -u)"
python - <<'EOF'
import json, glob
r = [json.load(open(f)) for f in glob.glob("res/cubo_*.json")]
print({x: sum(1 for c in r if c["resultado"] == x) for x in ("UNSAT", "SAT", "INDECISO")},
      "verificados:", sum(1 for c in r if c.get("drat_verificado") is True))
EOF
touch $W/TERMINOU
