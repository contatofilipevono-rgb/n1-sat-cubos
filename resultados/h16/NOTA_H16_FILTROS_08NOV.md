# H16: filtros 2-ádicos e SAT (08/11)

**Status:** em andamento, sem auditoria.

## Pergunta

Existe quártica homogênea simétrica por rotação (RS) bent em 16 variáveis?

O espaço tem **116 órbitas** quárticas, ou seja, 2¹¹⁶ candidatas. A contagem foi conferida, e bate com `GRAU4_T16_A100.py` do repositório.

## Filtros

**Proposição.** Seja f bent em 16 variáveis e seja a + V um subcubo coordenado de codimensão k, com k ≥ 1. Então o peso w de f restrita a a + V satisfaz

w ≡ 2^(15−k) (mod 2^(8−k)).

No caso k = 0, vale w ≡ 2⁷ (mod 2⁸).

**Prova.** Pela fórmula de Poisson, Σ_{a+V} (−1)^f = 2^(−k) Σ_{u∈V⊥} ±W_f(u). Cada W_f(u) vale ±2⁸, então a soma é 2^(8−k) vezes uma soma de 2^k sinais, e uma soma de 2^k sinais é par.

**Força dos filtros.** Comparação com H12, onde os subcubos de codimensão 4 dão só peso ≡ 0 mod 4:

| Codimensão k | Condição em H16 | Bits impostos |
|---|---|---|
| 4 | peso ≡ 0 mod 16 | 3 |
| 1 | condição mod 128 | 7 |

**O que não passa de H12 para H16.** A descida mod 3 de H12 não se transfere: 16 = 2⁴, então só há rotações de ordem potência de 2.

## Codificação

O arquivo é `h16_filtros.py`.

- Para cada ponto x do subcubo, t_x = f_c(x) é uma forma linear nas variáveis c.
- Os pontos com a mesma forma são agrupados e contados com multiplicidade.
- A soma é tomada mod 2^m por colunas de somadores completos, e os bits da soma são fixados no valor exigido.

**Controles** (`python h16_filtros.py controles`):

| Controle | O que verifica | Resultado |
|---|---|---|
| Teoria | A bent quadrática Σ x_i x_{i+8} satisfaz as congruências, k = 0..6, numa amostra com padrões aleatórios. | ok |
| Codificação | A CNF coincide com a checagem direta em 12 vetores c, incluindo c = 0. A família testada mistura k = 0, 1, 2 com padrão zero e uma amostra de k = 4, 5, 6 com padrões aleatórios. | ok |

## Rodadas

| Rodada | Tamanho | Resultado |
|---|---|---|
| Só k = 4, padrão zero (116 subcubos) | 570 mil variáveis, 4,05 milhões de cláusulas | SAT trivial com c = 0 |

A solução c = 0 é a função nula, que tem peso 0 em todo subcubo. Essa rodada não incluía o filtro k = 0 (w ≡ 128 mod 256), que é o que exclui a função nula.

**CEGAR** (`h16_cegar.py`):

- Começa com os subcubos k = 0, 1, 2, 4.
- Cada solução SAT é testada por Walsh completo.
- Se a solução não é bent, procura-se um subcubo violado (k = 1..6, padrão aleatório) e esse filtro é acrescentado.
- Se não houver subcubo violado na amostra, a solução é bloqueada e registrada como sobrevivente.

Saídas: `saida_cegar_k0124.txt` e `cegar_k0124.json`.

## Leitura

| Resultado | Consequência |
|---|---|
| UNSAT | Não existe quártica RS bent homogênea em n = 16. Para valer como resultado, precisa ser refeito com prova DRAT. |
| SAT com função bent | Contraexemplo à conjectura em n = 16. Exige conferência independente. |
| Sobreviventes não bent | Os filtros 2-ádicos amostrados não bastam. |
