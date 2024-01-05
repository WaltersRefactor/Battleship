from create_board import create_player_board, display_board
from bot_board import create_bot_board, display_bot_board
from random import choice
import time
import re

def main():
    #  player_board = create_player_board()
    print("---------------Your Board:----------------")
    player_board, player_ships = create_player_board()
    display_board(player_board)
    comp_board, computer_ships = create_bot_board()
    player_board[0][0] = "X"
    player_board[0][1] = "X"
    play(player_board, comp_board, player_ships, computer_ships)


def play(player_board, comp_board, player_ships, computer_ships):
    while True:
        for p in range(2):
            attack(p, player_board, comp_board, player_ships, computer_ships)
            sunk, msg = check_all_sunk(player_ships, computer_ships)
            if sunk:
                print(msg)
                break


def check_all_sunk(player_ships, computer_ships):
    players_sunk = []
    computers_sunk = []
    msg = ""
    for ship in player_ships:
        if player_ships[ship][3] == "sunk":
            players_sunk.append(player_ships[ship][0])
        if len(players_sunk) == 5:
            msg = "Computer sunk all your ships. Computer wins the game!"
            return True, msg

    for ship in computer_ships:
        if computer_ships[ship][3] == "sunk":
            computers_sunk.append(computer_ships[ship][0])
        if len(computers_sunk) == 5:
            msg = "You sunk all the ships. Player wins the game!"
            return True, msg

    return False, msg


def attack(p, player_board, comp_board, player_ships, computer_ships):
    if p == 0:
        print("-------------Computer's Board-------------")
        display_bot_board(comp_board)
        print("Player attacks")
        while True:
            target = input("Choose target location: Example A0 : ").upper()
            if re.fullmatch(r"[A-J][0-9]", target):

                col, row = target[0], target[1]
                h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

                row = int(row)

                # Give col an integer value
                for i in range(len(h)):
                    if col == h[i]:
                        col = i
            else:
                print("Not a valid location")
                continue

            if comp_board[row][col] == "■":
                comp_board[row][col] = "X"
                display_bot_board(comp_board)
                target = (row, col)
                sink, msg = check_sink(p, comp_board, computer_ships, target)
                if sink:
                    print(msg)
                    time.sleep(3)
                    break
                else:
                    print("          ------   Hit   ------")
                    time.sleep(3)
                    break
            elif comp_board[row][col] == "X" or comp_board[row][col] == "0":
                print("You already fired there")
                continue
            else:
                comp_board[row][col] = "0"
                display_bot_board(comp_board)
                print("          ------   Miss   ------")
                time.sleep(3)
                break

    else:
        h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        print("Bot attacks")
        hit, loc = check_hit(player_board, player_ships)
        while True:
            if hit:
                row = loc[0]
                col = loc[1]
                print(f"Bot tries row {row} col {col}")
                time.sleep(3)
            else:
                col = choice(h)
                row = choice(range(10))
            # Give col an integer value
            for i in range(len(h)):
                if col == h[i]:
                    col = i

            if player_board[row][col] == "■":
                player_board[row][col] = "X"
                print("-------------Player's Board-------------")
                display_board(player_board)
                time.sleep(3)
                target = (row, col)
                sink, msg = check_sink(p, player_board, player_ships, target)
                if sink:
                    print(msg)
                    time.sleep(3)
                    break
                else:
                    print("          ------   Hit   ------")
                    time.sleep(3)
                    break
            elif player_board[row][col] == "X" or player_board[row][col] == "0":
                continue
            else:
                player_board[row][col] = "0"
                print("-------------Player's Board-------------")
                display_board(player_board)
                print("          ------   Miss   ------")
                time.sleep(3)
                break


