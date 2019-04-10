class Bot:
    def __init__(self, method='random', heuristic=None, depth=None):
        self.method = method
        self.heuristic = heuristic
        self.depth = depth

    def step(self, board):
        if self.method == 'random':
            self.__random_step(board)

    def __random_step(self, board):
        print(board.legal_moves())
        pass

    def __generate_possible_moves(self, board):
        pass
