#!/bin/bash
# VM n1-cubos, 09/11/2026: N1 com I6 ∧ I7 (busca de SAT = contraexemplo da versao liftavel) em F4^2, Q4a, Q4b, Q4c,
# todas as orbitas, k=6 (64 cubos por classe), 8 nucleos por classe, ate 20000 s por cubo.
# Idempotente (retoma apos preempcao). Desliga a VM sozinha 48 h apos o primeiro boot deste script (prazo em /opt/i7/PRAZO).
set -u
B=/opt/i7; mkdir -p $B; exec >> $B/startup.log 2>&1
echo "=== boot $(date -u)"
[ -f $B/PRAZO ] || echo $(( $(date +%s) + 48*3600 )) > $B/PRAZO
( while true; do if [ "$(date +%s)" -ge "$(cat $B/PRAZO)" ]; then echo "prazo de 48 h: desligando $(date -u)"; pkill -x cadical; sleep 5; shutdown -h now; fi; sleep 300; done ) &
W=/opt/n1
cd $W/repo && git pull -q || true
export PATH=$W/repo/venv/bin:$PATH
for par in "F4^2:automorfismos_F42.json:0,1,2,3" "Q4a:automorfismos_Q4a.json:0,1,2" "Q4b:automorfismos_Q4b.json:0,1,2" "Q4c:automorfismos_Q4c.json:0,1,2"; do
  IFS=: read -r CL AU OR <<< "$par"
  D=$B/$(echo "$CL" | tr -d '^+')
  ( mkdir -p $D && cd $D
    [ -f cubo.py ] || cp $W/repo/*.py $W/repo/*.sh $W/repo/automorfismos_*.json $D/
    cp $W/ferr/cadical ./cadical; cp $W/ferr/drat-trim ./drat-trim
    [ -f inst/cubos.json ] || N1_I7=1 python cubo.py gera "$CL" "$AU" "$OR" 6 inst > gera.log 2>&1
    mkdir -p res
    pend=$(for i in $(seq 0 63); do f=res/cubo_$i.json; if [ -f $f ] && grep -q '"SAT"\|"UNSAT"' $f; then :; else echo $i; fi; done)
    echo "$CL pendentes: $(echo $pend | wc -w)"
    echo $pend | tr ' ' '\n' | xargs -P 8 -I{} bash resolve_lote.sh inst {} 1 20000 4500 > /dev/null
    echo "$CL fim $(date -u)" ) &
done
wait
echo "=== todas as classes terminaram $(date -u)"
