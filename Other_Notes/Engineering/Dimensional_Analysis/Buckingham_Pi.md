---
title: Dimensional Analysis with Linear Algebra
author: Jasper Day
colorlinks: true
header-includes:
- \usepackage{kmath,kerkis}
---

[Source](http://homepage.math.uiowa.edu/~rcurtu/MathBioGroup/MBGfiles/dimAnalysis.pdf)

Buckingham's Pi theorem states that any relations between natural quantities can be expressed in an equivalent form using *Pi groups*, dimensionless quantities formed between those quantities.

# Assumptions:

The following assumptions must hold:

1. $\textit{u}$, our quantity of interest, must equal some function $f\left(x_{1}, x_{2}, x_{3}, \ldots, x_{n}\right)$, that is, $\textit{n}$ measurable quantities expressed as independent variables & parameters $x_{i}$. It is further assumed that the equation

$$
u = f\left(x_{1}, x_{2}, x_{3}, \ldots, x_{n}\right)
$$ 
\t is dimensionally homogeneous.

2. The quantities $\{u, x_{1}, x_{2}, x_{3}, \ldots, x_{n}\}$ are measured in terms of $\text{m}$ fundamental dimensions $\{ L_{1}, L_{2}, L_{3}, \ldots, L_{n} \}$

3. If $\text{W}$ is any quantity of $\{ u, x_{1}, \ldots, x_{n}\}$, then

$$
\left[W\right] = L_{1}^{p_{1}} \cdot L_{2}^{p_{2}} \cdot \ldots \cdot L_{m}^{p_{m}}
$$

Then we can create $\textbf{P} = \begin{bmatrix}p_{1} \\ p_{2} \\ \vdots \\ p_{m} \\\end{bmatrix}$, the *dimension vector* of W.

This gives us the $m\times n$ dimension matrix

$$
\textbf{A} = \begin{bmatrix} \textbf{P}_{1} | \textbf{P}_{2} | \cdots | \textbf{P}_{n} \\ \end{bmatrix} = \begin{bmatrix}
    p_{11} & p_{12} & \cdots & p_{1n} \\
    p_{21} & p_{22} & \cdots & p_{2n} \\
    \vdots & \vdots & \vdots & \vdots \\
    p_{m1} & p_{m2} & \cdots & p_{mn} \\
    \end{bmatrix}
$$

# Conclusions of the Buckingham Pi Theorem

1. The relation $u = f\left(x_{1}, x_{2}, \ldots, x_{n} \right)$ can be expressed in terms of dimensionless quantities.

2. The number of dimensionless quantities is

$$
k + 1 = n + 1 - \texttt{rank}\left(A\right)
$$

\t (The reason for k + 1 is that we pull out the original quantity $u$ from the matrix $\textbf{A}$. Otherwise this term would not appear.)

3. Since $\textbf{A}$ has $\texttt{rank}\left(A\right) = n - k$, there are $k$ linearly independent solutions of $\textbf{Az} = \textbf{0}$ denoted as $z^{1}, z^{2}, \ldots, z^{k}$.

Let $\textbf{a}$, an $m$-column vector, be the dimension vector of $u$, and let $\textbf{y}$, an $n$-column vector, be a solution of 

$$
\textbf{Ay} = -\textbf{a}
$$

Then the relation $u = f\left(x_{1}, x_{2}, \ldots, x_{n} \right)$ simplifies to $g\left(\Pi_{1}, \Pi_{2}, \ldots, \Pi_{k} \right)$.

There is one $\Pi$ group for each linearly indepenent set of $\textbf{Az} = \textbf{0}$, plus one $\Pi$ group for $u$. The parameters in each pi group are raised to the respective row of $z\prime$.
