# Conjectura antipodal de complemento (10/11) — padrão extraído dos dados, SEM prova

Seja σ = ρ^{n/2} a antípoda, x_i ↦ x_{i+n/2}, e Fix(σ) = {(y,y)}, de dimensão n/2. Seja 𝟏 o vetor de uns.

> **(C)** Se g é RS bent em n variáveis, então g(x+𝟏) = g(x) + n/2 (mod 2) para todo x ∈ Fix(σ).

Tomando x = 0, (C) é exatamente a regra g(0)+g(1) ≡ n/2. Portanto (C) é uma versão ponto a ponto da regra, válida nos 2^{n/2} pontos antipodais.

Seja G(y) = g(y,y). Então G é RS em n/2 variáveis e (C) diz que G(y+𝟏) = G(y) + n/2.

## Evidência (exata)

| n | universo | RS bent | violações |
|---|---|---|---|
| 6 | grau ≤ 3, exaustivo | 24 | 0 |
| 8 | grau ≤ 4, exaustivo | 7552 | 0 |
| 10 | grau ≤ 3, exaustivo | 3168 | 0 |
| 12 | catálogo grau ≤ 4 do Astra (4.029.176 representantes normalizados) | 309.221.376 com afins | 0 |

Arquivos: antipodal_compl.py, d_compl_n12.py e d_compl_n12.txt.

- **(C) só aparece com bent.** Em RS genérica de grau ≤ 4 com n=12, D(x) = g(x)+g(x+𝟏) varia em 26 dos 64 pontos antipodais.
- **(C) é invariante pelas simetrias do Astra:**
  - circulantes inversíveis preservam Fix(σ) e fixam 𝟏;
  - os multiplicadores 5 e 7 também;
  - termos afins RS não alteram D, porque Σx_i se anula em Fix(σ) e em 𝟏.

  Logo, o teste nos representantes vale para o catálogo inteiro.
- **(C) não vale fora de Fix(σ).** Em Fix(ρ⁴) ⊄ Fix(σ), D não é constante em 8 dos 16 pontos.
- **Mineração de relações** (fix_restricoes_n12.txt): sobre Fix6 ∪ Fix4, o span afim das bent tem dimensão 6, contra 8 no caso genérico.

## Status

- (C) é conjectura. O argumento direto mod 4 em W(b,b) só dá S ≡ 0 mod 4, que é fraco.
- O caminho natural é estender a prova da paridade antipodal (thm:apar, n = 2p^a) de x = 0 para todo x ∈ Fix(σ).
- Falta comparação bibliográfica: pode ser conhecido para bent invariantes por involução.
## Tentativa de prova (10/11, tarde) — o que ficou estabelecido

**Notação.** n = 2m. E = {(z,z)} satisfaz E^⊥ = E. As coclasses de E são indexadas por w = x₁+x₂ ∈ F^m; ρ age em w como a rotação cíclica de m bits, e a coclasse w tem paridade de peso wt(w). G(z) = g(z,z) e G̃(z) = g̃(z,z), onde g̃ é a dual.

1. **Reformulação (provada, por Poisson).** Seja s_g(w) = Σ_{x₁+x₂=w} (-1)^{g(x)}. Então s_g(w) = W_{G̃}(w). Logo:

   > (C) para g̃ ⇔ (C') para g: s_g(w) = 0 sempre que wt(w) ≢ m (mod 2).

   Ou seja: **toda RS bent é balanceada em cada coclasse de E de paridade ≠ m.** A dual de uma RS bent é RS bent, então (C) para todas ⇔ (C') para todas.

   Conferência exata (coclasse_C.py): n=6, 8, 10 exaustivos, 0 violações. Nas demais coclasses, |s| ∈ {0, 8} (n=6), {0, 16} (n=8), {0, 8, 32} (n=10).

2. **A simetria cíclica completa é necessária.** (C) é FALSA para bent invariante só pela meia-volta τ. Contraexemplo em n=4: f(a,b) = aᵀAb com A = [[1,1],[1,0]] (simétrica e inversível, logo bent e τ-invariante). Aqui G(z) = z₁, então G(z+𝟏)+G(z) = 1 ≢ m = 2.

   Para A simétrica geral, G(z+𝟏)+G(z) = Σᵢ A_ii. Uma prova de (C) precisa usar ρ, e não só τ.

3. **O método do thm:apar não basta.**
   - Em coordenadas de Dillon (K², T(X,Y) = (X²+bY², Y²)): E ↔ K×{0}, 𝟏 ↔ (1,0), coclasse ↔ Y, paridade ↔ Tr(Y).
   - O argumento de congruência mod p (órbitas de T^k na coclasse Y ∈ F_{2^k}, com m/k = p^j) dá apenas s(w) ≡ s_{2k}(w) (mod p), para a restrição aos vetores 2k-periódicos.
   - Com k = 1, isso recupera a regra em x = 0 para n = 2p^a: s(0) ≡ 0 mod p, mais a cota. Mas para w com período k > 1 só sai a congruência, não s = 0.
   - Portanto **(C) em x ≠ 0 é nova mesmo nas famílias 2p^a, 4p^a, 6p^a.** Fechá-la exige outro ingrediente: um balanceamento exato, não modular.

**Próximo passo sugerido.** Procurar a identidade exata por trás de (C'). Candidatos:
- uma involução por coclasse que troque o sinal de (-1)^g, explorando T^k, que age na coclasse Y como X ↦ X^{2^k} + c_k Y;
- a estrutura de Hadamard da matriz M(a,c) = Σ_{x∈a+E} (-1)^{g(x)+c·x}.