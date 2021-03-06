"""Board class so we can store the relevant data pertaining to a Sudoku."""
import copy
import pygame
from tile import Tile, TileText


class SudokuBoard(object):
    DEFAULT_LINECOL = (0, 0, 0)

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

        self.tile_text = [[None for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                if self.data[i][j] is not None:
                    self.tile_text[i][j] = TileText(dig=self.data[i][j],
                                                    user=False)
                else:
                    self.tile_text[i][j] = TileText(user=True)

        self.tiles = [[Tile(self.tile_text[i][j]) for i in range(9)]
                      for j in range(9)]
        self.highlighted = {(i, j): False for i in range(9) for j in range(9)}

    def read_data_from_file(self, filename):
        data = None
        with open(filename, 'r+') as in_file:
            data = in_file.readlines()
        for i in range(len(data)):
            data[i] = data[i].strip()
            data[i] = list(data[i])
            for j in range(len(data[i])):
                if data[i][j] == '.':
                    data[i][j] = None
        # new_data = [[None for i in range(9)] for j in range(9)]
        # for i in range(len(data)):
        #     for j in range(len(data[0])):
        #         new_data[i][j] = data[j][i]
        self.data = data

    def draw(self, screen):
        # Since we force a 16:9 resolution on the board,
        # Code the board to occupy the middle 50% of the width
        # And the middle 8/9 of the screen
        width, height = screen.get_size()
        self.start_x, self.start_y = int(width / 4), int(height / 18)
        self.tile_size = int(width / 18)
        for i in range(9):
            for j in range(9):
                x = self.start_x + i*self.tile_size
                y = self.start_y + j*self.tile_size
                if self.highlighted[i, j]:
                    self.tiles[i][j].draw(x, y, self.tile_size, screen,
                                          highlight=True)
                else:
                    self.tiles[i][j].draw(x, y, self.tile_size, screen)
        bold_line_width = 8
        for i in range(4):
            start_pos = (self.start_x + 3*i*self.tile_size, self.start_y)
            end_pos = (self.start_x + 3*i*self.tile_size,
                       self.start_y + 9*self.tile_size)
            pygame.draw.line(screen, self.DEFAULT_LINECOL,
                             start_pos=start_pos, end_pos=end_pos,
                             width=bold_line_width)

            start_pos = (self.start_x, self.start_y + 3*i*self.tile_size)
            end_pos = (self.start_x + 9*self.tile_size,
                       self.start_y + 3*i*self.tile_size)

            pygame.draw.line(screen, self.DEFAULT_LINECOL,
                             start_pos=start_pos, end_pos=end_pos,
                             width=bold_line_width)

    def update_tile(self, tile_x, tile_y, tile_text):
        if tile_text.dig is not None:
            self.tile_text[tile_x][tile_y] = tile_text
            self.tiles[tile_x][tile_y] = Tile(tile_text)
        else:
            old_text = self.tile_text[tile_x][tile_y]
            if old_text.top is not None:
                new_top = set(old_text.top)
            else:
                new_top = set()
            if old_text.center is not None:
                new_center = set(old_text.center)
            else:
                new_center = set()

            # Reconcile top
            if tile_text.top is not None:
                for d in tile_text.top:
                    if d not in new_top:
                        new_top.add(d)
                    else:
                        new_top.remove(d)
            # Reconcile center
            if tile_text.center is not None:
                for d in tile_text.center:
                    if d not in new_center:
                        new_center.add(d)
                    else:
                        new_center.remove(d)

            new_top, new_center = list(new_top), list(new_center)
            new_top.sort()
            new_center.sort()
            new_tile_text = TileText(top=new_top,
                                     center=new_center,
                                     user=True)
            self.tile_text[tile_x][tile_y] = new_tile_text
            self.tiles[tile_x][tile_y] = Tile(new_tile_text)

    def get_clicked(self, mpos):
        # Return the tile index currently hovered over
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                cell_x = self.start_x + i*self.tile_size
                cell_y = self.start_y + j*self.tile_size
                if cell_x < mpos[0] < cell_x + self.tile_size:
                    if cell_y < mpos[1] < cell_y + self.tile_size:
                        self.highlighted[i, j] = True
                        return (i, j)
        return None

    def reset_highlight(self):
        self.highlighted = {(i, j): False for i in range(9) for j in range(9)}

    def highlight_repeats(self, tile_x, tile_y):
        if self.tiles[tile_x][tile_y].text.dig is None:
            return
        dig = self.tiles[tile_x][tile_y].text.dig
        for i in range(9):
            for j in range(9):
                rep = self.tiles[i][j].text.dig
                if rep == dig:
                    self.highlighted[i, j] = True
                if self.tiles[i][j].text.top is not None:
                    if dig in self.tiles[i][j].text.top:
                        self.highlighted[i, j] = True
                if self.tiles[i][j].text.center is not None:
                    if dig in self.tiles[i][j].text.center:
                        self.highlighted[i, j] = True

    def check_solve(self):
        # Check each square
        not_filled = False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                digs = {}
                for ii in range(i, i+3):
                    for jj in range(j, j+3):
                        if self.tiles[ii][jj].text.dig is None:
                            not_filled = True
                        elif self.tiles[ii][jj].text.dig in digs:
                            self.highlighted[ii, jj] = True
                            rep_idx = digs[self.tiles[ii][jj].text.dig]
                            self.highlighted[rep_idx] = True
                            return False
                        else:
                            digs[self.tiles[ii][jj].text.dig] = (ii, jj)
        # Check each row
        for i in range(9):
            digs = {}
            for j in range(9):
                if self.tiles[i][j].text.dig is None:
                    continue
                if self.tiles[i][j].text.dig in digs:
                    self.highlighted[i, j] = True
                    self.highlighted[digs[self.tiles[i][j].text.dig]] = True
                    return False
                digs[self.tiles[i][j].text.dig] = (i, j)
        # Check each column
        for i in range(9):
            digs = {}
            for j in range(9):
                if self.tiles[j][i].text.dig is None:
                    continue
                if self.tiles[j][i].text.dig in digs:
                    self.highlighted[j, i] = True
                    self.highlighted[digs[self.tiles[j][i].text.dig]] = True
                    return False
                digs[self.tiles[j][i].text.dig] = (j, i)

        if not_filled:
            return False
        return True
