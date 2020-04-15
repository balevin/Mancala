from game import Board

def play_game(board, player1, player2):
    player1.new_game(True)
    player2.new_game(False)
    finished = False
    moveCount = 0
    while not finished:
        if board.myTurn:
            # print('nn turn')
            player1.move(board)
        else:
            # print('random move')
            # print('random turn')
            player2.move(board)
        finished = board.isOver()
        # input()
        # moveCount+=1
        # if moveCount%5==0:
        #     print(board)
        #     input()
    if board.myScore>board.opScore:
        finalResult = 'me'
    elif board.opScore>board.myScore:
        finalResult = 'op'
    else:
        finalResult = 'tie'
    player1.final_result(board)
    player2.final_result(board)
    return finalResult

def battle(player1, player2, num_games = 100000, silent = False):
    draw_count = 0
    oneCount = 0
    twoCount = 0
    draw_count=0
    for i in range(num_games):
        board = Board()
        result = play_game(board, player1, player2)
        # print(board)
        if result == 'me':
            # print('nn won')
            oneCount += 1
        elif result == 'op':
            # print('random won')
            twoCount += 1
        else:
            # print('tie')
            draw_count += 1
        if i%10==0:
            print('finished game #' + str(i))
        # input()
    if not silent:
        print("After {} game we have draws: {}, Neural Net wins: {}, and Random wins: {}.".format(num_games, draw_count,
                                                                                                  oneCount,
                                                                                                  twoCount))

        print("Which gives percentages of draws: {:.2%}, Neural Net wins: {:.2%}, and Random wins:  {:.2%}".format(
            draw_count / num_games, oneCount / num_games, twoCount / num_games))
    print(board)
    return oneCount, twoCount, draw_count


def evaluate_players(p1, p2, games_per_battle=100, num_battles=100, writer = None, silent = False):
    p1_wins = []
    p2_wins = []
    draws = []
    game_number = []
    game_counter = 0

    for i in range(num_battles):
        # print('starting battle #'+str(i))
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