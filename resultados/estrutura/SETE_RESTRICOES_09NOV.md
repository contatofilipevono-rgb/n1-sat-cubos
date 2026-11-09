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

## Codificação por Möbius (comparação pedida)

`lift_mobius.py`: tabela-verdade + borboleta de Möbius mod 8 (subtratores de 3 bits).
- Controles: aceita o cubo 62 e rejeita os cubos 28 e 52.
- Tamanho sem as cláusulas de isotropia: **156.712 cláusulas** e 35.138 variáveis, contra 2.949.523 e 739.366 da codificação por pares e triplas (`i7.py`), cerca de 19 vezes menos.
- Tempo até SAT no cubo 62 (F4+F4, órbitas 15+60+240, k=6): em medição (`compara_codificacoes.py`).
