"""Board class so we can store the relevant data pertaining to a Sudoku."""
import copy
from tile import Tile, TileText


class SudokuBoard(object):

    def __init__(self, data=None, input_file=None):
        # Assume data is a 2D array of shape 9x9, with Nones to
        # represent blank tiles
        if data is None:
            if input_file is None:
                self.data = [[None for i in range(9)] for j in range(9)]
            else:
                self.read_data_from_file(input_file)
        else:
            assert len(data) == 9 and len(data[0]) == 9
            self.data = copy.deepcopy(data)

        self.tile_text = [[TileText(dig=self.data[i][j]) for i in range(9)]
                          for j in range(9)]
        self.tiles = [[Tile(self.tile_text[i][j]) for i in range(9)]
                      for j in range(9)]

    def read_data_from_file(self, filename):
        pass

    def draw(self, screen):
        # Since we force a 16:9 resolution on the board,
        # Code the board to occupy the middle 50% of the width
        # And the middle 8/9 of the screen
        width, height = screen.get_size()
        start_x, start_y = int(width / 4), int(height / 18)
        tile_size = int(width / 18)
        for i in range(9):
            for j in range(9):
                x, y = start_x + i*tile_size, start_y + j*tile_size
                self.tiles[i][j].draw(x, y, tile_size, screen)
        # TODO: draw the box lines

    def update_tile(self, tile_x, tile_y):
        pass

    def check_unique_solve(self):
        pass

    def check_solve(self):
        pass
