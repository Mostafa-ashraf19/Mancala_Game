import ast
from .console_draw import game_board
last_game_state = 'Last Game state.txt'


def alpha_beta_fun(state, depth, alpha, beta, _min_max_bool=True):

    # Stop conditions.
    if depth == 0 or state.end(state.game_list)[0]:
        return state.cost(state.game_list), -1
    # true -> max
    elif _min_max_bool == True:
        old_alpa = -50000
        bowl = -1
        start, end = (0, 6) if state._player_1 else (7, 13)

        for i in range(start, end):
            if state.game_list[i] == 0:
                continue
            s = mancala()
            s.game_list = state.game_list[:]
            _min_max_bool = s.move(i)
            new_alpha, _ = alpha_beta_fun(
                s, depth-1, alpha, beta, _min_max_bool)
            if old_alpa < new_alpha:
                bowl = i
                old_alpa = new_alpha
            alpha = max(alpha, old_alpa)
            if alpha >= beta:
                break
        return old_alpa, bowl
    else:
        old_beta = 50000
        bowl = -1
        for i in range(0, 6):
            if state.game_list[i] == 0:
                continue
            s = mancala()
            s.game_list = state.game_list[:]
            _min_max_bool = s.move(i)
            new_beta, _ = alpha_beta_fun(
                s, depth - 1, alpha, beta, not _min_max_bool)
            if old_beta > new_beta:
                bowl = i
                old_beta = new_beta
            beta = min(beta, old_beta)
            # cut off condition
            if alpha >= beta:
                break
        return old_beta, bowl


