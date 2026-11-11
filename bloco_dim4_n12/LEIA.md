# Bloco de dimensão quatro, n = 12, grau 4 (10/11)

Recontagem independente das quárticas RS bent afins nas classes de V1 = ⟨7,14,28,56⟩ ou V2 = ⟨5,10,20,40⟩. Sem auditoria externa.

## Convenções

- x = (a,b), z = a+b, w = b. A rotação desloca os índices em +1.
- w = s₁·K₁ + s₂·K₂ + Σ uᵢVᵢ, com K = (e₀, e₁) nos dois casos.
- Ponto y = (z, s₁, s₂), índice z + 64·s₁ + 128·s₂. **As duas coordenadas do complemento vêm depois das seis de z**, ao contrário da ordem do piloto.
- Rótulo de π: inteiro de 4 bits, bit i = derivada de f na direção Vᵢ.

## Cadeia

1. `base4.py V`: espaço RS de grau ≤ 4 afim nas classes de V (dimensão 52), π e H.
2. `exporta.py V`: base do espaço de π (31 ou 33 geradores) para o enumerador.
3. `Enumera.cs`: percorre **todos** os 2³¹ ou 2³³ mapas; mantém os que têm 16 fibras de 16 pontos com soma nula de toda função de grau ≤ 2 em cada fibra (código auto-ortogonal). Saída: `mapas_V.txt`.
4. `fases.py V [fatia n]`: para cada mapa, sistema linear h·c = wt(c)/2 nas fases e enumeração da condição wt(h) ≡ 2 (mod 4) em cada fibra.

O critério das fibras é o de `LEMA_FIBRAS_16.md`, com verificador em `verifica_lema_fibras.py`.

## Resultados

| | V2 | V1 |
|---|---|---|
| mapas percorridos | 2³¹ | 2³³ |
| todas as fibras com 16 pontos | 5.612.360 | 2.630.416 |
| auto-ortogonais | 166.472 | 113.040 |
| exclusivos (fora do bloco U e do antipodal) | 17.040 mapas | a contar |
| funções bent exclusivas | **2.326.528** | a contar (catálogo: 1.900.544) |

V2 exclusivo: 4.032 mapas caem por fibra de posto 8, 10.224 pelo sistema linear, 1.920 pela condição quadrática, e 864 admitem fase. O total confere com o catálogo.

A enumeração de V2 e V1 (passo 3) rodou localmente; as fases de V1 rodam no workflow `bloco-dim4`.
