# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:06:38 2020

@author: j_a_c
"""
import csv
import os

PLAYER_PEGGING = 1
PLAYER_HAND = 2
PLAYER_BOX = 3
COMPUTER_PEGGING = 4
COMPUTER_HAND = 5
COMPUTER_BOX = 6

possible_files = os.listdir()
our_file = ''
for f in possible_files:
    if 'MonteCarloOutput' in f:
        our_file = f
        version_no = f[16:f.index('.txt')]
        break

with open(our_file, 'r', encoding='utf-8') as raw_file:
    hands_counted = 0
    final_results = []
    round_no = -1
    scores = []
    for line in raw_file:
        if 'Monte Carlo round' in line:
#            print('Scores for round', round_no, ':', scores)
            round_no = int(line[-10:-4].lstrip())
            scores = [round_no] + 6 * [0]
            hands_counted = 0
        elif 'the box' in line:
            player_has_box = 'Comp 1 has' in line
        elif line[:8] == 'Computer' and ':' in line:
            players_turn = False
            scores_index = COMPUTER_PEGGING
        elif line[:8] == 'Comp 1 :':
            players_turn = True
            scores_index = PLAYER_PEGGING
            
        if len(scores) > 0:
            if 'for' in line and '[' not in line and '.' not in line and 'go' not in line and '!' not in line[-2:]:
                pegging_score_increment = int(line[-3:])
                scores[scores_index] += pegging_score_increment
            elif 'go' in line:
                scores[scores_index] += 1
            elif line[0] == '[':
                hands_counted += 1
                if hands_counted == 1:
                    if player_has_box:
                        scores_index = COMPUTER_HAND
                    else:
                        scores_index = PLAYER_HAND
                if hands_counted == 2:
                    if player_has_box:
                        scores_index = PLAYER_HAND
                    else:
                        scores_index = COMPUTER_HAND
                if hands_counted == 3:
                    if player_has_box:
                        scores_index = PLAYER_BOX
                    else:
                        scores_index = COMPUTER_BOX
                hand_score_increment = int(line[-3:])
                scores[scores_index] = hand_score_increment
                
                if hands_counted == 3 and round_no >= 0:
                    final_results.append(scores)

with open('MonteCarloResults' + version_no + '.csv', 'w', newline='') as csv_file:
    csv_file.writelines(',,PLAYER,,,COMPUTER,\n')
    csv_file.writelines('Round,' + 'Peg, Hand, Box,' * 2 + '\n')
    csvw = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
    csvw.writerows(final_results)
    
    # write averages:
    averages = []
    for s in range(7):
        if s == 0:
            averages.append('Ave')
        else:
            tot = 0
            for res in final_results:
                tot += res[s]
            averages.append(tot / (round_no + 1))
    csvw.writerow(averages)