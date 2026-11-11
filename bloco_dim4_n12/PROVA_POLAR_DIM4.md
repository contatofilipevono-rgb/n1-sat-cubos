# Forma da polar em dimensão quatro — redução provada e lista residual (11/11)

**Status.** Sem auditoria externa. Cada item traz uma marca:
- **[D]** demonstrado à mão;
- **[L]** álgebra linear certificada numa base (`espaco_q.py`), reproduzível em segundos;
- **[P]** verificação exaustiva pequena (`fatia_V.py`: 256 classes × 2⁷ restrições);
- **[E]** depende da enumeração completa dos 2³¹ ou 2³³ mapas.

**Resumo.** A lista completa não saiu à mão. O que ficou provado reduz o problema a duas perguntas finitas e pequenas, e explica o termo adicional do tipo B:

1. **[D]** Se a polar se anula na fatia z ∈ V (A = E = 0), ela é θ_z ∧ μ(z) com μ afim. Isso é só meia-volta e grau.
2. **[L]** O espaço das partes mistas tem dimensão 8, e a parte com A = E = 0 é exatamente {θ_z ∧ (Mz + c𝟏)}.
3. **[D]+[P]** Condições de paridade na fatia z ∈ V, tiradas só das somas de grau ≤ 2 nas fibras, eliminam 160 das 256 classes em V2 e 128 das 256 em V1.
4. **[E]** As classes restantes com A ≠ E não têm nenhum mapa auto-ortogonal. Logo toda função bent do bloco tem **A = E**.
5. **[D]** A = E implica que B_z é decomponível (posto ≤ 2) para todo z, qualquer que seja o coeficiente no complemento.
6. O termo do tipo B é exatamente a componente A = E ≠ 0: é a forma do bloco U, e é a única que sobrevive ao item 3.

## 1. Convenções

- V = ker r ∩ ker s; e_r, e_s duais a r, s. V2: r = ε_e (máscara 21), s = ε_o (42), e_r = e₀, e_s = e₁. V1: r = ρ₂₇, s = ρ₅₄, e_r = e₀, e_s = e₀+e₁.
- q₁(z) = B_z(e_r,·)|_V, q₂(z) = B_z(e_s,·)|_V, b(z) = B_z(e_r, e_s).
- Ponto y = (z, s_r, s_s), com w = s_r e_r + s_s e_s + u. Rótulo π(y) = g(z) + s_r q₁(z) + s_s q₂(z), onde g = π(·,0,0).
- θ_z = s(z)·r + r(z)·s, de modo que θ_z(e_r) = s(z) e θ_z(e_s) = r(z).
- Fatias: (r(z), s(z)) = (0,0) é z ∈ V; as outras três são (1,0), (0,1), (1,1).

O enumerador usa o complemento (e₀, e₁), que em V1 não é dual. A conversão é q₂^{dual} = q₁^{enum} + q₂^{enum}; q₁ não muda. Em V1 isso troca o segundo rótulo cruzado ρ₄₅ da nota anterior por ρ₂₇, e as fórmulas abaixo já estão no complemento dual.

## 2. Meia-volta e grau

**Teorema 1 [D].** Seja B_z com entradas de grau ≤ 2 em z, B_z|_{V×V} = 0 e B_z z = 0. Então:
- (a) r(z)·q₁(z) + s(z)·q₂(z) = 0;
- (b) com z = (x, r, s), x ∈ V: q₁ = (1+r)A + sB + rsD e q₂ = (1+s)E + r(B+D+H) + rsH, com A, B, E afins em x e D, H constantes;
- (c) **se A = E = 0, então (q₁, q₂) = (s·μ, r·μ) com μ(z) = B(x) + r·D + (1+s)·H, afim em z.** Isto é, B_z|_{(e_r,e_s)×V} = θ_z ∧ μ(z).

*Prova.* (a) é B_z(z,v) = 0 para v ∈ V. Para (b), escreva q₁ = P₀ + rP₁ + sP₂ + rsP₃; na fatia (1,0), (a) dá q₁ = 0, logo P₀ = P₁, que é afim. O resto é o mesmo nas outras fatias. Para (c): com A = E = 0, os valores de μ nas fatias (0,1), (1,1), (1,0) são B, B+D, B+D+H, e a função afim B + rD + (1+s)H toma exatamente esses valores. ∎

Na fatia z ∈ V sobram q₁ = A e q₂ = E, com A(x)(x) = E(x)(x) = 0.

