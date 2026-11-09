# Estado das buscas, para retomar (atualizado em 09/11/2026, ~10:20 UTC)

## ⚠ Snapshot de 09/11, 15:10 UTC: TESTEMUNHA SEM ISOTRÓPICO EM F4+F4

- GitHub run 42547926882 (F4+F4, órbitas 15+960): o cubo 52 deu SAT. A testemunha tem **I6 e zero U isotrópicos em todas as órbitas**.
- Confirmado por força bruta independente sobre os 788.035 subespaços de codimensão 3 de F₂⁹: nenhum tem queda de grau. O controle positivo passa.
- **N1 só com I6 é falso para F4+F4.** A testemunha **não** satisfaz I7, então a versão com I6 ∧ I7 segue aberta.
- Detalhes em `resultados/contraexemplo_N1_F4F4/LEIA.md`. Nada auditado ainda.

**09/11, ~21 UTC: tudo parado.** Pela prova do GPT, o caso de 3 lineares sem termos mistos é trivial (queda em codim 5 via W = ⟨e0, e1, c⟩ ⊕ ⟨x1, x2, x3⟩). As buscas de N1 com I6 ∧ I7 e das sete restrições perderam relevância. VM parada, runs do GitHub canceladas, Colabs desligados. O caso aberto, com termos mistos xᵢxⱼ, segue com o GPT. Ver esultados/estrutura/SETE_RESTRICOES_09NOV.md.

**09/11, 20:30 UTC: alocação.**
- Sete restrições, F4+F4 d=3: Colab tab-7, em 8 cubos.
- Sete restrições nas outras classes (F4^2, Q4a, Q4b, Q4c), d=2 e depois d=3: Colab seed.
- Piloto da codificação por Möbius: GitHub da conta da Débora (rodado pelo GPT), cubos 0, 17, 42 e 63; não duplicar.
- PC: só testes leves (7,7 GB de RAM).

**Snapshot de 09/11, 20:15 UTC:** F4+F4 completo com I7 no GitHub: primeiros 16 cubos, todos INDECISO (15000 s). F4+F4 960 com I7, VM (4 classes) e Colab: sem cubo concluído. Rota das 7 restrições: d=2 SAT, d=3 rodando no PC.

**09/11, 18:40 UTC: VM religada para I6 ∧ I7.**
- VM: F4^2, Q4a, Q4b e Q4c, todas as órbitas, 64 cubos por classe, 8 núcleos cada (`gcp/startup_i7.sh`, resultados em `/opt/i7/<classe>/res`).
- A VM **desliga sozinha em 48 h** (prazo em `/opt/i7/PRAZO`).
- GitHub: F4+F4 só na órbita 960 com I7 (run 42674975207, 16 cubos), além do F4+F4 completo com I7 (run 42649448135).
- Reavaliação da estratégia agendada para cerca de 02:30 UTC de 10/11.

**Snapshot de 09/11, 18:15 UTC:** sem resultado novo.
- I6 ∧ I7 F4+F4 completo no GitHub (run 42649448135): 16 jobs rodando, há 2h20.
- I6 ∧ I7 F4+F4 15+960 no Colab: 8 CaDiCaL, 0 de 64 cubos.
- VM parada; Débora, Q4c e Kaggle desligados de propósito.

**09/11, ~16:30 UTC: reorganização.**
- **Desligadas as buscas de UNSAT por força bruta**, que davam só INDECISO:
  - VM GCP `n1-cubos` **parada** (não apagada);
  - conta 2 cancelada;
  - Colabs da Débora (Q4b) e de Q4c completo encerrados.
- Os resultados delas estão em `resultados/`.
- **Onde N1 entra na cadeia:** o Lema L tem hipótese I6 ∧ I7, e a redução de 3 lineares só precisa de N1 com I6 ∧ I7. A testemunha F4+F4 mata só a versão com I6. Q≡1 e p=17 seguem abertos. Ver `resultados/contraexemplo_N1_F4F4/LEIA.md`.
- **Únicas rodadas ativas:** F4+F4 com I6 ∧ I7, completo no GitHub (run 42649448135) e 15+960 no Colab principal.

**Snapshot de 09/11, 16:15 UTC:** sem resultado novo.
- Conta 2 (Q4b, todas as órbitas, k=8): 72 cubos, todos INDECISO.
- I6 ∧ I7 no GitHub: 4 jobs rodando, 12 na fila. I6 ∧ I7 no Colab: 8 CaDiCaL ativos.

