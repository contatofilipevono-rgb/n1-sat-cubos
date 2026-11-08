#!/usr/bin/env bash
# Resolve os cubos I0..I0+N-1 em paralelo (um por nucleo) com CaDiCaL; UNSAT => prova DRAT verificada por drat-trim;
# SAT => modelo conferido por cubo.py confere.  Saida: res/cubo_<i>.json
# uso: resolve_lote.sh INST_DIR I0 N TEMPO_CADICAL_S TEMPO_DRAT_S
set -u
INST=$1; I0=$2; N=$3; TC=$4; TD=$5
mkdir -p res work
TOTAL=$(python -c "import json;print(len(json.load(open('$INST/cubos.json'))['cubos']))")
um() {
  i=$1
  python cubo.py cnf_cubo "$INST" "$i" "work/c$i.cnf"
  t0=$(date +%s)
  ./cadical -q -t "$TC" "work/c$i.cnf" "work/p$i.drat" > "work/s$i.txt"; rc=$?
  t1=$(date +%s)
  if [ $rc -eq 20 ]; then
    out=$(./drat-trim "work/c$i.cnf" "work/p$i.drat" -t "$TD" 2>&1 | tail -5)
    t2=$(date +%s)
    if echo "$out" | grep -q "s VERIFIED"; then ver=true; else ver=false; fi
    tam=$(stat -c %s "work/p$i.drat")
    echo "{\"cubo\": $i, \"resultado\": \"UNSAT\", \"tempo_cadical_s\": $((t1-t0)), \"drat_verificado\": $ver, \"tempo_drat_s\": $((t2-t1)), \"bytes_prova\": $tam}" > "res/cubo_$i.json"
  elif [ $rc -eq 10 ]; then
    conf=$(python cubo.py confere "$INST" "work/s$i.txt" | tail -1)
    echo "{\"cubo\": $i, \"resultado\": \"SAT\", \"tempo_cadical_s\": $((t1-t0)), \"conferencia\": $conf}" > "res/cubo_$i.json"
  else
    echo "{\"cubo\": $i, \"resultado\": \"INDECISO\", \"tempo_cadical_s\": $((t1-t0)), \"rc\": $rc}" > "res/cubo_$i.json"
  fi
  rm -f "work/p$i.drat" "work/c$i.cnf"
  cat "res/cubo_$i.json"
}
pids=()
for ((i=I0; i<I0+N && i<TOTAL; i++)); do um "$i" & pids+=($!); done
for p in "${pids[@]}"; do wait "$p"; done
