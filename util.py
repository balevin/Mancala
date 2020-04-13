from game import Board

def play_game(board, player1, player2):

    finished = False
    one = True
    while not finished:
        if one:
            result, finished = player1.move(board)
        else:
            result, finished = player2.move(board)
        one = not one
        
    # noinspection PyUnboundLocalVariable
    player1.final_result(board)
    # noinspection PyUnboundLocalVariable
    # try:
    player2.final_result(board)
    # except:
        # print(type(player2))
        # input()
    result = board.myScore>board.opScore
    return result

def battle(player1, player2, num_games = 100000, silent = False):
    draw_count = 0
    oneCount = 0
    twoCount = 0
    for _ in range(num_games):
        board = Board()
        result = play_game(board, player1, player2)
        if result:
            oneCount += 1
        else:
            twoCount += 1

    if not silent:
        print("After {} game we have draws: {}, Player 1 wins: {}, and Player 2 wins: {}.".format(num_games, draw_count,
                                                                                                  oneCount,
                                                                                                  twoCount))

        print("Which gives percentages of draws: {:.2%}, Player 1 wins: {:.2%}, and Player 2 wins:  {:.2%}".format(
            draw_count / num_games, oneCount / num_games, twoCount / num_games))

    return oneCount, twoCount, draw_count


def evaluate_players(p1, p2, games_per_battle=100, num_battles=100, writer = None, silent = False):
    p1_wins = []
    p2_wins = []
    draws = []
    game_number = []
    game_counter = 0

    for i in range(num_battles):
        p1win, p2win, draw = battle(p1, p2, games_per_battle, silent)
        p1_wins.append(p1win)
        p2_wins.append(p2win)
        draws.append(draw)
        game_counter = game_counter + 1
        game_number.append(game_counter)
        if writer is not None:
            summary = tf.Summary(value=[tf.Summary.Value(tag='Player 1 Win', simple_value=p1win),
                                        tf.Summary.Value(tag='Player 2 Win', simple_value=p2win),
                                        tf.Summary.Value(tag='Draw', simple_value=draw)])
            writer.add_summary(summary, game_counter)

    return game_number, p1_wins, p2_wins, draws