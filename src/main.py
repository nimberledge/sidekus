"""Run the program"""
import pygame
import logging

from board import SudokuBoard
from tile import TileText

DEFAULT_BG_COL = (255, 255, 255)


class Button(object):
    DEFAULT_COL = (0, 0, 0)
    DEFAULT_TEXTCOL = (0, 0, 0)

    def __init__(self, text):
        self.text = text

    def draw(self, screen, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.DEFAULT_COL, rect, width=2)
        font = pygame.font.SysFont(None, int(9*height/10))
        img = font.render(self.text, True, self.DEFAULT_TEXTCOL)
        screen.blit(img, (int(x + width/20), int(y + height//4)))


def main():
    # Set up logs
    logging.basicConfig()
    logging.info("Successfully imported pygame")

    pygame.init()
    pygame.font.init()
    logging.info("Successfully initialized pygame")
    # Set up sudoku board
    board = SudokuBoard(input_file='data/example1.txt')

    # Set up display
    screen_size = (1280, 720)
    screen = pygame.display.set_mode(size=(1280, 720),
                                     flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Sidekus")
    screen.fill(DEFAULT_BG_COL)
    check_button_x = int(3.25 * screen_size[0] / 4)
    check_button_y = int(0.4 * screen_size[1])
    b_width = int(screen_size[0] / 8)
    b_height = int(0.05 * screen_size[1])

    done = False
    is_highlight = False
    tiles_to_update = set()
    check_button = Button("Check Solution")
    show_solved_button = False
    solved = False
    logging.info("Initializing display")
    solved_button = None
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
                # Check for movement of cursor
                if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or
                    keys[pygame.K_UP] or keys[pygame.K_DOWN]):  # noqa: E129
                    if len(tiles_to_update) == 1:
                        tile = tiles_to_update.pop()
                        board.highlighted[tile] = False
                        if keys[pygame.K_UP]:
                            board.highlighted[tile[0], (tile[1]-1) % 9] = True
                            tiles_to_update.add((tile[0], (tile[1]-1) % 9))
                        elif keys[pygame.K_DOWN]:
                            board.highlighted[tile[0], (tile[1]+1) % 9] = True
                            tiles_to_update.add((tile[0], (tile[1]+1) % 9))
                        elif keys[pygame.K_LEFT]:
                            board.highlighted[(tile[0]-1) % 9, tile[1]] = True
                            tiles_to_update.add(((tile[0]-1) % 9, tile[1]))
                        elif keys[pygame.K_RIGHT]:
                            board.highlighted[(tile[0]+1) % 9, tile[1]] = True
                            tiles_to_update.add(((tile[0]+1) % 9, tile[1]))

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

                    if len(digs) == 0:
                        continue
                    # Center pencil mark
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        tile_text = TileText(dig=None, center=digs, user=True)
                    # Top pencil mark
                    elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        tile_text = TileText(top=digs, user=True)

                    for tile in tiles_to_update:
                        if board.tiles[tile[0]][tile[1]].text.user:
                            board.update_tile(tile[0], tile[1], tile_text)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                mpos = pygame.mouse.get_pos()
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    tile_idx = board.get_clicked(mpos)
                    if tile_idx is not None:
                        tiles_to_update.add(tile_idx)
                else:
                    is_highlight = True
                    tiles_to_update.clear()
                    board.reset_highlight()

                if check_button_x < mpos[0] < check_button_x + b_width:
                    if check_button_y < mpos[1] < check_button_y + b_height:
                        solved = board.check_solve()
                        if solved:
                            solved_button = Button("Looks good!")
                        else:
                            solved_button = Button("Nah mate you're off")
                        show_solved_button = True

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
        screen_size = screen.get_size()
        check_button_x = int(3.25 * screen_size[0] / 4)
        check_button_y = int(0.4 * screen_size[1])
        b_width = int(screen_size[0] / 7)
        b_height = int(0.05 * screen_size[1])
        check_button.draw(screen, check_button_x, check_button_y,
                          b_width, b_height)
        if show_solved_button:
            if solved:
                solved_button.draw(screen, check_button_x,
                                   check_button_y + 4 * b_height,
                                   0.8 * b_width,
                                   b_height)
            else:
                solved_button.draw(screen, check_button_x,
                                   check_button_y + 4 * b_height,
                                   1.25 * b_width,
                                   b_height)
        board.draw(screen)
        pygame.display.flip()

    logging.info("Display loop ended, program quitting")


if __name__ == '__main__':
    main()
