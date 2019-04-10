import pygame
import sys
from pygame.locals import *
import random
pygame.font.init()

##COLORS##
#             R    G    B
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GOLD = (255, 215,   0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


class Bot:
    def __init__(self, game, method='random', heuristic=None, depth=None):
        self.method = method
        self.heuristic = heuristic
        self.depth = depth
        self.game = game

    def step(self, board):
        self.game.turn = RED
        if self.method == 'random':
            self.__random_step(board)

    def __random_step(self, board):
        possible_moves = self.__generate_all_possible_moves(board)
        random_move = random.choice(possible_moves)
        print(random_move)
        rand_choice = random.choice(random_move[2])
        if rand_choice not in board.adjacent(random_move[0], random_move[1]):
            board.remove_piece(random_move[0] + (random_move[0] - random_move[0]) //
                               2, random_move[1] + (random_move[1] - random_move[1]) // 2)
        board.move_piece(random_move[0], random_move[1],
                         rand_choice[0], rand_choice[1])
        self.game.turn = BLUE
        return

    def __generate_all_possible_moves(self, board):
        possible_moves = []
        for i in range(7):
            for j in range(7):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    possible_moves.append(
                        (i, j, board.legal_moves(i, j, self.game.hop)))
        return possible_moves
