# Brief: lema das sete restrições (caso de 3 lineares do Lema L)

Texto autocontido para um modelo ou pessoa atacar **à mão**. Todas as definições foram tiradas do código do repositório `contatofilipevono-rgb/n1-sat-cubos`, nos arquivos `sat_n1.py`, `sat_n1_orbita.py` e `sat_n1_cegar.py`.

## 1. Objetos

Trabalhamos em F₂, com polinômios booleanos (y² = y) em Y = F₂⁸ (coordenadas y0..y7). O **grau** de um polinômio é o grau da sua ANF.

**Quárticas críticas.** T é a parte de grau 4 de q₁·q₂. Existem exatamente 5 classes de T, por equivalência linear, e T tem isotropia exatamente em codimensão 3. Os representantes usados são:

| Classe | q₁ | q₂ | T (parte quártica de q₁q₂) |
|---|---|---|---|
| F4+F4 | y0y2+y1y3+y4y6+y5y7 | y1y2+y0y3+y1y3+y5y6+y4y7+y5y7 | y0y1y2y3 + y1y2y4y6 + y0y3y4y6 + y1y3y4y6 + y0y2y5y6 + y1y3y5y6 + y0y2y4y7 + y1y3y4y7 + y0y2y5y7 + y1y2y5y7 + y0y3y5y7 + y4y5y6y7 |
| F4² | y0y4+y1y5+y2y6+y3y7 | y1y4+y2y5+y3y6+y0y7+y2y7 | y0y2y4y5 + y1y2y4y6 + y0y3y4y6 + y1y3y5y6 + y0y2y4y7 + y1y3y4y7 + y0y1y5y7 + y1y2y5y7 + y2y3y5y7 + y0y2y6y7 |
| Q4a | y0y4+y1y5+y2y6+y3y7 | y1y4+y2y5+y3y6+y0y7+y1y7 | y0y2y4y5 + y1y2y4y6 + y0y3y4y6 + y1y3y5y6 + y0y1y4y7 + y1y3y4y7 + y0y1y5y7 + y2y3y5y7 + y0y2y6y7 + y1y2y6y7 |
| Q4b | y0y4+y1y5+y2y6+y3y7 | y1y4+y2y5+y3y6+y0y7+y3y7 | y0y2y4y5 + y1y2y4y6 + y0y3y4y6 + y1y3y5y6 + y0y3y4y7 + y1y3y4y7 + y0y1y5y7 + y1y3y5y7 + y2y3y5y7 + y0y2y6y7 + y2y3y6y7 |
| Q4c | y0y4+y1y5+y2y6+y3y7 | y1y4+y2y5+y3y6+y0y7+y1y7+y2y7+y3y7 | y0y2y4y5 + y1y2y4y6 + y0y3y4y6 + y1y3y5y6 + y0y1y4y7 + y0y2y4y7 + y0y3y4y7 + y1y3y4y7 + y0y1y5y7 + y1y2y5y7 + y1y3y5y7 + y2y3y5y7 + y0y2y6y7 + y1y2y6y7 + y2y3y6y7 |

**Contração.** Para u ∈ Y e uma forma F, ι_u F é a parte de grau (deg F − 1) de F(y+u) − F(y). Equivalentemente, ι_u F = Σᵢ uᵢ ∂F/∂yᵢ, com a derivada formal agindo sobre monômios sem quadrados.

**Subespaços isotrópicos de T.** São os U_Y ⊂ Y de dimensão 5 (codimensão 3) em que T|U_Y tem grau ≤ 3; restringir é parametrizar U_Y por 5 coordenadas. Quantidades por classe:
- F4+F4: 1275, nas órbitas 15/60/240/960;
- F4²: 3195, nas órbitas 15/60/240/2880;
- Q4a, Q4b, Q4c: 3315, nas órbitas 255/1020/2040.

**Isotropia de uma cúbica φ.** Seja D = T + x·φ + (termos de grau ≤ 3) em Y ⊕ ⟨x⟩. Todo subespaço de codimensão 3 em que D cai para grau ≤ 3, e que não está contido em Y, é da forma U = U_Y ⊕ ⟨eₓ + u⟩, com U_Y isotrópico de T. Ele é isotrópico para D se e só se

> **φ|U_Y ∈ { (ι_u T)|U_Y : u ∈ Y }**, como formas cúbicas em U_Y.

Dizemos então que **U_Y é isotrópico para φ**.

**Gauge.** φ ↦ φ + ι_u T não altera nada; corresponde à troca y ↦ y + x·u.

**N.** É o conjunto das cúbicas φ sem nenhum U_Y isotrópico.

## 2. Fatos já verificados

Todos por computação exata, com controles; nenhum foi auditado por pessoa.

**(F1) Parte linear de I6 e I7.** Seja I6: c_S ≡ 0 mod 4 para |S| ≥ 6, com c_S os coeficientes da ANF inteira. Seja I7: c_S ≡ 0 mod 8 para |S| ≥ 7.
- A parte **linear** de I6 sobre φ é exatamente **φ ∧ T = 0 em Λ⁷Y** (8 condições), nas 5 classes.
- I7 não acrescenta nenhuma consequência linear nem quadrática que envolva só φ.

