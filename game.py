from solitaire import Solitaire


def play_game():
    print('------     NEW  GAME     ------')

    # create a game
    p = Solitaire()

    end_of_game = 0
    # make moves until the end of the game
    print('press enter to make a move')
    while abs(end_of_game) != 1:
        print()
        print(p)

        end_of_game = p.make_a_move(True)


def simulate_games(num_games):
    num_wins = 0

    print(f'started playing {num_games} games')
    for game in range(1, num_games + 1):
        # create a new game
        p = Solitaire()

        # make moves until the end of the game
        end_of_game = 0
        while abs(end_of_game) != 1:
            end_of_game = p.make_a_move(False)
            if end_of_game == 1:
                num_wins += 1

        if game % 500 == 0:
            print(f'{num_wins}/{game} ({round(num_wins * 100 / game, 1)}%)')

    print(f'Out of {num_games} games, computer won {num_wins}, '
          f'which is around {round(num_wins * 100 / num_games, 1)}% of games')


if __name__ == '__main__':
    # try this to simulate one game with all the prints:
    play_game()

    # try this to simulate a lot of games:
    simulate_games(10000)
