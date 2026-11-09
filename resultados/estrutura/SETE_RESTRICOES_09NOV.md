# Rota das sete restrições para o caso de 3 lineares do Lema L (09/11/2026, noite)

**Status:** em andamento. Nada auditado.

## Ideia

No caso de 3 lineares, Δ = T + x₁φ₁ + x₂φ₂ + x₃φ₃, com T crítico em 8 variáveis.
- A redução antiga fixava x₁ = x₂ = 0 e pedia N1 (codim 3) no que sobra. N1 só com I6 é falso em F4+F4 (testemunha do cubo 52).
- Mas existem **7** restrições desse tipo: (x₁, x₂, x₃) = t·v, com v ∈ F₂³ ∖ {0}. Nelas Δ| = T + t·(Σ vᵢφᵢ).
- Basta **uma** delas ter um U isotrópico de codim 3 para o Lema L sair: codim total ≤ 2 + 3 = 5.
- N1 falha na restrição v ⇔ Σ vᵢφᵢ ∈ N, o conjunto dos C₃ sem U_Y isotrópico.

## Teste (nível C₃ + parte linear de I6; `sete_restricoes.py`, `sete_dim.py`)

**Pergunta.** Existe um subespaço ⟨φ₁, …, φ_d⟩, com cada φᵢ ∧ T = 0, em que **todas** as combinações não nulas estão em N?
- UNSAT para d = 3 implica: alguma das 7 restrições sempre tem isotrópico. O caso de 3 lineares do Lema L sairia para a classe, usando só a parte linear de I6.
- Uma ressalva: falta checar se o modelo "T + Σxᵢφᵢ com T crítico fixo" cobre todos os casos de 3 lineares da cadeia.

| Classe | d | Resultado |
|---|---|---|
| F4+F4 | 2 | **SAT** em 48 s (conferido): N contém planos ⟨φ₁, φ₂⟩ inteiros |
| F4+F4 | 3 | rodando há mais de 70 min (CryptoMiniSat, 4 threads). O salto de dificuldade em relação a d = 2 sugere UNSAT, sem garantia |

## Resultado (09/11, ~20:40 UTC): o lema, só com φ ∧ T = 0, é FALSO em F4+F4

Outra sessão achou um trio explícito: φ₁, φ₂, φ₃ com as 7 combinações em N.
- Pasta local: `sete_restricoes_09nov/`.
- Arquivo: `trio_s22_seed1.json`.
- Método: enumeração exata de N ∩ S num subespaço aleatório S de dimensão 22.

**Conferência independente** (`confere_trio.py`, força bruta da testemunha F4+F4):
- φᵢ ∧ T = 0 para i = 1, 2, 3;
- para cada um dos 7 v ≠ 0, D = T + x·φ_v tem **0 de 788.035** subespaços de codimensão 3 com queda de grau.

**Consequência.** A rota das sete restrições não fecha usando só a parte linear de I6. Para o caso de 3 lineares do Lema L, é preciso:
- (a) usar I6/I7 completos, que acoplam os φᵢ por termos quadráticos; ou
- (b) usar subespaços de codim ≤ 5 que não estejam entre as 7 restrições, por exemplo os que se projetam em dimensão 2 ou 3 nas coordenadas x.

**Próximo teste preciso.** O trio se estende a um Δ = T + Σxᵢφᵢ + R em 11 variáveis com I6 ∧ I7? E tem queda de grau em codim ≤ 5 fora das 7 restrições?

A rodada d=3 de F4+F4 no Colab foi encerrada por redundância. As classes F4², Q4a, Q4b e Q4c seguem no Colab seed.

## Achado (09/11, ~20:45 UTC): o trio TEM queda de grau em codim 5, fora das 7 retas

**Montagem.** Q = T + x₁φ₁ + x₂φ₂ + x₃φ₃ em F₂¹¹, com o trio de F4+F4 (`queda_onze.py`, `confere_queda_k2.py`). Seja k a dimensão da projeção de U em X = ⟨x₁, x₂, x₃⟩.

| k | Subespaços de codim 5 com queda |
|---|---|
| 1 (as 7 retas) | **0**, como esperado |
| 2 (U_Y de dim 4 + 2 direções) | **12.682** (a contagem antiga, 10.844, omitia o plano ⟨x₁+x₂, x₁+x₃⟩ por um erro de filtro em queda_onze.py, corrigido; achado pela sessão 849f53da com sete4.py) |

**Conferência independente de um deles,** por substituição simbólica, sem tabela-verdade:
- dim U = 6, isto é, codim 5;
- projeção em X = ⟨x₁+x₂, x₃⟩;
- **deg(Q|U) = 3**.

Base de U (11 bits; os bits 8..10 são x₁..x₃): 00010110001, 00000000010, 00000010100, 00000001000, 10000100001, 01101100101.

**Controle negativo.** Perturbar φ₁ por uma cúbica aleatória destrói a queda nesse U em 2 de 3 casos.

**Consequências.**
- **O trio não é contraexemplo do Lema L.** A queda em codim ≤ 5 existe, só que fora das 7 restrições.
- Conjectura nova, mais fraca e talvez verdadeira: *para φ₁, φ₂, φ₃ com φᵢ ∧ T = 0, Q sempre tem queda em codim 5 com projeção de dimensão 1 ou 2 em X.* Isso usaria só a parte linear de I6.
- Teste em andamento no Colab tab-7 (`queda_lote.py`):
  - todos os trios do arquivo;
  - 20 trios aleatórios em L para F4+F4;
  - 10 trios aleatórios para cada uma das outras 4 classes.

