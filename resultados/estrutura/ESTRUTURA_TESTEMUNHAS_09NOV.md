# Estrutura das testemunhas SAT de N1 (09/11)

**Status:** sem auditoria.

- Script: `analisa_testemunhas.py`.
- Dados: `invariantes_testemunhas.json`.
- Testemunhas analisadas: as 12 soluções salvas, todas com I6 conferido por tabela-verdade.

## Tabela

**Colunas:**
- **posto C₃** = dim span{ι_v C₃ : v ∈ Y}, isto é, o número de variáveis essenciais de C₃;
- **∩** = dimensão da interseção comum de todos os U_Y isotrópicos da testemunha.

| Testemunha | Classe | I7 | C₃: monômios / posto | Isotrópicos por órbita | Total | ∩ |
|---|---|---|---|---|---|---|
| F42_o0 | F₄² | sim | 2 / 3 | [0, 7, 36, 552] | 595 | 0 |
| F42_o1 | F₄² | não | 2 / 6 | [7, 0, 3, 75] | 85 | 0 |
| F42_o2 | F₄² | sim | 16 / 7 | [0, 0, 0, 46] | 46 | 0 |
| F42_o3 (nuvem) | F₄² | não | 12 / 8 | [15, 24, 24, 0] | 63 | 0 |
| F4F4_o0 | F₄+F₄ | não | 9 / 6 | [0, 0, 9, 38] | 47 | 0 |
| F4F4_o1 | F₄+F₄ | não | 4 / 5 | [0, 0, 7, 36] | 43 | **2** |
| F4F4_o2 | F₄+F₄ | não | 9 / 6 | [15, 12, 0, 4] | 31 | 0 |
| GH cubo 28 | F₄+F₄ | não | 11 / 7 | [0, 0, 0, 12] | **12** | 0 |
| GH cubo 62 | F₄+F₄ | **sim** | 14 / 8 | [0, 0, 0, 21] | 21 | 0 |
| Q4a_o0 | Q4a | sim | 6 / 8 | [0, 27, 43] | 70 | 0 |
| Q4b_o0 | Q4b | não | 10 / 8 | [0, 22, 28] | 50 | 0 |
| Q4c_o0 | Q4c | sim | 8 / 7 | [0, 21, 44] | 65 | 0 |

Os tamanhos das órbitas são: F₄² 15/60/240/2880; F₄+F₄ 15/60/240/960; Q4 255/1020/2040.

## Observações

1. **I7 não muda o quadro.** Metade das testemunhas satisfaz também I7, ou seja, é liftável. Entre elas está a de F₄+F₄ que escapa de 15 + 60 + 240 (cubo 62).
   - Portanto as conclusões "órbitas pequenas não forçam isotropia" valem também sob a hipótese verdadeira do Lema L, que é I6 ∧ I7.
   - Reformular N1 com I7 não salvaria as abordagens por órbitas pequenas.

2. **Posto alto de C₃ e poucos isotrópicos andam juntos.**
   - Com posto 3 há 595 isotrópicos.
   - Com posto 7–8 há de 12 a 70.
   - Heurística: U_Y é isotrópico quando C₃|U_Y ∈ {ι_v T|U_Y}, e C₃ de posto baixo se anula com facilidade em subespaços grandes.
   - Pergunta natural: **I6 limita o posto de C₃ por cima?** Se limitar, junto com uma contagem de isotrópicos em função do posto, isso daria um caminho para uma prova humana de N1.

3. **Interseção comum.** Quase sempre é 0. A exceção é F4F4_o1: os 43 isotrópicos dessa testemunha contêm um mesmo subespaço de dimensão 2. Isso é estrutura a examinar.

4. **Mínimo observado de isotrópicos: 12**, em F₄+F₄, todos na órbita de 960.
   - N1 equivale a dizer que esse mínimo sobre todas as soluções de I6 é ≥ 1.
   - A classe completa (todas as órbitas) roda em cubos no Colab 2 e no PC; F₄+F₄ 15+960 roda no Kaggle.

## Correção sobre o posto

O posto 8, o máximo possível em Y = F₂⁸, ocorre em quatro testemunhas com I6: F42_o3, cubo 62, Q4a_o0 e Q4b_o0. Portanto **I6 não limita o posto de C₃**, e o passo (a) abaixo fica respondido negativamente. A correlação entre posto alto e poucos isotrópicos continua valendo, mas só como tendência.

## Estrutura dos isotrópicos nas testemunhas mínimas de F₄+F₄

Script: `isotropicos_minimos.py`.

**Cubo 28 (12 isotrópicos).**
- Interseções duas a duas: dimensão 2 (46 pares), 3 (12 pares), 4 (8 pares).
- A soma de todos os U_Y é Y inteiro.
- O vetor e₇ pertence a **10 dos 12** U_Y; e₆ e e₆+e₇ pertencem a 7 cada.

**Cubo 62 (21 isotrópicos).**
- O plano ⟨e₂, e₃⟩ está contido em **15 dos 21** U_Y.
- Há 108 pares com interseção de dimensão 4.

**Leitura.** Nas testemunhas que quase escapam, os U_Y isotrópicos que sobram não estão espalhados. Eles se concentram num "feixe" que passa por uma reta ou por um plano especial de Y.

Isso sugere uma forma possível para um argumento humano: identificar, para cada T crítica, a família de retas e planos especiais e provar que I6 obriga C₃ a ser compatível com pelo menos um U_Y do feixe correspondente.

**Advertência.** A base usada aqui é a do pencil, e T não é diagonal em blocos nessa base. Por isso as contagens (dim U∩Y₁, dim U∩Y₂) com Y₁ = ⟨e₀..e₃⟩ não têm leitura direta. É preciso recalcular na base em que T = F₄ ⊕ F₄.

## Próximos passos de extração

- (a) Medir o posto máximo de C₃ compatível com I6 por SAT, impondo "posto ≥ r" e testando cada r.
- (b) Descrever os 12 U_Y isotrópicos do cubo 28: geradores, posição em relação aos blocos F₄ e estabilizador no grupo.
- (c) Coletar mais soluções que minimizem os isotrópicos, usando cubos na classe completa com restrição de cardinalidade, para ver se o mínimo cai abaixo de 12.
