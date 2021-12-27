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
        self.top = top
        self.center = center


class Tile(object):
    DEFAULT_TEXTCOL = (255, 255, 255)

    def __init__(self, tile_text=None, font_name=None):
        self.text = tile_text
        self.font_name = font_name

    def draw(self, x, y, size, screen, highlight=False):
        font_size = int(2 * size / 3)
        font = pygame.font.SysFont(self.font_name, font_size)
        img = font.render(self.text.dig, True, self.DEFAULT_TEXTCOL)
        tile_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, self.DEFAULT_TEXTCOL, tile_rect, width=1)
        screen.blit(img, (int(x + 2.5*size/7), int(y + 2.5*size/7)))
