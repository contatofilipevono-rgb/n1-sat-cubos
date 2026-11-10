# Regra g(0)+g(1) ≡ n/2 em n=12, testada no catálogo do Astra (10/11)

**Fonte.** contatofilipevono-rgb/hrsbf-bent-verification, ref 8792261, research_updates/2026_11_09_n12_mixed.

**Redução.** Em n=12, uma órbita de rotação de tamanho ímpar tem tamanho 1 ou 3.
- Tamanho 1: monômio vazio ou x0…x11. A constante entra em g(0) e em g(1) e se cancela.
- Tamanho 3: máscara de período 3, com peso 4 ou 8. Bent tem grau ≤ 6, então só sobra o peso 4.

Logo, para RS bent em n=12, de qualquer grau:

> regra ⇔ o coeficiente da órbita {x0x3x6x9, x1x4x7x10, x2x5x8x11} é 0.

Essa órbita é o bit 42 do topo quártico do Astra. O bit é invariante pelos operadores de simetria dele.

**Grau ≤ 4: catálogo completo** (catalog/catalog-index.tsv).
- Representantes com bent: 2565, contando o topo 0.
- Registros: 4.029.176. Ponderados: 77.319.680 = 77.305.344 quárticas + 14.336 de grau 2/3. Bate com quartic-counts.json.
- **Nenhum representante com bent contém a órbita 42.** Portanto a regra vale para todas as RS bent de grau ≤ 4 em n=12, condicional à completude do catálogo do Astra.

**Grau 5–6: catálogos parciais.** Arquivos: dual5, two/three-quintic, two-sextic, su6, sparse.
- Nenhuma linha tem o bit 42 na coluna de topo.
- Ressalva: o layout das colunas foi inferido, não conferido no código.

Script: q1_estrutura_09nov/chk42.py (também está em %TEMP%).