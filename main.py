# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

MAX_MINIMAX_DEPTH = 5


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


def get_safe_moves(my_head, my_neck, board_width, board_height, my_body, opponents_body):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    # check if next move will take snake out of bounds
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False

    # check if next move will take snake to position on its own body or another snake
    if (my_head["x"]+1, my_head["y"]) in my_body:
        is_move_safe["right"] = False
    if (my_head["x"]-1, my_head["y"]) in my_body:
        is_move_safe["left"] = False
    if (my_head["x"], my_head["y"]+1) in my_body:
        is_move_safe["up"] = False
    if (my_head["x"], my_head["y"]-1) in my_body:
        is_move_safe["down"] = False

    if opponents_body is not None:
        # check if next move will take snake to position on its own body or another snake
        if (my_head["x"] + 1, my_head["y"]) in opponents_body:
            is_move_safe["right"] = False
        if (my_head["x"] - 1, my_head["y"]) in opponents_body:
            is_move_safe["left"] = False
        if (my_head["x"], my_head["y"] + 1) in opponents_body:
            is_move_safe["up"] = False
        if (my_head["x"], my_head["y"] - 1) in opponents_body:
            is_move_safe["down"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    return safe_moves


def update_board_state(move, head, body, body_lst):
    tail = body_lst.pop()  # ToDo: Need to account for when food is eaten
    if move == "up":
        new_head = {"x": head["x"], "y": head["y"]+1}
    if move == "down":
        new_head = {"x": head["x"], "y": head["y"]-1}
    if move == "left":
        new_head = {"x": head["x"]-1, "y": head["y"]}
    if move == "right":
        new_head = {"x": head["x"]+1, "y": head["y"]}
    body.add((new_head["x"], new_head["y"]))
    body.remove(tail)
    return new_head, body, body_lst


def minimax(depth, player, my_head, my_neck, board_width, board_height, my_body, my_body_lst, opponents_body,
            opponents_body_lst, opponents_head, opponents_neck):
    if depth == MAX_MINIMAX_DEPTH:  # Might always want to end on the best score for "me" not worst for "opponent"?
        return 0

    if player == "me":
        best_score = float('-inf')
        safe_moves = get_safe_moves(my_head, my_neck, board_width, board_height, my_body, opponents_body)
        for move in safe_moves:
            # ToDo: Get new board state for this move
            my_head, my_body, my_body_lst = update_board_state(move, my_head, my_body, my_body_lst)
            score = minimax(depth+1, "opponent", my_head, my_neck, board_width, board_height, my_body, my_body_lst,
                            opponents_body, opponents_body_lst, opponents_head, opponents_neck)
            best_score = max(best_score, score)
        return best_score

    elif player == "opponent":
        best_score = float('inf')
        safe_moves = get_safe_moves(opponents_head, opponents_neck, board_width, board_height, opponents_body, my_body)
        for move in safe_moves:
            # ToDo: Get new board state for this move
            opponents_head, opponents_body, opponents_body_lst = update_board_state(move, opponents_head,
                                                                                    opponents_body, opponents_body_lst)
            score = minimax(depth+1, "me", my_head, my_neck, board_width, board_height, my_body, my_body_lst,
                            opponents_body,opponents_body_lst, opponents_head, opponents_neck)
            best_score = min(best_score, score)
        return best_score


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    my_head = game_state["you"]["body"][0]
    my_neck = game_state["you"]["body"][1]
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_body = set((part["x"], part["y"]) for part in game_state['you']['body'])
    my_body_lst = [(part["x"], part["y"]) for part in game_state['you']['body']]
    opponents_body = set((part["x"], part["y"]) for opponent in game_state['board']['snakes'] for part in opponent['body'])  # Currently just one opponent
    opponents_body_lst = [(part["x"], part["y"]) for opponent in game_state['board']['snakes'] for part in opponent['body']]
    opponents_head = game_state['board']['snakes'][0]['body'][0]
    opponents_neck = game_state['board']['snakes'][0]['body'][1]

    # Minimax from ChatGPT
    best_move = None
    best_score = float('-inf')
    safe_moves = get_safe_moves(my_head, my_neck, board_width, board_height, my_body, opponents_body)
    for move in safe_moves:
        # ToDo: Get new board state for this move
        my_head, my_body, my_body_lst = update_board_state(move, my_head, my_body, my_body_lst)
        score = minimax(0, "opponent", my_head, my_neck, board_width, board_height, my_body, my_body_lst,
                        opponents_body, opponents_body_lst, opponents_head, opponents_neck)
        if score >= best_score:
            best_score = score
            best_move = move

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = best_move

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
