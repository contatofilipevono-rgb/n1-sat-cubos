# Testes algébricos de I6 ∧ I7 sobre C₃ (09/11/2026, fim da tarde)

**Status:** resultados negativos. As eliminações são exatas; as amostragens são empíricas. Nada foi auditado.

**Pergunta:** I7 (liftabilidade) impõe a C₃ alguma restrição que, sozinha, force U isotrópico em F4+F4? Se impusesse, N1 com I6 ∧ I7 sairia por álgebra linear, sem força bruta.

## 1. Relaxação de I6 ∧ I7 em 9 variáveis (`linear_c3_i7.py`, `quad_c3_i7.py`)

**Codificação.** I7 foi escrito como equações polinomiais booleanas exatas:
- N₂ ≡ 2·N₃ (mod 4), para |S| ≥ 7;
- equivalentemente, e₂(indicadoras de pares) + N₃ ≡ 0 (mod 2), dado N₂ par.

**Validação.** As equações reproduzem exatamente as falhas de I7 vistas por tabela-verdade:

| Testemunha | Equações violadas | Falhas de I7 por tabela |
|---|---|---|
| cubo 52 | 7 de 174 | 7 |
| cubo 28 | 9 de 174 | 9 |
| cubo 62 (com I7) | 0 | 0 |

**Resultado.** Eliminando todos os monômios que contêm variáveis de R, as consequências que envolvem só C₃ (até grau 2 em C₃) são **as mesmas 8 restrições lineares C₃ ∧ T = 0** de I6. I7 não acrescenta nada nesse nível.

## 2. Separação em x (`metades8.py`)

**Ideia.** Se D é liftável, D₀ = D|ₓ₌₀ e D₁ = D|ₓ₌₁ são liftáveis em 8 variáveis, ambas com parte quártica T. Logo C₃ = R₃(D₁) − R₃(D₀).

**Teste.**
- Amostradas 60 funções liftáveis T + R em 8 variáveis (F4+F4).
- Cada uma foi conferida por tabela-verdade: I6 e I7.
- Mediu-se W = span das diferenças das partes cúbicas, mais o gauge ι_u T.

**Resultado.** dim W = 48 e **W = L = {C : C ∧ T = 0}**. A separação em metades também não restringe C₃ além de L.
- Explicação: em 8 variáveis, a condição em |S| = 7 é T ∧ R₃ = const, que é linear.

## Conclusão

- Em F4+F4, o efeito de I6 e I7 sobre os isotrópicos passa **necessariamente pela parte R, de forma não linear**. Não há atalho "só em C₃", nem linear nem quadrático.
- Para N1 com I6 ∧ I7, restam duas vias:
  1. **SAT completo**, em andamento: GitHub, run 42649448135 (F4+F4, todas as órbitas); Colab (15+960).
  2. **Rota conceitual nova** para o caso "produto + 3 lineares" do Lema L, que não passe pela restrição fixa x₁ = x₂ = 0 com codimensão 3 exata.
