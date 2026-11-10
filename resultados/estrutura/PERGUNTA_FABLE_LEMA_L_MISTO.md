# Pergunta para o Fable 5.2: Lema L no caso misto (o que falta para Q≡1, p=17, ramo ímpar)

## Contexto, já estabelecido e verificado

**Cadeia.** No ramo ímpar de p=17 (f: F₂²⁰ → F₂, grau ≤ 4), tudo se reduz ao caso Q≡1, que fecha se valer o **Lema L**:

> D liftável (I6 ∧ I7: c_S ≡ 0 mod 4 para |S| ≥ 6, ≡ 0 mod 8 para |S| ≥ 7) ⇒ a parte quártica Δ cai de grau num subespaço de codimensão ≤ 5.

**O Lema L já vale em:**
- produto + resto de grau ≤ 3;
- produto + 2 lineares (Teorema A⁺).

**Falta:** produto + 3 lineares, e as quárticas que não são produto.

**Caso de 3 lineares SEM termos mistos** (Δ = T + Σ xᵢφᵢ, T crítica em 8 variáveis): é trivial.
- Tome K = ⟨e₀, e₁, c⟩, com c anulando as três formas trilineares φᵢ(e₀, e₁, ·): são 3 equações em 6 incógnitas, então c existe.
- W = K ⊕ ⟨x₁, x₂, x₃⟩ tem codim 5 e queda de grau, para qualquer R.

**Caso MISTO, o aberto:** Δ = T + Σ xᵢφᵢ + Σ_{i<j} xᵢxⱼAᵢⱼ + x₁x₂x₃B, com Aᵢⱼ quadráticas e B linear.

**O que I6 exige no grau 8 (exato):**
- φᵢ ∧ T = 0;
- φᵢ ∧ φⱼ = T ∧ Aᵢⱼ;
- T∧B + φ₁∧A₂₃ + φ₂∧A₁₃ + φ₃∧A₁₂ = 0.

Com L = ker(T∧) ∩ Λ³ (dim 48), G = ι_Y T (dim 8) e J = T∧Λ² (dim 18, codim 10 em Λ⁶), isso dá β([φᵢ], [φⱼ]) = φᵢ∧φⱼ mod J = 0. O mapa β: Λ²(L/G) → Λ⁶/J tem posto 10.

**Fatos computacionais em F4+F4 (todos conferidos):**
- N1 só com I6 é FALSO: há um D em 9 variáveis com I6 e sem nenhum subespaço de codim 3 com queda de grau. Força bruta sobre os 788.035 subespaços. Esse D não satisfaz I7.
- I7 não acrescenta nenhuma condição linear nem quadrática que envolva só C₃. O efeito de I7 passa pela parte R.
- Existem pares (φ₁, φ₂) com β = 0 e todas as retas sem subespaço isotrópico.
- Busca de trios com β = 0 e as 7 retas sem isotrópico:
  - por amostragem aleatória (22 sementes): zero trios;
  - busca dirigida (para cada par com β = 0, varre o subespaço linear C_ab de dimensão cerca de 20): em andamento.
- Mesmo quando as 7 retas falham, aparecem quedas em codim 5 com projeção de dimensão 2 ou 3 nos x.

## Pergunta

1. **Que argumento você sugere para o caso misto?** A construção trivial quebra porque, em W = K ⊕ X, os termos Aᵢⱼ|_K e B|_K geram 15 condições. Há uma escolha de K, de dimensão 3, com levantamentos inclinados xᵢ + uᵢ, que force a queda usando as três equações do grau 8 (φᵢ∧φⱼ = T∧Aᵢⱼ etc.)?
2. **Contagem.** Há cerca de 97 mil escolhas de K e 32³ de inclinações, contra 15 condições. Existe um argumento de contagem ou de dimensão que vire prova, por exemplo via Chevalley–Warning ou via um posto de um sistema que nunca se degenera?
3. **Experimento.** Se você acha que o caso misto pode ser falso, que contraexemplo ou que experimento computacional você faria primeiro?

Responda com passos verificáveis. Diga claramente o que é prova e o que é heurística.