class mancala:
    # Game Layout
    # ------------------------------------------------------------------------------------------------
    # |            | Pocket 12 | Pocket 11 | Pocket 10 | Pocket 9 | Pocket 8 | Pocket 7 |            |
    # |   Score    |--------------------------------------------------------------------|   Score    |
    # |     P1     | Pocket 6 | Pocket 5 | Pocket 4 | Pocket 3 | Pocket 2 | Pocket 1    |    P2      |
    # ------------------------------------------------------------------------------------------------
    def __init__(self, mode=10, _player_1=True, stealing=False, bot=False):
        '''
        This is Mancala AI game 
        If you select True Player 1 will be the bot, False other.
        '''
        self.start_state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.game_list = self.start_state
        self._player_1 = _player_1
        self.stealing = stealing
        self.last_score = (0, 0)
        self.bot = bot
        self.save_game = {}
        self.mode = mode

    def end(self, check_list):
        if sum(check_list[0:6]) == 0:
            return 1, (check_list[6], check_list[13]+sum(check_list[7:13]))
        elif sum(check_list[7:13]) == 0:
            return 1, (check_list[6]+sum(check_list[0:6]), check_list[13])
        else:
            return 0, (0, 0)

    def switch_player(self):
        self._player_1 = False if self._player_1 == True else True

    def cycle(self):
        _player_1 = self._player_1
        print('Player 1' if _player_1 else 'Player 2')
        if _player_1:
            if self.bot:
                _, in_pocket = alpha_beta_fun(
                    self, self.mode, -50000, 50000, True)
                print(in_pocket)
            else:
                user_in = input('Select Pocket (0->5) or q:  ')
                if user_in == 'q':
                    self.save_game['state_list'] = self.game_list
                    self.save_game['player'] = self._player_1
                    file = open(last_game_state, 'a')
                    file.write(str(self.save_game))
                    file.close()
                    return 1, 'Last Game State Saved'
                elif int(user_in) < 13:
                    in_pocket = int(user_in)
                else:
                    return 1, 'Wrong Input'
            pocket = in_pocket
            self.switch_player()
            if pocket <= 5:
                if self.game_list[pocket] != 0:
                    stones = self.game_list[pocket]
                    loop_counter = 1
                    next_pocket = 0
                    while stones > 0:
                        if next_pocket < 13 and loop_counter < 13:
                            next_pocket = pocket+loop_counter
                            loop_counter += 1
                            if next_pocket != 13:
                                self.game_list[next_pocket] = self.game_list[next_pocket] + 1
                                stones -= 1

                        else:
                            next_pocket = 0
                            pocket = 0
                            loop_counter = 0

                        if stones == 0 and next_pocket == 6 and self.end(self.game_list)[0] == 0:
                            self.switch_player()
                        if self.stealing and stones == 0 and next_pocket < 6 and self.game_list[next_pocket] == 1:
                            self.steal(next_pocket)

                    self.game_list[in_pocket] = 0
                    if self.end(self.game_list)[0] == 0:
                        game_board(self.game_list)
                        return 0, 'board printed'
                    else:
                        self.last_score = self.end(self.game_list)[1]
                        game_board(self.game_list)
                        print('Game Finished')
                        print('Last Score: ', self.last_score)
                        return 1, self.last_score, self.game_list

                else:
                    self.switch_player()
                    state = 'Empty Pocket Pick another one'
                    print(state)
                    return 0, state
            else:
                self.switch_player()
                state = 'Wrong Pocket Input'
                print(state)
                return 0, state

        elif not _player_1:
            if not self.bot:
                _, in_pocket = alpha_beta_fun(
                    self, self.mode, -50000, 50000, True)
                print(in_pocket)
            else:
                user_in = input('Select Pocket (7->12) or q: ')
                if user_in == 'q':
                    self.save_game['state_list'] = self.game_list
                    self.save_game['player'] = self._player_1
                    file = open(last_game_state, 'a')
                    file.write(self.save_game)
                    file.close()
                    return 1, 'Last Game State Saved'
                elif int(user_in) < 13:
                    in_pocket = int(user_in)
                else:
                    return 1, 'Wrong Input'
            pocket = in_pocket
            self.switch_player()
            if pocket in range(7, 13):
                if self.game_list[pocket] != 0:
                    stones = self.game_list[pocket]
                    loop_counter = 1
                    next_pocket = 0
                    while stones > 0:
                        if next_pocket < 13 and loop_counter < 13:
                            next_pocket = pocket+loop_counter
                            loop_counter += 1
                            if next_pocket != 6:
                                self.game_list[next_pocket] = self.game_list[next_pocket] + 1
                                stones -= 1
                        else:
                            next_pocket = 0
                            pocket = 0
                            loop_counter = 0

                        if stones == 0 and next_pocket == 13 and self.end(self.game_list)[0] == 0:
                            self.switch_player()

                        if self.stealing and stones == 0 and next_pocket in range(7, 13) and self.game_list[next_pocket] == 1:
                            self.steal(next_pocket)

                    self.game_list[in_pocket] = 0

                    if self.end(self.game_list)[0] == 0:
                        game_board(self.game_list)
                        return 0, 'board printed'
                    else:
                        self.last_score = self.end(self.game_list)[1]
                        game_board(self.game_list)
                        print('Game Finished')
                        print('Score: ', self.last_score)
                        return 1, self.last_score

                else:
                    self.switch_player()
                    state = 'Empty Pocket, Choose another one'
                    print(state)
                    return 0, state
            else:
                self.switch_player()
                state = 'Wrong Pocket input'
                print(state)
                return 0, state

    def cost(self, check_list):
        if self.end(check_list)[0]:
            if check_list[0] > check_list[6]:
                return 50
            elif check_list[13] == check_list[6]:
                return 0
            else:
                return -50
        else:
            return check_list[13] - check_list[6]

    def _calc_step(self, add, i, condition_value):
        stones = add
        while stones > 0:
            i += 1
            i = i % 14
            stones -= 1
            if i != condition_value:
                self.game_list[i % 14] += 1

    def _step(self, i, j):
        againturn = False
        add = self.game_list[j]
        self.game_list[j] = 0
        if i > 6:
            self._calc_step(add, i, 6)
            if i > 6 and self.game_list[i] == 1 and i != 13 and self.game_list[5-(i-7)] != 0:
                self.game_list[13] += 1+self.game_list[5-(i-7)]
                self.game_list[i] = 0
                self.game_list[5-(i-7)] = 0
            if i == 13:
                againturn = True
        else:
            self._calc_step(add=add, i=i, condition_value=13)
            if i < 6 and self.game_list[i] == 1 and i != 6 and self.game_list[-i + 12] != 0:
                self.game_list[6] += 1 + self.game_list[-i + 12]
                self.game_list[i] = 0
                self.game_list[-i + 12] = 0
            if i == 6:
                againturn = True
        return againturn

    def move(self, i):
        j = i
        againturn = self._step(i, j)
        return againturn

    def steal(self, last_pocket):
        if last_pocket < 6:
            self.game_list[6] += self.game_list[12-last_pocket] + 1
            self.game_list[12-last_pocket], self.game_list[last_pocket] = 0, 0

        elif last_pocket > 6:
            self.game_list[13] += self.game_list[12-last_pocket] + 1
            self.game_list[12-last_pocket], self.game_list[last_pocket] = 0, 0
