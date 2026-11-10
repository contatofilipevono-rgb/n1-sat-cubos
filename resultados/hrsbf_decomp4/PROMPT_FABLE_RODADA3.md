# Prompt para o Fable 5.2 (10/11, 3ª rodada): conferência do teorema b₀₁₂ = b₀₂₄ + ramo par de p = 17

## Parte A: o que conferi da sua última resposta

1. **Teorema b₀₁₂ = b₀₂₄ (n = 12): os passos verificáveis conferem.**
   - Passo 1: a classe w = 𝟏 tem 64 pontos, em órbitas de tamanhos [4, 12, 12, 12, 12, 12]. Logo s ≡ 0 (mod 8).
   - Passos 3–4: em todas as 256 funções G (RS, grau ≤ 3, 6 variáveis), W_G(𝟏) ≡ 0 (mod 8) ⇔ b₀₁₂ = b₀₂₄, com 0 violações.
   - O passo 2 (Poisson com h = g̃) é o que eu já tinha provado: s_g(w) = W_{G̃}(w).
   - Aceito a prova. Ainda falta uma leitura humana.
2. **O corolário n = 8 é MAIS forte do que você enunciou.** Em G quadrática RS de 4 variáveis:

   | termos de G | W(𝟏) |
   |---|---|
   | b₀₂ = 1 | ±4 |
   | b₀₁ = 1, b₀₂ = 0 | ±8 |
   | só linear ou nada | 0 ou ±16 |

   Como W_G(𝟏) ≡ 0 (mod 16), isso força **b₀₁ = b₀₂ = 0**, isto é, **g|_E é afim** em toda RS bent de 8 variáveis. Conferi nos dados exaustivos: nenhuma das 7552 RS bent de n = 8 contém x₀x₁x₄x₅ nem x₀x₂x₄x₆.
   - Pergunta: em n = 12, o seu argumento mais o caso 2 dão alguma informação análoga sobre o posto de G?
3. **A lista do SAT para n = 12 fica:** b₀₃ = 0 (a regra) e b₀₁₃ = b₀₂₃. Nos índices do Astra, {0,1,4} é a mesma órbita que {0,2,3}.

## Parte A, próximos passos sugeridos
- **(a)** A sua ideia com E₁ = ((x+1)⁴(x²+x+1)) e E₂ = ((x²+x+1)³), onde E₁^⊥ = E₂. Falta uma cota de grau para g̃|_{E₂}, análoga ao Lema 1. Se sair, tente a relação 3 ou b₀₃ = 0.
- **(b)** Mod 16: você provou W_G(w) ≡ W_G(0) + 8κ·wt(w), com κ = (b₁+b₂+b₃)(b₀₁₃+b₀₁₄). Do lado das órbitas, a classe w tem tamanhos conhecidos. Existe alguma classe w em que a 2-parte do grupo age livremente com órbitas de tamanho 8 ou 16? Se existir, o mod 16 fecha.
- **(c)** Caso 2 da redução mod 3 (g|_{P₄} = afim + δ). Já sabemos que o caso 2 implica g(0) ≠ g(𝟏). Uma pergunta concreta: G = g|_E pode ser bent em 6 variáveis? Se não puder, o caso 2 morre?

---

## Parte B: ramo par de p = 17 (o prompt que você pediu, completo)
# Prompt para o Fable 5.2: ramo par de p = 17 (o que falta fechar)

Contexto: pesquisa local, nada publicado. Peço provas verificáveis, com prova e heurística claramente separadas. Não declare p = 17 resolvido.

## Problema

Seja g: F₂²⁰ → F₂ de grau ≤ 4, com W(u) = Σₓ (−1)^{g(x)+u·x} e W(u)² ≡ 2²⁰ (mod 17) para todo u. Queremos provar que g é bent.

Escreva k = W/32. O **ramo par** é k par para todo u. O ramo ímpar já foi reduzido ao caso Q ≡ 1, que está em outra frente; não trate dele.

## Notação do ramo par

