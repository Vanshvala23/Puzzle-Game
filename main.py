import pygame
import random
import time
from collections import deque

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 20, 20  # Number of rows and columns
CELL_SIZE = WIDTH // COLS  # Size of each cell

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Directions for movement (row offset, col offset)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Maze Generator and Solver")
clock = pygame.time.Clock()

# Initialize grid
grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
start_pos = None  # Initially set to None (user can select)
end_pos = None  # Initially set to None (user can select)

# Draw grid
def draw_grid():
    """Draw the grid on the screen."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if grid[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GREY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Maze Generation using Recursive Backtracking
def generate_maze(x, y):
    """Generate a maze using recursive backtracking."""
    stack = [(x, y)]
    while stack:
        cx, cy = stack[-1]
        visited[cx][cy] = True
        grid[cx][cy] = 0

        # Find unvisited neighbors
        neighbors = []
        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and not visited[nx][ny]:
                neighbors.append((nx, ny))

        if neighbors:
            # Choose a random neighbor
            nx, ny = random.choice(neighbors)
            # Remove the wall between current and chosen cell
            grid[(cx + nx) // 2][(cy + ny) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

        # Visualization
        draw_grid()
        pygame.draw.rect(screen, BLUE, (cy * CELL_SIZE, cx * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        clock.tick(30)

# Backtracking Pathfinding
def backtrack_pathfinding(x, y, ex, ey):
    """Solve the maze using backtracking."""
    path = []
    stack = [(x, y)]
    visited_backtrack = [[False for _ in range(COLS)] for _ in range(ROWS)]
    visited_backtrack[x][y] = True

    while stack:
        cx, cy = stack[-1]
        path.append((cx, cy))
        if (cx, cy) == (ex, ey):
            return path

        found = False
        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 0 and not visited_backtrack[nx][ny]:
                visited_backtrack[nx][ny] = True
                stack.append((nx, ny))
                found = True
                break

        if not found:
            stack.pop()
            path.pop()

        # Visualization
        draw_grid()
        for px, py in path:
            pygame.draw.rect(screen, GREEN, (py * CELL_SIZE, px * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (cy * CELL_SIZE, cx * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        clock.tick(30)

    return None

# Draw the path
def draw_path(path):
    """Draw the solution path."""
    for x, y in path:
        pygame.draw.rect(screen, YELLOW, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        time.sleep(0.05)

# Reset the maze and grid
def reset_maze():
    global grid, visited, start_pos, end_pos
    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    start_pos = None
    end_pos = None

# Main loop
def main():
    global start_pos, end_pos
    running = True
    maze_generated = False
    maze_solved = False
    path = []

    while running:
        screen.fill(BLACK)

        # Draw grid and visual elements
        draw_grid()

        # Highlight start and end positions if set
        if start_pos:
            pygame.draw.rect(screen, BLUE, (start_pos[1] * CELL_SIZE, start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Start
        if end_pos:
            pygame.draw.rect(screen, RED, (end_pos[1] * CELL_SIZE, end_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # End

        if maze_solved and path:
            draw_path(path)
        elif maze_solved and path is None:
            # Display a message if no path is found
            font = pygame.font.Font(None, 36)
            text = font.render("No path found", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the grid cell that was clicked
                mx, my = event.pos
                col = mx // CELL_SIZE
                row = my // CELL_SIZE

                # Set start point (left click)
                if event.button == 1 and not start_pos:
                    start_pos = (row, col)

                # Set end point (right click)
                elif event.button == 3 and not end_pos:
                    end_pos = (row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not maze_generated and start_pos and end_pos:
                    # Generate the maze if start and end are selected
                    generate_maze(start_pos[0], start_pos[1])
                    maze_generated = True

                if event.key == pygame.K_s and maze_generated and not maze_solved:
                    # Solve the maze using backtracking if generated
                    if start_pos and end_pos:
                        path = backtrack_pathfinding(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                        maze_solved = True

                if event.key == pygame.K_r:
                    # Reset the maze
                    reset_maze()
                    maze_generated = False
                    maze_solved = False
                    path = []

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
