# Operaciones aritméticas

$$
\begin{aligned}
E &\to TE' \\
E' &\to +TE' \mid -TE' \mid \varepsilon \\
T &\to FT' \\
T' &\to *FT' \mid /FT' \mid \varepsilon \\
F &\to (E) \mid \text{id}
\end{aligned}
$$

# Tipos de dato

$$
\begin{aligned}
S &\to \text{int} \mid \text{char} \mid \text{float}
\end{aligned}
$$

# Uso de variables

$$
\begin{aligned}
S &\to \text{Tipo de dato id;} \mid \text{Tipo de dato id = V;} \\
V &\to \text{id} \mid E \\
E &\to S \mid SRS \mid \text{Operaciones Aritmeticas} \mid \text{id} \\
R &\to < \mid \leq \mid > \mid \geq \mid == \mid \neq 
\end{aligned}
$$

# Operaciones logicas

```math
\begin{aligned}
L &\to TX \\
X &\to \text{OTX} \mid \varepsilon \\
T &\to FY \\
Y &\to \text{AFY} \mid \varepsilon \\
F &\to \text{N} \mid (L) \mid T \\
N &\to \text{!F} \\
O &\to || \\
A &\to \text{\&amp;\&amp;} \\
I &\to \text{id} \\
\end{aligned}
```



## Condicion if-else

$$
\begin{aligned}
S &\to \text{if} (C) \lbrace S \rbrace \text{ E }  \\
E &\to \text{else} \lbrace S \rbrace \mid \varepsilon \\
C &\to B \mid C \verb|&&| C \mid C \verb+||+ C \mid \text{!}C \\
B &\to \text{true} \mid \text{false} \mid \text{Operaciones logicas} \\
\end{aligned}
$$


## Palabras Reservadas

$$
\begin{aligned}
R &\to \text{char} \mid \text{int} \mid \text{float} \mid \text{return} \mid \text{void} \mid \text{if} \mid \text{else}
\end{aligned}
$$

## Comentarios (Pendiente Maria Jose)

$$
\begin{aligned}
C &\to S \mid L \mid M \\
S &\to // \text{ comentario} \\
M &\to /* \text{ comentario } */
\end{aligned}
$$