**Lote (Colab, `queda_lote.py`): todos os 65 casos têm queda em codim 5 (k ≤ 2).** Distribuição:
- F4+F4: 25 casos (os 5 trios do arquivo e 20 trios aleatórios em L);
- F4²: 10 aleatórios;
- Q4a, Q4b, Q4c: 10 aleatórios cada.

Nenhum caso ficou sem queda. Os aleatórios costumam ter queda já com k = 1, e os trios de N têm com k = 2.

**Conjectura reforçada (nível C₃, só com a parte linear de I6).** Para φ₁, φ₂, φ₃ com φᵢ ∧ T = 0, Q = T + Σxᵢφᵢ tem queda de grau em codim 5. Ainda não há prova.

## Achado do GPT (09/11, ~20:50 UTC): o trio nem satisfaz I6

- Tome S = {y0, y1, y2, y3, y4, y6, x1, x2}. Exatamente 3 pares de monômios quárticos disjuntos têm união S, então c_S ≡ 2 (mod 4).
- Nenhum R de grau ≤ 3 corrige isso, porque um quártico mais um monômio de grau ≤ 3 cobre no máximo 7 variáveis.
- Na codificação por Möbius isso dá UNSAT com DRAT verificado. Os controles passaram: φ = 0 é SAT, conferido nos 2.048 pontos, e o controle negativo é rejeitado.
- **Condição nova:** I6 exige também **φᵢ ∧ φⱼ = 0** para cada par i < j. São as condições de |S| = 8 com dois x.
- Então há duas razões independentes para o trio não ser contraexemplo do Lema L:
  1. ele não se estende a I6;
  2. ele tem queda em codim 5 de qualquer forma.
- As próximas buscas de trios devem impor φᵢ ∧ T = 0 **e** φᵢ ∧ φⱼ = 0.

**Correção (sessão 849f53da):** "φᵢ ∧ φⱼ = 0" vale só no modelo **sem termos mistos**. Com xᵢxⱼψᵢⱼ na quártica, a condição de |S| = 8 com dois x é:

> **φᵢ ∧ φⱼ + ψᵢⱼ ∧ T = 0** em Λ⁶Y, ou seja, φᵢ ∧ φⱼ ∈ T ∧ Λ²Y.

- Em F4+F4, T∧ : Λ² → Λ⁶ tem posto 18 (conúcleo de dimensão 10).
- O trio do JSON falha também nessa forma: φᵢ ∧ φⱼ ∉ T∧Λ²Y nos três pares, conferido por eliminação. Logo ele não se estende a I6 em 11 variáveis nem com ψᵢⱼ e x₁x₂x₃ℓ livres.
- Falta conferir se o certificado DRAT do GPT foi gerado no modelo sem ψ.
- No caso misto, a prova trivial quebra: em W = K ⊕ ⟨x₁, x₂, x₃⟩ aparecem ψᵢⱼ|_K (3 coeficientes cada) e ℓ|_K (3), num total de 15 condições sobre K. A contagem heurística de candidatos (cerca de 10⁵ esperados) não é prova.

## Prova do GPT (09/11, ~21 UTC): sem termos mistos em x, o caso de 3 lineares é trivial

**Enunciado.** Toda D = T + Σ xᵢφᵢ + R, com deg R ≤ 3, tem queda de grau em codim 5. Não é preciso nenhuma condição de cunha.

**Prova.**
1. Tome K = ⟨e_{y0}, e_{y1}, c⟩, com dim K = 3. Então T|_K tem grau ≤ 3.
2. O coeficiente cúbico de φᵢ|_K é a forma trilinear φᵢ(e_{y0}, e_{y1}, c), linear em c.
3. Com c ∈ ⟨e_{y2}, …, e_{y7}⟩, são 3 equações em 6 incógnitas, logo existe c ≠ 0 que zera os três coeficientes.
4. Em W = K ⊕ ⟨x₁, x₂, x₃⟩, cada xᵢφᵢ|_K tem grau ≤ 1 + 2 = 3. Como dim W = 6, a codimensão é 5.

**Conferências.**
- Verifiquei o argumento à mão.
- O GPT conferiu os 64 pontos de W nos 5 trios, com c = e_{y3} + e_{y4}.
- Isso bate com a minha busca: em k = 3, ela acha queda logo no primeiro U_Y.

**Consequência.** No modelo T + Σxᵢφᵢ, a pergunta das sete restrições era fraca demais: o caso é trivial em codim 5. **O caso que importa é o das quárticas com termos mistos xᵢxⱼψᵢⱼ** (ψ quadrática) e xᵢxⱼxₖℓ, em que essa construção não garante a queda. O GPT segue nesse caso.

**Encerradas em 09/11, ~21 UTC, por perda de relevância:**
- VM: parada;
- GitHub: F4+F4 com I7, completo e 960, cancelado;
- Colabs tab-4 (15+960 com I7), seed (sete restrições) e tab-7 (lote): desligados.

## Codificação por Möbius (comparação pedida)

`lift_mobius.py`: tabela-verdade + borboleta de Möbius mod 8 (subtratores de 3 bits).
- Controles: aceita o cubo 62 e rejeita os cubos 28 e 52.
- Tamanho sem as cláusulas de isotropia: **156.712 cláusulas** e 35.138 variáveis, contra 2.949.523 e 739.366 da codificação por pares e triplas (`i7.py`), cerca de 19 vezes menos.
- Tempo até SAT no cubo 62 (F4+F4, órbitas 15+60+240, k=6): em medição (`compara_codificacoes.py`).
