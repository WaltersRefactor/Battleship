import re

headings = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def create_player_board():
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
    display_board(board)
    pick_ship(board, ships)
    return board, ships


def display_board(eb):
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
                print(str(eb[row][i]) + " | ")
            else:
                print(str(eb[row][i]) + " | ", end="")


def pick_ship(eb, ships):
    not_picked = []

    # Create ships not placed
    for ship in ships:
        not_picked.append(ship)

    while not_picked:
        if len(not_picked) == 1:
            choose_location(eb, ships, not_picked[0])
            not_picked.pop()
        else:
            print("Available ships: ")
            for ship in not_picked:
                print(f"{str(ship)}) {ships[ship][0]}, {ships[ship][1]} spaces")

            avail_ships = " ".join(s for s in not_picked)
            ship = input(f"Pick a ship to place {avail_ships}: ").upper()

            if ship in not_picked:
                not_picked.remove(ship)
                choose_location(eb, ships, ship)

            else:
                print("That is not an available ship")
                continue


def choose_location(eb, ships, ship):
    ship_placed = False
    while not ship_placed:
        #  Choose horizontal or vertical
        hv_pos = input(f"Will your {ships[ship][0]} be (h)horizontal or (v)vertical?:").lower()
        if hv_pos == "h" or hv_pos == "v":
            s_pos = input("Choose starting location: Example A,0: ").upper()
            if re.fullmatch(r"[A-J],[0-9]", s_pos):
                s_pos = (s_pos[0], s_pos[2])

                # Checks for valid placement
                valid = check_valid(eb, ships, ship, hv_pos, s_pos)
                if valid == "placed":
                    ship_placed = True
                    display_board(eb)
                    print("Ship placed")
                elif valid == "outside":
                    print("Outside the game board")
                    continue
                else:
                    print("A ship is already in that location. Try a new placement.")
                    continue
            else:
                print("Not a valid location. Choose a new location")
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
