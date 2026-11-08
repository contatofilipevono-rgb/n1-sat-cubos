# n1-sat-cubos

Instâncias SAT de uma etapa de pesquisa em funções booleanas: quárticas em 9 variáveis sob uma condição de divisibilidade mod 4 (I6). A pergunta é se essa condição força um subespaço isotrópico de codimensão 3, isto é, um *degree-drop space*.

O problema é resolvido por cube-and-conquer no GitHub Actions:

- **Ferramentas:** CaDiCaL resolve cada cubo e drat-trim confere as provas.
- **Execução:** o workflow `cubos` é disparado manualmente, com parâmetros classe, órbitas e k. Ele gera a instância e divide em 2^k cubos pelos sinais de k variáveis, o que dá cobertura completa por construção.
- **Saída:** cada cubo termina em UNSAT com prova DRAT verificada, em SAT com a solução conferida por tabela-verdade, ou em INDECISO.

**Status:** resultados preliminares, sem auditoria. Nenhuma afirmação de resultado é feita aqui.
