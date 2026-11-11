# Lema das fibras de 16 pontos — auditoria e prova (10/11)

**Status.** O lema proposto está correto. Prova completa abaixo, conferida por força bruta (`verifica_lema_fibras.py`). Sem auditoria externa. A ligação com sombras de códigos é de memória, não conferi a fonte.

## Enunciado

Seja P ⊂ F₂⁸ com 16 pontos distintos e C ⊂ F₂¹⁶ o código gerado pela constante 𝟏 e pelas oito coordenadas avaliadas em P; k = dim C = 1 + dim afim de P. Para h ∈ F₂¹⁶ ponha

Ŵ_h(α) = Σ_{x∈P} (−1)^{h(x)+α·x}.

**Lema.** Existe h com |Ŵ_h(α)| = 4 para todo α ∈ F₂⁸ se e só se C ⊆ C^⊥ e k ≤ 7. Se C ⊆ C^⊥, o número de tais h é 2^{15−k} − 128.

| dimensão afim de P | k | escolhas de sinais |
|---|---|---|
| 4 | 5 | 896 |
| 5 | 6 | 384 |
| 6 | 7 | 128 |
| 7 | 8 | 0 |

## Prova

**Passo 1: reformulação em pesos.** Para c_α = (α·x)_{x∈P}, Ŵ_h(α) = 16 − 2·wt(h + c_α). Como 𝟏 ∈ C e wt(h+c+𝟏) = 16 − wt(h+c), a condição é

(∗) wt(h + c) ∈ {6, 10} para todo c ∈ C.

**Passo 2: basta a congruência.** (∗) equivale a

(∗∗) wt(h + c) ≡ 2 (mod 4) para todo c ∈ C.

- (∗) ⇒ (∗∗) é imediato.
- (∗∗) ⇒ (∗): (∗∗) dá Ŵ_h(α) ∈ {±4, ±12}, logo Ŵ_h(α)² ≥ 16. Como os 16 pontos são distintos, Parseval dá Σ_α Ŵ_h(α)² = 2⁸·16, isto é, média 16. Então Ŵ_h(α)² = 16 sempre.

A distinção dos pontos entra só aqui.

**Passo 3: (∗∗) em três condições.** Com wt(h+c) = wt(h) + wt(c) − 2|h∩c|:
- c = 0: wt(h) ≡ 2 (mod 4);
- em geral: wt(c) é par e h·c ≡ wt(c)/2 (mod 2).

Chame φ(c) = wt(c)/2 mod 2. Como h·c é linear em c, φ tem de ser linear em C. De wt(c+c′) = wt(c) + wt(c′) − 2|c∩c′| sai φ(c+c′) = φ(c) + φ(c′) + |c∩c′|. Logo φ é linear se e só se |c∩c′| é par para todos c, c′ ∈ C. Junto com os pesos pares, isso é C ⊆ C^⊥.

Portanto (∗∗) ⇔ C ⊆ C^⊥, h·c = φ(c) em C, e wt(h) ≡ 2 (mod 4).

**Passo 4: o trasladado.** Se C ⊆ C^⊥, as soluções de h·c = φ(c) formam h₀ + C^⊥, com 2^{16−k} elementos. Como 𝟏 ∈ C e φ(𝟏) = 0, todas têm peso par.

**Passo 5: contagem.** Para h de peso par, i^{wt(h)} = (−1)^{wt(h)/2}. Por Poisson no trasladado,

Σ_{h∈h₀+C^⊥} i^{wt(h)} = 2^{−k} Σ_{c∈C} (−1)^{h₀·c} · Σ_{h∈F₂¹⁶} i^{wt(h)}(−1)^{c·h}.

A soma interna fatora: (1+i)^{16−wt(c)}(1−i)^{wt(c)} = 256·(−i)^{wt(c)} = 256·(−1)^{φ(c)} para c ∈ C. E (−1)^{h₀·c} = (−1)^{φ(c)}. Cada termo vale 256, e a soma total é 256.

Se N₀ e N₂ contam os h do trasladado com peso ≡ 0 e ≡ 2 (mod 4), então N₀ − N₂ = 256 e N₀ + N₂ = 2^{16−k}. Logo N₂ = 2^{15−k} − 128. ∎

**Caso autodual k = 8.** N₂ = 0: o trasladado h₀ + C tem todos os pesos ≡ 0 (mod 4). Se C é duplamente par, φ = 0 e o trasladado é o próprio C. Se não, é a sombra de C, e o resultado é a congruência conhecida dos pesos da sombra (n/2 mod 4, com n = 16).

## Forma equivalente, útil na enumeração

C ⊆ C^⊥ equivale a: **toda função de grau ≤ 2 tem soma nula em P** (módulo 2). Em coordenadas: Σ_P 1 = 0, Σ_P x_i = 0 e Σ_P x_i x_j = 0.

E as fases: h é admissível se e só se
- h·c = wt(c)/2 para c numa base de C (k equações lineares em h), e
- e₂(h) = Σ_{x<x′} h(x)h(x′) = 1 (uma equação quadrática), pois para peso par wt(h)/2 ≡ e₂(h) (mod 2).

## O que é literatura e o que foi deduzido

- **Deduzido aqui:** a redução de "amplitude 4" a (∗∗) por Parseval, a equivalência com auto-ortogonalidade, e a contagem 2^{15−k} − 128.
- **Literatura (de memória, não conferida):** o trasladado h₀ + C^⊥ é a sombra no sentido de Conway e Sloane (1990, cota superior para a distância mínima de códigos autoduais), estendida a códigos auto-ortogonais por Brualdi e Pless (1991). A identidade do passo 5 é o cálculo padrão do enumerador da sombra. Não conheço enunciado publicado na forma "conjunto de 16 pontos com espectro plano", mas não fiz busca bibliográfica.

## Conferência

`verifica_lema_fibras.py` conta por força bruta as 2¹⁶ escolhas de sinais em 12 conjuntos P e compara com a fórmula: flats de dimensão 4 (896), dois 3-flats cujas direções se cortam num plano e quatro planos paralelos (384), dois 3-flats cujas direções se cortam numa reta (128), dois 3-flats independentes, que é E₈⊕E₈ (0), e quatro casos não auto-ortogonais (0). Todos conferem.
