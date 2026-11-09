# Testemunha F4+F4 sem nenhum U isotrópico (09/11/2026)

**Status:** verificado por dois métodos independentes no PC. Ainda **não auditado** por pessoa, nem comparado com a literatura.

## Origem

GitHub Actions, run 42547926882, cubo 52 de 64.
- Classe: F4+F4.
- Órbitas restritas: 15 + 960 (índices 0 e 3).
- Tempo de CaDiCaL: 11.522 s.

## Objeto

D = q₁q₂ + x·C₃ + R em 9 variáveis, com:
- a parte quártica de q₁q₂ igual a T na classe F4+F4;
- os monômios fixos dados por `base("F4+F4")` em `q1_tres_lineares/sat_n1_orbita.py`;
- os monômios extras em `testemunha_cubo52.json` (`anf_extra`; bits 0–7 são Y e o bit 8 é x).

## Verificações

**1. Modelo de órbitas** (`analisa_testemunhas.analisa`):
- I6 sim, I7 **não**;
- isotrópicos por órbita [0, 0, 0, 0], ou seja, nenhum dos 1275 U_Y;
- posto de C₃ = 8.

**2. Independente** (`verifica_independente.py`, sem usar o modelo de U_Y):
- I6 pela ANF inteira (Möbius sobre Z, 512 pontos): sim;
- grau de D = 4;
- força bruta sobre **todos os 788.035** subespaços lineares de dimensão 6 de F₂⁹: **0** com deg(D|U) ≤ 3;
- controle positivo: a testemunha F4+F4 do cubo 28 dá exatamente os 12 isotrópicos conhecidos.

## Consequência

O enunciado **N1 com hipótese só I6** ("a parte quártica tem um subespaço isotrópico de codimensão 3") é **falso para T em F4+F4**.

O que **não** se conclui:
- Esta testemunha não satisfaz I7 (liftabilidade). A versão com I6 ∧ I7, usada pelo Lema L, continua aberta.
- Antes de qualquer conclusão sobre Q≡1 ou p=17, é preciso conferir se a cadeia usa N1 só com I6 ou com hipóteses adicionais.
- Não declarar nada resolvido nem refutado na cadeia sem essa conferência.

## Próximos passos

1. Rodar F4+F4 completo com I6 ∧ I7. Há um SAT em F4+F4 15+60+240 (cubo 62, [0, 0, 0, 21]) que satisfaz I7, mas tem isotrópicos.
2. Reexaminar onde N1 entra na redução de p=17 (ver `reducao-p17-certificada`, `ponte-astra-liftabilidade`).
