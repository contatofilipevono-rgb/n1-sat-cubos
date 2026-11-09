# Estado das buscas, para retomar (atualizado em 09/11/2026, ~08:10 UTC)

**Snapshot de 09/11, 04:15 UTC:**
- Todas as plataformas no ar.
- Na VM, F4^2 completa ainda nÃ£o fechou nenhum cubo depois de 6,6 h, e o H16 ainda nÃ£o terminou nenhuma iteraÃ§Ã£o.
- Os Colabs com classes completas e o Kaggle ainda nÃ£o tÃªm cubo concluÃ­do.
- A segunda conta do GitHub roda com 5 jobs.

**Snapshot de 09/11, 08:10 UTC:**
- Segunda conta, Q4b todas com k=8: os 20 primeiros cubos (5 jobs) deram **INDECISO a 15000 s** (`resultados/github_conta2/Q4b_o012_k8/`). Nem k=8 basta para a classe completa; para UNSAT, serÃ¡ preciso kâ‰¥10 ou mais tempo por cubo.
- Colabs (F4+F4, Q4c e Q4b da DÃ©bora), Kaggle e VM (F4^2): seguem sem cubo concluÃ­do. Nada novo.

**VM spot interrompida pelo Google Ã s 05:43 UTC; religada Ã s ~06:50 UTC.**
- O F4^2 completo retomou com 32 CaDiCaL. Os cubos recomeÃ§am do zero, porque nenhum havia terminado.
- **O H16 nÃ£o foi relanÃ§ado.** Em 6,6 h dividindo a mÃ¡quina com o N1, ele nÃ£o completou nenhuma iteraÃ§Ã£o do CEGAR. Antes de gastar mais mÃ¡quina com ele, Ã© preciso uma codificaÃ§Ã£o mais leve.

Leia isto primeiro se vocÃª Ã© uma pessoa ou IA continuando o trabalho.

**Regras do projeto:**
- Nada aqui Ã© resultado auditado.
- UNSAT sÃ³ vale com prova DRAT verificada.
- Toda soluÃ§Ã£o SAT Ã© conferida por tabela-verdade.
- NÃ£o declarar novidade nem resoluÃ§Ã£o de problema sem revisÃ£o e comparaÃ§Ã£o bibliogrÃ¡fica.

## O problema (N1)

T Ã© uma quÃ¡rtica em 8 variÃ¡veis Y, de uma de 5 classes crÃ­ticas: F4+F4, F4^2, Q4a, Q4b, Q4c.

D = q1Â·q2 + xÂ·C3 + R Ã© uma funÃ§Ã£o booleana em 9 variÃ¡veis, com grau â‰¤ 4. A parte quÃ¡rtica de q1Â·q2 Ã© T.

I6 Ã© a condiÃ§Ã£o de divisibilidade dos coeficientes inteiros da ANF: c_S â‰¡ 0 mod 4 para |S| â‰¥ 6.

**Pergunta de N1:** I6 obriga a parte quÃ¡rtica de D a se anular num subespaÃ§o de codimensÃ£o 3 (um "U isotrÃ³pico")?

**ReformulaÃ§Ã£o usada no cÃ³digo.** Todo U isotrÃ³pico de codimensÃ£o 3 tem a forma U_Y + âŸ¨e_x + vâŸ©, em que U_Y Ã© um subespaÃ§o de codimensÃ£o 3 de Y isotrÃ³pico para T. As restriÃ§Ãµes ficam assim:

- "nÃ£o isotrÃ³pico em U_Y" vira uma restriÃ§Ã£o linear em C3 (`sat_n1_cegar.prepara_U`);
- os U_Y isotrÃ³picos se dividem em Ã³rbitas do grupo de automorfismos de T (arquivos `automorfismos_*.json`; script `sat_n1_orbita.py`);
- um SAT restrito a um conjunto S de U_Y dÃ¡ um D com I6 que escapa de todos os U_Y de S;
- UNSAT com S igual a todas as Ã³rbitas prova N1 para a classe.

Tamanhos das Ã³rbitas:

| Classe | Ã“rbitas de U_Y |
|---|---|
| F4^2 | 15, 60, 240, 2880 |
| F4+F4 | 15, 60, 240, 960 |
| Q4a, Q4b, Q4c | 255, 1020, 2040 |

O Ã­ndice da Ã³rbita no cÃ³digo (k) segue a ordem crescente de tamanho.

## Resultados jÃ¡ obtidos (`resultados/`)

Todas as soluÃ§Ãµes SAT abaixo tÃªm I6 conferido; a Ãºltima coluna diz em quais Ã³rbitas a testemunha tem U_Y isotrÃ³picos. Para F4+F4 e F4^2 a ordem Ã© [15, 60, 240, maior]; para Q4, [255, 1020, 2040].

