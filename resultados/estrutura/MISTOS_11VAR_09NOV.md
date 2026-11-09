# Missão: quárticas com termos mistos em 11 variáveis (F4+F4), 09/11/2026, noite

**Status:** em andamento. Os resultados vêm separados em três tipos: SAT verificado, UNSAT certificado e indeciso. Nada aqui foi auditado.

## Modelo

**Variáveis.** Os bits 0–7 são y₀..y₇ e os bits 8–10 são x₁..x₃.

**Parte quártica.**

Δ = T + Σᵢ xᵢφᵢ + Σ_{i<j} xᵢxⱼAᵢⱼ + x₁x₂x₃B

- T está em F4+F4, com máscaras 15, 86, 89, 90, 101, 106, 149, 154, 165, 166, 169 e 240.
- A função completa é D = Δ + R, com deg R ≤ 3.

**Espaços** (definições da missão):
- L = ker(T∧ : Λ³ → Λ⁷);
- G = ι_Y T;
- J = T ∧ Λ² ⊂ Λ⁶;
- β([a], [b]) = a ∧ b mod J, definida em L/G.

## Passo 1: pares e trios em L/G com β = 0 e sem isotrópico nas retas (`beta_busca.py`, Colab)

**Controles exatos:** dim J = 18 e posto de β em Λ²(L/G) = 10. Os dois batem com os valores da missão.
- Uma versão anterior tinha um erro: a máscara cúbica estava com o bit de x ligado e dava posto 0. O erro foi corrigido e o resultado daquela versão foi descartado.

**Pares (d = 2):** SAT em 2 de 2 sementes (123 e 141 s), cada um conferido de forma independente:
- β(φ₁, φ₂) = 0;
- as 3 combinações não têm U_Y isotrópico.

Logo **existem pares com β = 0 e todas as retas em N**.

**Trios (d = 3):** 4 sementes rodando no Colab seed; ainda sem resposta.

## Passo 2: extensão a I6 ∧ I7 com A_ij, B, R livres (`ext_cms.py`)

**(a) Relaxação linear exata de I6** (produtos como colunas): uma inconsistência dá um certificado de paridade, isto é, uma lista de conjuntos S cuja soma das equações dá 0 = 1.

**(b) SAT:** CryptoMiniSat, com a tabela-verdade em XOR nativo e a borboleta de Möbius mod 8 em cláusulas. Qualquer SAT é conferido nos 2.048 pontos.

**Controles:**

| Controle | Resultado |
|---|---|
| Trio antigo (`trio_s22_seed1`, trio 0) | **UNSAT por certificado de paridade em I6** em 0,2 s, com S = {879, 927, 943, 1014, 1017, 1018}. Coerente com o GPT. |
| Solução conhecida: testemunha F4+F4 do cubo 62 (I6 ∧ I7 em 9 variáveis), mergulhada com φ₁ = C₃ dela e φ₂ = φ₃ = 0 | aceita; tabela: I6 sim, I7 sim, grau 4 |
| A mesma, com 1 monômio cúbico trocado | rejeitada; tabela: I6 não |
| φ = 0, busca livre | relaxação consistente; o CMS ainda não achou solução (mais de 15 min) |

**Codificação anterior.** A versão em CNF pura (`ext_mobius.py` com CaDiCaL) não decidiu nenhum dos controles em 15 min, porque as cadeias de XOR da tabela-verdade atrapalham o CDCL. Essa versão foi substituída.

## Passo 3: cobertura das quedas em codim 5

Ainda não foi rodado. Só será necessário se algum trio sobreviver ao passo 2.
