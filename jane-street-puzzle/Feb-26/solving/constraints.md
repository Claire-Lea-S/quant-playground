# Constraints

## Variable Constraints
- a, b, c are positive integers
- All 37 labeled cell expressions must evaluate to positive integers

## Grid Filling Constraints
- Grid is 13×13 (169 cells total)
- Place values 1 through N in the grid for some N
- Exactly K cells contain value K, for each K = 1, 2, ..., N
- Total filled cells = N(N+1)/2 ≤ 143, so N ≤ 16
- Remaining cells are empty

## Connectivity Constraints
- For each value K, the K cells containing K must form an orthogonally connected region (a K-omino)
- Orthogonal = sharing an edge (up/down/left/right), not diagonal

## Containment Constraints
- For each K > 1, the K-omino must "contain" the (K−1)-omino
- "Contain" means: the shape of the (K−1)-omino, under some rotation and/or reflection, fits entirely within the shape of the K-omino
- Formally: normalize both polyominoes to origin, then there exists a rigid transformation T (rotation/reflection + translation) such that T(shape(K−1)) ⊆ shape(K)

## Labeled Cell Constraints
- Each labeled cell's expression defines that cell's value
- The value must equal a positive integer in [1, N]
- A labeled cell cannot be empty

## Answer Computation
- For each row, compute the sum of all labeled cell values in that row
- Answer = max(row_sums) × min(row_sums)
