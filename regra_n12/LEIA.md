# Piloto CP-SAT: RS bent em n=12 (10/11) — NEGATIVO

**Modelo** (cpsat_rs_bent.py):
- incógnitas: 215 coeficientes de órbitas, graus 1 a 6;
- tabela-verdade nos 352 representantes de órbita, via AddBoolXOr;
- 352 igualdades de Walsh com pesos inteiros, W(u) = ±64.

**Controle positivo** (qualquer RS bent, sem restrição; existem centenas de milhões):

| grau máximo | variáveis | resultado |
|---|---|---|
| ≤ 2 | 7 | achou em 5 s (bent conferida nos 4096 pontos) |
| ≤ 3 | 26 | UNKNOWN em 60 s (a força bruta em 2²⁶ seria mais rápida) |
| ≤ 4 | 69 | UNKNOWN em 60 s |
| ≤ 6 | 215 | UNKNOWN em 120 s |

**Conclusão.** A codificação direta (XOR + somas de Walsh) é fraca demais para o solver. Ela não acha nem as bent que existem, então um UNSAT dela nunca seria alcançável. Pelo critério combinado, o piloto parou aqui, sem uso da VM.

**Leitura.** Fechar a regra em n=12 por computação exige estrutura, e isso vale também para o pipeline do Astra.
- Os graus 5 e 6 têm 146 órbitas altas, 2¹⁴⁶ partes altas. O Astra só cobre famílias estruturadas delas.
- O fechamento realista é teórico: as relações por classes laterais de E e de P₄^⊥ (Teoremas do Fable) param em mod 8 em n=12. Falta um ingrediente que veja b₃ diretamente.