**Corolário 2 [D].** Se A = E, então B_z é decomponível para todo z e todo b.
- z ∉ V: B_z = θ′∧μ′ + b·r∧s com θ′ ∈ ⟨r,s⟩ não nulo; como r∧s = θ′∧ρ para algum ρ ∈ ⟨r,s⟩, B_z = θ′∧(μ′ + bρ).
- z ∈ V: B_z = (r+s)∧A_x + b·r∧s = (r+s)∧(A_x + b·r).

Se A_x e E_x são independentes para algum x, B_x tem posto 4.

## 3. O espaço real das partes mistas

**Proposição 3 [L].** Para V1 e V2, nas funções RS de grau ≤ 4 afins em V:
- o espaço de (q₁, q₂) tem dimensão 8, e a forma normal do Teorema 1 vale em toda a base;
- o subespaço A = E = 0 tem dimensão 4 em V2 e 5 em V1, e **todos** os seus elementos são θ_z ∧ μ com μ afim; ele é gerado por θ_z∧R^k z (k = 0..5) e, em V1, também por θ_z∧𝟏;
- (A, E) toma 16 valores em V2 e 8 em V1; A e E são dados por matrizes simétricas na base de V, sem parte constante em V2;
- em V2, A = E ocorre em 4 dos 16 valores: 0, x, R³x e Nx = (I+R³)x. Em V1, A = E só em 0;
- o coeficiente no complemento é b = b_q + ε·1_V(z): a única liberdade com q fixo é somar a indicadora de z ∈ V.

O último item resolve o controle pedido: o termo livre é 1_V(z)·r∧s, e pelo Corolário 2 ele nunca altera a decomponibilidade.

## 4. Condição necessária na fatia z ∈ V

Para um rótulo fixo, seja a^{(s_r,s_s)} = #{x ∈ V : g(x) + s_r A(x) + s_s E(x) = rótulo}.

**Lema 4 [D].** Se toda função de grau ≤ 2 tem soma nula em cada fibra, então, para cada rótulo:
- (P1) os quatro números a^{00}, a^{10}, a^{01}, a^{11} têm a mesma paridade;
- (P2) a soma dos x sobre as quatro pré-imagens é zero.

*Prova.* Pelo Teorema 1(a): na fatia (1,0), q₁ = 0 e os pontos da fibra vêm em pares que diferem só em s_r; na fatia (0,1), em pares que diferem só em s_s.
- m = (1+r)(1+s) é a indicadora da fatia z ∈ V: Σ a = 0.
- m = (1+r)·s_r vive nas fatias (0,0) e (0,1). Na (0,1) os dois pontos de cada par têm o mesmo s_r e se cancelam. Sobra a^{10} + a^{11} = 0.
- m = (1+s)·s_s: do mesmo modo, a^{01} + a^{11} = 0.
- Somando, a^{00} = a^{11}. Isso é (P1).
- m = (1+r)·z_i: na fatia (0,1) os pares têm o mesmo z e se cancelam. Sobra (P2). ∎

**Proposição 5 [P].** g = π₀|_V percorre um trasladado de dimensão 7. Percorrendo as 256 classes de q e os 2⁷ valores de g:

| | V2 | V1 |
|---|---|---|
| classes com A = E = 0 que passam | 16 de 16 | 32 de 32 |
| classes com A = E ≠ 0 que passam | 16 de 48 (só A = E = Nx) | — |
| classes com A ≠ E que passam | 64 de 192 | 96 de 224 |
| **eliminadas** | **160** | **128** |

Em V2 isso já mostra que, das formas com A = E ≠ 0, só a do bloco U sobrevive: as com A = E = x ou R³x caem em (P1).

**Proposição 6 [E].** Nenhuma classe com A ≠ E tem mapa auto-ortogonal (0 de 166.472 em V2, 0 de 113.040 em V1). Faltam, portanto, 4 pares (A,E) em V2 e 3 em V1 para excluir à mão; (P1) e (P2) não bastam para eles.

**Consequência.** Toda função bent do bloco tem A = E, logo polar decomponível em todo z, da forma

**B_z = θ_z ∧ (Mz + c𝟏) + κ·(1+r+s)(r+s)∧Nz + b·r∧s**, com κ ∈ {0,1} e κ = 0 em V1.

## 5. O termo do tipo B

- **[L]** Em V2, as 64 classes com A = E são {θ_z∧Mz} ⊕ {0, x, R³x, Nx}. A componente Nx é (1+r+s)(r+s)∧Nz, a forma do bloco U; ela vive nas fatias (0,0) e (1,1) e, na (1,1), soma Nz a μ.
- **[D]+[P]** As componentes x e R³x caem pelo Lema 4. Só κ = 1 com N sobrevive.
- Em V1 o bloco U não aparece como componente A = E ≠ 0: ele é a classe θ_z∧(Nz + 𝟏), com A = E = 0. Por isso V1 não tem análogo do tipo B.

