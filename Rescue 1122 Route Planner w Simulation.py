import pygame
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("RESCUE 1122 Route Planner")

# --- COLOR DEFINITIONS ---
RED = (255, 0, 0)       # Closed nodes (visited)
GREEN = (0, 255, 0)     # Open nodes (in queue)
YELLOW = (255, 255, 0)  # The final path
WHITE = (255, 255, 255) # Empty node
BLACK = (0, 0, 0)       # Barrier/Wall
ORANGE = (255, 165, 0)  # Start node
GREY = (128, 128, 128)  # Grid lines
TURQUOISE = (64, 224, 208) # End node
PURPLE = (128, 0, 128)  # [ADDITIONAL FEATURE] Added Purple for intermediate "waypoints"

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # --- STATE CHECKS ---
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    # --- STATE SETTERS ---
    def make_start(self):
        self.color = ORANGE

    # [IMROVEMENT] Modified to protect the path (Yellow) and stops (Purple/Orange)
    def make_closed(self):
        # A node is only turned RED (visited) if it isn't already part of a path or a stop
        # This prevents the 2nd leg of the trip from erasing the 1st leg's path.
        if self.color != YELLOW and self.color != ORANGE and self.color != PURPLE:
            self.color = RED

    # [IMPROVEMENT] Modified to protect the path and stops
    def make_open(self):
        # A node is only turned GREEN (open set) if it isn't already special
        if self.color != YELLOW and self.color != ORANGE and self.color != PURPLE:
            self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Check UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Check RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Check LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path() # Turns the node YELLOW
        draw()

def A_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    # Initialize scores for all nodes
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end() # Keeps the destination TURQUOISE
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # Turns node GREEN

        draw()

        if current != start:
            current.make_closed() # Turns node RED

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x // gap
    col = y // gap
    return row, col

# --- MAIN FUNCTION (HEAVILY MODIFIED) ---
def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)

    # [IMPROVEMENT] 'start' and 'end' variables were replaced  with a list called 'stops'
    # This list will hold [Start, Waypoint 1, Waypoint 2, ... End]
    stops = [] 

    run = True
    while run:
        draw(win, grid, ROWS, width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # --- LEFT MOUSE CLICK (Add Stops/Barriers) ---
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                # [IMPROVEMENT] Logic for adding nodes to the list
                # If the node isn't a wall and isn't already in the route list:
                if not node.is_barrier() and node not in stops:
                    stops.append(node) # Add it to our route
                    
                    # [ADDITIONAL FEATURE] Determine color based on order
                    if len(stops) == 1:
                        node.make_start()   # The first click is always start (ORANGE)
                    else:
                        node.make_end()     # The most recent click is currently the end (TURQUOISE)
                        
                        # [ADDITIONAL FEATURE] If there are more than 2 stops (e.g., start -> waypoint -> end),
                        # the node *before the new end needs to change from TURQUOISE to PURPLE.
                        if len(stops) > 2:
                            stops[-2].color = PURPLE

                # [IMPROVED] If we click a node not in 'stops', it becomes a wall (BLACK)
                elif node not in stops:
                    node.make_barrier()

            # --- RIGHT MOUSE CLICK (Remove items) ---
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                # [IMPROVED] Logic to remove stops from the list
                if node in stops:
                    stops.remove(node) # Remove from list
                    node.reset()       # Turn white on screen
                    
                    # [ADDITIONAL FEATURE] Re-color the remaining list to keep start/end correct
                    # If start us deleted, the next node must become Orange
                    # If end is deleted, the previous node must become Turquois
                    for i, stop_node in enumerate(stops):
                        if i == 0:
                            stop_node.make_start()
                        elif i == len(stops) - 1:
                            stop_node.make_end()
                        else:
                            stop_node.color = PURPLE
                else:
                    node.reset() # If it was just a wall, reset it to white

            # --- SPACEBAR (Run Algorithm) ---
            if event.type == pygame.KEYDOWN:
                # [IMPROVEMENT] Check if we have at least 2 points (Start + End)
                if event.key == pygame.K_SPACE and len(stops) > 1:
                    
                    # Update neighbors for the whole grid
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # [ADDITIONAL FEATURE] The Loop Logic
                    # Iterate through the list in pairs
                    # If stops = [A, B, C], we run A* for (A->B), then for (B->C).
                    for i in range(len(stops) - 1):
                        start_node = stops[i]
                        end_node = stops[i+1]
                        
                        # Run the algorithm for this specific segment
                        A_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start_node, end_node)
                        
                        # [ADDITIONAL FEATURE] Visual Cleanup
                        # A* might turn the start node RED (closed). We force it back to correct color.
                        if i == 0:
                            start_node.make_start() # Keep true Start ORANGE
                        else:
                            start_node.color = PURPLE # Keep Waypoints PURPLE

                # [IMOROVEMENT] Clear the board and reset the list
                if event.key == pygame.K_c:
                    stops = []
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)
