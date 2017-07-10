# Python 3.6.0

import pygame
import pymysql
from pygame.locals import *
from sys import exit
from Point import *
from Winner import *
from File import *

class Loop(Exception): pass


def main():

    # init the window
    pygame.init()
    screen = pygame.display.set_mode((SIZE + EXTRA_WIDTH, SIZE), 0, 32)     # Basic canvas
    pygame.display.set_caption("WuZi")

    # load picture of the board and convert
    background = pygame.image.load("board.jpg").convert()
    button_start = pygame.image.load("start.png").convert_alpha()
    button_start = pygame.transform.scale(button_start, (EXTRA_WIDTH - 4, BUTTON_HEIGHT))

    # black firs
    turn = BLACK

    # create the virtual board
    x0, y0 = 23, 23  # according to Photoshop
    dist = 35  # according to Photoshop
    board = [[Point(x, y, x0 + x * dist, y0 + y * dist) for y in range(15)] for x in range(15)]

    # steps list
    game = Game()

    # main loop
    while True:

        # draw rectangle
        rect_rgb = (213, 180, 145)
        rect_size = Rect((0, 0), (EXTRA_WIDTH, SIZE))
        pygame.draw.rect(screen, rect_rgb, rect_size)

        # show the background
        screen.blit(background, (EXTRA_WIDTH, 0))

        # show the buttons
        screen.blit(button_start, (2, 2))

        # event loop
        for event in pygame.event.get():

            if event.type == QUIT:
                # debug
                # print(game.load("game.txt", 1))
                # print(game.load("game.txt", 2))
                exit()

            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = pygame.mouse.get_pos()
                # if click in the board
                if x_pos > EXTRA_WIDTH:
                    x_pos -= EXTRA_WIDTH
                    try:
                        for x in range(15):
                            for y in range(15):
                                cur_point = board[x][y]
                                if cur_point.in_round(x_pos, y_pos):

                                    '''save the position'''
                                    step = (turn, x, y)
                                    game.append(step)

                                    '''paint the point and mark the position'''
                                    if turn == BLACK and cur_point.occupy is None:
                                        point_pic = pygame.image.load("black.png").convert_alpha()
                                        board[x][y].occupy = BLACK
                                        turn = WHITE
                                    elif turn == WHITE and cur_point.occupy is None:
                                        point_pic = pygame.image.load("white.png").convert_alpha()
                                        board[x][y].occupy = WHITE
                                        turn = BLACK
                                    else:   # cur_point has been occupied
                                        raise Loop
                                    # show the point
                                    background.blit(point_pic,
                                                    (cur_point.x_pos - POINT_R, cur_point.y_pos - POINT_R))
                                    raise Loop
                    except Loop:
                        pass

                # if click out of board
                else:
                    pass

                # check if someone wins
                winner = check_win(board)
                print_result(background, winner)

                # if finished save this game to file
                if winner is not None:
                    file = game.save("game.txt")

                    # debug
                    # print(game.step_num)
                    # print(game.winner)

                    # reset steps list
                    game = Game()

            else:
                pass

        pygame.display.update()


if __name__ == '__main__':
    main()
