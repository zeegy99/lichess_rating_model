import csv
import numpy as np
import pandas as pd



emoji = "\U0001F60A" #debugging emoji
interval = 50 #how much to change by
start = 800 #starting rating when parsing
file_path = 'earliest_games.clj' #don't change


def read_elo_lines(file_path): #Tester function, not used

    lines = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if line[1:9] == 'WhiteElo' or line[1:9] == 'BlackElo':
                lines.append(line.strip())
            if i >= 20:
                return lines
    return lines


def batch2(file_path, lower_elo, higher_elo): ##Takes input of the filepath, lower elo bound and higher elo bound.
                                              #An h-interval in the form (a, b] and finds all games based off of one players elo.
                                              #Returns info about all of the games including the empty ''. game[-2] is where the notation is.
    count = 0
    full_games = []
    lines = []
    store_game = False  
    
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            lines.append(line.strip())
      
            if line.startswith('[WhiteElo'):
                try:
                    white_elo = int(line.split('"')[1])  
                    if white_elo > lower_elo and white_elo <= higher_elo: 
                        store_game = True  
                    else:
                        store_game = False 
                except ValueError:
                    print(f"Error parsing Elo on line {i}: {line}")
                    store_game = False  

            if line.strip() == "":
                count += 1
                if count % 2 == 0:
         
                    if store_game:
                   
                        full_games.append(lines[:])
                    
                    lines = []
                    store_game = False 
    return full_games




## Filing the games.


for i in range(1, 2):
    filename = f'{start + i*interval}rating.csv'
    lower_rating = start + (i - 1) * interval
    upper_rating = start + i * interval

    under_1000 = batch2(file_path, lower_rating, upper_rating)  # Call to create the games
    #print(f"Number of games in range {lower_rating} to {upper_rating}: {len(under_1000)}")

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Move number', 'White Moves', 'Black Moves'])

        for game in under_1000:
            moves_line = game[-2]  # Assuming the second last line contains the moves
        
            if moves_line:  
                move_list = moves_line.split(' ') 

            
                
                move_number = -1  # Initialize move number, not sure why -1 works but it does. 

                # Process moves in pairs
                for index in range(len(move_list)): 

            
                    if index % 3 == 0:
                        move_number += 1

                    elif index % 3 == 1:
                        white_move = move_list[index]
                    
                    else:
                        black_move = move_list[index]

                    if index % 3 == 0 and index // 3 >= 1:
                        writer.writerow([move_number, white_move, black_move])

                ## Writing down the result
                temp = game[4]

                temp_joined = ''.join(temp)
                print(emoji, temp_joined)

                split_result = temp_joined.split()
                writer.writerow(split_result)
                writer.writerow('')
                ##
       