## 6. Lista residual: destino das classes com A = E — **[E]**

Contagens de mapas auto-ortogonais por classe e onde morrem (`destino_classes.py`).

**V2, 16 classes θ_z∧Mz (κ = 0):**

| M | auto-ort. | posto 8 | linear | quadrática | com fase | funções |
|---|---|---|---|---|---|---|
| 0 (antipodal) | 132.152 | fora do escopo | | | | |
| R, R², R⁴, R⁵ | 460 cada | 24 | 400 | 0 | 36 | 90.112 cada (tipo C) |
| R+R⁴, R²+R⁵ | 1.272 cada | 0 | 1.152 | 0 | 120 | 589.824 cada (tipo A) |
| I, R³ | 384 cada | 0 | 384 | 0 | 0 | 0 |
| I+R³ | 1.152 | 0 | 864 | 288 | 0 | 0 |
| I+R, I+R⁵, R²+R³, R³+R⁴ | 452 cada | 16 | 436 | 0 | 0 | 0 |
| R+R², R⁴+R⁵ | 368 cada | 0 | 368 | 0 | 0 | 0 |

**V2, 16 classes θ_z∧Mz + U (κ = 1):**

| M | auto-ort. | posto 8 | linear | quadrática | com fase | funções |
|---|---|---|---|---|---|---|
| 0 (bloco U) | 17.280 | fora do escopo | | | | |
| R+R⁴, R²+R⁵ | 2.112 cada | 864 | 624 | 432 | 192 | 393.216 cada (tipo B) |
| I+R³ | 1.824 | 0 | 960 | 864 | 0 | 0 |
| as outras 12 | 144 a 256 | todos | 0 | 0 | 0 | 0 |

**V1, 32 classes θ_z∧(Mz + c𝟏):**

| M, c | auto-ort. | posto 8 | linear | quadrática | com fase | funções exclusivas |
|---|---|---|---|---|---|---|
| 0, 0 (antipodal) | 63.504 | fora do escopo | | | | |
| I+R³, 1 (bloco U) | 12.832 | 0 | 12.176 | 16 | 640 | 0 (10.485.760 afins em U) |
| I+R, 1 e R²+R³, 1 | 704 cada | 0 | 688 | 8 | 8 | 196.608 cada |
| R²+R⁴, 0 | 2.176 | 0 | 2.144 | 24 | 8 | 196.608 |
| R²+R⁴, 1 | 3.072 | 512 | 2.432 | 96 | 32 | 262.144 |
| I+R², 1 e R+R³, 1 | 1.536 cada | 256 | 1.152 | 96 | 32 | 524.288 cada |
| 0, 1 | 12.416 | 0 | 11.200 | 1.216 | 0 | 0 |
| I+R³, 0 | 11.232 | 0 | 11.232 | 0 | 0 | 0 |
| I+R, 0; R²+R³, 0 | 512 cada | 0 | 512 | 0 | 0 | 0 |
| I+R², 0; R+R³, 0 | 1.152 cada | 0 | 1.152 | 0 | 0 | 0 |
| as outras 18 | 0 | | | | | |

Os representantes de M são os de menor peso módulo V^⊥; `formas_V1.py` usa outros representantes das mesmas seis classes.

Leituras:
- **A seleção de M precisa de fase.** Toda classe com A = E e θ-parte não nula que tem mapas auto-ortogonais mas nenhuma função morre no sistema linear h·c = wt(c)/2, ou só por posto 8 (as 12 classes κ = 1 de V2), ou, nos dois casos M = I+R³ de V2, também na condição quadrática. Não há exclusão de M só por suporte, exceto nas 18 classes de V1 sem nenhum mapa auto-ortogonal.
- **Posto 8** só aparece em classes com κ = 1 ou com M de peso 1 ou 2 "não antipodal"; é o que mata as 12 classes θ∧M + U.

## 7. O que fica por provar

1. Os 4 pares (A,E) de V2 e os 3 de V1 com A ≠ E que passam em (P1) e (P2). Precisam de funções de teste que envolvam as outras fatias.
2. A lista de M: 6 de 15 em V2 sem U, 2 de 15 com U, 6 de 31 em V1. Pela tabela, isso é um enunciado sobre o sistema linear de fases, não sobre suportes.
3. Uma prova conceitual do Lema 4 → Proposição 5, sem percorrer os 2⁷ valores de g.

## Arquivos

- `espaco_q.py V`: Proposição 3.
- `fatia_V.py V`: Proposição 5.
- `destino_classes.py V <fonte>`: tabelas da seção 6.
- `formas_V1.py`, `formas_V2.py`: as formas fechadas dos mapas com fase.
