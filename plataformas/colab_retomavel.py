# Colab gratuito (2 nucleos), generico: definir antes CLASSE, AUTO, ORB, K, TMAX (s por cubo), HMAX (h).
# Ex.: CLASSE,AUTO,ORB,K,TMAX,HMAX='Q4a','automorfismos_Q4a.json','0,1',8,3000,70
# Se o Drive ja estiver montado, copia resultados para MyDrive/n1_inst_09nov/<CLASSE>_o<ORB>_k<K> e retoma de la.
# Sem Drive, tudo fica em /content e o SAT completo e impresso na saida da celula.
# Encerra o runtime em: rodada completa, SAT encontrado ou HMAX horas.
import subprocess, os, time, glob, json, shutil
NOME = f"{CLASSE}_o{ORB.replace(',', '')}_k{K}"
D = f'/content/drive/MyDrive/n1_inst_09nov/{NOME}' if os.path.isdir('/content/drive/MyDrive') else None
if D: os.makedirs(D + '/res', exist_ok=True)
R = '/content/repo'
if not os.path.isdir(R):
    subprocess.run(f'git clone -q --depth 1 https://github.com/contatofilipevono-rgb/n1-sat-cubos.git {R}', shell=True, check=True)
os.makedirs(R + '/res', exist_ok=True); os.makedirs(R + '/inst', exist_ok=True)
if D:
    for f in glob.glob(D + '/res/cubo_*.json'): shutil.copy(f, R + '/res')
    if os.path.exists(D + '/cubos.json') and not os.path.exists(R + '/inst/cubos.json'): shutil.copy(D + '/cubos.json', R + '/inst')
H0 = json.load(open(D + '/RESUMO.json')).get('horas_acumuladas', 0) if D and os.path.exists(D + '/RESUMO.json') else 0
N = 2 ** K
SH = f'''set -u
cd /content/repo
pip -q install python-sat numpy > /dev/null 2>&1
[ -x cadical ] || {{ git clone -q --depth 1 https://github.com/arminbiere/cadical.git cad && (cd cad && ./configure -q && make -s -j2) && cp cad/build/cadical ./cadical; }}
[ -x drat-trim ] || {{ curl -sL https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c -o drat-trim.c && gcc -O2 -o drat-trim drat-trim.c; }}
python - <<'EOF'
n, m = 7, 6
v = lambda i, j: i * m + j + 1
cl = [[v(i, j) for j in range(m)] for i in range(n)] + [[-v(i, j), -v(k, j)] for j in range(m) for i in range(n) for k in range(i + 1, n)]
open("php.cnf", "w").write(f"p cnf {{n*m}} {{len(cl)}}\\n" + "".join(" ".join(map(str, c)) + " 0\\n" for c in cl))
EOF
./cadical php.cnf php.drat > /dev/null; ./drat-trim php.cnf php.drat | grep -q "s VERIFIED" && echo "controle DRAT: VERIFIED" || {{ echo "controle DRAT FALHOU"; exit 1; }}
[ -f inst/cubos.json ] || python cubo.py gera {CLASSE} {AUTO} {ORB} {K} inst
seq 0 {N - 1} | xargs -P 2 -I{{}} bash -c '[ -f res/cubo_{{}}.json ] || bash resolve_lote.sh inst {{}} 1 {TMAX} 1800 > /dev/null'
echo FIM
'''
open('/content/run.sh', 'w').write(SH)
if not os.path.exists('/content/iniciado'):
    open('/content/iniciado', 'w').write('1')
    subprocess.Popen(['bash', '/content/run.sh'], stdout=open('/content/run.log', 'a'), stderr=subprocess.STDOUT, start_new_session=True)
T0 = time.time()
from IPython.display import clear_output
while True:
    r = [json.load(open(f)) for f in glob.glob(R + '/res/cubo_*.json')]
    log = open('/content/run.log').read()
    sat = [x for x in r if x['resultado'] == 'SAT']
    h = round(H0 + (time.time() - T0) / 3600, 2)
    motivo = 'rodada terminou' if log.rstrip().endswith('FIM') else ('SAT encontrado' if sat else (f'limite {HMAX}h' if h > HMAX else None))
    res = {'classe': CLASSE, 'orbitas': ORB, 'k': K, 'cubos': N,
           'UNSAT_verificados': sum(1 for x in r if x['resultado'] == 'UNSAT' and x.get('drat_verificado')),
           'UNSAT_sem_verificacao': sum(1 for x in r if x['resultado'] == 'UNSAT' and not x.get('drat_verificado')),
           'SAT': [x['cubo'] for x in r if x['resultado'] == 'SAT'],
           'INDECISO': len([x for x in r if x['resultado'] == 'INDECISO']),
           'horas_acumuladas': h, 'encerrado_por': motivo, 'utc': time.strftime('%Y-%m-%d %H:%M:%S')}
    if D:
        for f in glob.glob(R + '/res/cubo_*.json'): shutil.copy(f, D + '/res')
        if os.path.exists(R + '/inst/cubos.json'): shutil.copy(R + '/inst/cubos.json', D)
        shutil.copy('/content/run.log', D + '/run_ultimo.log')
        json.dump(res, open(D + '/RESUMO.json', 'w'), indent=1)
    clear_output(wait=True)
    print(time.strftime('%H:%M:%S UTC'), subprocess.run('tail -2 /content/run.log; echo cadical: $(pgrep -c -x cadical)', shell=True, capture_output=True, text=True).stdout)
    print('RESUMO', json.dumps(res))
    for x in sat: print('SAT', json.dumps(x))
    if motivo:
        print('ENCERRANDO:', motivo); time.sleep(20)
        subprocess.run('pkill -x cadical; pkill -f resolve_lote.sh', shell=True)
        if motivo != 'SAT encontrado' or D:
            from google.colab import runtime; runtime.unassign()
        break
    time.sleep(180)
