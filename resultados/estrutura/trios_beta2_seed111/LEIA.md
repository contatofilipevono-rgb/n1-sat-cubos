# Busca dirigida de trios (trios-beta2, run 42721088027): resultado e teste de extensão (10/11)

**Busca.** 16 sementes, s=22, cerca de 950 pares com β=0 por semente.
- 15 sementes: 0 trios.
- Semente 111: 3 trios, todos dentro de um conjunto de 4 vetores de L/G. Cada um tem β=0 nos três pares e nenhum subespaço isotrópico nas 7 combinações.

**Extensão a 11 variáveis** (ext_cms.py; Aᵢⱼ, B e R livres; I6 ∧ I7). Os 3 trios dão **UNSAT por certificado de paridade já na relaxação linear de I6**, em cerca de 0,1 s cada (certificados em ext_trio*.log, com 45 a 48 equações). O controle desse código, feito em 09/11, segue válido: uma solução embutida (cubo 62) é aceita e uma perturbada é rejeitada.

**Leitura.**
- Os 4 trios conhecidos com β=0 e sem isotrópico (trio0 de 09/11 e estes 3) são incompatíveis com I6. Portanto não são contraexemplo ao Lema L.
- β=0 resume só parte das condições de I6 no grau 8. O que mata os trios é o restante do sistema: T∧B + Σφ∧A = 0 e as equações de grau mais baixo com R.
- **Conjectura de trabalho:** "β=0 + 7 retas sem isotrópico + I6 completo" seria vazio. Se isso for provado, o caso misto fecha pelo argumento das 7 restrições.
- **Pergunta para a frente teórica:** qual combinação das equações do certificado S é a obstrução? Os certificados dos 3 trios compartilham a maior parte dos índices.