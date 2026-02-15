# Robot Road Trip - July 2025 (Solution)

**Puzzle:** [07_robot_road_trip.md](../../puzzles/2025/07_robot_road_trip.md)

## Official Solution

### Key Insight: Base Rates of Overtaking

The trickiest part of this probability puzzle is determining the relative base rates between cars of different speeds overtaking each other. The notes about how cars rarely meet and all trips are the same long length N (made precise by taking limits) implies that we can minimize the "first order term" of the cost of exactly two cars meeting and we can ignore the boundary effects of meeting near the beginning or end of one of the cars' journeys.

### Setting Up the Problem

Each car's speed is uniformly chosen in [1,2]. To find the relative rates of overtaking, integrate over two speeds being drawn and then consider the set of positions in distance and time that the slower car would've had to start at to be overtaken by the faster car.

If two speeds are *u* < *v*, and we fix the position of the car traveling *v* to enter the highway at (0, 0), then the car will exit at (N, N/v). The starting positions of the *u*-speed car that need to be overtaken form a parallelogram with area N²(1/u - 1/v).

### Cost Calculation

The cost of each overtake is proportional to the square of the difference between *u* and the speed the car must reduce to. This means we are trying to choose *a* to minimize the sum of:
1. The cost of reducing speed from the slow lane to zero
2. The cost of reducing speed from the fast lane to the slow lane

The N² factors out and can be ignored.

### Answer

Using fundamental theorem of calculus and integration, the optimal value is:

**a = 1.1771414168**
