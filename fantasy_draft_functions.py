"""CSCA08: Fall 2025 -- Assignment 1: Ice Hockey Fantasy Draft

This file implements the functions required in fantasy_draft_functions.py.
It follows the Function Design Recipe and uses only the provided constants.
No input/print statements or additional imports are used.
"""

from constants import (
    POINTS_PER_GOAL,
    POINTS_PER_ASSIST,
    POINTS_PER_HIT,
    F_DCS_PER_POINT,
    D_DCS_PER_POINT,
    FORWARDS_NEEDED,
    DEFENCEMEN_NEEDED,
    GOALIES_NEEDED,
    FORWARD,
    DEFENCEMEN,
    GOALIE,
    SV_VALUE,
    GAA_VALUE,
    BUDGET,
    PLAYERS_TO_SELECT,
)


def get_player_id(player: str) -> str:
    """Return the id of player if the string is non-empty;
    otherwise return the empty string.

    Precondition: player is the string of player stats as
    seen in players.txt

    >>> get_player_id('MGO_PD_G0-_A14_DC43_H70_Pr5-')
    'MGO'
    >>> get_player_id('NSH_PF_G7-_A14_DC20_H73_Pr10')
    'NSH'
    >>> get_player_id('')
    ''
    """
    if len(player) == 0:
        return ""
    return player[:3]


def is_player_available(player: str, players_available: str) -> bool:
    """Return True if and only if the id of player is in players_available.

    Precondition: player is the string of player stats
                  as seen in players.txt,
                  players_available is the string of player ids
                  that are currently available for selection seperated
                  by _.

    >>> is_player_available('MGO_PD_G0-_A14_DC43_H70_Pr5-', 'DOL_NCA_MGO_AHS_')
    True
    >>> is_player_available('GGG_PD_G0-_A14_DC43_H70_Pr5-', 'DOL_NCA_MGO_AHS_')
    False
    >>> is_player_available('', 'DOL_NCA_MGO_AHS_')
    False
    """
    if len(player) == 0:
        return False
    return get_player_id(player) in players_available


def get_position(player: str) -> str:
    """Return the position of player if player is non-empty;
    otherwise return the empty string.

    Precondition: player is the string of player stats
    as seen in players.txt

    >>> get_position('MGO_PD_G0-_A14_DC43_H70_Pr5-')
    'D'
    >>> get_position('NSH_PF_G7-_A14_DC20_H73_Pr10')
    'F'
    >>> get_position('CLA_PG_GAA2.23_SV0.910_Pr20')
    'G'
    >>> get_position('')
    ''
    """
    if len(player) == 0:
        return ""
    return player[5]


def get_price(player: str) -> int:
    """Return the price of the player, or 0 if empty.

    The price is the last two characters of the string.
    If the second character is '-', it means the price is one digit.

    >>> get_price('NSH_PF_G7-_A14_DC20_H73_Pr10')
    10
    >>> get_price('MGO_PD_G0-_A14_DC43_H70_Pr5-')
    5
    >>> get_price('')
    0
    """
    if player == "":
        return 0
    s = player[-2:]
    if s[1] == "-":
        value = int(s[0])
    else:
        value = int(s)
    return value


def can_select(
    player: str,
    num_forwards: int,
    num_defencemen: int,
    num_goalies: int,
) -> bool:
    """Return True if choosing this player does not exceed position limits.

    player is the player string or ''.
    num_forwards, num_defencemen, and num_goalies are how many are already
    picked.

    >>> can_select('NSH_PF_G7-_A14_DC20_H73_Pr10', 2, 0, 0)
    True
    >>> can_select('NSH_PF_G7-_A14_DC20_H73_Pr10', 3, 0, 0)
    False
    >>> can_select('', 3, 3, 3)
    True
    """
    if player == "":
        return True
    pos = get_position(player)
    if pos == FORWARD:
        return num_forwards < FORWARDS_NEEDED
    if pos == DEFENCEMEN:
        return num_defencemen < DEFENCEMEN_NEEDED
    if pos == GOALIE:
        return num_goalies < GOALIES_NEEDED
    return False


def can_afford(budget: int, player: str) -> bool:
    """Return True if budget is enough to afford the player.

    >>> can_afford(50, 'NSH_PF_G7-_A14_DC20_H73_Pr10')
    True
    >>> can_afford(5, 'NSH_PF_G7-_A14_DC20_H73_Pr10')
    False
    """
    if player == "":
        return True
    price = get_price(player)
    return budget - price >= 0


