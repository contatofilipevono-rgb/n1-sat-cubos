#!/bin/bash
# Q4a, C3 fixo (elemento de N âˆ© L): 16 cubos sobre R3, CaDiCaL com DRAT; pausa 16 cadical do F4^2 (SIGSTOP) e retoma no fim.
mkdir -p /opt/c3fixo && cd /opt/c3fixo
tar -xzf /tmp/c3fixo.tgz
CAD=/opt/n1/repo/cadical; DT=/opt/n1/repo/drat-trim
pgrep -x cadical | grep -v -f <(pgrep -f /opt/c3fixo) | head -16 > pausados.txt
xargs -r kill -STOP < pausados.txt
python3 - <<'EOF'
import json
d = json.load(open("c3fixo_cubos.json"))
base = open("c3fixo_Q4a.cnf").read().split("\n", 1)
nv, nc = base[0].split()[2:4]
for i, cu in enumerate(d["cubos"]):
    open(f"cubo_{i}.cnf", "w").write(f"p cnf {nv} {int(nc) + len(cu)}\n" + base[1] + "".join(f"{l} 0\n" for l in cu))
EOF
for i in $(seq 0 15); do
  ( s=$(date +%s); $CAD cubo_$i.cnf cubo_$i.drat > cubo_$i.out 2>&1; rc=$?; t=$(( $(date +%s) - s ))
    if [ $rc -eq 20 ]; then $DT cubo_$i.cnf cubo_$i.drat -t 20000 > cubo_$i.dt 2>&1; v=$(grep -c "s VERIFIED" cubo_$i.dt); rm -f cubo_$i.drat
      echo "{\"cubo\":$i,\"resultado\":\"UNSAT\",\"tempo_s\":$t,\"drat_verificado\":$([ $v -ge 1 ] && echo true || echo false)}" > cubo_$i.json
    elif [ $rc -eq 10 ]; then rm -f cubo_$i.drat; echo "{\"cubo\":$i,\"resultado\":\"SAT\",\"tempo_s\":$t}" > cubo_$i.json
    else echo "{\"cubo\":$i,\"resultado\":\"rc$rc\",\"tempo_s\":$t}" > cubo_$i.json; fi ) &
done
wait
xargs -r kill -CONT < pausados.txt
echo FIM > fim.txt
