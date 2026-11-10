# Caso misto do Lema L: busca EXATA pelo grau 8 completo de I6 (10/11)

**Origem.** Os certificados de paridade dos 3 trios da semente 111 usam só equações de grau 8:
- |S| = 8 com {xᵢ, xⱼ} + 6 y, que codifica φᵢ∧φⱼ = T∧Aᵢⱼ;
- |S| = 8 com {x₁, x₂, x₃} + 5 y, que codifica T∧B + φ₁∧A₂₃ + φ₂∧A₁₃ + φ₃∧A₁₂ = 0.

β=0 só garante cada Aᵢⱼ separadamente. A obstrução é o sistema conjunto, um produto triplo do tipo Massey: γ(φ₁,φ₂,φ₃) = [φ₁A₂₃ + φ₂A₁₃ + φ₃A₁₂] mod T·Λ¹, a menos das escolhas de Aᵢⱼ.

**gama_massey.py.**
- Controle: os 3 trios da semente 111 dão γ insolúvel, como o certificado.
- Em 400 trios aleatórios com β=0, γ é insolúvel em 99,5%: o grau 8 completo é muito mais forte que β=0.

**gama_dirigido.py** (exato por par):
- Para cada par (a,b) com a, b e a+b em N e β=0, e para cada uma das 2¹⁰ escolhas de A₁₂, as condições sobre (φ₃, A₁₃, A₂₃, B) são lineares.
- O núcleo, projetado em φ₃, é um subespaço P, que enumeramos inteiro.
- Testamos se c, c+a, c+b e c+a+b estão em N.

**Resultado.**
- 800 pares (sementes 101 e 102) × 1024 escolhas de A₁₂: **0 trios** com o grau 8 de I6 completo e as 7 combinações sem isotrópico.
- Controle cruzado: 6400 vezes, um φ₃ sorteado em P torna solúvel o sistema independente de gama_massey. Esse controle pegou e corrigiu um bug de iteração antes da rodada.

**Observação estrutural.** dim P = 6 em todos os casos, e P contém a e b, porque φ₃ = φ_a satisfaz o sistema com A₁₃ = 0 e A₂₃ = A₁₂. Ou seja, o grau 8 deixa só 2⁴ classes de φ₃ por escolha de A₁₂.

**Conjectura (Lema do caso misto).** Se φ₁, φ₂, φ₃ satisfazem o grau 8 de I6 (β=0 e γ=0), então alguma das 7 combinações tem subespaço isotrópico. Pelo argumento das 7 restrições, isso daria queda de grau em codimensão 5 e fecharia o caso misto do Lema L.

**Limite da evidência.**
- É amostral nos pares (800). A enumeração é exata dentro de cada par.
- Não há controle positivo, porque não se conhece nenhum trio que passe.
- **Pergunta para a frente teórica:** por que dim P = 6? Provar dim P = 6 e descrever P explicitamente pode tornar o lema finito e verificável.