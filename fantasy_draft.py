import random
import fantasy_draft_functions as df

from constants import (
    POINTS_PER_GOAL,
    POINTS_PER_ASSIST,
    POINTS_PER_HIT,
    F_DCS_PER_POINT,
    D_DCS_PER_POINT,
    FORWARDS_NEEDED,
    DEFENCEMEN_NEEDED,
    GOALIES_NEEDED,
    BUDGET,
    PLAYERS_TO_SELECT,
    FORWARD,
    DEFENCEMEN,
    GOALIE
)


def init_player() -> dict:
    """Return a dictionary of all necessary
    player information.
    """
    return {
        "num_forwards": 0,
        "num_defence": 0,
        "num_goalies": 0,
        "budget": BUDGET,
        "team": "",
        "players": [],
    }


def players_selected(gm_info: dict) -> int:
    """Return the number of players selected by general manager."""

    return gm_info["num_forwards"] + gm_info["num_defence"] + gm_info["num_goalies"]


def display_move_prompt(current_player: str, player_score: int, gm: dict) -> None:
    """Display a prompt for the player to select the next move."""

    print("=" * 50)
    print(
        f"{current_player}, it is your turn. You have {player_score} fantasy"
        f" points, and ${gm['budget']} remaining."
    )
    print(
        f'You have selected {gm["num_forwards"]} forwards, '
        f'{gm["num_defence"]} defencemen and '
        f"{gm['num_goalies']} goalies."
    )


def compute_gm_score(gm_info: dict) -> float:
    """Return the fantasy score of the general manager.
    The fantasy score is defined as the sum of all players
    selected.
    """

    score = 0
    for player in gm_info["players"]:
        # If correct implementation, one of these will always
        # be 0
        score += df.compute_fantasy_score(player)

    return score


def can_create_team(gm: dict, players: list[str]) -> bool:
    """Return True if and only if the user can select a future player 
    without exceeding the maxmimum per position.
    """

    forward_prices = [df.get_price(p) for p in players]
    defence_prices = [df.get_price(p) for p in players if df.get_position(p) == DEFENCEMEN]
    goalie_prices = [df.get_price(p) for p in players if df.get_position(p) == GOALIE]

    forward_prices = sorted(forward_prices)
    defence_prices = sorted(defence_prices)
    goalie_prices = sorted(goalie_prices)

    return (
        sum(forward_prices[: FORWARDS_NEEDED - gm["num_forwards"]])
        + sum(defence_prices[: DEFENCEMEN_NEEDED - gm["num_defence"]])
        + sum(goalie_prices[: GOALIES_NEEDED - gm["num_goalies"]])
        <= gm["budget"]
    )


def interactive_select_player(
    gm: dict,
    player_ids: list[str],
    players: list[str],
    all_players: str,
    computer: bool = False,
) -> str:
    """Prompt the user to select a player. Return the updated all_players.
    """
    has_selected = False
    while not has_selected:
        if not computer:
            selected_player = input("Player or Command: ")
            if selected_player == "available_players":
                for p in players:
                    print("=" * 50)
                    print(f"Player: {p}")
                continue
        else:
            selected_player = player_ids[random.randint(0, len(player_ids) - 1)]

        if df.is_player_available(selected_player, players_available=all_players):
            index = player_ids.index(selected_player)
            player_info = players[index]

            players_copy = players.copy()
            gm_copy = gm.copy()
            players_copy.remove(player_info)
            position = df.get_position(player_info)
            if position == FORWARD:
                gm_copy["num_forwards"] += 1
            elif position == DEFENCEMEN:
                gm_copy["num_defence"] += 1
            else:
                gm_copy["num_goalies"] += 1
            gm_copy["budget"] = df.update_budget(gm_copy["budget"], player_info)

            if (
                df.can_select(
                    player_info,
                    gm["num_forwards"],
                    gm["num_defence"],
                    gm["num_goalies"],
                )
                and df.can_afford(gm["budget"], player_info)
                and can_create_team(gm_copy, players_copy)
            ):

                has_selected = True
                players.remove(player_info)
                player_ids.remove(selected_player)
                all_players = df.remove_player(
                    all_players, all_players.index(selected_player) + 3
                )
                gm["team"] = df.add_to_team(player_info, gm["team"])

                gm["budget"] = df.update_budget(gm["budget"], player_info)
                position = df.get_position(player_info)
                if position == FORWARD:
                    gm["num_forwards"] += 1
                elif position == DEFENCEMEN:
                    gm["num_defence"] += 1
                else:
                    gm["num_goalies"] += 1

                gm["players"].append(player_info)
            else:
                if not computer:
                    print(
                        "You can either not afford this player, selecting this "
                        "player will cause you to be shorthanded (lack of budget for "
                        "remaining players)"
                        " or have selected too "
                        "many in one position."
                    )
        else:
            if not computer:
                print("That player does not exist or has already "
                "been selected. Please select another...")

    if computer:
        print(f"Computer has selected {selected_player}")

    return all_players


