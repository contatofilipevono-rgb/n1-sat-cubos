# Estado das buscas, para retomar (atualizado em 09/11/2026, ~04:15 UTC)

**Snapshot de 09/11, 04:15 UTC:**
- Todas as plataformas no ar.
- Na VM, F4^2 completa ainda não fechou nenhum cubo depois de 6,6 h, e o H16 ainda não terminou nenhuma iteração.
- Os Colabs com classes completas e o Kaggle ainda não têm cubo concluído.
- A segunda conta do GitHub roda com 5 jobs.

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
