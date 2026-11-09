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

**Identificação das 8 restrições** (`hipotese_cunha.py`): nas cinco classes (Q4a, Q4b, Q4c, F₄², F₄+F₄), o espaço das consequências lineares de I6 sobre C₃ coincide exatamente com

> **C₃ ∧ T = 0 em Λ⁷Y ≅ Y** (8 condições).

Explicitamente, f_i(C₃) = #{(a ∈ C₃, c ∈ T) : a ⊔ c = [8]∖{i}} mod 2.

Logo o C₃ efetivo vive em L = {C₃ : C₃ ∧ T = 0} módulo o gauge {ι_u T}, um espaço de dimensão 56 − 8 − 8 = 40. É uma condição intrínseca: não depende de base nem de gauge.

**Amostragem de 200 000 C₃ uniformes em L (Q4a)** (`amostra_L.py`):
- nenhum sem isotrópico;
- média de 25,9 isotrópicos;
- mínimo observado: 2.

Logo |N ∩ L| < cerca de 2⁴⁰/2·10⁵, mas ainda é grande demais para enumerar caso a caso.

**Custo do teste interno:** com C₃ fixo em N ∩ L, a extensão a I6 não respondeu em 25 min no PC. A dificuldade está na parte não linear de I6 em R, com produtos R₃·R₃ nos graus 6 e 7.

**Forma explícita de I6.** Como D tem grau ≤ 4, c_S ≡ a_S − 2·#{pares {m, m'} ⊂ supp D : m ∪ m' = S} (mod 4). Logo:

> I6 ⇔ para todo S com |S| ≥ 6, o número de pares de monômios de D cuja união é S é par.

Separando D = T + x·C₃ + R₃ + x·R₂ + R₂' + (grau ≤ 1), com C₃ fixo as equações ficam:

| Caso | Equações | Forma |
|---|---|---|
| \|S\| = 8 com x | — | C₃ ∧ T = 0 (as 8 restrições lineares) |
| \|S\| = 7 sem x | 8 | T ∧ R₃ = const; lineares em R₃ |
| \|S\| = 7 com x | 28 | C₃∧C₃ + C₃⋆₁T + C₃∧R₃ + R₂∧T = 0; lineares em (R₃, R₂) |
| \|S\| = 6 sem x | 28 | T⋆₂T + T⋆₁R₃ + T∧R₂' + R₃∧R₃ = 0; quadráticas em R₃ |
| \|S\| = 6 com x | 56 | aparecem os produtos R₂·R₃; bilineares |

Ao todo são 112 incógnitas e 120 equações independentes.

Em Q4, T∧· : Λ²→Λ⁶ tem posto 26 de 28. Assim, R₂ e R₂' ficam determinados a menos de núcleos de dimensão 2, e sobra **um sistema quadrático com cerca de 50 incógnitas e 58 equações** (uma instância de MQ). Em F₄² e F₄+F₄ o posto é 20 e 18.

**Solver.** O CryptoMiniSat, com XOR nativo, resolve os controles positivos em 6–45 s, contra 80–430 s do CaDiCaL (`interno_cms.py`).

**Por que testar C₃ um a um não basta.** Com C₃ fixo há 112 incógnitas e 120 equações independentes. Um C₃ genérico em L, portanto, não se estende: espera-se cerca de 2⁻⁸ soluções.
- O conjunto E dos C₃ extensíveis tem por volta de 2³² elementos.
- N ∩ L é pequeno, mas grande o bastante para que, por acaso, E ∩ N fosse não vazio.
- Se N1 vale, é por uma razão estrutural. Por isso o teste de um C₃ isolado de N ∩ L, que não terminou em ~1 h no CMS nem em 2 h em 16 cubos na VM, diz pouco.
- Foram gerados 6 elementos distintos de N ∩ L (`NL_Q4a.jsonl`).

**Próximo passo: descrever E.**
- Amostrar soluções de I6 com CMS (`amostra_E.py`, 11 processos no PC).
- Procurar relações polinomiais de grau ≤ 2 em C₃ que se anulem em E (`relacoes_E.py`).
- Se N ∩ L ∩ V(relações) for vazio (SAT de 48 variáveis), N1 em Q4a fica reduzido a provar que essas relações seguem de I6.

**Resultado da tentativa de descrever E (09/11, ~15 h UTC): negativo/inconclusivo.**
- Amostras: 952 soluções de I6 (C₃ distintos: cerca de 750), obtidas com CMS e suposições aleatórias.
- O span afim das amostras é todo L (dimensão 40), então E não tem relações lineares além de C₃∧T = 0.
- Grau 2 (821 monômios nas coordenadas livres de L):
  - o posto ficou abaixo do número de amostras, mas foi efeito do agrupamento das soluções do SAT;
  - das 274 relações candidatas, 240 falharam em amostras de teste;
  - das 34 restantes, só 23 valem nas 952 amostras, e o número continua caindo.
  - Não há evidência de que E seja cortado por quádricas.
- Com as 34 relações, N ∩ L ∩ V tem solução (SAT em 478 s).
- O teste de um C₃ isolado de N ∩ L foi encerrado sem resposta: ~1 h no CMS e 3 h em 16 cubos na VM.

**Leitura.**
- O "ponto duro" de N1 está na interação não linear de I6 entre C₃ e R.
- A redução útil obtida é estrutural: N1 ⇔ E ∩ N = ∅, com L = {C₃∧T = 0}, N descrito pelo espalhamento (Lemas 1–3) e E = projeção de I6.
- Um ataque humano provavelmente precisa entender E via a forma "paridade de uniões de pares", isto é, a estrutura de Λ* com T.

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

## Simetria de ordem 17 (09/11, noite; `ordem17.py`)

- Nas três classes Q4, |Aut(T)| = 8160 = 2⁵·3·5·17, com 1920 elementos de ordem 17.
- Cada elemento de ordem 17 age como **um único 17-ciclo** nos 17 W e não fixa nenhum vetor não nulo de F₂⁸.
- Leitura provável: é a multiplicação por μ₁₇ = F₂₅₆*/F₁₆*, e os W são as retas de F₁₆ (espalhamento desarguesiano).
- Possível elo com p = 17 e com o bloco de 16, já que ord₁₇(2) = 8. Ainda não conferido contra a cadeia.
