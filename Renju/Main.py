# Python 3.6.0

import pygame
from pygame.locals import *
from sys import exit
from Point import *
from Winner import *


class Loop(Exception): pass


def main():

    # init the window
    pygame.init()
    screen = pygame.display.set_mode((SIZE + EXTRA_WIDTH, SIZE), 0, 32)
    pygame.display.set_caption("WuZi")

    # load picture of the board and convert
    background = pygame.image.load("board.jpg").convert()

    # black first
    turn = BLACK

    # create the virtual board
    x0, y0 = 23, 23  # according to Photoshop
    dist = 35  # according to Photoshop
    board = [[Point(x, y, x0 + x * dist, y0 + y * dist) for y in range(15)] for x in range(15)]

    # main loop
    while True:

        # show the background
        screen.blit(background, (EXTRA_WIDTH, 0))

        # draw rectangle
        rect_rgb = (213, 180, 145)
        rect_size = Rect((0, 0), (EXTRA_WIDTH, SIZE))
        pygame.draw.rect(screen, rect_rgb, rect_size)

        # event loop
        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = pygame.mouse.get_pos()
                # click in the board
                if x_pos > EXTRA_WIDTH:
                    x_pos -= EXTRA_WIDTH
                    try:
                        for x in range(15):
                            for y in range(15):
                                cur_point = board[x][y]
                                if cur_point.in_round(x_pos, y_pos):
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

                # click out of board
                else:
                    pass
            else:
                pass

        # check if someone wins
        winner = check_win(board)
        print_result(background, winner)

        pygame.display.update()

if __name__ == '__main__':
    main()