**I6 ∧ I7 (lançado em 09/11, 16 h UTC):**
- I7 (c_S ≡ 0 mod 8 para |S| ≥ 7) agora é codificado em CNF (`i7.py`): N₂ ≡ 2·N₃ (mod 4) em cada um dos 46 conjuntos S, com contador mod 4 dos pares e paridade das triplas.
- Controles (`controle_i7.py`): aceita a testemunha com I7 (cubo 62) e rejeita as duas sem I7 (cubos 28 e 52).
- Workflow: entrada `i7=1`.
- Em andamento:
  - **F4+F4 completo com I6 ∧ I7**: GitHub, run 42649448135 (64 cubos, 16 jobs);
  - **F4+F4 15+960 com I6 ∧ I7**: Colab principal (tab-4, 8 núcleos, `/content/repo_i7`). Ele substitui o F4+F4 completo só com I6, que já foi respondido.
- Um SAT em qualquer dessas rodadas seria contraexemplo também à versão liftável de N1.

**Outros resultados deste snapshot:**
- Q4c órbita 2040 terminou com 9 SAT de 64 (todos com isotrópicos [15, 0, 0] ou [15, 8, 0]).
- Conta 2, Q4b todas (k=8): 44 cubos, todos INDECISO.
- **O Kaggle caiu** (sessão "off", provavelmente pelo limite de 12 h). Não houve "Save Version", então a saída se perdeu.
- Débora: 13,25 h, sem cubo concluído.

**Estrutura nova (09/11, tarde; detalhes em `resultados/estrutura/Q4_ESPALHAMENTO_09NOV.md`):**
- Q4: a órbita 255 é formada pelas estrelas de um espalhamento de 17 subespaços W (dim 4). Isotropia exige C3|W = 0 (na estrela) ou C3|W' = 0 (W' = U∩W, órbitas 1020/2040).
- A parte linear de I6 sobre C3 é exatamente **C3 ∧ T = 0** (8 condições), nas 5 classes.
- Sem I6, os U isotrópicos **não** cobrem todos os C3 (Q4a, Q4c, F4^2, F4+F4), mas o conjunto N dos C3 sem isotrópico é raríssimo. **N1 ⇔ nenhum C3 ∈ N ∩ {C3∧T=0} se estende a I6.** Com C3 fixo, isso é um sistema quadrático em 112 incógnitas.
- Teste de um C3 ∈ N ∩ L de Q4a: **encerrado sem resposta** (3 h na VM, 1 h no CMS). Como uma C3 genérica não se estende (112 incógnitas, 120 equações), esse teste isolado tem pouco valor. A VM voltou ao F4^2 completo, com 32 núcleos.
- Tentativa de descrever E (as C3 extensíveis) por quádricas: 952 amostras, sem relações que sobrevivam à validação. Resultado inconclusivo (ver a nota).
- Colab da Valéria (75 h livres): células prontas em `plataformas/celula_valeria_Q4a_o01.txt` (Q4a, órbitas 255+1020). Falta montar o Drive e colar; o Chrome não estava conectado.

**Snapshot de 09/11, 10:20 UTC:**
- GitHub, Q4b órbita 2040 (run 42521672988, concluída): **14 SAT** de 64, 50 INDECISO.
- GitHub, Q4c órbita 2040 (run 42521679875, parcial): **7 SAT** de 48 concluídos.
- Os 21 SAT foram reconferidos no PC (`reconferencia_pc.json` em `resultados/github_cubos/Q4b_o2` e `Q4c_o2`). Todos têm I6, e 19 têm isotrópicos **só na órbita 255, exatamente 15 deles** ([15, 0, 0]).
- Com isso, nas três classes Q4 (a, b, c) toda família forçante precisa conter a órbita 255. Padrão a investigar: o número 15 é o de hiperplanos de F_2^4, o que sugere uma estrutura fixa nas testemunhas.
- Runs antigas 42521686575, 42529019676/27880 e 42543042454/49518 aparecem como "cancelled/failure". Foram canceladas em 08/11 21:43 e só o job `resumo` rodou agora, sem artefato. Não houve perda.
- Colabs, Kaggle (8h34m de sessão), VM (F4^2, 32 CaDiCaL) e conta 2: sem cubo novo.
- Correção: o commit 3f5fcbb gravou este arquivo com acentos corrompidos; foi corrigido aqui.

**Snapshot de 09/11, 04:15 UTC:**
- Todas as plataformas no ar.
- Na VM, F4^2 completa ainda não fechou nenhum cubo depois de 6,6 h, e o H16 ainda não terminou nenhuma iteração.
- Os Colabs com classes completas e o Kaggle ainda não têm cubo concluído.
- A segunda conta do GitHub roda com 5 jobs.

**Snapshot de 09/11, 08:10 UTC:**
- Segunda conta, Q4b todas com k=8: os 20 primeiros cubos (5 jobs) deram **INDECISO a 15000 s** (`resultados/github_conta2/Q4b_o012_k8/`). Nem k=8 basta para a classe completa; para UNSAT, será preciso k≥10 ou mais tempo por cubo.
- Colabs (F4+F4, Q4c e Q4b da Débora), Kaggle e VM (F4^2): seguem sem cubo concluído. Nada novo.

