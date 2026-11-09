# Q4: as órbitas de U_Y isotrópicos vistas por um espalhamento de Y (09/11)

**Status:** sem auditoria.

- Lemas 1 a 3 foram conferidos por álgebra linear exata em F₂ nas três classes (Q4a, Q4b, Q4c).
- A dedução à mão está esboçada abaixo.
- Scripts em `q1_estrutura_09nov/` (pasta local, copiados em `resultados/estrutura/scripts/`).

## Notação

- Y = F₂⁸ e T = q₁q₂, onde (q₁, q₂) é o pencil do bloco regular de grau 4 (polinômios 10011, 11001, 11111).
- U_Y percorre os subespaços de dimensão 5 de Y com T|U_Y ≡ 0.
- A isotropia de U = U_Y ⊕ ⟨e_x + u⟩ para D é a condição C₃|U_Y ∈ {ι_u T|U_Y}, que é linear em C₃.
- O espaço de C₃ módulo o gauge tem dimensão 48.

## Lema 1: espalhamento

Existem exatamente **17 subespaços W ⊂ Y de dimensão 4** com a propriedade de que todo U_Y ⊃ W de dimensão 5 é isotrópico.
- Eles formam um **espalhamento** (spread) de Y: são disjuntos dois a dois fora do 0 e cobrem Y.
- Cada W é totalmente singular para todo o pencil (q₁|W = q₂|W = 0); daí T|_{W+⟨v⟩} tem grau ≤ 3.

A órbita 255 é a união das 17 "estrelas" {W + ⟨v⟩ : v ∉ W}, cada uma com 15 elementos (255 = 17·15).

Nas órbitas 1020 e 2040, todo U_Y encontra os W do espalhamento assim:
- exatamente um W em dimensão 3;
- quatro W em dimensão 2;
- doze W em dimensão 1.

(Contagem de vetores: 7 + 4·3 + 12·1 = 31.)

## Lema 2: isotropia na estrela

Para U_Y = W + ⟨v⟩, a isotropia equivale a duas condições:
- (a) **C₃|W = 0**: 4 condições, uma por monômio cúbico nas coordenadas de W, iguais para toda a estrela;
- (b) uma condição de posto 3 sobre ∂_v C₃|W, que é uma forma quadrática em W: ela deve estar num subespaço J_v de dimensão 3.

O posto total é 7 por U_Y.

A função posto das condições de isotropia sobre subconjuntos S ⊂ Y/W ≅ F₂⁴ é a mesma nas três classes:

| S | posto |
|---|---|
| 1 ponto | 7 |
| 2 pontos | 10 |
| reta (3 pontos) | 12 |
| 3 pontos em posição geral | 13 |
| plano (7 pontos) | 18 |
| estrela inteira | 24 |

O conjunto dos v isotrópicos **não é** fechado por soma para C₃ arbitrário: o teste exato falha em todos os pares.

## Lema 3: condição necessária nas órbitas 1020/2040

Seja U_Y numa das órbitas 1020 ou 2040, e seja W' = U_Y ∩ W o único encontro de dimensão 3.
- Então **C₃|W' = 0** é condição necessária para a isotropia (conferido para todos os 3060 U_Y).
- Dedução: q₁|W' = q₂|W' = 0, logo ι_u T|W' = 0.

**Leitura por "campo de vetores".** Identifique a forma cúbica C₃|W em W ≅ F₂⁴ com um vetor s_W ∈ W, via Λ³W* ≅ W.
- C₃|W' = 0 equivale a s_W ∈ W'.
- C₃ define assim uma seção W ↦ s_W ∈ W do espalhamento.
- Isotropia em qualquer órbita só é possível sobre um W', ou um W inteiro, que contenha s_W. Na estrela de W é preciso s_W = 0.

## Testemunhas SAT à luz disso

| Testemunhas | Isotrópicos | Estrutura |
|---|---|---|
| 33 testemunhas (Q4a, Q4b, Q4c; GitHub e Colab) | [15, 0, 0] | exatamente uma estrela inteira; o W dela tem s_W = 0 |
| Q4a, Colab cubo 1 | [7, 0, 14] | 7 pontos de uma estrela formando um **plano** de Y/W |
| — | [19, 0, 0] | uma estrela inteira e 4 pontos isolados em outras 4 estrelas |
| Testemunhas da órbita 255 | [0, *, *] | s_W ≠ 0 para os 17 W |

Número de W com s_W = 0 nas testemunhas: sempre 0, 1, 3 ou 5.

## Cobertura sem I6 e decomposição de N1 (09/11, tarde)

Cada U impõe 7 condições lineares ao C₃ de 48 variáveis; seja K_U o subespaço que elas definem.

**Pergunta de cobertura:** os K_U cobrem F₂⁴⁸?

| Classe | Resultado | Detalhe |
|---|---|---|
| F₄+F₄ | não | C₃ achado em 1,2 s |
| F₄² | não | 34 s |
| Q4a | não | 327 s |
| Q4c | não | 151 s |

Todos os C₃ achados foram conferidos.

Mas o conjunto N de C₃ sem isotrópico é **raríssimo**.
- Em amostra aleatória: 0 de 300 em Q4a, Q4b, Q4c e F₄²; 2 de 300 em F₄+F₄.
- A média de isotrópicos por C₃ aleatório é cerca de |{U}|/2⁷, como esperado.

**Decomposição.** N1 para a classe ⇔ nenhum C₃ ∈ N se estende a uma solução de I6.

**Teste com o C₃ de N achado em Q4a:** com C₃ fixo, I6 dá UNSAT em 0,0 s.
- Controle positivo: os C₃ de testemunhas conhecidas estendem (SAT em 80–430 s, I6 conferido).

**Relaxação linear de I6** (`linear_c3.py`): cada produto vira uma coluna livre, e eliminam-se todas as colunas exceto as variáveis simples de C₃.
- Em Q4a, I6 implica **8 restrições lineares afins sobre C₃**.
- O C₃ de N viola 5 delas.
- A cobertura restrita a esse subespaço afim de dimensão 40 ainda falha: SAT em 381 s, conferido.

**CEGAR sobre C₃** (`cegar_c3.py`, rodando no PC):
- O laço externo procura C₃ ∈ N ∩ (restrições lineares) ∩ (cláusulas aprendidas).
- O interno testa a extensão a I6 com C₃ fixo; se não estende, o core minimizado vira uma cláusula.
- Se o externo ficar UNSAT, N1 vale na classe, condicionado a certificar cada cláusula aprendida por DRAT. Cada uma é uma instância pequena (I6 com parte de C₃ fixa).

## Consequências e perguntas

1. **I6 não força s_W = 0 para nenhum W.** As testemunhas da órbita 255 têm s_W ≠ 0 nos 17 W. Assim, um argumento para N1 em Q4 precisa usar as órbitas 1020/2040 quando s não tem zeros.
2. **Pergunta precisa (estrutural).** A seção s se lê como polinômio sobre F₁₆, com Y ≅ F₁₆² e os W como retas F₁₆? Os números de zeros observados (0, 1, 3, 5) sugerem isso.
3. **Pergunta precisa (SAT, menor que a classe completa).** As uniões 255+1020 e 255+2040 ainda não foram testadas em Q4.
   - 1020+2040 não força: há testemunhas [15, 0, 0].
   - 255 sozinha não força.
