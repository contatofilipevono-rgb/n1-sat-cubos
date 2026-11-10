# Missão "pares de posto conjunto menor" (caso misto do Lema L, F4+F4): rodada 1 (10/11)

**Execução.**
- Rodou no PC local. A missão previa 40 vCPUs, mas não foi preciso: a etapa 1 leva cerca de 34 s por semente e a etapa 2 cerca de 15 s por plano.
- Código: beta_posto.py e radical_grau8.py do pacote, sem alteração; fonte/ igual ao commit 8bf789a.
- Os artefatos estão aqui, porque não há acesso local à conta filipemvono-ops.

**Etapa 1** (sementes 18001 a 18040, 32 cúbicas iniciais cada):
- 1280 cúbicas a ∈ N, cada uma com cobertura exata em b;
- 1550 pares (a,b) com a, b, a+b ∈ N, β(a,b) = 0 e posto conjunto menor;
- **775 planos distintos**: dim C/G = 21 em 684 e 22 em 91.

**Etapa 2** (para cada plano, as 1024 escolhas de A₁₂; radical inteiro de Ω_A com as translações por 0, a, b, a+b):
- 793.600 escolhas no total;
- dimensões do radical: {2: 38811, 3: 587391, 4: 52242, 5: 112080, 6: 2092, 7: 945, 8: 36, **10: 3**}. Os radicais de dimensão 8 e 10 são novos em relação à rodada anterior;
- conferência pela eliminação original: 984 radicais de dimensão ≥ 7 e 13.370 controles amostrais. Todos bateram, sem falha de assert.
- **Trios encontrados: 0.**

**Alcance.** A cobertura é exata para os 775 planos listados em consolidado.json, que vêm de um conjunto amostrado de 1280 vetores a. Não é exclusão do caso misto. O lema misto e p=17 seguem abertos.

**Nota.** Os 3 radicais de dimensão 10 são os casos mais "frouxos" achados até agora: muitas escolhas de φ₃ e, ainda assim, nenhuma com as 7 combinações em N. São bons candidatos para entender a estrutura (planos e A₁₂ listados em rad-*.json, no campo directly_verified_radicals...).