**VM spot interrompida pelo Google às 05:43 UTC; religada às ~06:50 UTC.**
- O F4^2 completo retomou com 32 CaDiCaL. Os cubos recomeçam do zero, porque nenhum havia terminado.
- **O H16 não foi relançado.** Em 6,6 h dividindo a máquina com o N1, ele não completou nenhuma iteração do CEGAR. Antes de gastar mais máquina com ele, é preciso uma codificação mais leve.

Leia isto primeiro se você é uma pessoa ou IA continuando o trabalho.

**Regras do projeto:**
- Nada aqui é resultado auditado.
- UNSAT só vale com prova DRAT verificada.
- Toda solução SAT é conferida por tabela-verdade.
- Não declarar novidade nem resolução de problema sem revisão e comparação bibliográfica.

## O problema (N1)

T é uma quártica em 8 variáveis Y, de uma de 5 classes críticas: F4+F4, F4^2, Q4a, Q4b, Q4c.

D = q1·q2 + x·C3 + R é uma função booleana em 9 variáveis, com grau ≤ 4. A parte quártica de q1·q2 é T.

I6 é a condição de divisibilidade dos coeficientes inteiros da ANF: c_S ≡ 0 mod 4 para |S| ≥ 6.

**Pergunta de N1:** I6 obriga a parte quártica de D a se anular num subespaço de codimensão 3 (um "U isotrópico")?

**Reformulação usada no código.** Todo U isotrópico de codimensão 3 tem a forma U_Y + ⟨e_x + v⟩, em que U_Y é um subespaço de codimensão 3 de Y isotrópico para T. As restrições ficam assim:

- "não isotrópico em U_Y" vira uma restrição linear em C3 (`sat_n1_cegar.prepara_U`);
- os U_Y isotrópicos se dividem em órbitas do grupo de automorfismos de T (arquivos `automorfismos_*.json`; script `sat_n1_orbita.py`);
- um SAT restrito a um conjunto S de U_Y dá um D com I6 que escapa de todos os U_Y de S;
- UNSAT com S igual a todas as órbitas prova N1 para a classe.

Tamanhos das órbitas:

| Classe | Órbitas de U_Y |
|---|---|
| F4^2 | 15, 60, 240, 2880 |
| F4+F4 | 15, 60, 240, 960 |
| Q4a, Q4b, Q4c | 255, 1020, 2040 |

O índice da órbita no código (k) segue a ordem crescente de tamanho.

## Resultados já obtidos (`resultados/`)

Todas as soluções SAT abaixo têm I6 conferido; a última coluna diz em quais órbitas a testemunha tem U_Y isotrópicos. Para F4+F4 e F4^2 a ordem é [15, 60, 240, maior]; para Q4, [255, 1020, 2040].

| Classe | Órbitas testadas | Resultado | Isotrópicos da testemunha |
|---|---|---|---|
| F4^2 | 15 | SAT | [0, 7, 36, 552] |
| F4^2 | 60 | SAT | [7, 0, 3, 75] |
| F4^2 | 240 | SAT | [0, 0, 0, 46] |
| F4^2 | 2880 | SAT (VM GCP, cubo 7) | [15, 24, 24, 0] |
| F4+F4 | 15 | SAT | — |
| F4+F4 | 60 | SAT | — |
| F4+F4 | 240 | SAT | — |
| F4+F4 | 960 | SAT (Colab) | [15, 20, 0, 0] |
| F4+F4 | 15+60+240 | SAT (GitHub, cubos 28 e 62) | [0, 0, 0, 12] e [0, 0, 0, 21] |
| Q4a, Q4b, Q4c | 255 | SAT | só nas órbitas de 1020 e 2040 |
| Q4a | 1020 | SAT (Colab, cubo 1 de 64, 15641 s; reconferido no PC em 09/11) | [7, 0, 14]; I6 sim, I7 não, posto de C3 = 8 |
| Q4a | 2040 | SAT em 17 de 64 cubos (GitHub run 42521666326; 47 INDECISO; os 17 reconferidos no PC) | quase todos **[15, 0, 0]** ou [19, 0, 0]; alguns [15, 8, 0]; posto de C3 = 8 |
| Q4c | 1020 | SAT (Colab, cubo 0 de 64, 23439 s; reconferido no PC) | **[19, 0, 0]**; reta comum a todos os 19 |
| Q4b | 2040 | SAT em 14 de 64 cubos (GitHub run 42521672988; 50 INDECISO; reconferidos no PC em 09/11) | 12 × **[15, 0, 0]**, 2 × [15, 8, 0]; I7 não; posto de C3 = 8 |
| Q4c | 2040 | SAT em 9 de 64 cubos (GitHub run 42521679875, concluída; reconferidos no PC) | 8 × **[15, 0, 0]**, 1 × [15, 8, 0]; um com I7 |
| **F4+F4** | **15+960** | **SAT (GitHub run 42547926882, cubo 52; reconferido no PC e por força bruta independente)** | **[0, 0, 0, 0]: nenhum isotrópico. I6 sim, I7 não** |

