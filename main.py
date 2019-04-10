import checkers
import gamebot


def main():
    game = checkers.Game()
    game.setup()
    random_bot = gamebot.Bot()
    while True:  # main game loop
        game.player_turn()
        game.update()
        game.board.legal_moves
        random_bot.step(game.board)
        game.update()


if __name__ == "__main__":
    main()
    pass
