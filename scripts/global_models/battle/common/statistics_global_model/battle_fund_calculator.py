from global_models.battle.common.tank_global_model.team import Team

import math

def calculate_blue_and_red_fund(blue_score, red_score, fund):
    if blue_score == red_score:
        return fund / 2, fund / 2

    if blue_score <= red_score:
        blue_fund = int(blue_score / red_score * fund * 0.25)
        red_fund = fund - blue_fund
    else:
        red_fund = int(red_score / blue_score * fund * 0.25)
        blue_fund = fund - red_fund

    return blue_fund, red_fund

def find_user_info_with_largest_score(user_infos):
    user_info_by_score = {user_info.score:user_info for user_info in user_infos}
    scores = list(user_info_by_score.keys())
    scores.sort()
    return user_info_by_score[scores[-1]]

def share_battle_fund_between_tanks(user_infos, fund):
    if len(user_infos) == 0: return

    sum_square = sum([user_info.score**1.5 for user_info in user_infos])
    prizes_sum = 0

    # calculate funds
    for user_info in user_infos:
        if fund != 0 and sum_square != 0:
            user_info_score = user_info.score
            prize = math.floor( fund * user_info_score**1.5 / sum_square )
            prizes_sum += prize
        else:
            prize = 0

        user_info.fund = prize

    if sum_square == 0: return

    # add left over fund to winner tank fund
    user_info = find_user_info_with_largest_score(user_infos)
    user_info.fund += math.floor(fund - prizes_sum)
