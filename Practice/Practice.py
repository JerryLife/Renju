# Python 3.6.0

import pygame
from pygame.locals import *
from sys import exit

SIZE = 535
EXTRA_WIDTH = 100
POINT_R = 15
BLACK = 1
WHITE = 2
DRAW = 3


class Loop(Exception): pass

class BlackWin(Loop): pass

class WhiteWin(Loop): pass


class Point:

    def __init__(self, x, y, x_pos, y_pos):
        self.__x = x
        self.__y = y
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__flag = None

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def x_pos(self):
        return self.__x_pos

    @property
    def y_pos(self):
        return self.__y_pos

    @property
    def occupy(self):
        return self.__flag  # BLACK or WHITE

    @occupy.setter
    def occupy(self, flag):
        self.__flag = flag

    def in_round(self, x_mouse, y_mouse) -> bool:
        r = 13
        if (self.__x_pos - x_mouse) ** 2 + (self.__y_pos - y_mouse) ** 2 <= r ** 2:
            return True
        else:
            return False


def print_result(background, winner):

    if winner == BLACK:
        winner_string = u"The Black Win"
    elif winner == WHITE:
        winner_string = u"The White Win"
    elif winner == DRAW:
        winner_string = u"Draw"
    else:
        return
    font = pygame.font.SysFont('Times New Roman', 60)
    text = font.render(winner_string, 1, (10, 10, 10))
    text_pos = text.get_rect()
    text_pos.center = background.get_rect().center
    background.blit(text, text_pos)


def check_win(board):

    draw = True
    try:
        # check the column
        for x in range(15):
            black_num, white_num = 0, 0
            for y in range(15):
                if board[x][y].occupy == BLACK:
                    white_num = 0
                    black_num += 1
                elif board[x][y].occupy == WHITE:
                    black_num = 0
                    white_num += 1
                else:   # occupy == None
                    black_num, white_num = 0, 0
                    draw = False

                # see if there are 5 string
                if black_num == 5:
                    raise BlackWin
                elif white_num == 5:
                    raise WhiteWin
                else:
                    pass

        # check the row
        for y in range(15):
            black_num, white_num = 0, 0
            for x in range(15):
                if board[x][y].occupy == BLACK:
                    white_num = 0
                    black_num += 1
                elif board[x][y].occupy == WHITE:
                    black_num = 0
                    white_num += 1
                else:  # occupy == None
                    black_num, white_num = 0, 0
                    draw = False

                # see if there are 5 string
                if black_num == 5:
                    raise BlackWin
                elif white_num == 5:
                    raise WhiteWin
                else:
                    pass

        # check angle \
        x, y = 0, 14
        while x < 15 and y >= 0:
            black_num, white_num = 0, 0
            try:
                for i in range(15):
                    if not (0 <= x+i <= 14 and 0 <= y+i <= 14):
                        raise IndexError
                    if board[x+i][y+i].occupy == BLACK:
                        white_num = 0
                        black_num += 1
                    elif board[x+i][y+i].occupy == WHITE:
                        black_num = 0
                        white_num += 1
                    else:  # occupy == None
                        black_num, white_num = 0, 0
                        draw = False

                    # see if there are 5 string
                    if black_num == 5:
                        raise BlackWin
                    elif white_num == 5:
                        raise WhiteWin
            except IndexError:
                pass
            finally:
                if y == 0:
                    x += 1
                else:
                    y -= 1

        # check angle /
        x, y = 0, 0
        while x < 15 and y < 15:
            black_num, white_num = 0, 0
            try:
                for i in range(15):
                    if not (0 <= x + i <= 14 and 0 <= y - i <= 14):
                        raise IndexError
                    if board[x + i][y - i].occupy == BLACK:
                        white_num = 0
                        black_num += 1
                    elif board[x + i][y - i].occupy == WHITE:
                        black_num = 0
                        white_num += 1
                    else:  # occupy == None
                        black_num, white_num = 0, 0
                        draw = False
                    # see if there are 5 string
                    if black_num == 5:
                        raise BlackWin
                    elif white_num == 5:
                        raise WhiteWin
            except IndexError:
                pass
            finally:
                if y == 14:
                    x += 1
                else:
                    y += 1

        # check if draw
        if draw:
            return DRAW
        else:
            return None
    except Loop as rst:
        if isinstance(rst, BlackWin):
            return BLACK
        else:
            return WHITE



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