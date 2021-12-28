"""Tile class to hold data for a given square of
a sudoku and render the appropriate text in the
appropriate locations."""
import pygame


class TileText(object):
    """Class that defines what goes in a cell, sorts out
    pencil-marks vs actual digits"""
    def __init__(self, dig=None, top=None, center=None):
        if dig is not None:
            self.dig = str(dig)
        else:
            self.dig = None

        if top is not None:
            self.top = [str(t) for t in top]
        else:
            self.top = None

        if center is not None:
            self.center = [str(c) for c in center]
        else:
            self.center = None


class Tile(object):
    DEFAULT_TEXTCOL = (0, 0, 0)
    DEFAULT_TOPCOL = (68, 112, 173)
    DEFAULT_CENTER_COL = (141, 98, 112)

    def __init__(self, tile_text=None, font_name=None):
        self.text = tile_text
        self.font_name = font_name

    def draw(self, x, y, size, screen, highlight=False):
        # Base font size (for digit)
        font_size = int(2 * size / 3)
        # Deal with pencil marks
        if self.text.dig is not None:
            font = pygame.font.SysFont(self.font_name, font_size)
            img = font.render(self.text.dig, True, self.DEFAULT_TEXTCOL)
            screen.blit(img, (int(x + 2.5*size/7), int(y + 2.5*size/7)))
        elif self.text.top is not None or self.text.center is not None:
            font = pygame.font.SysFont(self.font_name, font_size // 2)
            if self.text.top is not None:
                top_str = ' '.join(self.text.top)
                top_img = font.render(top_str, True, self.DEFAULT_TOPCOL)
                screen.blit(top_img, (int(x + size/7), int(y + size/7)))
            if self.text.center is not None:
                center_str = ' '.join(self.text.center)
                center_img = font.render(center_str, True,
                                         self.DEFAULT_CENTER_COL)

                screen.blit(center_img, (int(x + 2.3*size/7),
                                         int(y + 3.5*size/7)))

        tile_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, self.DEFAULT_TEXTCOL, tile_rect, width=1)
