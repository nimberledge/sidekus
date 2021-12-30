"""Run the program"""
import pygame
import logging
import copy

from board import SudokuBoard
from tile import TileText

DEFAULT_BG_COL = (255, 255, 255)
MAX_BACKUP_LENGTH = 100


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


class TextBox(object):
    DEFAULT_COL = (0, 0, 0)
    DEFAULT_TEXTCOL = (0, 0, 0)

    def __init__(self, text):
        self.text = text

    def draw(self, screen, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.DEFAULT_COL, rect, width=-1)
        font = pygame.font.SysFont(None, int(8.5*height/10))
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
    board = SudokuBoard(input_file='data/med29.txt')

    # Set up display
    screen_size = (1280, 720)
    screen = pygame.display.set_mode(size=screen_size,
                                     flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Sidekus")
    screen.fill(DEFAULT_BG_COL)

    # Implement check button
    check_button_x = int(3.25 * screen_size[0] / 4)
    check_button_y = int(0.35 * screen_size[1])
    b_width = int(screen_size[0] / 7)
    b_height = int(0.05 * screen_size[1])
    # Implement undo button
    undo_button_x = int(3.25 * screen_size[0] / 4)
    undo_button_y = int(0.45 * screen_size[1])
    ub_width = int(screen_size[0] / 10)
    ub_height = int(0.05 * screen_size[1])
    # Implement redo button
    redo_button_x = int(3.25 * screen_size[0] / 4)
    redo_button_y = int(0.55 * screen_size[1])
    rb_width = int(screen_size[0] / 10)
    rb_height = int(0.05 * screen_size[1])
    # Instructions boxes
    inst_start_x = 0
    inst_start_y = int(3 * screen_size[1] / 18)
    inst_width = int(screen_size[0] / 8)
    inst_height = int(0.05 * screen_size[1])
    inst_title = TextBox("Controls")
    inst_1 = TextBox("1-9              : enter digit")
    inst_2 = TextBox("Ctrl+1-9      : green pencil mark")
    inst_3 = TextBox("Shift+1-9    : red pencil mark")
    inst_4 = TextBox("Space         : highlight repeats")
    inst_5 = TextBox("Mouse click: select cell")
    inst_6 = TextBox("Ctrl+click   : select cells")
    controls = [inst_title, inst_1, inst_2, inst_3, inst_4, inst_5, inst_6]

    # Set up game loop
    done = False
    is_highlight = False
    tiles_to_update = set()
    check_button = Button("Check Solution")
    undo_button = Button("Undo Move")
    redo_button = Button("Redo Move")
    show_solved_button = False
    solved = False
    logging.info("Initializing display")
    solved_button = None
    board_backup = []
    board_backup.append(copy.deepcopy(board))
    redo_list = []
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
                move_made = False
                if keys[pygame.K_SPACE]:
                    if len(tiles_to_update) == 1:
                        tile = tiles_to_update.pop()
                        tile_x, tile_y = tile
                        board.highlight_repeats(tile_x, tile_y)
                        tiles_to_update.add(tile)

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
                    move_made = True

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
                    move_made = True

                # Add board backups so we can undo moves
                if move_made:
                    if (len(board_backup) == MAX_BACKUP_LENGTH and
                        board_backup[-1] is not None): # noqa : E129
                        board_backup.pop()
                    board_backup.insert(0, copy.deepcopy(board))

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

                # Implement check solution
                if check_button_x < mpos[0] < check_button_x + b_width:
                    if check_button_y < mpos[1] < check_button_y + b_height:
                        solved = board.check_solve()
                        if solved:
                            solved_button = TextBox("Looks good!")
                        else:
                            solved_button = TextBox("Nah mate you're off")
                        show_solved_button = True
                # Implement undo
                if undo_button_x < mpos[0] < undo_button_x + ub_width:
                    if undo_button_y < mpos[1] < undo_button_y + ub_height:
                        if len(board_backup) > 0:
                            board = board_backup.pop(0)
                            redo_list.insert(0, copy.deepcopy(board))
                            board.draw(screen)
                # Implement redo
                if redo_button_x < mpos[0] < redo_button_x + rb_width:
                    if redo_button_y < mpos[1] < redo_button_y + rb_height:
                        if len(redo_list) > 0:
                            board = redo_list.pop(0)
                            board_backup.insert(0, copy.deepcopy(board))
                            board.draw(screen)

            elif event.type == pygame.MOUSEBUTTONUP:
                is_highlight = False

        if is_highlight:
            mpos = pygame.mouse.get_pos()
            tile_idx = board.get_clicked(mpos)
            if tile_idx is not None:
                tiles_to_update.add(tile_idx)

        # Draw on screen
        screen.fill(DEFAULT_BG_COL)
        screen_size = screen.get_size()
        # Print controls
        for i, ctrl in enumerate(controls):
            inst_y = inst_start_y + int(i * 1.25 * inst_height)
            ctrl.draw(screen, inst_start_x, inst_y, inst_width, inst_height)
        # Deal with buttons
        check_button.draw(screen, check_button_x, check_button_y,
                          b_width, b_height)
        undo_button.draw(screen, undo_button_x, undo_button_y,
                         ub_width, ub_height)
        if len(redo_list):
            redo_button.draw(screen, redo_button_x, redo_button_y,
                             rb_width, rb_height)

        if show_solved_button:
            if solved:
                solved_button.draw(screen, check_button_x - 0.1*b_width,
                                   check_button_y + 6 * b_height,
                                   0.8 * b_width,
                                   b_height)
            else:
                solved_button.draw(screen, check_button_x - 0.1*b_width,
                                   check_button_y + 6 * b_height,
                                   1.25 * b_width,
                                   b_height)
        board.draw(screen)
        pygame.display.update()

    logging.info("Display loop ended, program quitting")


if __name__ == '__main__':
    main()
