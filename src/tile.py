"""Tile class to hold data for a given square of
a sudoku and render the appropriate text in the
appropriate locations."""
import pygame


class TileText(object):
    """Class that defines what goes in a cell, sorts out
    pencil-marks vs actual digits"""
    def __init__(self, dig=None, top=None, center=None, user=True):
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

        self.user = user


class Tile(object):
    DEFAULT_GIVENCOL = (0, 0, 0)
    DEFAULT_USERCOL = (68, 112, 173)
    DEFAULT_TOPCOL = (255, 0, 0)
    DEFAULT_CENTER_COL = (0, 100, 0)
    DEFAULT_HLCOL = (241, 231, 64, 10)

    def __init__(self, tile_text=None, font_name=None):
        self.text = tile_text
        self.font_name = font_name

    def draw(self, x, y, size, screen, highlight=False):
        tile_rect = pygame.Rect(x, y, size, size)
        if highlight:
            pygame.draw.rect(screen, pygame.Color(self.DEFAULT_HLCOL),
                             tile_rect)

        pygame.draw.rect(screen, self.DEFAULT_GIVENCOL, tile_rect, width=1)
        # Base font size (for digit)
        font_size = int(7.5 * size / 10)
        # Deal with pencil marks
        if self.text.dig is not None:
            font = pygame.font.SysFont(self.font_name, font_size)
            if self.text.user:
                img = font.render(self.text.dig, True, self.DEFAULT_USERCOL)
            else:
                img = font.render(self.text.dig, True, self.DEFAULT_GIVENCOL)

            screen.blit(img, (int(x + 2.5*size/7), int(y + 2.2*size/7)))
        elif self.text.top is not None or self.text.center is not None:
            font = pygame.font.SysFont(self.font_name, int(5.5*font_size/10))
            if self.text.top is not None:
                top_str = ' '.join(self.text.top)
                top_img = font.render(top_str, True, self.DEFAULT_TOPCOL)
                screen.blit(top_img, (int(x + size/8), int(y + size/7)))
            if self.text.center is not None:
                center_str = ' '.join(self.text.center)
                center_img = font.render(center_str, True,
                                         self.DEFAULT_CENTER_COL)

                screen.blit(center_img, (int(x + 2.2*size/7),
                                         int(y + 2.9*size/7)))
