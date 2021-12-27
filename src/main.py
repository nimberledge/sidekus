"""Run the program"""
import pygame
import logging
from board import SudokuBoard


def main():
    # Set up logs
    logging.basicConfig()
    logging.info("Successfully imported pygame")

    pygame.init()
    pygame.font.init()
    logging.info("Successfully initialized pygame")
    # Set up sudoku board
    toy_data = [[None for i in range(9)] for j in range(9)]
    toy_data[0][0] = 5
    toy_data[1][3] = 5
    toy_data[1][1] = 6
    board = SudokuBoard(data=toy_data)

    # Set up display
    screen = pygame.display.set_mode(size=(1280, 720),
                                     flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Sidekus")
    screen.fill((0, 0, 0))

    done = False
    logging.info("Initializing display")
    while not done:
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                done = True
                break

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                for i, k in enumerate(range(pygame.K_1, pygame.K_9+1)):
                    print("{}: {}".format(i+1, keys[k]))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # clicked_pos = []

        # Draw on screen
        board.draw(screen)
        pygame.display.flip()

    logging.info("Display loop ended, program quitting")


if __name__ == '__main__':
    main()
