'''
Game of Life

Rules taken from
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
'''

import pprint
import random
import time
from typing import Generator, Iterable, Iterator, List

class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self._is_alive = False

    def __str__(self):
        return 'O' if self.is_alive() else '.'

    def set_alive(self, is_alive: bool):
        self._is_alive = is_alive

    def is_alive(self) -> bool:
        return self._is_alive

    def is_dead(self) -> bool:
        return not self._is_alive

class Cells:

    def __init__(self, cells: Iterable[Cell]):
        self._cells = cells

    def get_n_alive(self) -> int:
        alive = filter(lambda cell: cell.is_alive(), self._cells)
        return len(list(alive))

    def toggle_alive(self):
        for cell in self._cells:
            cell.set_alive(not cell.is_alive())

class Board:

    def __init__(self, n_rows: int, n_cols: int):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = [
            [
                Cell(row, col) for col in range(n_cols) 
            ]
            for row in range(n_rows)
        ]

    def __str__(self):
        return '\n'.join([
            ' '.join([ str(cell) for cell in row ]) for row in self.cells
        ])

    def one_dim_size(self):
        return self.n_rows * self.n_cols

    def find_cell(self, idx: int) -> Cell:
        row = int(idx / self.n_cols)
        col = idx % self.n_cols
        return self.cells[row][col]

    def find_cell_by_row_col(self, row: int, col: int) -> Cell:
        return self.cells[row][col]

    def get_living_cells(self):
        for row in self.cells:
            for cell in row:
                if cell.is_alive():
                    yield cell

    def get_dead_cells(self):
        for row in self.cells:
            for cell in row:
                if cell.is_dead():
                    yield cell

    def _get_cell_neighbour_indices(self, cell: Cell) -> Generator[list[int], None, None]:
        for row_delta in range(-1, 2):
            for col_delta in range(-1, 2):
                if row_delta == col_delta == 0:
                    continue
                else:
                    yield [ cell.row + row_delta, cell.col + col_delta ]

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbour_indices = self._get_cell_neighbour_indices(cell)

        valid_indices = filter(lambda idx: idx[0] >= 0 and idx[0] < self.n_rows and idx[1] >= 0 and idx[1] < self.n_cols, neighbour_indices)

        cells = map(lambda idx: self.cells[idx[0]][idx[1]], valid_indices)
        return Cells(cells)

class World:

    def __init__(self, board: Board):
        self.board = board
        self._tick = 0

    def __str__(self):
        return f'tick={self._tick}\n{self.board}'

    def _one_dim_size(self):
        return self.board.one_dim_size()

    def _tick_living_cells(self) -> Cells:
        living_cells = self.board.get_living_cells()
        toggling_cells: List[Cell] = []

        for living_cell in living_cells:
            neighbours = self.board.get_neighbours(living_cell)
            n_alive_neighbours = neighbours.get_n_alive()

            if n_alive_neighbours < 2:
                # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                toggling_cells.append(living_cell)
            elif 3 >= n_alive_neighbours >= 2:
                # Any live cell with two or three live neighbours lives on to the next generation.
                pass
            elif n_alive_neighbours > 3:
                # Any live cell with more than three live neighbours dies, as if by overpopulation.
                toggling_cells.append(living_cell)

        return Cells(toggling_cells)

    def _tick_dead_cells(self) -> Cells:
        dead_cells = self.board.get_dead_cells()
        toggling_cells = []

        for dead_cell in dead_cells:
            neighbours = self.board.get_neighbours(dead_cell)
            n_alive_neighbours = neighbours.get_n_alive()

            if n_alive_neighbours == 3:
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                toggling_cells.append(dead_cell)

        return Cells(toggling_cells)

    def tick(self):
        live_to_toggle = self._tick_living_cells()
        dead_to_toggle = self._tick_dead_cells()

        live_to_toggle.toggle_alive()
        dead_to_toggle.toggle_alive()

        self._tick += 1

    def random_seed(self, n_live: int):
        world_len = self._one_dim_size()
        for x in range(n_live):
            cell_idx = random.randint(0, world_len - 1)
            cell = self.board.find_cell(cell_idx)
            cell.set_alive(True)

    def rectangle_seed(self, row_start:int, row_end: int, col_start: int, col_end:int):
        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                cell = self.board.find_cell_by_row_col(row, col)
                cell.set_alive(True)

def main():
    world = World(Board(20, 20))
    #world.random_seed(100)
    world.rectangle_seed(0, 15, 7, 8)
    n_ticks = 500

    for tick in range(n_ticks):
        print(world)
        world.tick()
        time.sleep(0.1)

if __name__ == '__main__':
    main()
