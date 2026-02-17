# Formal Mathematical Constraints

## Definitions

- Grid G of size 13×11, cells indexed (r, c) where r ∈ {0,...,12}, c ∈ {0,...,10}
- Variables: a, b, c ∈ ℤ⁺
- Cell value: x(r,c) ∈ {0, 1, 2, ..., N} where 0 = empty
- L ⊂ G = set of labeled cells (37 cells with expressions)
- f(r,c)(a,b,c) = expression at labeled cell (r,c)
- N ∈ ℤ⁺ = maximum value placed in the grid
- S_k = {(r,c) ∈ G : x(r,c) = k} = set of cells with value k

## C1: Variable Domain

    a, b, c ∈ ℤ⁺       (positive integers)

## C2: Expression Integrality

    ∀ (r,c) ∈ L :  f(r,c)(a,b,c) ∈ ℤ⁺

All 37 expressions must evaluate to positive integers.

## C3: Expression Binding

    ∀ (r,c) ∈ L :  x(r,c) = f(r,c)(a,b,c)

Labeled cells take the value of their expression.

## C4: Cell Value Range

    ∀ (r,c) ∈ G :  x(r,c) ∈ {0, 1, 2, ..., N}

## C5: Labeled Cells Are Non-Empty

    ∀ (r,c) ∈ L :  x(r,c) ≥ 1

## C6: Count Constraint

    ∀ k ∈ {1, ..., N} :  |S_k| = k

Equivalently:

    |{(r,c) : x(r,c) = k}| = k     ∀ k ∈ {1,...,N}

## C7: Total Fill

    ∑_{k=1}^{N} k = N(N+1)/2 ≤ 143

    |{(r,c) : x(r,c) > 0}| = N(N+1)/2

## C8: Upper Bound on N

    N(N+1)/2 ≤ 143  ⟹  N ≤ 16

## C9: Connectivity (K-omino)

For each k ∈ {1, ..., N}, the induced subgraph of S_k under 4-adjacency is connected:

    ∀ (r₁,c₁), (r₂,c₂) ∈ S_k :  ∃ path  p₀, p₁, ..., p_m  where
        p₀ = (r₁,c₁),  p_m = (r₂,c₂),
        ∀ i : p_i ∈ S_k,
        ∀ i : |p_i.r - p_{i+1}.r| + |p_i.c - p_{i+1}.c| = 1

## C10: Containment

Define the normalized shape of S_k:

    shape(k) = {(r - r_min, c - c_min) : (r,c) ∈ S_k}
    where r_min = min{r : (r,c) ∈ S_k}, c_min = min{c : (r,c) ∈ S_k}

Define the 8 rigid transformations (dihedral group D₄):

    T₀(r,c) = ( r,  c)       identity
    T₁(r,c) = ( c, -r)       90° CW
    T₂(r,c) = (-r, -c)       180°
    T₃(r,c) = (-c,  r)       270° CW
    T₄(r,c) = ( r, -c)       reflect horizontal
    T₅(r,c) = (-r,  c)       reflect vertical
    T₆(r,c) = ( c,  r)       reflect main diagonal
    T₇(r,c) = (-c, -r)       reflect anti-diagonal

Normalize after transformation:

    norm(P) = {(r - min_r, c - min_c) : (r,c) ∈ P}

Containment constraint:

    ∀ k ∈ {2, ..., N} :  ∃ i ∈ {0,...,7}, ∃ (δr, δc) ∈ ℤ² :
        {T_i(p) + (δr, δc) : p ∈ norm(shape(k-1))} ⊆ shape(k)

Equivalently: some rotation/reflection of the (k−1)-omino can be translated to fit entirely inside the k-omino.

## C11: Value Upper Bound

    ∀ (r,c) ∈ L :  1 ≤ f(r,c)(a,b,c) ≤ N

## Objective

No optimization — this is a constraint satisfaction problem.

After finding x(r,c) for all cells, compute:

    row_sum(r) = ∑_{(r,c) ∈ L} x(r,c)       for each row r

    answer = max_r(row_sum(r)) × min_r(row_sum(r))
