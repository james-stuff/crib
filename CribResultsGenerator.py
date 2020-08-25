# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:06:38 2020

@author: j_a_c
"""
import csv
import os


class RoundBuilder:
    def __init__(self, first_line):
        self.round_no = int(first_line[-10:-4].lstrip())
        self.pegging, self.hands, self.boxes = ([0, 0] for n in range(3))
        self.all_scores, self.parsed_hands = ([] for n in range(2))
        self.box_owner = ''
        self.pegging_points_index = 0

    def parse_line(self, line):
        if 'the box' in line:
            self.box_owner = line[:line.index(' has')]
        if line[0] == '[':
            self.parsed_hands.append(int(line[-3:]))
            if len(self.parsed_hands) == 3:
                self.allocate_all_points()
        if ':' in line:
            self.pegging_points_index = line[:8] == 'Computer'
            if 'for' in line:
                self.pegging[self.pegging_points_index] += int(line[-3:])
        if 'go' in line or ' for 1\n' in line:
            self.pegging[self.pegging_points_index] += 1

    def allocate_all_points(self):
        self.hands = self.parsed_hands[:2]
        if self.box_owner == 'Comp 1':
            self.hands = self.hands[::-1]
        self.boxes[self.box_owner == 'Computer'] = self.parsed_hands[2]
        self.all_scores = [self.pegging, self.hands, self.boxes]

    def get_totals(self):
        return [self.round_no] + [a[n] for n in range(2) for a in self.all_scores]


our_file = [f for f in os.listdir('.') if 'MonteCarloOutput' in f][0]
version_no = our_file[16:our_file.index('.txt')]

with open(our_file, 'r', encoding='utf-8') as raw_file:
    final_results = []
    for line in raw_file:
        if 'Monte Carlo round' in line:
            current_round = RoundBuilder(line)
        else:
            current_round.parse_line(line)
            if len(current_round.all_scores) == 3:
                final_results.append(current_round.get_totals())
    no_of_rounds = len(final_results)
    final_results.append(['Ave'] + [sum([pts[ind] for pts in final_results]) / 10000
                                    for ind in range(1, 7)])

with open('MonteCarloResults' + version_no + '.csv', 'w', newline='') as csv_file:
    csv_file.writelines(',,PLAYER,,,COMPUTER,\n')
    csv_file.writelines(f'Round,{"Peg, Hand, Box," * 2}\n')
    csvw = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
    csvw.writerows(final_results)