import linecache


class Game(list):
    """
    (T, a, b)
    | T : BLACK(1) or WHITE(2)
    | a : x of the stone
    | b : y of the stone
    """
    @property
    def step_num(self):
        return len(self)

    @property
    def winner(self):
        return self[-1][0]

    @property
    def first(self):
        return self[0][0]

    '''
        def count_game(self, file_name):
            count = 0
            with open(file_name, 'r') as file:
                for line in file:
                    count += 1
            return count
    '''

    def save(self, file_name):
        try:
            with open(file_name, 'a') as file:
                file.write(str(self) + "\n")
            return True
        except (FileExistsError, FileNotFoundError) as err:
            print("FILE SAVE ERROR : {0}".format(err))
            return False

    def load(self, file_name, line_num):
        try:
            game = linecache.getline(file_name, line_num)
            # print(game)
            return game
        except (FileExistsError, FileNotFoundError) as err:
            print("FILE LOAD ERROR: {0}".format(err))
            return None

