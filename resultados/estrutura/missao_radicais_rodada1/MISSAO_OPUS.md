# Missão para o Opus — pares de posto conjunto menor em \(F_4+F_4\)

Use as 40 vCPUs para buscar um trio no caso misto do Lema L. O recorte é o de pares \(a,b\) para os quais \(a,b,a+b\in N\), \(\beta(a,b)=0\) e \(\dim C_{ab}/G>20\). A frente do Fable trata o ramo par de \(p=17\). A enumeração de \(n=12\) está no GitHub.

## Ponto de partida

O pacote contém a geometria de \(F_4+F_4\), a prova da redução a formas alternadas e dois verificadores. Em \(N\), o posto individual de \(\beta(a,\cdot)\) é 10, por uma checagem dos 1.023 radicais. Já encontramos oito planos com \(\dim C_{ab}/G\) igual a 21 ou 22. Neles apareceram cinco radicais de dimensão 7. O grau oito de \(I6\) e as sete condições de ausência de isotrópico foram testados conjuntamente em todas as 1.024 escolhas de \(A_{12}\) de cada um desses oito planos, com zero trios.

## Primeira rodada

- Use as sementes de 18001 a 18040 e 32 cúbicas iniciais amostradas por semente. Use até 40 processos, com um thread de BLAS por processo. Guarde um JSON por semente para permitir retomada.
- Para cada \(a\in N\), enumere os 1.023 valores não nulos de \(\mu\). Resolva \(B_\mu b=B_\lambda a\) e \(\beta(a,b)=0\) como um sistema linear em \(b,\lambda\). Filtre \(b,a+b\in N\). A cobertura é exata em \(b\) para cada \(a\) escolhido.
- Agrupe e deduplique os planos pela tripla ordenada \(\{a,b,a+b\}\) antes de distribuir a segunda etapa. Para cada plano distinto, use a matriz alternada \(\Omega_A\) para as 1.024 escolhas de \(A=A_{12}\). Teste o radical inteiro, com as quatro translações por \(0,a,b,a+b\).
- Registre quantidades por semente, dimensões de \(C_{ab}/G\), histogramas dos radicais e tempo. Depois de 20 minutos, preserve o que estiver completo e informe a cobertura, inclusive se a rodada fechar antes.

~~~text
python beta_posto.py fonte rank-18001.json --seed 18001 --sampled-first-cubics 32
python radical_grau8.py fonte radicais.json --rank-audit rank-consolidado.json
~~~

O segundo comando aceita o campo sampled_pair_rank do relatório de posto. Para paralelizar essa etapa, distribua os planos distintos em relatórios desse formato. O arquivo LEIA.md contém as equações e as dependências.

## Se aparecer um trio

1. Confira por eliminação independente o grau oito completo de \(I6\) e confira as sete restrições. Salve \(a,b,c\) e os suportes de \(A_{12}\).
2. Resolva para \(A_{13},A_{23},B\) e teste a extensão completa a \(I6\land I7\) com \(R\) de grau até três. Guarde a ANF e refaça Möbius nos 2.048 pontos para qualquer SAT. Para qualquer UNSAT apresentado como certificado, guarde CNF, DRAT e a verificação do DRAT.
3. Qualquer afirmação de ausência de queda em codimensão 5 precisa cobrir todos os postos de projeção em \(x_1,x_2,x_3\), inclusive levantamentos inclinados.
4. Salve checkpoints e resultados em artefatos da conta filipemvono-ops. Preserve ESTADO.md e resultados/. Um teste sem testemunha neste conjunto amostrado de \(a\) encerra apenas a cobertura informada.

