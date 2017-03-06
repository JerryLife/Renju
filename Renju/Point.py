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
