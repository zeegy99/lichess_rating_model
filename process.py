import csv
import numpy as np
import pandas as pd



def read_elo_lines(file_path):

    lines = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if line[1:9] == 'WhiteElo' or line[1:9] == 'BlackElo':
                lines.append(line.strip())
            if i >= 20:
                return lines
    return lines

emoji = "\U0001F60A"


def batch2(file_path, lower_elo, higher_elo):
    count = 0
    full_games = []
    lines = []
    store_game = False  # Flag to track if we should store the game
    
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            lines.append(line.strip())
            
            # Check if the line contains WhiteElo
            if line.startswith('[WhiteElo'):
                try:
                    white_elo = int(line.split('"')[1])  # Extract Elo from between quotes
                    # Check if the Elo is less than 1000
                    if white_elo > lower_elo and white_elo <= higher_elo: #h-interval's xd
                        store_game = True  # Set flag to store this game
                    else:
                        store_game = False  # Don't store the game if Elo >= 1000
                except ValueError:
                    print(f"Error parsing Elo on line {i}: {line}")
                    store_game = False  # Skip game if we can't parse Elo

            # End of a game detected by empty line
            if line.strip() == "":
                count += 1
                if count % 2 == 0:
                    # Store the game only if the flag is set
                    if store_game:
                        print(lines, emoji)
                        #print(emoji, full_games)
                        full_games.append(lines[:])
                       # print(f"Appended game {emoji}: {lines}")
                    # Reset for next game
                    lines = []
                    store_game = False  # Reset store_game flag for the next game
            
            

    print(full_games, emoji)
    return full_games

interval = 50
start = 800
file_path = 'earliest_games.clj'


##Store rating in csv file


for i in range(0, 5):
    filename = f'{start + i*interval}rating.csv'
    lower_rating = start + (i - 1) * interval
    upper_rating = start + i * interval

    under_1000 = batch2(file_path, lower_rating, upper_rating)  # Call to create the games
    print(f"Number of games in range {lower_rating} to {upper_rating}: {len(under_1000)}")

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Move number', 'White Moves', 'Black Moves'])

        for game in under_1000:
            moves_line = game[-2]  # Assuming the second last line contains the moves
            print(emoji, moves_line)
            if moves_line:  # Ensure moves are present
                move_list = moves_line.split(' ')  # Split the moves by space

                print('this is move list', move_list)
                
                move_number = -1  # Initialize move number

                # Process moves in pairs
                for index in range(0, len(move_list)): #I chatgpt'd this, changed range to 1 to adjust indexes xd

                    #print(move_list[index], index)
                    if index % 3 == 0:
                        move_number += 1

                    elif index % 3 == 1:
                        white_move = move_list[index]
                    
                    else:
                        black_move = move_list[index]

                    if index % 3 == 0 and index // 3 >= 1:
                        writer.writerow([move_number, white_move, black_move])
                writer.writerow(game[4])
                writer.writerow('')
                    #print(index)
                    # white_move = move_list[index] if index < len(move_list) else ''
                    # #print(white_move)
                    # black_move = move_list[index + 1] if index + 1 < len(move_list) else ''
                    
                    # # Remove trailing dot from white move if it has one
                    # if white_move.endswith('.'):
                    #     white_move = white_move[:-1]

                    # writer.writerow([move_number, white_move, black_move])
                    # move_number += 1  # Increment move number for the next pair


