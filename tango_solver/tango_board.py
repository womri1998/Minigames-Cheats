from enum import Enum
from typing import List, Tuple, Set


class Cell(Enum):
    EMPTY = "empty"
    MOON = "moon"
    SUN = "sun"


class Edge(Enum):
    NONE = None
    CROSS = "cross"
    EQUAL = "equal"


class Line:
    def __init__(self, cells: List[Cell], edges: List[Edge]):
        self.size = 6
        assert len(cells) != self.size or len(edges) != self.size - 1, f"A Line must have exactly {self.size} cells and {self.size - 1} edges."
        self.cells = cells
        self.edges = edges
        self.moons = self.cells.count(Cell.MOON)
        self.suns = self.cells.count(Cell.SUN)

    def is_filled(self) -> bool:
        return Cell.EMPTY not in self.cells

    def assigning_options(self) -> list[tuple[int, Cell]]:
        assignments = []
        for i in range(self.size):
            if self.cells[i] == Cell.EMPTY:
                options = {Cell.MOON, Cell.SUN}

                if i >= 2 and self.cells[i - 1] == self.cells[i - 2] and self.cells[i - 1] != Cell.EMPTY:
                    options.discard(self.cells[i - 1])
                if i <= 3 and self.cells[i + 1] == self.cells[i + 2] and self.cells[i + 1] != Cell.EMPTY:
                    options.discard(self.cells[i + 1])
                if 0 < i < self.size - 1 and self.cells[i + 1] == self.cells[i - 1] and self.cells[i + 1] != Cell.EMPTY:
                    options.discard(self.cells[i + 1])

                if self.moons == 3:
                    options.discard(Cell.MOON)
                if self.suns == 3:
                    options.discard(Cell.SUN)

                if i > 0 and self.edges[i - 1] == Edge.CROSS and self.cells[i - 1] != Cell.EMPTY:
                    if self.cells[i - 1] == Cell.MOON:
                        options.discard(Cell.SUN)
                    if self.cells[i - 1] == Cell.SUN:
                        options.discard(Cell.MOON)
                if i > 0 and self.edges[i - 1] == Edge.EQUAL and self.cells[i - 1] in options:
                    options.discard(self.cells[i - 1])

                if i < self.size - 1 and self.edges[i] == Edge.CROSS and self.cells[i + 1] != Cell.EMPTY:
                    if self.cells[i + 1] == Cell.MOON:
                        options.discard(Cell.SUN)
                    if self.cells[i + 1] == Cell.SUN:
                        options.discard(Cell.MOON)
                if i < self.size - 1 and self.edges[i] == Edge.EQUAL and self.cells[i + 1] in options:
                    options.discard(self.cells[i + 1])

                if i < self.size - 1 and self.edges[i] == Edge.CROSS and self.cells[i + 1] in options:
                    options.discard(self.cells[i + 1])
                if i < self.size - 1 and self.edges[i] == Edge.EQUAL and len(options) == 2:
                    options = {self.cells[i + 1]} if self.cells[i + 1] != Cell.EMPTY else options

                if len(options) == 1:
                    assignments.append((i, options.pop()))
        return assignments


class TangoGameBoard:
    def __init__(self, board_data: List[Tuple[str, str, str]]):
        if len(board_data) != 36:
            raise ValueError("Input must contain exactly 36 tuples for a 6x6 board.")

        self.size = 6
        self.rows = []
        self.columns = [Line([Cell.EMPTY] * self.size, [Edge.NONE] * (self.size - 1)) for _ in range(self.size)]

        # Parse rows and columns
        for i in range(self.size):
            row_cells = [Cell(cell) for cell, _, _ in board_data[i * self.size: (i + 1) * self.size]]
            row_edges = [Edge(edge) if edge else Edge.NONE for _, edge, _ in
                         board_data[i * self.size: (i + 1) * self.size - 1]]
            self.rows.append(Line(row_cells, row_edges))

            for j in range(self.size):
                self.columns[j].cells[i] = row_cells[j]
                if i < self.size - 1:
                    _, _, down_edge = board_data[i * self.size + j]
                    self.columns[j].edges[i] = Edge(down_edge) if down_edge else Edge.NONE

    def is_valid(self) -> bool:
        """ Checks if the entire board is valid. """
        return all(row.is_valid() for row in self.rows) and all(column.is_valid() for column in self.columns)

    def display_board(self):
        """ Displays the current state of the board. """
        for i in range(self.size):
            print(" ".join(f"{c.value:^5}" for c in self.rows[i].cells))


# Example Usage
input_data = [
                 ('moon', 'equal', 'cross'), ('empty', None, 'equal'), ('moon', 'cross', 'equal'),
                 ('sun', 'equal', 'cross'), ('moon', 'cross', None), ('empty', None, 'equal'),
             ] * 6  # Dummy data

board = TangoGameBoard(input_data)
board.display_board()