| Classe | Ã“rbitas testadas | Resultado | IsotrÃ³picos da testemunha |
|---|---|---|---|
| F4^2 | 15 | SAT | [0, 7, 36, 552] |
| F4^2 | 60 | SAT | [7, 0, 3, 75] |
| F4^2 | 240 | SAT | [0, 0, 0, 46] |
| F4^2 | 2880 | SAT (VM GCP, cubo 7) | [15, 24, 24, 0] |
| F4+F4 | 15 | SAT | â€” |
| F4+F4 | 60 | SAT | â€” |
| F4+F4 | 240 | SAT | â€” |
| F4+F4 | 960 | SAT (Colab) | [15, 20, 0, 0] |
| F4+F4 | 15+60+240 | SAT (GitHub, cubos 28 e 62) | [0, 0, 0, 12] e [0, 0, 0, 21] |
| Q4a, Q4b, Q4c | 255 | SAT | sÃ³ nas Ã³rbitas de 1020 e 2040 |
| Q4a | 1020 | SAT (Colab, cubo 1 de 64, 15641 s; reconferido no PC em 09/11) | [7, 0, 14]; I6 sim, I7 nÃ£o, posto de C3 = 8 |
| Q4a | 2040 | SAT em 17 de 64 cubos (GitHub run 42521666326; 47 INDECISO; os 17 reconferidos no PC) | quase todos **[15, 0, 0]** ou [19, 0, 0]; alguns [15, 8, 0]; posto de C3 = 8 |
| Q4c | 1020 | SAT (Colab, cubo 0 de 64, 23439 s; reconferido no PC) | **[19, 0, 0]**; reta comum a todos os 19 |

**Leitura nova para Q4 (09/11, manhÃ£).** HÃ¡ testemunhas com I6 que escapam ao mesmo tempo das Ã³rbitas 1020 e 2040:
- Q4a: 13 dos 17 cubos tÃªm isotrÃ³picos sÃ³ na Ã³rbita 255;
- Q4c: o cubo 0 tem isotrÃ³picos sÃ³ na Ã³rbita 255.

Logo, em Q4a e Q4c, uma famÃ­lia que force isotropia precisa conter a Ã³rbita de 255. Como a Ã³rbita 255 sozinha nÃ£o forÃ§a (jÃ¡ hÃ¡ SAT), a prÃ³xima pergunta precisa Ã© a uniÃ£o 255 + 1020 + 2040, isto Ã©, as rodadas de classe completa.

**Leitura:**
- Nenhuma Ã³rbita isolada forÃ§a isotropia, nem as uniÃµes testadas.
- Invariantes das testemunhas (I7, posto de C3, estrutura): `resultados/estrutura/`.
  - Metade das testemunhas satisfaz tambÃ©m I7, isto Ã©, sÃ£o liftÃ¡veis.
  - O mÃ­nimo observado Ã© 12 U_Y isotrÃ³picos.

## Em andamento (quem roda o quÃª)

| Problema | Onde | Como acompanhar |
|---|---|---|
| F4^2, todas as Ã³rbitas | VM GCP `n1-cubos` (32 nÃºcleos), `/opt/n1/repo/res` | `gcloud compute ssh n1-cubos --zone us-central1-a` |
| H16: filtros 2-Ã¡dicos, CEGAR | mesma VM, `/opt/h16/saida.txt` | `resultados/h16/` |
| F4+F4, todas as Ã³rbitas | Colab (Drive: `n1_colab_08nov/F4F4_todas`); tambÃ©m PC local, instÃ¢ncia inteira | `RESUMO.json` no Drive |
| F4+F4, 15+960 | GitHub Actions (run 42547926882) | `gh run view` |

F4^2, 15+2880: Kaggle (4 nÃºcleos, internet ligada), saÃ­da em `/kaggle/working/n1`. Use "Save Version" para guardar os arquivos; o placar sai na saÃ­da da cÃ©lula.
| Q4a, todas as Ã³rbitas; Q4b/Q4c 2040 | GitHub Actions, workflow `cubos` | `gh run list` |
| Q4b, todas as Ã³rbitas, k=8 (256 cubos) | GitHub Actions da segunda conta, fork `filipemvono-ops/n1-sat-cubos`, run 42557164345 | `gh run view 42557164345 -R filipemvono-ops/n1-sat-cubos` |
| Q4b, todas as Ã³rbitas, k=6 (64 cubos) | Colab da conta parceira (Drive dela: `n1_inst_09nov/Q4b_todas`), 2 nÃºcleos, sÃ³ como conferÃªncia independente | `RESUMO.json` no Drive dela |
| Q4c, todas as Ã³rbitas | Colab (Drive: `n1_inst_09nov/Q4c_todas`) | â€” |
| Q4a/b/c, Ã³rbita 1020 em cubos; Q4 2040 inteira | Colab principal (Drive: `n1_colab_08nov/cubos_q4`) | â€” |

## Dificuldade dos cubos (medida)

- A rodada F4+F4 15+60+240 no GitHub (k=6, 64 cubos, 15000 s por cubo) terminou assim:
  - 2 cubos SAT, os cubos 28 e 62;
  - **62 cubos INDECISO**.
- Nas classes completas, que tÃªm mais restriÃ§Ãµes, cubos k=6 provavelmente tambÃ©m estouram o tempo. Uma resposta UNSAT vai exigir subdividir os INDECISO (k maior) ou dar mais tempo por cubo. Um SAT jÃ¡ responde.
- Para Colab gratuito, que desconecta por inatividade, use `plataformas/colab_retomavel_q4b_k10.py`:
  - 1024 cubos com 50 min cada;
  - copia os resultados ao Drive a cada 3 min;
  - ao reconectar, retoma do que jÃ¡ estÃ¡ no Drive.

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

Cubos jÃ¡ resolvidos ficam em `res/` e sÃ£o pulados ao relanÃ§ar no mesmo diretÃ³rio.

## PrÃ³ximas perguntas (da anÃ¡lise de estrutura)

1. I6 limita o posto de C3?
2. Descrever os 12 U_Y isotrÃ³picos da testemunha mÃ­nima de F4+F4.
3. Classes completas: algum cubo SAT seria contraexemplo a N1. Conferir de forma independente antes de qualquer conclusÃ£o.
