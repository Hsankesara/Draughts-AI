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

    def __action(self, selected_piece, mouse_pos, board):
        if self.game.hop == False:
            if board.location(mouse_pos[0], mouse_pos[1]).occupant != None and board.location(mouse_pos[0], mouse_pos[1]).occupant.color == self.game.turn:
                selected_piece = mouse_pos

            elif selected_piece != None and mouse_pos in board.legal_moves(selected_piece[0], selected_piece[1]):

                board.move_piece(
                    selected_piece[0], selected_piece[1], mouse_pos[0], mouse_pos[1])

                if mouse_pos not in board.adjacent(selected_piece[0], selected_piece[1]):
                    board.remove_piece(selected_piece[0] + (mouse_pos[0] - selected_piece[0]) //
                                       2, selected_piece[1] + (mouse_pos[1] - selected_piece[1]) // 2)

                    self.game.hop = True
                    selected_piece = mouse_pos
                else:
                    self.game.end_turn()

        if self.game.hop == True:
            if selected_piece != None and mouse_pos in board.legal_moves(selected_piece[0], selected_piece[1], self.game.hop):
                board.move_piece(
                    selected_piece[0], selected_piece[1], mouse_pos[0], mouse_pos[1])
                board.remove_piece(selected_piece[0] + (mouse_pos[0] - selected_piece[0]) //
                                   2, selected_piece[1] + (mouse_pos[1] - selected_piece[1]) // 2)

            if board.legal_moves(mouse_pos[0], mouse_pos[1], self.game.hop) == []:
                self.game.end_turn()

            else:
                selected_piece = mouse_pos

    def __random_step(self, board):
        possible_moves = self.__generate_all_possible_moves(board)
        if possible_moves == []:
            self.game.end_turn()
            self.game.turn = BLUE
            return
        random_move = random.choice(possible_moves)
        rand_choice = random.choice(random_move[2])
        self.__action(random_move, rand_choice, board)
        self.game.turn = BLUE
        return

    def __generate_all_possible_moves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    print(board.legal_moves(i, j, self.game.hop))
                    possible_moves.append(
                        (i, j, board.legal_moves(i, j, self.game.hop)))
        return possible_moves
