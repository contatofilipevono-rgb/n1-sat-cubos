# Prompt para o Fable 5.2: provar a conjectura antipodal de complemento (C)

## Notação

- n = 2m. O shift cíclico é ρ, com (ρx)_{i+1} = x_i. Uma função g: F₂ⁿ → F₂ é RS se g∘ρ = g.
- τ = ρ^m é a meia-volta. E = Fix(τ) = {(z,z) : z ∈ F₂^m} é o subespaço antipodal. Vale E^⊥ = E.
- 𝟏 é o vetor de uns; 𝟏 ∈ E.
- G(z) = g(z,z) é a restrição a E; G é RS em m variáveis.
- As classes laterais de E são indexadas por w = x₁ + x₂ ∈ F₂^m, com x = (x₁, x₂).
  - ρ age em w como a rotação cíclica de m bits.
  - Todo vetor da classe w tem paridade de peso wt(w).
- s_g(w) = Σ_{x₁+x₂=w} (-1)^{g(x)} = Σ_{y∈F₂^m} (-1)^{g(y, y+w)}.

## Conjectura

> **(C)** Se g é RS bent em n = 2m variáveis, então g(x+𝟏) = g(x) + m (mod 2) para todo x ∈ E.

Em x = 0, (C) é a regra g(0)+g(𝟏) ≡ n/2. Essa regra já está provada em dois casos:
- n = 2^t, pelo limite de grau;
- n = 2p^a, pela paridade antipodal (congruências mod p nas restrições a vetores periódicos e o critério de classes laterais de E).

Para n = 12, a regra equivale a dizer que nenhuma RS bent contém a órbita x₀x₃x₆x₉. Isso está aberto.

## Já provado: reformulação via Poisson

Como E^⊥ = E, temos s_g(w) = W_{G̃}(w), onde G̃ é a restrição a E da dual g̃. A dual de uma RS bent é RS bent. Logo:

> (C) para todas as RS bent ⇔ **(C')**: toda RS bent g tem s_g(w) = 0 para todo w com wt(w) ≢ m (mod 2).

Em palavras: **toda RS bent é balanceada em cada classe lateral de E de paridade diferente de m.**

## Evidência exata (zero violações)

- n=6 (grau ≤ 3), n=8 (grau ≤ 4) e n=10 (grau ≤ 3): exaustivo.
- n=12: catálogo completo de grau ≤ 4. São 4.029.176 representantes normalizados, ou 309.221.376 funções contando termos afins.
- (C) só vale para bent. Numa RS genérica de grau ≤ 4 em n=12, g(x)+g(x+𝟏) varia em 26 dos 64 pontos de E.
- (C) não vale fora de E. Em Fix(ρ⁴), em n=12, falha em 8 dos 16 pontos.
- Nas classes permitidas, |s_g| ∈ {0, 8} para n=6, {0, 16} para n=8 e {0, 8, 32} para n=10.

## O que NÃO funciona (não repetir)

1. **Usar só τ.** (C) é falsa para bent apenas τ-invariante. Contraexemplo em n=4: f(a,b) = aᵀAb com A = [[1,1],[1,0]]. Então G(z) = z₁ e G(z+𝟏)+G(z) = 1 ≠ m = 2. Em geral, para A simétrica, G(z+𝟏)+G(z) = Σᵢ A_ii. **A prova precisa da rotação completa ρ.**
2. **Congruência mod p.**
   - Em coordenadas de Dillon (base normal, K = F_{2^m}, T(X,Y) = (X²+bY², Y²), T^m(X,Y) = (X+Y, Y)), temos E ↔ K×{0}, 𝟏 ↔ (1,0), a classe lateral ↔ Y e a paridade ↔ Tr(Y).
   - Contar órbitas de T^k na classe Y ∈ F_{2^k}, com m/k = p^j, dá só s(w) ≡ s_{2k}(w) (mod p) para a restrição a vetores 2k-periódicos.
   - Isso recupera x = 0 para n = 2p^a, mas não dá s = 0 nos outros pontos. **(C) em x ≠ 0 é nova mesmo para n = 2p^a.**
3. **Estrutura linear anti-invariante por classe** (existe e com g_w(y+e) = g_w(y)+1).
   - Vale em todos os dados, mas o e depende de g.
   - Como g_w tem período w, ela vive em m−1 variáveis. Para n ≤ 8 isso equivale a ser balanceada, então não é um mecanismo.
   - Numa RS genérica de grau ≤ 4 em n=8, 55% dos casos já têm esse e.
4. **Mod 4 / mod 8 em W(b,b) com b ∈ E.** Só dá Σ_E (-1)^g ≡ 0 (mod 4), que é fraco.

## Pergunta

1. **Prove (C') ou (C)**, para todo n par ou para uma família que inclua n = 12.

   Caminhos que parecem promissores:
   - **(a)** A matriz M(a,c) = Σ_{x∈a+E} (-1)^{g(x)+c·x}, com a, c em F₂ⁿ/E. Ela é "Hadamard por blocos" para g bent; junte a isso a equivariância por ρ, que age em a e em c como rotação de m bits, e a dualidade g ↔ g̃.
   - **(b)** Um argumento que use ρ e não só τ. Por exemplo, a ação de ⟨ρ⟩ sobre o conjunto das classes laterais de uma dada paridade, combinada com Parseval: Σ_w s_g(w)² = 2ⁿ.
   - **(c)** Indução pela restrição aos vetores periódicos Fix(ρ^k).
2. **Se achar que (C) pode ser falsa** para algum n (por exemplo, n=12 com grau 5 ou 6, n=14 ou n=16), diga qual teste computacional exato faria primeiro.

Separe claramente o que é prova e o que é heurística. Dê passos verificáveis. Antes de reivindicar novidade, verifique se (C) ou (C') já é conhecida, por exemplo para bent invariantes por involução ou como "normalidade" relativa a E.

Arquivos de apoio: github.com/contatofilipevono-rgb/n1-sat-cubos, pasta resultados/hrsbf_decomp4 (CONJECTURA_ANTIPODAL_COMPLEMENTO.md e scripts).