Esta é a notação da nota de reparo, auditada por modelo.
- Na região S₁ = {β₁ = 1}, k = 32ε + 34s. Ponha σ = (−1)^{β₂} e s₀ = σs ≡ 1 (mod 4).
- O excesso é exc = k² − 4. Por Parseval, E_{S₁} k² ≤ 1024, logo o orçamento médio é E_{S₁} exc ≤ 1020.
- Os bits βᵢ são as funções de bit de k. Defina D = β₃ ⊕ β₂, E = β₄ ⊕ β₂ e H = β₅ ⊕ β₂.
- Pela filtração 2-ádica, deg D ≤ 4. Restrita a flats contidos em {D = 0}, E tem grau ≤ 6; restrita a flats contidos em {D = E = 0}, H tem grau ≤ 8.
- Congruências, válidas também para inteiros negativos:

| condição | excesso mínimo |
|---|---:|
| D = 1 | exc ≥ 4896 |
| D = 0, E = 1 | exc ≥ 42432 |
| D = E = 0, H = 1 | exc ≥ 228480 |
| D = E = H = 0 e \|s\| ≠ 1 | exc ≥ 1044480 |

## Ferramentas já disponíveis (auditadas)

- **Folha Ω = {D = E = H = 0}.** Se F ⊂ Ω tem codimensão c e E_F exc ≤ B, então E_F Y ≥ 2 − B/1020, com Y = σk. A cota de Fourier dá |E_F Y| ≤ 2^{c+h}/32, onde 2h é o posto da polar de β₂|_F. Logo é preciso posto ≥ 6.
- **Contradição de Poisson.** Num subespaço não degenerado de dimensão 6, alguma classe tem ponto com exc ≥ 1044480, de modo que E_F exc ≥ 16320. Toda folha com B < 16320 e posto ≥ 6 é impossível.
- **Coberturas.** Um flat Z de codimensão r é evitado por 2^r − 1 hiperplanos, com fator de orçamento 2^r/(2^r − 1). Para D = A ⊕ B, dois produtos quárticos em blocos independentes, há 225 flats de codimensão 2 e fator 256/225.
- **Casos já fechados** (todos os orçamentos < 16320):
  - D = 0;
  - D um flat de peso 1/16;
  - D com hiperplano de zeros e peso ≥ 3/32;
  - D = A ⊕ B, de peso 15/128.
- **Teorema P′.** Fecha o caso em que D tem flat de zeros de codimensão ≤ 2 **e** a polar de β₂ em S₁ tem posto ≥ 18. Os orçamentos são 1632 → 1938 → 2091, com Kasami–Tokura–Azumi (KTA) nos níveis E e H.
- **Dependências externas:** divisibilidade espectral de funções de grau ≤ 4; primeiros pesos de Reed–Muller; Kasami–Tokura; KTA, que dá um flat de zeros de codimensão ≤ 2 quando wt < 5/32.

## O que resta (alvo)

> **Ramo par residual.** D ≠ 0, de grau ≤ 4, **sem hiperplano de zeros**, com **1/8 ≤ wt_{S₁}(D) ≤ 5/24**, fora das hipóteses de P′. Isso inclui:
> - (i) wt(D) ∈ [5/32, 5/24], onde KTA não fornece o flat;
> - (ii) posto de β₂ < 18.

## Perguntas

1. **Peso.** Existe um argumento de orçamento ou de cobertura que feche D de grau ≤ 4 sem hiperplano de zeros com peso em [1/8, 5/24]?
   - Use a classificação de RM(4,20) até 5/24 se ela for conhecida (Kasami–Tokura–Azumi vai até 2,5·d_min).
   - Ou use um análogo de "flat de zeros de codimensão ≤ 3", aceitando um fator de cobertura pior: 8/7 por nível. Diga se o orçamento ainda fica abaixo de 16320.
2. **Posto baixo de β₂ (< 18).** O que acontece quando a quadrática β₂ restrita a S₁ tem posto pequeno? Há uma redução a menos variáveis (a parte afim de β₂) que permita repetir a árvore em dimensão menor?
3. **Orçamento.** Estime B₀, B₁ e B₂ no pior caso de (i) com flats de codimensão 3 e diga se fecha abaixo de 16320. Seja explícito nas frações.
4. **Contraexemplo.** Se achar que o caso residual pode ser realizável, que teste computacional exato faria? Por exemplo, um modelo local em poucas variáveis com D fixo e as congruências de bits.

Responda com passos verificáveis e frações exatas. Separe o que é prova do que depende de resultados externos (KT, KTA) e do que é heurística.
