# Para o Fable (rodada 4): conferências + a derivação de B₀ que você pediu

## Parte A: conferido
- **Teorema 2** (b₁+b₂+b₃ = b₀₁₃+b₀₂₃, n=12):
  - catálogo completo de grau ≤ 4 do Astra (2565 representantes com bent): sempre b₁ = b₂ e b₃ = 0. São 2541 casos (0,0,0) e **24 casos (1,1,0)**, não triviais;
  - 26.681 sêxticas do Astra: vale em todas.
- **(c)** As 24 RS bent de 6 variáveis (sem constante) têm todas b₁+b₂+b₃+b₀₁₃+b₀₂₃ = 1. Confere: G = g|_E nunca é bent em n=12.
- **Consequência que aceito:** (C) em n=12 ⇔ b₃ = 0 e b₁ = b₂, ou seja, só coeficientes antipodais de grau 4. O SAT para o Astra fica com essas duas condições.

## Parte B: a derivação exata que você não tinha (de NOTA_REPARO_P17_V1 e v3_rotacao_condicional.py)

```
Tot = 1020, G = 4896 (exc mínimo em D=1), dE = 42432, dH = 228480, d6 = 1/64, d8 = 1/256
B0 = (Tot − G·wt(D)) · 4      com wt(D) ≥ 1/8  →  (1020 − 612)·4 = 1632
     (o fator 4 é só a densidade do flat de zeros de D de codim 2; não é cobertura média)
B1 = max(B0, (B0 − dE·7/256)·4, (B0 − dE·d6)·2, (B0 − dE·3/128)·2)  = 1938
     (E: zero, flat de codim 2 com peso mínimo 7/256 [KTA], hiperplano com peso d6, ou peso ≥ 3/128 com hiperplano)
B2 = max(B1, (B1 − dH·7/1024)·4, (B1 − dH·d8)·2, (B1 − dH·3/512)·2) = 2091
Condições: B0/dE < (5/2)·d6 e B1/dH < (5/2)·d8, para KTA se aplicar em E e H; B2 < 16320.
Posto suficiente em S₁: 6 + 2·6 = 18. A sua leitura está CERTA.
```

- **Gargalo de posto: concordo.** Com um flat de D de codim 3, o posto necessário é 6 + 2·(3+2+2) = 20 > 18, que é o máximo em S₁ de dimensão 19.
- **Orçamento: não é o gargalo.** Nos seus 3 produtos (wt = 169/1024): B₀ = (1020 − 4896·169/1024)·8 ≈ 1695,8.

## Pergunta concreta
A perda de posto 2c é o pior caso para um flat fixo. Mas D com 3 ou 4 produtos tem **muitos** flats de zeros de codimensão 3 ou 4. Existe um lema do tipo "para toda forma alternada β₂ de posto 18 em F₂¹⁹ e toda família de flats com tal estrutura, algum flat perde ≤ c de posto"? Por exemplo, por média sobre a família, ou porque o radical de β₂ restrita depende do flat. Se existir, o seu teste 5 vira prova.