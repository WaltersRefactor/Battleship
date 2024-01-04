import re
from random import choice


headings = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def create_bot_board():
    # 10 x 10 starting board
    board = [
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"]
    ]
    ships = {
        "A": ["Carrier", 5, [], "float"],
        "B": ["Battleship", 4, [], "float"],
        "C": ["Destroyer", 3, [], "float"],
        "D": ["Submarine", 3, [], "float"],
        "E": ["Patrol_boat", 2, [], "float"]
    }

    pick_ship(board, ships)
    return board, ships


# Change to just display X for hits
def display_bot_board(eb):
    # print headings
    for i in range(10):
        if i == 0:
            print("    " + str(headings[i]) + " ", end="")
        elif i == 9:
            print("  " + str(headings[i]) + " ")
        else:
            print("  " + str(headings[i]) + " ", end="")

    # print empty board
    for row in range(len(eb)):
        print(str(row) + " | ", end="")
        for i in range(10):
            if i == 9:
                if eb[row][i] == "■":
                    print("_" + " | ")
                else:
                    print(str(eb[row][i]) + " | ")
            else:
                if eb[row][i] == "■":
                    print("_" + " | ", end="")
                else:
                    print(str(eb[row][i]) + " | ", end="")


def pick_ship(eb, ships):
    picked = []
    not_picked = []

    # Create ships not placed
    for ship in ships:
        not_picked.append(ship)

    while not_picked:
        # Random ship choice
        ship = choice(not_picked)

        if ship not in picked and ship in not_picked:
            not_picked.remove(ship)
            picked.append(ship)

            choose_location(eb, ships, ship)

        else:
            continue


def choose_location(eb, ships, ship):
    ship_placed = False
    while not ship_placed:
        #  Random horizontal or vertical
        hv_pos = choice(["h", "v"])
        if hv_pos == "h" or hv_pos == "v":
            # Random placement
            y = choice(headings)
            x = choice(range(10))
            s_pos = f"{y},{x}"
            if re.fullmatch(r"[A-J],[0-9]", s_pos):
                s_pos = (s_pos[0], s_pos[2])

                # Checks for valid placement
                valid = check_valid(eb, ships, ship, hv_pos, s_pos)
                if valid == "placed":
                    ship_placed = True
                elif valid == "outside":
                    continue
                else:
                    continue
            else:
                continue
        else:
            continue


def check_valid(eb, ships, ship, hv_pos, s_pos):
    h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    col, row = s_pos
    row = int(row)

    # Give x an integer value
    for i in range(len(h)):
        if col == h[i]:
            col = i

    ship_length = ships[ship][1]

    if hv_pos == "h":
        # Check for valid horizontal placement
        for i in range(ship_length):
            try:
                if eb[row][col + i] != "_":
                    return False
            except IndexError:
                return "outside"

        # If it does not return false, place the ship
        for i in range(ship_length):
            eb[row][col+i] = "■"
            ships[ship][2].append((row, col + i))

    if hv_pos == "v":
        # Check for valid vertical placement
        for i in range(ship_length):
            try:
                if eb[row + i][col] != "_":
                    return False
            except IndexError:
                return "outside"

        # If it does not return false, place the ship
        for i in range(ship_length):
            eb[row + i][col] = "■"
            ships[ship][2].append((row + i, col))

    return "placed"
