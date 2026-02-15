# Good Chemistry - July 2015 (Solution)

**Puzzle:** [07_good_chemistry.md](../../puzzles/2015/07_good_chemistry.md)

## Official Solution

Euler's formula (V-E+F=2) applies to planar graphs as well as polyhedra. The molecular structure of each molecule corresponds to a planar graph, where Vertices are atoms (excluding hydrogens, per the typical convention for molecular diagrams), bonds are Edges, and "Faces" are the number of distinct regions into which the graph splits the plane.

So for example, for paracetamol, V=11, E=11, and F=2.

If you knew that, then you could probably figure out that we had set f(molecule) equal to V × E × F!

So, f(adenosine triphosphate) = 31 × 33 × 4 = **4092**.
