import pygame
from Global import *


class Loop(Exception): pass

class BlackWin(Loop): pass

class WhiteWin(Loop): pass


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