# Bloco de dimensão quatro — resultados de 10/11

Separação usada abaixo: **[D]** demonstrado; **[C]** conferido por computação exaustiva ou álgebra linear exata; **[O]** observado nos dados, sem prova.

## 1. Lema das fibras

**[D]** O lema proposto vale: sinais com Walsh de amplitude 4 existem se e só se C ⊆ C^⊥ e k ≤ 7, e são 2^{15−k} − 128. Prova em `LEMA_FIBRAS_16.md`; força bruta em `verifica_lema_fibras.py`.

Formas usadas na enumeração:
- **[D]** C ⊆ C^⊥ ⇔ toda função de grau ≤ 2 tem soma nula na fibra.
- **[D]** h é admissível ⇔ h·c = wt(c)/2 numa base de C (linear) e wt(h) ≡ 2 (mod 4) (uma condição quadrática, e₂(h) = 1).

## 2. Espaços

**[C]** `base4.py`:

| | V1 = ⟨7,14,28,56⟩ | V2 = ⟨5,10,20,40⟩ |
|---|---|---|
| espaço RS afim em V | 52 | 52 |
| dimensão de π | 33 | 31 |
| núcleo de H | 19 | 21 |
| dimensão de (q₁,q₂) | 8 | 8 |
| dimensão de π₀ | 25 | 23 |

Aqui π(z,s) = π₀(z) + s₁q₁(z) + s₂q₂(z).

**[D]** Critérios de separação:
- V2: f é afim em U ⇔ q₁ = q₂; antipodal ⇔ q₁ = q₂ = 0. Não depende de H.
- V1: f é afim em U ⇔ q₁ e q₂ só tomam os valores 0 e 1111, e o coeficiente b(z) de s₁s₂ em H é t₁+t₂, com q_a = t_a·1111. Depende da fase.

## 3. V2

**[C]** Enumeração exaustiva dos 2³¹ mapas (`Enumera.cs`), fases em `fases.py`:

| etapa | mapas |
|---|---|
| todas as fibras com 16 pontos | 5.612.360 |
| auto-ortogonais | 166.472 |
| destes: antipodal (q₁ = q₂ = 0) | 132.152 |
| destes: bloco U (q₁ = q₂ ≠ 0) | 17.280 |
| destes: exclusivos | 17.040 |
| exclusivos com alguma fibra de posto 8 | 4.032 |
| exclusivos com sistema linear de fases inconsistente | 10.224 |
| exclusivos mortos pela condição quadrática | 2.016 |
| **exclusivos com fase** | **768** |

**Total: 2.326.528 funções, igual ao catálogo.**

**[C]** As 768 em três tipos de (q₁,q₂). Em todas, q₁(z) e q₂(z) são proporcionais em cada z:

| tipo | wt q₁, q₂, q₁+q₂ | pares (q₁,q₂) | postos das fibras (k: quantas) | mapas × fases | funções |
|---|---|---|---|---|---|
| A | 24, 24, 24 | 2 | 5:1, 6:15 | 192 × 2¹² + 48 × 2¹³ | 1.179.648 |
| B | 36, 36, 24 | 2 | 5:1, 6:3, 7:12 | 384 × 2¹¹ | 786.432 |
| C | 30, 30, 30 | 4 | 5:1, 6:6, 7:9 | 64 × 2¹⁰ + 32 × 2¹¹ + 16 × 2¹¹ + 16 × 2¹² + 16 × 2¹³ | 360.448 |

### 3.1 Forma fechada dos oito pares (q₁, q₂) — **[C]** (`formas_V2.py`)

Notação: s_e(z) e s_o(z) são as paridades das coordenadas de índice par e ímpar de z; s = s_e + s_o; N = I + R³. V2 = {w : s_e(w) = s_o(w) = 0}, K₁ = e₀ (índice par), K₂ = e₁ (índice ímpar). Lembre que q₁ = B_z(e₀,·)|V2 e q₂ = B_z(e₁,·)|V2.

| família | q₁(z) | q₂(z) | mapas | funções |
|---|---|---|---|---|
| C_k, k = 1, 2, 4, 5 | s_o(z)·R^k z | s_e(z)·R^k z | 36 cada | 90.112 cada |
| A_j, j = 1, 2 | s_o(z)·R^j N z | s_e(z)·R^j N z | 120 cada | 589.824 cada |
| B_j, j = 1, 2 | A_j + (1+s(z))·N z | A_j + (1+s(z))·N z | 192 cada | 393.216 cada |

Os 768 mapas caem todos numa dessas oito formas, e a soma dá 2.326.528.