def begin_draft(players: list[str], all_players: str) -> None:
    """ Play the Game!
    """

    print("=" * 50)
    print("Welcome to the UTSC Fantasy Hockey Draft!")
    print("=" * 50)
    print("Please select a mode:")
    print("0 : Computer")
    print("1 : Multiplayer")

    correct_mode = False
    while not correct_mode:
        mode = input("Mode: ")
        if mode not in ["0", "1"]:
            print("Incorrect mode. Please select either 0 or 1")
        else:
            correct_mode = True

    player_ids = [df.get_player_id(p) for p in players]

    gm1 = init_player()
    gm2 = init_player()

    gm1_is_selecting = True
    gm2_is_selecting = True

    while gm1_is_selecting or gm2_is_selecting:
        # First we do GM1
        gm1_score = compute_gm_score(gm1)
        display_move_prompt("GM 1", player_score=gm1_score, gm=gm1)

        if can_create_team(gm1, players):
            all_players = interactive_select_player(
                gm1, player_ids, players, all_players
            )
        else:
            print("You blew your budget....")
            print("You will be playing shorthanded!")
            gm1_is_selecting = False

        if mode == "1":
            gm2_score = compute_gm_score(gm2)
            display_move_prompt("GM 2", player_score=gm2_score, gm=gm2)
            if can_create_team(gm2, players):
                all_players = interactive_select_player(
                    gm2, player_ids, players, all_players
                )
            else:
                print("You blew your budget....")
                print("You will be playing shorthanded!")
                gm2_is_selecting = False
        else:
            gm2_score = compute_gm_score(gm2)
            display_move_prompt("Computer", player_score=gm2_score, gm=gm2)
            if can_create_team(gm2, players):
                all_players = interactive_select_player(
                    gm2, player_ids, players, all_players, computer=True
                )
            else:
                print("You blew your budget....")
                print("You will be playing shorthanded!")
                gm2_is_selecting = False

        if gm1_is_selecting:
            gm1_is_selecting = players_selected(gm1) != PLAYERS_TO_SELECT
        if gm2_is_selecting:
            gm2_is_selecting = players_selected(gm2) != PLAYERS_TO_SELECT

    gm1_score = compute_gm_score(gm1)
    gm2_score = compute_gm_score(gm2)

    print("=" * 50)
    print("=" * 50)
    print("=" * 50)
    print("=" * 50)
    print("=" * 50)
    print("=" * 50)
    print("=" * 50)
    print("The Results....")
    print(f"GM 1's Fantasy Team: {gm1['team']}")
    print(f"{'GM 2' if mode == '1' else 'Computer'}'s Fantasy Team: {gm2['team']}")
    print("=" * 50)
    print(f"GM 1's Fantasy Team Score: {gm1_score}")
    print(f"{'GM 2' if mode == '1' else 'Computer'}'s Fantasy Team Score: {gm2_score}")
    print("=" * 50)
    print("And the winner is.......")
    print(
        f"{'GM 1' if gm1_score > gm2_score else 'GM 2' if mode == '1' else 'Computer'}!!!!!!!!!!"
    )
    print("=" * 50)
    print("Thanks for playing!!")
    print("=" * 50)

    return


############################# The Program: #############################
if __name__ == "__main__":

    import doctest

    doctest.testmod()
    import os

    DATA_FILE = "players.txt"

    PLAYERS = []
    ALL_PLAYERS_STRING = ""
    with open(DATA_FILE, encoding="utf-8") as data_file:
        for line in data_file:
            if line == "\n":
                continue
            player_name, player_info = line.split(":")
            player_name, player_info = player_name.strip(), player_info.strip()

            ids = player_info.split("_")
            player_id = ids[0]
            ALL_PLAYERS_STRING = ALL_PLAYERS_STRING + player_id + "_"
            PLAYERS.append(player_info)

    begin_draft(PLAYERS, ALL_PLAYERS_STRING)

