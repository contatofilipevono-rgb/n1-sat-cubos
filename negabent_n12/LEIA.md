# RS bent-negabent de grau ≤ 4 em n=12: verificação exata no catálogo do Astra (10/11)

**Critério.** f é negabent ⇔ f + s₂ é bent, onde s₂ = Σ_{i<j} xᵢxⱼ (RS de grau 2, as 6 órbitas de grau 2). Termos afins não alteram nenhuma das duas bentness, então a normalização do catálogo é inofensiva.

**Método** (negabent_n12.py):
- Expande cada representante a toda a sua órbita de topos quárticos, pela mesma transformação do `lookup` do Astra, vetorizada.
- Para cada topo t, conta as partes baixas L com L ⊕ s₂ também presente para t.

**Resultado:**
- topos: **67.648** (67.647 com quártica + o topo 0);
- registros normalizados: **77.319.680**, que bate exatamente com quartic-counts.json;
- **bent-negabent: 0.**

**Controles:**
- 25 funções sorteadas após a transformação, reconstruídas e conferidas por Walsh nos 4096 pontos: 25 de 25 são bent. Isso valida a expansão das órbitas.
- Nas mesmas 25, f + s₂ por Walsh direto: 0 bent, de acordo com o veredito por pertinência.
- Limite: não há controle positivo de negabent, porque o teorema prevê zero.

**Leitura.** É consistente com a inexistência prevista para n = 4pᵏ (Mandal–Singh–Gangopadhyay–Maitra–Vetrivel, DAM 2018; Mandal–Maitra–Stănică, AAECC 2022; conferir o enunciado exato antes de citar). Serve como **validação externa do catálogo de grau ≤ 4 em n=12**, não como resultado novo.