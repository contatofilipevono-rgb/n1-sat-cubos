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