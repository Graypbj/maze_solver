from cell import Cell
import time
import random

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        left_x = (i * self._cell_size_x) + self._x1
        top_y = (j * self._cell_size_y) + self._y1
        right_x = left_x + self._cell_size_x
        bottom_y = top_y + self._cell_size_y
        current_cell = self._cells[i][j]
        current_cell.draw(left_x, top_y, right_x, bottom_y)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
            self._cells[i][j].visited = True
            while True:
                next_index_list = []

                if i > 0 and not self._cells[i - 1][j].visited:
                    next_index_list.append((i - 1, j))
                if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                    next_index_list.append((i + 1, j)) 
                if j > 0 and not self._cells[i][j - 1].visited:
                    next_index_list.append((i, j - 1))
                if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                    next_index_list.append((i, j + 1))
                if len(next_index_list) == 0:
                    self._draw_cell(i, j)
                    return

                direction_index = random.randrange(len(next_index_list))
                next_i, next_j = next_index_list[direction_index]
                    
                if next_i > i:
                    self._cells[i][j].has_top_wall = False
                    self._cells[i + 1][j].has_bottom_wall = False
                if next_i < i:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i - 1][j].has_top_wall = False
                if next_j > j:
                    self._cells[i][j].has_right_wall = False
                    self._cells[i][j + 1].has_left_wall = False
                if next_j < j:
                    self._cells[i][j].has_left_wall = False
                    self._cells[i][j - 1].has_right_wall = False
                self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
