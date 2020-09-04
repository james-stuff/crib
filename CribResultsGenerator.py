# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:06:38 2020

@author: j_a_c
"""
import csv
import Crib
import re


PLAYER = PEG = 0
COMPUTER = HAND = 1
BOX = 2


class ScoreList:
    base_score_categories = ['15', 'pair', 'run']


class HandScoreList(ScoreList):
    def __init__(self):
        super(HandScoreList, self).__init__()
        self.score_dict = {t: 0 for t in ['15', 'run', 'flush', 'pair', 'knob']}


class PeggingScoreList(ScoreList):
    def __init__(self):
        super(PeggingScoreList, self).__init__()
        categories = self.base_score_categories.copy()
        categories.insert(1, '31')
        categories.append('go')
        self.score_dict = {t: 0 for t in categories}


class RoundSearchable:
    def __init__(self, first_line, bd_dicts):
        self.round_no = int(first_line[-10:-4].lstrip())
        self.hands_seen = 0
        self.all_text = ''

    def parse_line(self, whole_line):
        self.all_text += whole_line
        if whole_line[0] == '[':
            self.hands_seen += 1

    def get_hand_points_breakdown(self, hand_line, pl_ind, hd_type):
        pass

    def get_pegging_points_breakdown(self, peg_line):
        pass

    def add_go_point(self):
        pass


class RoundAnalyst(RoundSearchable):
    card_dict = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    dict_of_a_kind = {1: 0, 2: 2, 3: 6, 4: 12}

    def __init__(self, first_line, bd_dicts):
        super(RoundAnalyst, self).__init__(first_line, bd_dicts)
        self.box_owner = ''
        self.last_scorer_index = 0
        self.peg_dict = None
        self.peg_seq = Crib.PeggingSequence()
        self.player_lookup = {'Computer': COMPUTER}
        self.round_scores = [[0 for m in range(3)] for n in range(2)]
        self.bd_dicts = bd_dicts

    def parse_line(self, whole_line):
        if 'the box' in whole_line:
            self.determine_player_sequence(whole_line)
        if ' : ' in whole_line:
            self.handle_pegging_card(whole_line)
        if 'go' in whole_line or ' for 1\n' in whole_line:
            self.add_go_point()
        if whole_line[0] == '[':
            self.score_hand(whole_line)

    def determine_player_sequence(self, box_line):
        self.box_owner = box_line[:box_line.index(' ha')]  # old versions say 'You have the box'
        self.add_player_to_lookup_if_needed(self.box_owner)

    def add_player_to_lookup_if_needed(self, player_id):
        if player_id not in self.player_lookup:
            self.player_lookup[player_id] = PLAYER

    def handle_pegging_card(self, raw_line):
        player = raw_line[:raw_line.index(':')].strip()
        self.add_player_to_lookup_if_needed(player)
        self.last_scorer_index = self.player_lookup[player]
        if 'for' in raw_line:
            self.round_scores[self.player_lookup[player]][PEG] += int(raw_line[-3:])
        self.get_pegging_points_breakdown(raw_line)

    def get_card_from_pegging_line(self, peg_line):
        colon_pos = peg_line.index(' : ')
        string_card = peg_line[colon_pos + 3:colon_pos + 6].strip()
        suit = string_card[-1]
        raw_rank = string_card[:-1]
        rank = self.card_dict[raw_rank] if raw_rank in self.card_dict else int(raw_rank)
        return Crib.Card(rank, suit)

    def add_go_point(self):
        self.round_scores[self.last_scorer_index][PEG] += 1
        self.peg_dict['go'] += 1

    def score_hand(self, hand_line):
        self.hands_seen += 1
        player_index = self.player_lookup[self.box_owner] if self.hands_seen > 1 else \
            [v for k, v in self.player_lookup.items() if k != self.box_owner][0]
        hand_type = HAND if self.hands_seen < 3 else BOX
        self.round_scores[player_index][hand_type] = int(hand_line[-3:])
        self.get_hand_points_breakdown(hand_line, player_index, hand_type)

    def get_pegging_points_breakdown(self, peg_line):
        self.peg_seq.add_card(self.get_card_from_pegging_line(peg_line))
        self.peg_dict = self.bd_dicts[self.last_scorer_index][PEG].score_dict
        if self.peg_seq.fifteen_or_thirty_one_score():
            self.peg_dict[str(self.peg_seq.running_total)] += 2
        self.peg_dict['run'] += self.peg_seq.run_score()
        self.peg_dict['pair'] += self.peg_seq.pairs_score()

    def get_hand_points_breakdown(self, hand_line, pl_ind, hd_type):
        score_types = list(HandScoreList().score_dict.keys())
        number_dict = dict(zip(Crib.NUMBERS[:7], range(7)))
        number_dict['one'] = 1
        score_line = hand_line.lower()
        score_line = score_line[score_line.index(']') + 1:]
        self.bd_dicts[pl_ind][hd_type].score_dict['15'] += score_line.count('fifteen') * 2
        score_words = [sw.strip(',s') if sw[-1] == 's' else sw.strip(',') for sw in score_line.split()]
        for st in score_types[1:]:
            if st in score_words:
                occurrences = length = 1
                ind = score_words.index(st)
                if st != 'knob':
                    occurrences = number_dict[score_words[ind - 1]]
                    length = 2 if st == 'pair' else number_dict[score_words[ind + 2]]
                self.bd_dicts[pl_ind][hd_type].score_dict[st] += occurrences * length
        if 'orchard' in score_words:
            self.bd_dicts[pl_ind][hd_type].score_dict['pair'] += 4

    def get_totals(self):
        return [self.round_no] + [sc for pl in self.round_scores for sc in pl]


class CRG:
    def __init__(self, version=''):
        self.version = version
        if not self.version:
            self.version = Crib.VERSION
        self.filename = f'MonteCarloOutput{self.version}.txt'
        self.file = open(self.filename, 'r', encoding='utf-8')
        self.breakdown_dicts = [[PeggingScoreList(), HandScoreList(), HandScoreList()]
                                for n in range(2)]

    def generate(self):
        check_file = open(self.filename, 'r', encoding='utf-8')
        csv_vals = []
        current_round = None
        for line in self.file:
            if 'Monte Carlo round' in line:
                current_round = RoundAnalyst(line, self.breakdown_dicts)
            elif current_round:
                current_round.parse_line(line)
                if current_round.hands_seen == 3:
                    csv_vals.append(current_round.get_totals())
        csv_vals.append(['Ave'] + [sum([pts[ind] for pts in csv_vals]) / len(csv_vals)
                                   for ind in range(1, 7)])
        self.file.close()
        csv_vals += self.extract_score_breakdowns()
        self.write_csv(csv_vals)

    def extract_score_breakdowns(self):
        bd_lines = ['']
        all_score_types = ['15', '31', 'go', 'run', 'flush', 'pair', 'knob']
        for st in all_score_types:
            new_line = [st]
            for pl in self.breakdown_dicts:
                for score_list in pl:
                    if st in score_list.score_dict:
                        new_line.append(score_list.score_dict[st])
                    else:
                        new_line.append('')
            bd_lines.append(new_line)
        totals = [sum([bd[n] for bd in bd_lines[1:] if isinstance(bd[n], int)])
                  for n in range(1, 7)]
        bd_lines.append(['Totals'] + totals)
        return bd_lines


    def write_csv(self, values):
        with open('MonteCarloResults' + self.version + '.csv', 'w', newline='') as csv_file:
            csv_file.writelines(',,PLAYER,,,COMPUTER,\n')
            csv_file.writelines(f'Round,{"Peg, Hand, Box," * 2}\n')
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerows(values)

    def search_for_regex(self, regex):
        matching_rounds = []
        instances = 0
        current_round = None
        for line in self.file:
            if 'Monte Carlo round' in line:
                current_round = RoundSearchable(line, self.breakdown_dicts)
            elif current_round:
                current_round.parse_line(line)
                if current_round.hands_seen == 3:
                    result = re.search(regex, current_round.all_text)
                    # TODO: only finds first instance in Round - change to finditer()?
                    # currently, it is actually answering the question 'How many rounds
                    # have a <regex>?'
                    if result:
                        instances += 1
                        if instances < 6:
                            matching_rounds.append((current_round.round_no, result.start()))
        self.file.close()
        print(f'\n"{regex}" was found {instances} time{"" if instances == 1 else "s"}'
              f' in {self.filename}')
        if instances:
            print(f' . . . including:')
            for m in matching_rounds:
                print(f'Round {m[0]}, position {m[1]}')
        return instances



if __name__ == '__main__':
    CRG(version='2.1.8').generate()
