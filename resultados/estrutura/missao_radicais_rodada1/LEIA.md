# Equações de grau oito no caso misto em $F_4+F_4$

Usamos a quártica $T$ de sete.py, $Y=\mathbb F_2^8$, $L=\ker(T\wedge-\colon\Lambda^3Y^*\to\Lambda^7Y^*)$ e $G=\{\iota_u T:u\in Y\}$. O espaço $L/G$ tem dimensão 40. Seja $N\subset L/G$ o conjunto de cúbicas sem nenhum $U_Y$ isotrópico, definido pelos 1.275 conjuntos de sete funcionais de base.npz. As máscaras de 40 bits usam as coordenadas de comp desse arquivo.

## Redução a uma forma alternada

Fixe $a,b\in L$ com $a\wedge b\in J=T\wedge\Lambda^2Y^*$ e $A=A_{12}$ com $T\wedge A=a\wedge b$. Defina $K=\ker(T\wedge-\colon\Lambda^2Y^*\to\Lambda^6Y^*)$ e
$$
C=\{c\in L:a\wedge c,b\wedge c\in J\}.
$$
Escolha levantamentos lineares $U(c),V(c)\in\Lambda^2Y^*$ com $T\wedge U(c)=a\wedge c$ e $T\wedge V(c)=b\wedge c$. A equação restante de grau oito é resolúvel exatamente quando
$$
c\wedge A+a\wedge V(c)+b\wedge U(c)\in S=T\wedge\Lambda^1Y^*+a\wedge K+b\wedge K.
$$
O anulador de $S$ para o emparelhamento perfeito $\Lambda^5Y^*\times\Lambda^3Y^*\to\Lambda^8Y^*$ é $C$. Anular $T\wedge\Lambda^1Y^*$ exige $d\wedge T=0$. Anular $a\wedge K$ exige $a\wedge d\in K^\perp=J$, pois a aplicação adjunta de $T\wedge-$ sob o emparelhamento entre $\Lambda^2$ e $\Lambda^6$ é a própria aplicação. O mesmo vale para $b$.

Logo a projeção das soluções em $c$ é o radical de
$$
\Omega_A(c,d)=\big[c\wedge d\wedge A+T\wedge(U(d)\wedge V(c)+V(d)\wedge U(c))\big]_8.
$$
A expressão vem de multiplicar o resíduo por $d$ e usar as equações dos levantamentos. A forma é simétrica e a diagonal é zero. Mudar os levantamentos altera o resíduo por um elemento de $S$. Para $g=\iota_uT$, podemos escolher $U(g)=\iota_u a$ e $V(g)=\iota_u b$. A identidade de derivação e $T\wedge A=a\wedge b$ dão resíduo $T\wedge\iota_u A$. Portanto $G$ está no radical, e a forma desce a $C/G$.

Os vetores $a,b$ também estão no radical no quociente. O programa representa a família por uma matriz inicial e dez matrizes de direção correspondentes a $K$. O posto de uma forma alternada é par. A nulidade tem a mesma paridade que $\dim C/G$.

## Certificado de posto individual

Para $a\in N$, o mapa $c\mapsto\beta(a,c)$ tem posto 10. Um posto menor colocaria $a$ no radical de alguma combinação não nula $B_\lambda=\lambda\circ\beta$. Enumeramos as 1.023 combinações. Das 255 com radical de dimensão 16, cada radical está contido em um dos $A_U$ definidos pelos sete funcionais da base. Nas outras 768, os radicais de dimensão oito contêm em união 187.681 vetores distintos, todos com algum $U_Y$ isotrópico. O JSON registra um índice $U$ por radical de dimensão 16 e o programa refaz a cobertura dos radicais menores.

O posto individual não implica posto 20 para o mapa conjunto. Para uma cúbica $a$ fixada, enumeramos as dependências $B_\lambda a=B_\mu b$ com $\mu\ne0$, adicionando $\beta(a,b)=0$ ao sistema linear em $b,\lambda$. Filtramos $b,a+b\in N$. A busca foi exata para cada um dos 16 valores de $a$ amostrados e produziu oito planos distintos com $\dim C/G=21$ ou 22.

## Busca nas extensões

Testamos todas as 1.024 escolhas de $A$ em oito pares amostrados sem direcionamento e nos oito planos com posto conjunto menor. Entre as 16.384 escolhas, os radicais tiveram dimensões de 2 a 7. A eliminação original reconfirmou os cinco casos de dimensão 7. Nenhuma escolha produziu um terceiro vetor com as sete combinações em $N$. A cobertura é exata para os 16 pares. O lema misto e $p=17$ seguem abertos.

## Reprodução

Use Python 3.12 e NumPy 2. Os cinco arquivos de fonte vêm do material do Claude no repositório n1-sat-cubos, commit 8bf789a. Reconstituímos a base e conferimos igualdade de todos os campos com a original.

~~~text
python fonte/sete.py base
python beta_posto.py fonte beta-rank-audit.json
python radical_grau8.py fonte radical-audit.json
python radical_grau8.py fonte radical-degenerate-audit.json --rank-audit beta-rank-audit.json
~~~