def check_hit(board, ships):
    loc = (0, 0)
    hit_locations = []
    number_ships_hit = 0
    location_ships_hit = []
    for ship in ships:
        if ships[ship][3] == "sunk":
            continue
        else:
            hits = 0
            for loc in ships[ship][2]:
                row = loc[0]
                col = loc[1]
                if board[row][col] == "X":
                    hit_locations.append((row, col))
                    hits += 1
            if hits > 0:
                number_ships_hit += 1
                location_ships_hit.append(ships[ship][2])
                print("Check location_ships_hit", location_ships_hit)

    if hit_locations:
        direction = [-1, 1]
        if len(hit_locations) == 1:
            while True:
                r_d = choice(direction)
                row = hit_locations[0][0]
                col = hit_locations[0][1]
                r_l = choice(["row", "col"])
                board_range = list(range(0, 10))

                if r_l == "row":
                    target = col + r_d
                    if target not in board_range or board[row][col + r_d] == "X" or board[row][col + r_d] == "0":
                        continue
                    else:
                        return True, (row, col + r_d)

                if r_l == "col":
                    target = row + r_d
                    if target not in board_range or board[row + r_d][col] == "X" or board[row + r_d][col] == "0":
                        continue
                    else:
                        return True, (row + r_d, col)
        elif number_ships_hit == 1:
            row_numbers = set()
            col_numbers = set()

            for loc in hit_locations:
                row_numbers.add(loc[0])
                col_numbers.add(loc[1])
            while True:
                if len(col_numbers) == 1:
                    r_d = choice(direction)
                    target_point = choice([hit_locations[0], hit_locations[-1]])
                    target = target_point[0] + r_d
                    col = target_point[1]
                    if target < 0 or target > 9 or board[target][col] == "X" or board[target][col] == "0":
                        continue
                    else:
                        return True, (target, col)

                if len(row_numbers) == 1:
                    r_d = choice(direction)
                    target_point = choice([hit_locations[0], hit_locations[-1]])
                    row = target_point[0]
                    target = target_point[1] + r_d
                    if target < 0 or target > 9 or board[row][target] == "X" or board[row][target] == "0":
                        continue
                    else:
                        return True, (row, target)
        else:
            chosen_ship_locations = choice(location_ships_hit)
            row_numbers = set()
            col_numbers = set()
            new_hit_locations = []
            for loc in chosen_ship_locations:
                if board[loc[0]][loc[1]] == "X":
                    row_numbers.add(loc[0])
                    col_numbers.add(loc[1])
                    new_hit_locations.append(loc)
                    print("Check new_hit_locations", new_hit_locations)

            if len(new_hit_locations) == 1:
                while True:
                    r_d = choice(direction)
                    row = new_hit_locations[0][0]
                    col = new_hit_locations[0][1]
                    r_l = choice(["row", "col"])
                    board_range = list(range(0, 10))

                    if r_l == "row":
                        target = col + r_d
                        if target not in board_range or board[row][col + r_d] == "X" or board[row][col + r_d] == "0":
                            continue
                        else:
                            return True, (row, col + r_d)

                    if r_l == "col":
                        target = row + r_d
                        if target not in board_range or board[row + r_d][col] == "X" or board[row + r_d][col] == "0":
                            continue
                        else:
                            return True, (row + r_d, col)
            else:
                while True:
                    if len(col_numbers) == 1:
                        r_d = choice(direction)
                        target_point = choice([new_hit_locations[0], new_hit_locations[-1]])
                        target = target_point[0] + r_d
                        col = target_point[1]
                        if target < 0 or target > 9 or board[target][col] == "X" or board[target][col] == "0":
                            continue
                        else:
                            return True, (target, col)

                    if len(row_numbers) == 1:
                        r_d = choice(direction)
                        target_point = choice([new_hit_locations[0], new_hit_locations[-1]])
                        row = target_point[0]
                        target = target_point[1] + r_d
                        if target < 0 or target > 9 or board[row][target] == "X" or board[row][target] == "0":
                            continue
                        else:
                            return True, (row, target)

    return False, loc


def check_sink(p, board, ships, target):
    if p == 0:
        player = "Player 1"
    else:
        player = "Computer"
    for ship in ships:
        damage = 0
        # Checks the ship that was attacked
        if target in ships[ship][2]:
            for loc in ships[ship][2]:
                x = loc[0]
                y = loc[1]
                if board[x][y] == "X":
                    damage += 1

            if ships[ship][1] == damage:
                msg = f"{player} sunk the {str(ships[ship][0])}"
                ships[ship][3] = "sunk"
                return True, msg

    return False, ""


if __name__ == "__main__":
    main()
