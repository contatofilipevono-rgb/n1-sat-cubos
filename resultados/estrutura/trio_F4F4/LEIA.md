# Lema das sete restrições: falso em F4+F4 (09/11/2026)

**Resultado.** Existem cúbicas φ₁, φ₂, φ₃ em Y = F₂⁸ com φᵢ ∧ T = 0 (T de F4+F4), independentes módulo o gauge ι_u T, tais que **nenhuma** das 7 combinações φ_v tem U_Y isotrópico. O trio está em `trio_s22_seed1.json` (primeira entrada de `trios`).

Nada aqui foi auditado por pessoa. A conferência é por computação, com dois caminhos independentes (abaixo).

## O trio

```
φ1 = y0y1y2 + y0y1y6 + y0y2y3 + y0y2y5 + y0y2y7 + y0y3y4 + y0y3y5 + y0y3y6 + y0y3y7 + y0y4y5 + y0y5y6 + y0y6y7 + y1y2y7 + y1y5y6 + y1y5y7 + y1y6y7 + y2y3y4 + y2y3y5 + y2y3y7 + y2y4y7 + y2y5y6 + y2y6y7 + y3y4y5 + y3y5y6 + y4y6y7
φ2 = y0y1y3 + y0y1y4 + y0y1y5 + y0y1y6 + y0y2y3 + y0y2y4 + y0y2y5 + y0y2y6 + y0y2y7 + y0y3y5 + y0y3y6 + y0y3y7 + y0y4y6 + y0y4y7 + y1y2y6 + y1y4y5 + y1y5y6 + y1y6y7 + y2y3y4 + y2y3y5 + y2y3y6 + y2y3y7 + y2y4y6 + y2y4y7 + y2y5y7 + y2y6y7 + y3y4y5 + y3y5y6 + y3y6y7 + y4y5y6 + y4y5y7 + y4y6y7 + y5y6y7
φ3 = y0y1y2 + y0y1y6 + y0y1y7 + y0y2y3 + y0y3y6 + y0y4y5 + y0y4y7 + y0y5y6 + y0y6y7 + y1y2y3 + y1y2y4 + y1y2y5 + y1y2y6 + y1y2y7 + y1y4y5 + y1y5y6 + y2y3y6 + y2y3y7 + y2y4y5 + y2y4y7 + y2y6y7 + y3y5y6 + y4y5y6 + y4y5y7 + y4y6y7
```

## Como conferir

```
python verifica_trio.py trio_s22_seed1.json --repo ../n1-sat-cubos
```

`verifica_trio.py` não importa nada dos outros scripts desta pasta. Ele:

- (a) confere φᵢ ∧ T = 0 pelo produto de ANFs;
- (b) reenumera os 97155 subespaços de dimensão 5, acha os 1275 isotrópicos de T, e para cada um testa, por tabela-verdade e transformada de Möbius, se a parte cúbica de φ_v|U está no span das partes cúbicas de (T(y+eᵢ) − T(y))|U. Resultado: 0 isotrópicos nas 7 combinações;
- controle positivo: φ = ι_{e3+e5} T acusa isotrópico;
- (c) com `--repo`, chama `iso_nove.tem_iso3` do repositório nas 7 combinações: `None` em todas.

## Redução usada (verificável à mão)

1. Para u ∈ U_Y, (ι_u T)|U_Y = ι_u(T|U_Y), que não tem parte cúbica porque T|U_Y tem grau ≤ 3. Logo R_U = {ι_u T|U_Y} é imagem de Y/U_Y e tem dimensão ≤ 3. Computação: é exatamente 3 nos 1275 casos.
2. As cúbicas em U_Y têm dimensão 10, então "U_Y isotrópico para φ" são 7 equações lineares em φ. A_U = {φ ∈ L/G isotrópico em U} tem codimensão 7 em L/G (dim 40), nos 1275 casos.
3. N = (L/G) ∖ ⋃_U A_U. O lema equivale a: **não existe subespaço V de dimensão 3 em L/G com V ∩ A_U = 0 para todo U.**
4. Critério C2 (suficiente para o lema): se existe polinômio Q de grau ≤ 2 em L/G com Q(0)=0 e Q ≡ 1 em N, então N não contém 3-subespaço, porque Σ_{S ⊆ {a,b,c}} Q(ΣS) = 0 para grau ≤ 2 e as 7 parcelas não nulas somariam 1. Era o único mecanismo simples compatível com d=2 falso e d=3 verdadeiro.
5. C2 falha: com 4119 amostras de N, nenhum polinômio de grau ≤ 2 (821 monômios) se anula no conjunto de treino.

## Como o trio foi achado

`sete3.py 22 1`: subespaço aleatório S de dimensão 22 em L/G; N ∩ S enumerado exatamente (20849 elementos, 0,50%); dentro de S, somas viram XOR de índices. Foram achados 20 trios entre os primeiros 116431 planos contidos em N ∩ S (a busca para em 20). Ou seja, 3-subespaços em N são abundantes, na ordem da previsão por independência (densidade 0,005⁷).

Números medidos: densidade de N em L/G ≈ 0,50% (o brief diz ≈ 0,7%); média de isotrópicos 9,96 = 1275/128.

## O que isto NÃO diz

- Não refuta o caso de 3 lineares do Lema L. O trio só usa a parte linear de I6 (φᵢ ∧ T = 0). I6 e I7 completos sobre Δ = T + Σ xᵢφᵢ + (grau ≤ 3) impõem condições quadráticas que acoplam os φᵢ, e não foi testado se este trio se estende.
- As sete restrições à reta t·v não esgotam os subespaços de codimensão ≤ 5: há os que projetam em (x₁,x₂,x₃) com dimensão 2 ou 3 (U_Y de codimensão 4 ou 5 em Y). Não foram testados para este trio.
- Nada sobre F4², Q4a/b/c. Nada sobre Q≡1 ou p=17.

## Arquivos

- `sete.py`: base (T, 1275 U_Y, funcionais), amostragem de N, teste C2, busca por triângulos em pool.
- `sete2.py`: φ₃ sobre plano fixo (CMS com 40 variáveis; recozimento). Não deu resposta no tempo testado.
- `sete3.py`: busca exata em subespaço S. Foi a que funcionou.
- `verifica_trio.py`: conferência independente.
