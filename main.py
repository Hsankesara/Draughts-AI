import checkers
import gamebot
from time import sleep
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


def main():
    while True:
        game = checkers.Game(loop_mode=True)
        game.setup()
        bot = gamebot.Bot(game, RED, mid_eval='piece_and_board',
                          end_eval='sum_of_dist', method='alpha_beta', depth=3)
        random_bot_blue = gamebot.Bot(
            game, BLUE, mid_eval='piece_and_board_pov', method='alpha_beta', depth=3, end_eval='sum_of_dist')
        while True:  # main game loop
            if game.turn == BLUE:
                 # TO start player's turn uncomment the below line and comment a couple  of line below than that
                # game.player_turn()
                count_nodes = random_bot_blue.step(game.board, True)
                print('Total nodes explored in this step are', count_nodes)
                game.update()
            else:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                # game.player_turn()
                count_nodes = bot.step(game.board, True)
                print('Total nodes explored in this step are', count_nodes)
                game.update()
            if game.endit:
                break


if __name__ == "__main__":
    main()
    pass
