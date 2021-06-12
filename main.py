import ast
from src import mancala, game_board

def main():

    bot = int(input('Press 0/1 for Player 1 (player1 plays first) or Player 2:   '))
    mode = input('Easy 1, Hard 0:  ')
    stealing = int(input('Stealing 1, 0 without:  '))
    mod = 3 if mode == '0' else 15
    game_object = mancala(stealing=stealing, bot=bot, mode=mod)
    Continue_ = int(input('New Game 0, Continue 1:  '))
    if Continue_ == 1:
        game_file_ = open('Last Game state.txt', 'r')
        read = ast.literal_eval(game_file_.read())
        board_start = read['state_list']
        game_object._player_1 = read['player']

    else:
        board_start = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    game_object.game_list = board_start
    game_board(board_start)

    while True:
        turn = game_object.cycle()
        if turn[0] == 1:
            print(turn[1])
            break
    play_again = input('play agin press y/n: ')
    if  play_again.lower() == 'y':
        main()
    else:
        exit()       

if __name__ == '__main__':
    main()

    