**Leitura nova para Q4 (09/11, manhã).** Há testemunhas com I6 que escapam ao mesmo tempo das órbitas 1020 e 2040:
- Q4a: 13 dos 17 cubos têm isotrópicos só na órbita 255;
- Q4c: o cubo 0 tem isotrópicos só na órbita 255.

Logo, em Q4a e Q4c, uma família que force isotropia precisa conter a órbita de 255. Como a órbita 255 sozinha não força (já há SAT), a próxima pergunta precisa é a união 255 + 1020 + 2040, isto é, as rodadas de classe completa.

**Leitura:**
- Nenhuma órbita isolada força isotropia, nem as uniões testadas.
- Invariantes das testemunhas (I7, posto de C3, estrutura): `resultados/estrutura/`.
  - Metade das testemunhas satisfaz também I7, isto é, são liftáveis.
  - O mínimo observado é 12 U_Y isotrópicos.

## Em andamento (quem roda o quê)

| Problema | Onde | Como acompanhar |
|---|---|---|
| F4^2, todas as órbitas | VM GCP `n1-cubos` (32 núcleos), `/opt/n1/repo/res` | `gcloud compute ssh n1-cubos --zone us-central1-a` |
| H16: filtros 2-ádicos, CEGAR | mesma VM, `/opt/h16/saida.txt` | `resultados/h16/` |
| F4+F4, todas as órbitas | Colab (Drive: `n1_colab_08nov/F4F4_todas`); também PC local, instância inteira | `RESUMO.json` no Drive |
| F4+F4, 15+960 | GitHub Actions (run 42547926882) | `gh run view` |

F4^2, 15+2880: Kaggle (4 núcleos, internet ligada), saída em `/kaggle/working/n1`. Use "Save Version" para guardar os arquivos; o placar sai na saída da célula.
| Q4a, todas as órbitas; Q4b/Q4c 2040 | GitHub Actions, workflow `cubos` | `gh run list` |
| Q4b, todas as órbitas, k=8 (256 cubos) | GitHub Actions da segunda conta, fork `filipemvono-ops/n1-sat-cubos`, run 42557164345 | `gh run view 42557164345 -R filipemvono-ops/n1-sat-cubos` |
| Q4b, todas as órbitas, k=6 (64 cubos) | Colab da conta parceira (Drive dela: `n1_inst_09nov/Q4b_todas`), 2 núcleos, só como conferência independente | `RESUMO.json` no Drive dela |
| Q4c, todas as órbitas | Colab (Drive: `n1_inst_09nov/Q4c_todas`) | — |
| Q4a/b/c, órbita 1020 em cubos; Q4 2040 inteira | Colab principal (Drive: `n1_colab_08nov/cubos_q4`) | — |

## Dificuldade dos cubos (medida)

- A rodada F4+F4 15+60+240 no GitHub (k=6, 64 cubos, 15000 s por cubo) terminou assim:
  - 2 cubos SAT, os cubos 28 e 62;
  - **62 cubos INDECISO**.
- Nas classes completas, que têm mais restrições, cubos k=6 provavelmente também estouram o tempo. Uma resposta UNSAT vai exigir subdividir os INDECISO (k maior) ou dar mais tempo por cubo. Um SAT já responde.
- Para Colab gratuito, que desconecta por inatividade, use `plataformas/colab_retomavel_q4b_k10.py`:
  - 1024 cubos com 50 min cada;
  - copia os resultados ao Drive a cada 3 min;
  - ao reconectar, retoma do que já está no Drive.

## Como retomar uma rodada

**Qualquer Linux:**
```
git clone https://github.com/contatofilipevono-rgb/n1-sat-cubos.git
cd n1-sat-cubos
python plataformas/executor.py "Q4b" automorfismos_Q4b.json 0,1,2
```

**GitHub Actions:**
```
gh workflow run cubos -f classe=Q4b -f auto=automorfismos_Q4b.json -f orbitas=0,1,2 -f k=6
```

Cubos já resolvidos ficam em `res/` e são pulados ao relançar no mesmo diretório.

## Próximas perguntas (da análise de estrutura)

1. I6 limita o posto de C3?
2. Descrever os 12 U_Y isotrópicos da testemunha mínima de F4+F4.
3. Classes completas: algum cubo SAT seria contraexemplo a N1. Conferir de forma independente antes de qualquer conclusão.