**(F2) Contraexemplo a N1 só com I6, em F4+F4.** O D abaixo (em y0..y7, x) tem grau 4, satisfaz I6, **não** satisfaz I7 e não tem subespaço de codimensão 3 com queda de grau (força bruta sobre os 788.035):

    y0y1y2y3 + y1y2y4y6 + y0y3y4y6 + y1y3y4y6 + y0y2y5y6 + y1y3y5y6 + y0y2y4y7 + y1y3y4y7 + y0y2y5y7 + y1y2y5y7 + y0y3y5y7 + y4y5y6y7
    + x(y0y1y4 + y0y2y4 + y0y3y4 + y1y3y4 + y2y4y5 + y0y1y6 + y0y2y6 + y1y2y6 + y0y3y6 + y0y1y7 + y1y2y7 + y2y3y7 + y1y6y7)
    + y0y1y2 + y0y1y3 + y0y2y3 + y1y2y3 + y0y2y4 + y0y3y4 + y2y3y4 + y1y2y5 + y0y3y5 + y2y4y5 + y1y3y6 + y0y4y7 + y1y4y7 + y0y5y7 + y0y6y7
    + x(y0y1 + y0y2 + y1y3 + y2y3 + y0y4 + y2y4 + y3y4 + y0y5 + y2y5 + y3y5 + y4y5 + y0y6 + y1y6 + y2y6 + y3y6 + y4y6 + y5y6 + y0y7 + y1y7 + y2y7 + y3y7 + y5y7)
    + y1y3 + y2y3 + y0y4 + y1y4 + y2y4 + y3y5 + y4y5 + y0y6 + y1y6 + y2y6 + y3y6 + y4y6 + y5y6 + y1y7 + y2y7 + y3y7 + y4y7 + y5y7 + x(y0 + y2 + y6 + y7)

**(F3) Planos em N.** Em F4+F4 existem φ₁, φ₂ com φᵢ ∧ T = 0 e φ₁, φ₂, φ₁+φ₂ todos em N.

**(F4) Estrutura de Q4.**
- Os U_Y da órbita 255 são as "estrelas" W ⊕ ⟨v⟩ de um espalhamento de Y em 17 subespaços W de dimensão 4. Cada W é totalmente singular para q₁ e q₂.
- Isotropia na estrela de W exige φ|W = 0.
- Nas órbitas 1020/2040, U_Y encontra um único W em dimensão 3 (W'), e a isotropia exige φ|W' = 0.

**(F5) Raridade de N.** C₃ aleatórios no espaço L = {φ : φ ∧ T = 0} (dim 40, após o gauge) têm em média cerca de |{U_Y}|/2⁷ isotrópicos.
- Em Q4, nenhum C₃ de 200 mil amostras ficou sem isotrópico.
- Em F4+F4, a fração sem isotrópico é de cerca de 0,7%.

## 3. Pergunta

**Lema das sete restrições.** Seja T uma das 5 quárticas críticas. Se φ₁, φ₂, φ₃ são cúbicas em Y com φᵢ ∧ T = 0, então alguma combinação φ_v = Σ vᵢφᵢ (v ∈ F₂³ ∖ {0}) tem um U_Y isotrópico.

**Motivação.** No caso de 3 lineares do Lema L, Δ = T + x₁φ₁ + x₂φ₂ + x₃φ₃. Restringir (x₁, x₂, x₃) à reta t·v custa codimensão 2 e deixa T + t·φ_v. Um U_Y isotrópico para φ_v dá queda de grau em codimensão total ≤ 5, que é o que o Lema L pede. N1 sozinho é falso em F4+F4 (F2), mas basta que **uma** das 7 restrições funcione.

**Status computacional.**
- d=2 é falso em F4+F4 (F3).
- d=3 em F4+F4 roda como SAT (CryptoMiniSat) e, até a última conferência, estava sem resposta.
- Um UNSAT confirmaria o lema para F4+F4 só com a parte linear de I6. Um SAT mostraria que é preciso usar mais de I6/I7.

**Pedido.**
1. Começar por F4+F4: T = (q₁q₂)₄ com q₁, q₂ como acima.
2. Usar a estrutura de Λ*Y e o produto por T. Pistas:
   - φ ∧ T = 0;
   - φ|U_Y ∈ ι T|U_Y;
   - no caso Q4, o espalhamento de (F4).
3. Entregar uma prova com cada passo verificável, ou o ponto exato em que ela falha, junto com um candidato a contraexemplo (φ₁, φ₂, φ₃) que possamos conferir por computação.
4. Não usar força bruta.

**Escopo.** Não declarar Q≡1 nem p=17 resolvidos: o ramo par da cadeia não foi auditado, e o modelo "T fixo + 3 lineares" ainda precisa ser conferido contra a redução completa.
