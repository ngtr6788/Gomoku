import pygame
import numpy as np
from pygame.locals import *
from typing import Tuple

"""
This program implements Tic-Tac-Toe or Gomoku-like games, where
you have to win k-in-a-row on a m x n grid. 
"""

# set some colour constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAROON = (128, 0, 0)
NAVY_BLUE = (0, 0, 128)
GREEN = (0, 128, 0)
PURPLE = (128,  0, 128)

def gomoku_game(width_squares: int, height_squares: int, grid_size: int = 25,
                winner_length: int = 5, number_of_players: int = 2) -> None:
    """
    Displays a PyGame screen of width_squares x height_squares Gomoku game
    grid_size, winner_length, and number_of_players are optional.

    effects: displays a PyGame screen
    requires: 2 <= number_of_players <= 4
              2 < winner_length
              winner_length <= width_squares
              winner_length <= height_squares
    """
    pygame.init()

    # sanity checks
    assert 2 <= number_of_players <= 4  # (for now)
    assert 2 < winner_length
    assert winner_length <= width_squares
    assert winner_length <= height_squares
    
    SCREEN = create_grid(width_squares, height_squares, grid_size)
    # You swap height_squares and width_squares so the array looks like the grid
    # displayed on the screen
    screen_array = np.zeros((height_squares, width_squares))

    turn = 1  # determines who's turn it is.
    # 1 = O, 2 = X, 3 = square, 4 = triangle
    game = True
    while pygame.get_init():  # main game loop
        for event in pygame.event.get():
            print(event)
            if event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                game = False
                continue
            elif event.type == MOUSEWHEEL:
                continue
            elif event.type == MOUSEBUTTONUP:
                if game == False:
                  continue
                # BUG: sometimes, scrolling makes an O or X
                mouse_click = event.pos

                square_coord = pixel_to_array_idx(mouse_click, grid_size)
                # print(square_coord)
                nearest_square = find_centre_square(mouse_click, grid_size)

                # make a symbol depending on whose turn it is
                if screen_array[square_coord] == 0:
                    screen_array[square_coord] = turn
                    if turn == 1:
                        make_o(SCREEN, nearest_square, grid_size)
                    elif turn == 2:
                        make_x(SCREEN, nearest_square, grid_size)
                    elif turn == 3:
                        make_square(SCREEN, nearest_square, grid_size)
                    elif turn == 4:
                        make_triangle(SCREEN, nearest_square, grid_size)
                    # only switch turns when you successfully draw on square
                    turn = (turn) % number_of_players + 1
                else:  
                    # if you clicked on an occupied square, you don't lose
                    # your turn
                    continue
                winner = winner_found(screen_array, square_coord, winner_length)
                if (winner != 0) or (not 0 in screen_array):
                  # either we haven't found a length in a row or every single
                  # grid square is filled
                  game = False
            pygame.display.update()

def create_grid(width: int, height: int, size: int = 30) -> pygame.Surface:
    """
  create_grid(width, height, size) creates a grid of squares,
  width x height, and each square has side length size, on the pygame
  "screen" (surface)

  requires: width, height, size > 0
  """
    assert width > 0
    assert type(width) is int  # deal with the devil
    assert height > 0
    assert type(height) is int  # IDK how to make Python
    assert size > 0 # statically typed

    # sets the screen size
    SCREEN_WIDTH = size * width
    SCREEN_HEIGHT = size * height
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe on steroids")
    screen.fill(WHITE)

    # add some grid lines
    for i in range(0, SCREEN_WIDTH, size):
        pygame.draw.line(screen, BLACK, (i, 0), (i, SCREEN_HEIGHT), 1)
    for j in range(0, SCREEN_HEIGHT, size):
        pygame.draw.line(screen, BLACK, (0, j), (SCREEN_WIDTH, j), 1)

    assert type(screen) is pygame.Surface
    return screen

"""
The following is valid for all make_SHAPE (SHAPE = o, x, square, triangle)
requires: size > 0
          thickness > 0
          point is within surf's dimensions [not asserted]
"""

def assert_ox(surf: pygame.Surface, point: Tuple[float, float],
              size: float, thickness: float) -> None:
    """ 
  assert_ox(surf, point, size, thickness) asserts that the parameters
  passed to make_o and make_x are valid
  requires: size > 0
            thickness > 0
            point is within surf's dimensions [not asserted]
            point has two elements
  """
    assert type(surf) is pygame.Surface
    # assert type(point) is tuple
    assert len(point) == 2
    assert size > 0
    assert thickness > 0

GRID_OX_RATIO = 3  