Leitura estrutural:
- Com θ_z = s_o(z)·ε_e + s_e(z)·ε_o, onde ε_e e ε_o são as paridades par e ímpar de w, as três famílias são **B_z = θ_z ∧ Mz** módulo o termo livre em ε_e∧ε_o, com M = R^k (tipo C), M = R^j N (tipo A), ou tipo A somado à forma do bloco U.
- O termo somado no tipo B é exatamente a forma do tipo wt(q) = 24 do bloco U, (1+s(z))·σ∧Nz. **O tipo B é o tipo A deslocado pelo bloco U.**
- O bloco U e os tipos A e B usam N = I + R³, isto é, a diagonal antipodal (v,v). O tipo C usa uma rotação pura R^k com k ∉ {0, 3}.
- Em todos os casos o posto de B_z|_{K×V2} é ≤ 1 em cada z: q₁(z) e q₂(z) são proporcionais.
**[O]** Fatos estruturais:
- Só uma fibra é um flat de dimensão 4. As outras 15 têm dimensão afim 5 ou 6. A classificação não pode presumir fibras planas.
- Nenhuma fibra de posto 8 sobrevive, como o lema exige; elas aparecem em 4.032 mapas auto-ortogonais.
- O número de fases não é o produto dos números por fibra: é 2^d menos o que a condição quadrática corta, com d entre 14 e 18.

**[C]** Testemunhas: uma função de cada uma das 8 linhas (tipo × número de fases) foi reconstruída em F₂¹², com RS, grau exatamente 4, os 4.096 coeficientes de Walsh iguais a ±64, afim em V2 e não afim em U (`testemunhas.py`, `testemunhas_V2.json`). Lista completa dos 768 mapas em `V2_exclusivo_mapas.json`.

## 4. V1

**[C]** Enumeração exaustiva dos 2³³ mapas: 2.630.416 com fibras de 16 pontos, 113.040 auto-ortogonais (`mapas_V1.txt`).

Fases: workflow `bloco-dim4` no GitHub (run 42943488389, 20 fatias, todas concluídas), agregadas por `agrega.py`; resumo em `fases_V1_resumo.txt`.

**[C]** Em V1 a afinidade em U depende da fase, então a separação é feita função a função:

| classe | funções |
|---|---|
| antipodal (B ≡ 0) | 290.062.336 |
| bloco U | 10.485.760 |
| **exclusivo de V1** | **1.900.544** |

- O exclusivo confere com o catálogo, e o bloco U reaparece inteiro dentro de V1 com o mesmo total 10.485.760.
- Nenhum mapa com q₁, q₂ em {0, 1111} dá função exclusiva: as funções exclusivas vêm de 120 mapas próprios.

| postos das fibras (k: quantas) | mapas | fases por mapa | funções |
|---|---|---|---|
| 6:16 | 64 | 2¹⁴ | 1.048.576 |
| 5:2, 6:14 | 16 | 3·2¹³ | 393.216 |
| 5:8, 6:8 | 32 | 2¹³ | 262.144 |
| 5:4, 6:12 | 8 | 3·2¹³ | 196.608 |

**[O]** Em V1 não aparece posto 7; em 64 dos 120 mapas nenhuma fibra é plana. Lista em `V1_exclusivo_mapas.json`. Não reconstruí testemunhas de V1 nem busquei a forma fechada dos seus (q₁,q₂).

**Soma dos dois blocos: 2.326.528 + 1.900.544 = 4.227.072**, o total do catálogo para dimensão quatro.

## 5. Lema geral para os blocos de dimensão três e dois

Para f afim nas classes de V com dim V = r, as fibras têm N = 2^{12−2r} pontos em F₂^{12−r} e a amplitude exigida é 2^{6−r}. Com N = 4^t (t = 2, 3, 4 para r = 4, 3, 2):

- **[D]** Amplitude 2^t em toda frequência ⇔ wt(h+c) ≡ 2^{t−1} (mod 2^t) para todo c ∈ C. A prova é a mesma: a congruência dá |Ŵ| ≥ 2^t e Parseval fecha.
- **[D]** Reduzindo módulo 4: C ⊆ C^⊥ e h·c = wt(c)/2 continuam necessários para todo t ≥ 2. Em particular toda função de grau ≤ 2 tem soma nula em cada fibra, e k ≤ N/2.
- **Não demonstrado:** para t ≥ 3 a congruência módulo 2^t impõe condições de divisibilidade de ordem mais alta (interseções triplas para t = 3), e a contagem de sinais deixa de ser 2^{15−k} − 128. Não derivei a fórmula.

## 6. O que falta

1. Testemunhas e forma fechada dos (q₁,q₂) de V1.
2. Provar à mão que só as formas θ_z∧Mz da seção 3.1 ocorrem (hoje é resultado da enumeração).
3. Explicar d e o corte quadrático por família.
4. O critério de ordem mais alta para t = 3 e t = 4.
