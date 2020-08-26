# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:06:38 2020

@author: j_a_c
"""
import csv
import os
import Crib


class ScoreList:
    base_score_categories = ['15', 'pair', 'run']


class HandScoreList(ScoreList):
    def __init__(self):
        super(HandScoreList, self).__init__()
        self.score_dict = {t: 0 for t in ['15', 'run', 'flush', 'pair', 'knob']}


class PeggingScoreList(ScoreList):
    def  __init__(self):
        super(PeggingScoreList, self).__init__()
        categories = self.base_score_categories.copy()
        categories.insert(1, '31')
        categories.append('go')
        self.score_dict = {t: 0 for t in categories}


class RoundBuilder:
    card_dict = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    dict_of_a_kind = {1: 0, 2: 2, 3: 6, 4: 12}

    def __init__(self, first_line):
        self.round_no = int(first_line[-10:-4].lstrip())
        self.pegging, self.hands, self.boxes = ([0, 0] for n in range(3))
        self.hand_lines = []
        self.all_scores, self.parsed_hands = ([] for n in range(2))
        self.box_owner = ''
        self.pegging_points_index = 0
        self.target_dict = None
        self.peg_seq = Crib.PeggingSequence()

    def parse_line(self, line):
        if 'the box' in line:
            self.box_owner = line[:line.index(' ha')]  # old versions say 'You have the box'
        if line[0] == '[':
            self.parsed_hands.append(int(line[-3:]))
            self.hand_lines.append(line)
            if len(self.parsed_hands) == 3:
                self.allocate_all_points()
        if ' : ' in line:
            self.get_card(line)
            self.pegging_points_index = line[:8] == 'Computer'
            self.target_dict = PSL.score_dict if self.pegging_points_index else PLAYER_PSL.score_dict
            if self.peg_seq.fifteen_or_thirty_one_score():
                self.target_dict[str(self.peg_seq.running_total)] += 2
            self.target_dict['run'] += self.peg_seq.run_score()
            self.target_dict['pair'] += self.peg_seq.pairs_score()
            if 'for' in line:
                self.pegging[self.pegging_points_index] += int(line[-3:])
        if 'go' in line or ' for 1\n' in line:
            self.pegging[self.pegging_points_index] += 1
            self.target_dict['go'] += 1

    def get_card(self, raw_line):
        string_card = raw_line[raw_line.index(' : ') + 3:raw_line.index(' : ') + 6].strip()
        suit = string_card[-1]
        raw_rank = string_card[:-1]
        rank = self.card_dict[raw_rank] if raw_rank in self.card_dict else int(raw_rank)
        self.peg_seq.add_card(Crib.Card(rank, suit))

    def allocate_all_points(self):
        self.hands = self.parsed_hands[:2]
        ah_index = 1
        if self.box_owner == 'Comp 1' or self.box_owner == 'You':
            self.hands = self.hands[::-1]
            ah_index = 0
        self.analyse_hands(ah_index)
        self.boxes[self.box_owner == 'Computer'] = self.parsed_hands[2]
        self.all_scores = [self.pegging, self.hands, self.boxes]

    def analyse_hands(self, hand_index):
        score_types = list(HSL.score_dict.keys())
        number_dict = dict(zip(Crib.NUMBERS[:7], range(7)))
        number_dict['one'] = 1
        score_line = self.hand_lines[hand_index].lower()
        score_line = score_line[score_line.index(']') + 1:]
        HSL.score_dict['15'] += score_line.count('fifteen') * 2
        score_words = [sw.strip(',s') if sw[-1] == 's' else sw.strip(',') for sw in score_line.split()]
        for st in score_types[1:]:
            if st in score_words:
                occurrences = length = 1
                ind = score_words.index(st)
                if st != 'knob':
                    occurrences = number_dict[score_words[ind - 1]]
                    length = 2 if st == 'pair' else number_dict[score_words[ind + 2]]
                HSL.score_dict[st] += occurrences * length
        if 'orchard' in score_words:
            HSL.score_dict['pair'] += 4
        # if self.round_no == 3566:
        #     print(f'score types: {score_types}')
        #     print(f'score in words: {[w for w in score_words]}')

    def get_totals(self):
        return [self.round_no] + [a[n] for n in range(2) for a in self.all_scores]


our_file = [f for f in os.listdir('.') if 'MonteCarloOutput' in f][0]
version_no = our_file[16:our_file.index('.txt')]
# our_file = 'Previous versions\\MonteCarloOutput2.1.2.txt'
# version_no = '2.1.2'

PSL = PeggingScoreList()
PLAYER_PSL = PeggingScoreList()
HSL = HandScoreList()

with open(our_file, 'r', encoding='utf-8') as raw_file:
    final_results = []
    current_round = None
    for line in raw_file:
        if 'Monte Carlo round' in line:
            current_round = RoundBuilder(line)
        elif current_round:
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

print(PSL.score_dict)
ref_dict = {'15': 3018, '31': 1724, 'pair': 4706, 'run': 3547, 'go': 8254}
print(f'PSL dictionary still OK? {PSL.score_dict == ref_dict}')
print(f'Player scores: {PLAYER_PSL.score_dict}')
print(f'Hand scores: {HSL.score_dict}')