def make_o(surf: pygame.Surface, point: Tuple[int, int], size=30, thickness=2) -> None:
    """
  make_o(surf, point, radius=10, thickness=3) creates a blue O on the [surf]ace

  make_o(surf: pygame.Surface, point: Tuple[int, int], size: float = 30, width: float = 2) -> None

  effects: modifies surf
  """
    assert_ox(surf, point, size, thickness)
    radius = (size // GRID_OX_RATIO)
    pygame.draw.circle(surf, NAVY_BLUE, point, radius, thickness)

def make_x(surf: pygame.Surface, point: Tuple[int, int], size=30, thickness=2) -> None:
    """
  make_x(surf, point, size=30, thickness=2) creates a red X on the [surf]ace

  make_x(surf: pygame.Surface, point: Tuple[int, int], size: float = 30, width: float = 2) -> None
  effects: modifies surf
  """
    assert_ox(surf, point, size, thickness)
    radius = (size // GRID_OX_RATIO)
    x_coord, y_coord = point
    x_min = x_coord - radius
    y_min = y_coord - radius
    x_max = x_coord + radius
    y_max = y_coord + radius
    pygame.draw.line(surf, MAROON, (x_min, y_min), (x_max, y_max), thickness)
    pygame.draw.line(surf, MAROON, (x_min, y_max), (x_max, y_min), thickness)

def make_square(surf: pygame.Surface, point: Tuple[int, int], size=30, thickness=2) -> None:
  """
  Draws a square in the centre of the grid square on the surface
  effects: modifies surf
  """
  assert_ox(surf, point, size, thickness)
  radius = size // GRID_OX_RATIO
  x_coord, y_coord = point
  square_coord_size = (x_coord - radius, y_coord - radius, 2 * radius, 2 * radius)
  pygame.draw.rect(surf, GREEN, square_coord_size, thickness)

def make_triangle(surf: pygame.Surface, point: Tuple[int, int], size=30, thickness=2) -> None:
  """
  Draws a triangle in the centre of the grid square onscreen
  """
  assert_ox(surf, point, size, thickness)
  radius = size // GRID_OX_RATIO
  x_coord, y_coord = point
  triangle_coords = ((x_coord - radius, y_coord + radius * 2 / 3), \
                     (x_coord + radius, y_coord + radius * 2 / 3), 
                     (x_coord, y_coord - radius))
  pygame.draw.polygon(surf, PURPLE, triangle_coords, thickness)

def pixel_to_array_idx(mouse_pixel: Tuple[int, int], grid_size: float) -> Tuple[int, int]:
  """
  Converts the pixel the mouse clicked on to grid (array) coordinates,
  depending on how big the grid's size is.
  requires: mouse_pixel is a tuple with 2 numbers
            grid_size > 0
  """
  assert len(mouse_pixel) == 2
  assert grid_size > 0

  # y and x seem switched because the gamestate array needs to match
  # the same shape as the screen displayed
  grid_y, grid_x = mouse_pixel 
  grid_x //= grid_size
  grid_y //= grid_size
  return (grid_x, grid_y)

def find_centre_square(point: Tuple[int, int], size: int=30) -> Tuple[int, int]:
    """
  find_centre_square(point, size=30) finds the pixel nearest to the 
  mouse pixel, such that the O or X is in the centre of that square
  
  find_centre_square(point: Tuple[float, float], size: int) -> Tuple[int, int]
  requires: size > 0
  """
    assert size > 0
    assert len(point) == 2
    return tuple((np.array(point) // size) * size + np.array((size, size)) // 2)

# Examples of find_centre_square in action
assert find_centre_square((23, 65)) == (15, 75)
assert find_centre_square((124, 98)) == (135, 105)

def winner_found(grid: np.ndarray,
                 last_point: Tuple[int, int], length: int) -> int:
  """
  winner_found(grid, last_point, length) determines if there exists a
  "length-in-a-row" of X or O in the grid, and if so, return who the winner is.
  Otherwise, return 0 for no winner exists

  note: returns 1, 2, 3, 4 if winner is found, 0 otherwise
  (it feels a little, unpythonic)

  requires: 2 < length
            length is within dimensions of grid
            grid is a 2-D array
            last_point is a valid index in grid  
  """
  assert length > 2
  assert type(length) is int

  assert isinstance(grid, np.ndarray)
  assert grid.ndim == 2
  col_len, row_len = grid.shape

  # print(col_len, row_len)
  assert length <= col_len
  assert length <= row_len

  assert len(last_point) == 2
  lx, ly = last_point
  assert 0 <= lx < col_len
  assert 0 <= ly < row_len

  def dir_winner_check(step_x: int, step_y: int) -> bool:
    """
    dir_winner_check(step_x, step_y) determines if there is a length-in-a-row
    in a given direction, determined by how many steps in the x or y direction
    requires: -1 <= step_x, step_y <= 1
    """
    assert -1 <= step_x <= 1
    assert isinstance(step_x, int)
    assert -1 <= step_y <= 1
    assert isinstance(step_y, int)

    dir_longest = 1
    for i in range(1 - length, length - 1):
      init_x = lx + step_x * i
      init_y = ly + step_y * i
      final_x = lx + step_x * (i + 1)
      final_y = ly + step_y * (i + 1)

      if not ((0 <= final_x < col_len) and \
              (0 <= final_y < row_len) and \
              (0 <= init_x < col_len) and \
              (0 <= init_y < row_len)):
        continue

      if grid[init_x, init_y] == 0:
        dir_longest = 1
        continue
      if grid[init_x, init_y] == grid[final_x, final_y]:
        dir_longest += 1
      else:
        dir_longest = 1
    
      if dir_longest == length:
        return True
    return False

  # Horizontal direction (0, 1) steps
  h_win = dir_winner_check(0, 1)
  
  # Vertical direction (1, 0) steps
  v_win = dir_winner_check(1, 0)

  # northwest - southeast diagonal direction (1, 1) steps
  nw_win = dir_winner_check(1, 1)

  # northeast - southwest diagonal direction (1, -1) steps
  ne_win = dir_winner_check(1, -1)
  
  if (h_win or v_win or nw_win or ne_win):
    return grid[last_point]
  else:
    return 0

if __name__ == "__main__":
    gomoku_game(30, 30)
