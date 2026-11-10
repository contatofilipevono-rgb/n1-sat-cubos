# Decomposição em 4 de RS bent no subespaço invariante V = {pares = 0 = ímpares} (09/11)

As RS bent de n = 8 foram enumeradas por completo (todas têm grau ≤ 4); em n = 10, até grau 3; em n = 12, até grau 2.

- **Regularidade:** sinal(W(0)·W(1)) = (−1)^{n/2} em todas as funções testadas. Consequência: o tipo BBBB nunca ocorre com n ≡ 0 mod 4, e o tipo SSSS nunca ocorre com n ≡ 2 mod 4.
- Não usa homogeneidade, e a prioridade não foi verificada.
- Detalhes no caderno de técnicas (Técnica 39).

## Redução (09/11)

- Pela dualidade, a regra equivale a: toda RS bent g tem g(0) + g(1) ≡ n/2. Na ANF, isso é a soma dos coeficientes das órbitas de monômios de tamanho ímpar.
- n = 2^t: trivial (grau ≤ n/2).
- n = 2p^a: é a paridade antipodal (thm:apar, m = 2) da nota de grau ímpar.
- Demais n (12, 20, 24, …): aberto.
- Os dados de n = 8, 10 e 14 caem nos casos já provados.

## n = 12, caso aberto (09/11)

- A busca semi-exaustiva (linear + quadrática arbitrárias + até 2 órbitas de grau 3 ou 4) achou 128 RS bent: 32 de grau 2 e 96 de grau 3. **Todas** satisfazem g(0) + g(1) = 0 = n/2 mod 2, e o tipo é SSSS.
- Não há RS bent PS de Dillon em n = 12: as órbitas de Frobenius em Z/65 têm tamanhos {1, 4, 12×5} e nunca somam 32 ou 33.
- É evidência a favor da regra no primeiro caso aberto, ainda sem prova.