def update_budget(budget: int, player: str) -> int:
    """Return updated budget after drafting the player.

    If player is '', budget stays the same.

    >>> update_budget(50, 'NSH_PF_G7-_A14_DC20_H73_Pr10')
    40
    >>> update_budget(10, 'NSH_PF_G7-_A14_DC20_H73_Pr20')
    -10
    """
    if player == "":
        return budget
    price = get_price(player)
    new_budget = budget - price
    return new_budget


def add_to_team(player: str, team: str) -> str:
    """Add the player's id to the team string if not already there.

    pid is the 3-letter id of the player.
    token is the id followed by '_', for example 'NSH_'.

    >>> add_to_team('NSH_PF_G7-_A14_DC20_H73_Pr10', 'MGO_')
    'MGO_NSH_'
    >>> add_to_team('', 'MGO_')
    'MGO_'
    """
    if player == "":
        return team
    pid = get_player_id(player)
    token = pid + "_"
    if token in team:
        return team
    return team + token


def remove_player(players: str, index: int) -> str:
    """Remove the player id that ends at the given underscore index.

    players is the team string of ids separated by '_'.
    index is the location in that string we are checking.

    >>> remove_player('DOL_NCA_MGO_AHS_', 7)
    'DOL_MGO_AHS_'
    >>> remove_player('DOL_NCA_MGO_AHS_', 8)
    'DOL_NCA_MGO_AHS_'
    """
    if index < 0 or index >= len(players):
        return players
    if players[index] != "_":
        return players
    return players[0:index - 4] + players[index:]


def compute_dc_points(player: str) -> int:
    """Return defensive contribution points.

    player is the full player string.

    >>> compute_dc_points('NSH_PF_G7-_A14_DC20_H73_Pr10')
    2
    >>> compute_dc_points('MGO_PD_G0-_A14_DC43_H70_Pr5-')
    8
    >>> compute_dc_points('CLA_PG_GAA2.23_SV0.910_Pr20')
    0
    """
    pos = get_position(player)
    if player == "" and pos == GOALIE:
        return 0

    s = player[17:19]
    if s[1] == "-":
        dc = int(s[0])
    else:
        dc = int(s)

    if pos == FORWARD:
        return dc // F_DCS_PER_POINT
    return dc // D_DCS_PER_POINT


def compute_goal_points(player: str) -> int:
    """Return goal points for a player.

    >>> compute_goal_points('NSH_PF_G7-_A14_DC20_H73_Pr10')
    28
    >>> compute_goal_points('CLA_PG_GAA2.23_SV0.910_Pr20')
    0
    """
    if player == "" or get_position(player) == GOALIE:
        return 0

    s = player[8:10]
    if s[1] == "-":
        goals = int(s[0])
    else:
        goals = int(s)

    points = goals * POINTS_PER_GOAL
    return points


def compute_assist_points(player: str) -> int:
    """Return assist points for a player.

    >>> compute_assist_points('NSH_PF_G7-_A14_DC20_H73_Pr10')
    28
    >>> compute_assist_points('CLA_PG_GAA2.23_SV0.910_Pr20')
    0
    """
    if player == "" or get_position(player) == GOALIE:
        return 0

    s = player[12:14]
    if s[1] == "-":
        assists = int(s[0])
    else:
        assists = int(s)

    points = assists * POINTS_PER_ASSIST
    return points


def compute_hit_points(player: str) -> float:
    """Return hit points for a player.

    >>> compute_hit_points('NSH_PF_G7-_A14_DC20_H73_Pr10')
    18.25
    >>> compute_hit_points('CLA_PG_GAA2.23_SV0.910_Pr20')
    0.0
    """
    if player == "" or get_position(player) == GOALIE:
        return 0.0

    s = player[21:23]
    if s[1] == "-":
        hits = int(s[0])
    else:
        hits = int(s)

    points = hits * POINTS_PER_HIT
    return points


def compute_fantasy_score(player: str) -> float:
    """Return total fantasy score.

    player is the full player string.
    For skaters: sum of goal, assist, DC, and hit points.
    For goalies: SV_VALUE * sv - GAA_VALUE * gaa.

    >>> compute_fantasy_score('NSH_PF_G7-_A14_DC20_H73_Pr10')
    76.25
    >>> round(compute_fantasy_score('CLA_PG_GAA2.23_SV0.910_Pr20'), 2)
    68.7
    >>> compute_fantasy_score('')
    0.0
    """
    if player == "":
        return 0.0

    pos = get_position(player)
    if pos == GOALIE:
        gaa_text = player[10:14]
        sv_text = player[17:22]
        gaa = float(gaa_text)
        sv = float(sv_text)
        value = SV_VALUE * sv - GAA_VALUE * gaa
        return value

    total = 0.0
    total = total + compute_goal_points(player)
    total = total + compute_assist_points(player)
    total = total + compute_dc_points(player)
    total = total + compute_hit_points(player)
    return total


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    