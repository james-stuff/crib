# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 20:22:44 2020

@author: j_a_c
"""
import Crib
import os

run_instances = 0
flush_instances = 0

def string_to_card(card_str):
    picdic = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    card_str = card_str.rstrip()
    suit = card_str[-1]
    card_num = card_str[:-1]
    rank = 0
    if card_num in picdic:
        rank = picdic[card_num]
    else:
        rank = int(card_num)
        
    return Crib.Card(rank, suit)
        
def analyse_hand(text):
    results = []
    things_to_look_for = ['run', 'runs', 'flush', 'pair', 'pairs', 'knob']
    number_dict = {'a': 1, 'one': 1, 'two': 2, 'three': 3, 'three,': 3, 
                   'four': 4, 'four,': 4, 'five': 5, 'five,': 5, 'six': 6}
    
    start_of_desc = text.index(']') + 1
    text = text[start_of_desc:].lower()
        
    fifteens_in_hand = text.count('fifteen')
    results.append(fifteens_in_hand * 2)

    split_text = text.split()
    
    for th in things_to_look_for:
        item_score = 0
        if th in split_text:
            index_in_text = split_text.index(th)
            no_of_occurrences = 1
            length = 1
            if th != 'knob':
                no_of_occurrences = number_dict[split_text[index_in_text - 1]]
            if th in things_to_look_for[:3]:
                length = number_dict[split_text[index_in_text + 2]]
            elif 'pair' in th:
                length = 2
            item_score = no_of_occurrences * length

        results.append(item_score)
        
    if 'orchard' in split_text:
        results[5] = 4
        
    # runs:
    run_agg = results[1] + results[2]
    results[1] = run_agg
    del results[2]
    
    # pairs:
    pair_agg = results[3] + results[4]
    results[3] = pair_agg
    del results[4]
    
    return results
            
version_to_look_at = input('Type the version whose results you want to analyse: (n.n.n):')
#version_to_look_at = 'today'

os.chdir('Previous versions')
file_to_open = 'MonteCarloOutput' + version_to_look_at + '.txt'
with open(file_to_open, 'r', encoding='utf-8') as raw_file:
    
    fifteens = 0
    thirty_ones = 0
    pairs = 0
    runs = 0
    pure_go_points = 0
    scoring_instances = 0
    card_plays = []
    round_no = -1
    recording_data = False
    last_scoring_line = ''
    hand_and_box_raw_data = []
    players_box = False
    hand_totals = [0] * 5
    box_totals = [0] * 5
    morgans_orchard_total = [0, 0]
    for line in raw_file:
        if 'Monte' in line:
            round_no = int(line[22:28])
#            if round_no > 9900:
#                print('round:', round_no)
            
        if 'the box' in line:
            players_box = line[:3] == 'You'
            
        if '[' in line and round_no > -1:
            hand_and_box_raw_data.append(line)
            
        if len(line) > 9 and line[9] == ':' and round_no > -1:# and round_no == 150:
            recording_data = True
        if recording_data:
            if 'too high' not in line:  # only applicable before v2.0.9 refactoring 
                card_plays.append(line)
        if len(card_plays) == 10:
            for ind, cp in enumerate(card_plays):
                if 'Computer' in cp and ':' in cp and 'for' in cp:
                    line_score = int(cp[-3:-1])
                    scoring_instances += 1
#                    print('line score:', line_score)
                    if '!' in cp and 'Bob' not in cp:
                        thirty_ones += 2
                        line_score -= 2
                    elif '15 for' in cp:
                        fifteens += 2
                        line_score -= 2
                    
                    if line_score > 1 and ' go is ' not in cp:
                        this_card = string_to_card(cp[11:14])
                        previous_card = string_to_card(card_plays[ind - 1][11:14])
                        if this_card.rank == previous_card.rank:
                            pairs += line_score
                        else:
                            runs += line_score
                if 'for 1' in cp or 'go is' in cp:
                    lines_back = 0
                    while 'go is' in card_plays[ind - lines_back] or ':' not in card_plays[ind - lines_back]:
                        lines_back += 1
                        last_scoring_line = card_plays[ind - lines_back]
                    if 'Computer' in last_scoring_line:
                        pure_go_points += 1
                        
#            for cp in card_plays:
#                print(cp)
                        
            card_plays.clear()
            recording_data = False
                       
        if len(hand_and_box_raw_data) == 3:
#            print('Round', round_no, 10 * '-')
            if players_box:
                hand_index = 0
            else:
                hand_index = 1
            
#            print('computer hand:', hand_and_box_raw_data[hand_index][:17])
            hand_data = analyse_hand(hand_and_box_raw_data[hand_index])
#            if 'run' in hand_and_box_raw_data[hand_index]:
#                run_instances += 1
#            if 'flush' in hand_and_box_raw_data[hand_index]:
#                flush_instances += 1
            if 'Morgan' in hand_and_box_raw_data[hand_index]:
                morgans_orchard_total[0] += 4
            for ind, sc in enumerate(hand_data):
                hand_totals[ind] += sc
            if not players_box:
#                print('Computer box:')
                box_data = analyse_hand(hand_and_box_raw_data[2])
                if 'Morgan' in hand_and_box_raw_data[2]:
                    morgans_orchard_total[1] += 4
#                if 'run' in hand_and_box_raw_data[2]:
#                    run_instances += 1
#                if 'flush' in hand_and_box_raw_data[2]:
#                    flush_instances += 1
                for b_ind, scr in enumerate(box_data):
                    box_totals[b_ind] += scr
            hand_and_box_raw_data = []
                
total_score = fifteens + thirty_ones + pairs + runs + pure_go_points

print('Version:', version_to_look_at)
print('PEGGING TOTALS')
print('15s:\t', fifteens)
print('31s:\t', thirty_ones)
print('pairs:\t', pairs)
print('runs:\t', runs)
print('goes: ', pure_go_points)
print('Total:\t', total_score)
print('Inst:\t', scoring_instances, 'scoring instances')
print('HAND TOTALS')
print('15s:\t', hand_totals[0])
print('Runs:\t', hand_totals[1])
print('Flush:\t', hand_totals[2])
print('Pairs:\t', hand_totals[3])
print('Knobs:\t', hand_totals[4])
print('BOX TOTALS')
print('15s:\t', box_totals[0])
print('Runs:\t', box_totals[1])
print('Flush:\t', box_totals[2])
print('Pairs:\t', box_totals[3])
print('Knobs:\t', box_totals[4])
#print('Run instances:', run_instances, 'Flush instances:', flush_instances)
print('Morgan\'s Orchard total:', morgans_orchard_total)