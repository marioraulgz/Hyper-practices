def board(game):
    print("---------")
    for i in [0, 3, 6]:
        print("|" + " " + game[i] + " " + game[i + 1] + " " + game[i + 2] + " " + "|")
    print("---------")


def game_state(game):
    x_game = 0  # Number of x in the board
    o_game = 0  # Number of o in the board
    ngame = 0  # Number of null in the board

    h_win = 0  # Counters for the type of win (horizonal, vertical, diagonal), they currently have no use other than debugging
    v_win = 0
    d_win = 0
    x_win = 0  # Counter for x wins
    o_win = 0  # Counter for o wins

    for i in game:  # Counters for the plays
        if i in "Xx":
            x_game += 1
        elif i in "Oo":
            o_game += 1
        elif i in "_ ":
            ngame += 1

    if abs(x_game - o_game) > 1:  # Lets see if the difference is bigger than one
        return "Impossible"  # If it is true for this case, then it has no sense to continue
    else:
        for i in range(3):
            if game[i] == game[i + 3] and game[i] == game[i + 6]:  # Vertical winnings
                v_win += 1
                if game[i] in "Xx":
                    x_win += 1
                elif game[i] in "Oo":
                    o_win += 1
        for i in [0, 3, 6]:
            if game[i] == game[i + 1] and game[i] == game[i + 2]:  # Horizontal winnings
                h_win += 1
                if game[i] in "Xx":
                    x_win += 1
                elif game[i] in "Oo":
                    o_win += 1
        for j in [2, 4]:  # Diagonal winnings
            if game[4] == game[4 + j] and game[4] == game[4 - j]:
                d_win += 1
                if game[4] in "Xx":
                    x_win += 1
                elif game[4] in "Oo":
                    o_win += 1
        if (
            x_win >= 1 and o_win >= 1
        ):  # Same as before, if the impossible is true, then it has no sense to move on.
            return "Impossible"
        else:
            if x_win == 1:
                return "X wins"
            elif o_win == 1:
                return "O wins"
            elif x_win == 0 and o_win == 0:
                if ngame == 0:
                    return "Draw"
                else:
                    return "Game not finished"


def n_mapping(coordinates, previous_state):  #We define a function to know which cells in the selected coordenate system have something in them
    mapping = [" " for play in previous_state]
    for i, _ in enumerate(previous_state):
        if previous_state[i] not in "_ ":
            mapping[i] = coordinates[i]
    return mapping


def new_move(coordinates, mapping, previous_state, n_move, player):  #Function to get a new game state based on the previous and a move
    if n_move in coordinates:
        if n_move not in mapping:
            for i, num in enumerate(coordinates):
                if num == n_move:
                    next_state = list(previous_state)
                    if player in "Xx":
                        next_state[i] = "X"
                        return next_state
                    elif player in "Oo":
                        next_state[i] = "O"
                        return next_state
        else:
            print("This cell is occupied! Choose another one!")  #Adding recursion to ensure that the program asks until a valid input is given
            n_move2 = int(input("Enter the coordinates: ").replace(" ", ""))
            return new_move(coordinates, mapping, previous_state, n_move2, player)

    else:
        print("Coordinates should be from 1 to 3!")  #Same as before
        n_move2 = int(input("Enter the coordinates: ").replace(" ", ""))
        return new_move(coordinates, mapping, previous_state, n_move2, player)


def available_space(state):  
    available = [1 if (play not in " _") else 0 for play in state]
    return available


def game(coordinates, first_state):  #Lets gather all the functions into one that actually lets us play the game
    board(first_state)   #Initiate board in the first state
    available = available_space(first_state) 
    previous_state = first_state
    i = 2                   #We begin the counter at 2 to avoid problems in the next if
    while not all(available):
        if i % 2 == 0:      #Apparently X always goes first, so if i is even, the play goes to X
            player = "X"
        else:
            player = "O"
        move = int(input("Enter the coordinates: ").replace(" ", ""))
        mapa = n_mapping(coordinates, previous_state)
        n_state = new_move(coordinates, mapa, previous_state, move, player)
        board(n_state)
        available = available_space(n_state)
        previous_state = n_state
        i += 1
        if game_state(n_state) != "Game not finished":      #If the game is not finished, it continues the loop 
            break
    print(game_state(n_state))                  #If it broke the loop, it means we have a result


blank_board = [" " for i in range(9)]  #Defining our blank slate
cartesian_coord = [13, 23, 33, 12, 22, 32, 11, 21, 31]  #Given coordinate system

game(cartesian_coord, blank_board)      #Lets play!

