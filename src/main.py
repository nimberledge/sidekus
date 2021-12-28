"""Run the program"""
import pygame
import logging

from pygame.constants import K_LSHIFT, K_RSHIFT
from board import SudokuBoard
from tile import TileText

DEFAULT_BG_COL = (255, 255, 255)


def main():
    # Set up logs
    logging.basicConfig()
    logging.info("Successfully imported pygame")

    pygame.init()
    pygame.font.init()
    logging.info("Successfully initialized pygame")
    # Set up sudoku board
    board = SudokuBoard(input_file='data/example1.txt')
    # toy_text = TileText(dig=None, top=[7], center=None)
    # board.update_tile(3, 6, toy_text)
    # board.update_tile(5, 6, toy_text)

    # toy_text = TileText(dig=None, top=None, center=[6, 8])
    # board.update_tile(6, 8, toy_text)
    # toy_text = TileText(dig=3, user=True)
    # board.update_tile(3, 1, toy_text)

    # Set up display
    screen = pygame.display.set_mode(size=(1280, 720),
                                     flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Sidekus")
    screen.fill(DEFAULT_BG_COL)

    done = False
    is_highlight = False
    tiles_to_update = set()
    logging.info("Initializing display")
    while not done:
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                done = True
                break

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if len(tiles_to_update) == 0:
                    continue
                # If no modifiers, then just write the digit
                if not (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or
                        keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    dig = None
                    for i, k in enumerate(range(pygame.K_1, pygame.K_9+1)):
                        if keys[k]:
                            dig = i+1
                            break
                    else:
                        continue
                    tile_text = TileText(dig=dig, user=True)
                    for tile in tiles_to_update:
                        if board.tiles[tile[0]][tile[1]].text.user:
                            board.update_tile(tile[0], tile[1], tile_text)

                else:
                    # Pencil marks
                    digs = []
                    for i, k in enumerate(range(pygame.K_1, pygame.K_9+1)):
                        if keys[k]:
                            digs.append(i+1)
                    # Center pencil mark
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        tile_text = TileText(dig=None, center=digs, user=True)
                    elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        tile_text = TileText(top=digs, user=True)
                    else:
                        continue
                    for tile in tiles_to_update:
                        if board.tiles[tile[0]][tile[1]].text.user:
                            board.update_tile(tile[0], tile[1], tile_text)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    mpos = pygame.mouse.get_pos()
                    tile_idx = board.get_clicked(mpos)
                    if tile_idx is not None:
                        tiles_to_update.add(tile_idx)
                else:
                    is_highlight = True
                    tiles_to_update.clear()
                    board.reset_highlight()

            elif event.type == pygame.MOUSEBUTTONUP:
                is_highlight = False
                # print(tiles_to_update)

        if is_highlight:
            mpos = pygame.mouse.get_pos()
            tile_idx = board.get_clicked(mpos)
            if tile_idx is not None:
                tiles_to_update.add(tile_idx)

        # Draw on screen
        screen.fill(DEFAULT_BG_COL)
        board.draw(screen)
        pygame.display.flip()

    logging.info("Display loop ended, program quitting")


if __name__ == '__main__':
    main()
