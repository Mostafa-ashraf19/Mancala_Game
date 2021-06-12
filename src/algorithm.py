from .mancala import mancala

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