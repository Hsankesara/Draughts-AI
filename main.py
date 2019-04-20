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
    game = checkers.Game()
    game.setup()
    bot = gamebot.Bot(game, RED, mid_eval='piece_and_row',
                      end_eval='sum_of_dist', method='alpha_beta', depth=4)
    random_bot_blue = gamebot.Bot(
        game, BLUE, mid_eval='piece_and_row', method='alpha_beta', depth=4, end_eval='sum_of_dist')
    while True:  # main game loop
        if game.turn == BLUE:
            # game.player_turn()
            random_bot_blue.step(game.board)
            game.update()
        else:
            bot.step(game.board)
            game.update()


if __name__ == "__main__":
    main()
    pass
