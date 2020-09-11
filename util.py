from game import Board
def play_game(board, player1, player2):
    player1.new_game(True)
    player2.new_game(False)
    finished = False
    moveCount = 0
    hadCount = 0
    while not finished:
        if board.myTurn:
            # print('nn turn')
            # print('start turn')
            # moveCount += 1
            # if player1.training:
                # player1.move(board)
            # else:
                # had = player1.move(board)
                # if had:
                    # hadCount += 1
            # else:
            player1.move(board)
            # print('done turn')
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
    return finalResult, moveCount, hadCount

    # return finalResult, moveCount, hadCount, set(player1.currentPosition)

def battle(player1, player2, num_games = 100000, silent = False):
    draw_count = 0
    oneCount = 0
    twoCount = 0
    draw_count=0
    medTotal = 0
    medHad = 0
    medPos = set()
    for i in range(num_games):
        board = Board()
        result, total, had = play_game(board, player1, player2)
        medTotal += total
        medHad += had
        # medPos.update(pos)
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
        #if i%20==0:
   #         print('finished game #' + str(i))
        # input()
    if not silent:
        p1 = player1.typeRep()
        p2 = player2.typeRep()
        print("After {} games we have draws: {}, {} wins: {}, and {} wins: {}.".format(num_games, draw_count, p1, oneCount, p2, twoCount))

        print("Which gives percentages of draws: {:.2%}, {} wins: {:.2%}, and {} wins:  {:.2%}".format(
            draw_count / num_games, p1, oneCount / num_games, p2, twoCount / num_games))

    return oneCount, twoCount, draw_count, medTotal, medHad
    # return oneCount, twoCount, draw_count, medTotal, medHad, medPos


def evaluate_players(p1, p2, games_per_battle=100, num_battles=100, writer = None, silent = False):
    p1_wins = []
    p2_wins = []
    draws = []
    game_number = []
    game_counter = 0
    bigTotal = 0
    bigHad = 0
    bigPos = set()
    
    for i in range(num_battles):
        if i%10==0:
            print('starting battle #'+str(i))
        p1win, p2win, draw, total, had = battle(p1, p2, games_per_battle, silent)
        bigTotal += total
        bigHad += had
        p1_wins.append(p1win)
        p2_wins.append(p2win)
        draws.append(draw)
        # bigPos.update(pos)
        game_counter = game_counter + 1
        game_number.append(game_counter)
        if writer is not None:
            summary = tf.Summary(value=[tf.Summary.Value(tag='Player 1 Win', simple_value=p1win),
                                        tf.Summary.Value(tag='Player 2 Win', simple_value=p2win),
                                        tf.Summary.Value(tag='Draw', simple_value=draw)])
            writer.add_summary(summary, game_counter)
        # if i%5==0:
            # print('total moves: ', bigTotal)
            # print('total had: ', bigHad)
            # print('percentage had: ', bigHad/bigTotal)

    # return game_number, p1_wins, p2_wins, draws
    return game_number, p1_wins, p2_wins, draws
