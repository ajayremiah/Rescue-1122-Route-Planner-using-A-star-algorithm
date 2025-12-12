# Rescue 1122 Route Planner using A* Algorithm

Rescue 1122 Route Planner is an Artificial Intelligence project that implements the A* (A-Star) pathfinding algorithm using Python. The project features an interactive simulation built with Pygame, performance benchmarking tools, and data visualization for algorithm analysis.

Essentially, the user defines a start point, multiple waypoints, and a goal on a 2D grid, along with obstacles. The program calculates the optimal path traversing all points in order.
## Node Color Legend
  🟠(red) - starting point of the rescue unit,
  🔵(turqouise) - final destination,
  🟣(purple) - intermediate stops the path must visit,
  ⚫(black) - blocked areas that cannot be traversed,
  🟢(green) - nodes currently being considered for exploration (open),
  🔴(red) - nodes that have already been visited (closed), and
  🟡(yellow) - calculated optimal route

## File Structure

* `Simulation.py`: main application containing the Pygame simulation and A* implementation.
* `benchmark.py`: script to run automated performance tests on the algorithm without the graphic overhead.
* `graphs.py`: generates visual plots (using Matplotlib) based on the data collected from benchmarking.
