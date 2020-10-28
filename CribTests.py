# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:57:50 2019

@author: j_a_c
"""

import Crib
import unittest
import tkinter
from Crib import Card as cc
import re
from CribResultsGenerator import CRG
from random import shuffle


HEARTS = '\u2665'
CLUBS = '\u2663'
DIAMONDS = '\u2666'
SPADES = Crib.SPADES#'\u2660'

class CribTest(unittest.TestCase):
    
    def testFifteenTwo(self):
        h = Crib.Hand([cc(5, HEARTS), cc(10, SPADES)])
        score = Crib.HandScore(h)
        self.assertEqual(2, score.points_value)
        print('\n', score)
        
    def testFifteenEight(self):
        h = Crib.Hand([cc(5, HEARTS), cc(10, SPADES), cc(5, DIAMONDS), cc(10, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(12, score.points_value)
        print('\n', score)
        
    def testLongFifteen(self):
        h = Crib.Hand([cc(1, HEARTS), cc(12, SPADES), cc(2, DIAMONDS), cc(2, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(4, score.points_value)
        print('\n', score)
        
    def testLongFifteensInTheBox(self):
        h = Crib.Hand([cc(1, CLUBS), cc(9, SPADES), cc(3, HEARTS), cc(2, DIAMONDS), cc(2, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(12, score.points_value)
        print('\n', score)
        
    def testTripletFifteen(self):
        h = Crib.Hand([cc(1, HEARTS), cc(13, SPADES), cc(2, DIAMONDS), cc(4, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(2, score.points_value)
        print('\n', score)
               
    def testFlushInHand(self):
        h = Crib.Hand([cc(13, CLUBS), cc(12, CLUBS), cc(6, CLUBS), cc(2, DIAMONDS)])
        score = Crib.HandScore(h)
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testNotAFlushInHand(self):
        h = Crib.Hand([cc(13, CLUBS), cc(12, CLUBS), cc(2, DIAMONDS), cc(4, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(0, score.points_value)
        print('\n', score)

    def testMultiplePairs(self):
        h = Crib.Hand([cc(12, CLUBS), cc(6, HEARTS), cc(12, DIAMONDS), cc(12, HEARTS),
                       cc(6, DIAMONDS), cc(12, SPADES), cc(6, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(18, score.points_value)
        print('\n', score)
        
    def testBlotchy(self):
        h = Crib.Hand([cc(6, HEARTS), cc(4, SPADES), cc(8, DIAMONDS), cc(2, CLUBS)])
        score = Crib.HandScore(h)
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testMegaRuns(self):
        h = Crib.Hand([cc(9, HEARTS), cc(4, SPADES), cc(10, DIAMONDS), cc(11, CLUBS),
                       cc(12, DIAMONDS), cc(10, HEARTS), cc(11, CLUBS), cc(3, SPADES)])
        score = Crib.HandScore(h)
        self.assertEqual(20, score.points_value)
        print('\n', score)
        
    def testPegs(self):
        row = Crib.PegRow(tkinter.Label())
        expected = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19]
        for n in range(len(expected)):
            self.assertEqual(row.calc_peg_pos(n + 1), expected[n])
            
    def testFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, CLUBS), cc(6, CLUBS), cc(12, CLUBS)])
        score = Crib.HandScore(hand, cc(13, CLUBS))
        self.assertEqual(5, score.points_value)
        print('\n', score)
        
    def testNotAFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, CLUBS), cc(6, CLUBS), cc(12, CLUBS)])
        score = Crib.HandScore(hand, cc(13, HEARTS))
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testDefinitelyNotAFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, SPADES), cc(6, CLUBS), cc(12, CLUBS)])
        score = Crib.HandScore(hand, cc(13, CLUBS))
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testRunsInPegging(self):
        played_cards = [cc(2, CLUBS), cc(3, HEARTS), cc(4, DIAMONDS)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in played_cards]
        self.assertEqual(3, ps.run_score())
        
    def testComplexRunInPegging(self):
        played_cards = [cc(10, CLUBS), cc(3, HEARTS), cc(5, DIAMONDS), cc(6, CLUBS), cc(4, SPADES)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in played_cards]
        self.assertEqual(4, ps.run_score())
        
    def testShouldntBeARun(self):   
        played_cards = [cc(9, DIAMONDS), cc(11, HEARTS), cc(11, DIAMONDS)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in played_cards]
        self.assertEqual(0, ps.run_score())
        
    def testTwentyNine(self):
        hand = Crib.Hand([cc(11, CLUBS), cc(5, DIAMONDS), cc(5, HEARTS), cc(5, SPADES)])
        score = Crib.HandScore(hand, cc(5, CLUBS))
        self.assertEqual(29, score.points_value)
        print('\n', score)
        
    def testThreeCardsForHandScore(self):
        hand = Crib.Hand([cc(7, HEARTS), cc(7, SPADES), cc(8, DIAMONDS)])
        score = Crib.HandScore(hand)
        self.assertEqual(6, score.points_value)
        print('\n', score)
        
    def testThreeCardsLongFifteen(self):
        hand = Crib.Hand([cc(6, HEARTS), cc(7, SPADES), cc(2, DIAMONDS)])
        score = Crib.HandScore(hand)
        self.assertEqual(2, score.points_value)
        print('\n', score)
        
    def testThreeCardsKnobCheck(self):
        # shouldn't give one for his knob
        hand = Crib.Hand([cc(11, HEARTS), cc(7, SPADES), cc(2, HEARTS)])
        score = Crib.HandScore(hand)
        self.assertEqual(0, score.points_value)
        print('\n', score)

    def testThreeCardsFlush(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(6, HEARTS), cc(13, HEARTS)])
        score = Crib.HandScore(hand)
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testHowManyPairsInFiveCards(self):
        hand = Crib.Hand([cc(7, SPADES), cc(7, HEARTS), cc(7, SPADES), cc(7, SPADES)])
        score = Crib.HandScore(hand, cc(7, SPADES))
        self.assertEqual(20, score.points_value)
        print('\n', score)
        
    def testRunsSimple(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS)])
        score = Crib.HandScore(hand, cc(3, CLUBS))
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testTwoRunsOfFour(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)])
        score = Crib.HandScore(hand, cc(9, DIAMONDS))
        self.assertEqual(10, score.points_value)
        print('\n', score)
        
    def testNoRuns(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(7, HEARTS), cc(3, CLUBS)])
        score = Crib.HandScore(hand)
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def test_box_creation(self):
        p_cards = [cc(6, CLUBS), cc(5, DIAMONDS), cc(5, HEARTS), cc(5, SPADES), cc(5, CLUBS)]
        c_cards = [cc(11, CLUBS), cc(10, DIAMONDS), cc(12, HEARTS), cc(13, SPADES), cc(11, CLUBS)]
        player, computer = Crib.ComputerPlayer('P'), Crib.ComputerPlayer('C')
        crib_round = Crib.Round([player, computer], game=None)
        crib_round.interface.update_score_info('=== testBoxCreation ===')
        player.receive_cards(p_cards)
        computer.receive_cards(c_cards)
        crib_round.play_round()
        print('=' * 23)
        
    def test_dozen_in_pairs_pegging(self):
        player = Crib.ComputerPlayer(name='Dummy player')
        computer = Crib.ComputerPlayer()
        player_hand = [cc(2, CLUBS), cc(2, DIAMONDS), cc(5, SPADES), cc(1, HEARTS), cc(6, CLUBS)]
        comp_hand = [cc(12, CLUBS), cc(2, SPADES), cc(2, HEARTS), cc(1, CLUBS), cc(9, DIAMONDS)]
        crib_round = Crib.Round([player, computer], game=None)
        crib_round.interface.update_score_info('=== testDozenInPairsPegging ===')
        player.receive_cards(player_hand)
        computer.receive_cards(comp_hand)
        crib_round.play_round()
        print('=' * 23)
        
    def testPegRow01_Init(self):
        pr = Crib.PegRow('not used')
        self.assertEqual(pr.full_peg_row[:9], '\u2022' + ' ¦.....¦')
        
    def testPegRow02_FirstPoint(self):
        pr = Crib.PegRow('blah')
        pr.increment_by(1)
        self.assertEqual(pr.full_peg_row[:9], '\u2022' + ' ¦' + '\u2022' + '....¦')
        
    def testPegRow03_MidGamePoints(self):
        pr = Crib.PegRow('')
        pr.increment_by(2)
        pr.increment_by(4)
        self.assertEqual(pr.full_peg_row[:12], '  ¦.' + '\u2022' + '...¦' + '\u2022' + '..')
        
    def testPegRow04_WinningPoints(self):
        pr = Crib.PegRow('')
        pr.increment_by(119)
        pr.increment_by(6)
        self.assertEqual(pr.full_peg_row[141:], '...' + '\u2022' + '.¦ ' + '\u2022' + ' 125')
        
    def test_hand_score(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)])
        hs = Crib.HandScore(hand, cc(9, DIAMONDS))
        print('\n', hs)
        self.assertEqual(10, hs.points_value)

    def test_hand_score_fifteens(self):
        hand = Crib.Hand([cc(5, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)])
        hs = Crib.HandScore(hand, cc(5, DIAMONDS))
        print('\n', hs)
        self.assertEqual(17, hs.points_value)

    def test_hand_score_fifteens_and_nothing_else(self):
        hand = Crib.Hand([cc(5, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(13, CLUBS)])
        hs = Crib.HandScore(hand, cc(2, DIAMONDS))
        print('\n', hs)
        self.assertEqual(6, hs.points_value)

    def test_morgans_orchard_and_one_for_his_knob(self):
        hand = Crib.Hand([cc(4, HEARTS), cc(11, HEARTS), cc(11, CLUBS)])
        hs = Crib.HandScore(hand, cc(4, CLUBS))
        print('\n', hs)
        self.assertEqual(5, hs.points_value)

    def test_mess_about_with_suits(self):
        card = cc(3, CLUBS)
        # for s in Crib.SUITS:
        print('\n')
        dict_suits = {globals()[gk]: gk.lower() for gk in globals().keys() if globals()[gk] in Crib.SUITS}
        print(dict_suits)
        # print(globals())

    def test_box_cards_easy(self):
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        expected_discards = [cc(1, HEARTS), cc(4, HEARTS)]
        init_cards = [cc(10, CLUBS), cc(11, CLUBS), cc(5, CLUBS)] + expected_discards
        computer.receive_cards(init_cards)
        round.play_round()
        for d in expected_discards:
            self.assertNotIn(d, computer.hand.cards)

    def test_box_cards_flush(self):
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        expected_discards = [cc(11, HEARTS), cc(9, HEARTS)]
        init_cards = [cc(10, CLUBS), cc(11, CLUBS), cc(9, CLUBS)] + expected_discards
        computer.receive_cards(init_cards)
        round.play_round()
        for d in expected_discards:
            self.assertNotIn(d, computer.hand.cards)

    def test_box_cards_favour_strong_run_potential(self):
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        keep_cards = [cc(10, CLUBS), cc(11, CLUBS)]
        init_cards = [cc(6, DIAMONDS), cc(1, HEARTS), cc(2, SPADES)] + keep_cards
        computer.receive_cards(init_cards)
        round.play_round()
        for c in keep_cards:
            self.assertIn(c, computer.hand.cards)

    def test_box_cards_favour_fifteen_potential(self):
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        keep_cards = [cc(1, CLUBS), cc(4, CLUBS)]
        init_cards = [cc(5, DIAMONDS), cc(7, HEARTS), cc(2, SPADES)] + keep_cards
        computer.receive_cards(init_cards)
        round.play_round()
        for c in keep_cards:
            self.assertIn(c, computer.hand.cards)

    def test_box_cards_keep_jack_if_no_box(self):
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        round.player_has_box = True # TEST FAILS IF FALSE
        keep_card = cc(11, CLUBS)
        init_cards = [keep_card] + [cc(6, DIAMONDS), cc(1, HEARTS), cc(3, SPADES), cc(7, CLUBS)]
        computer.receive_cards(init_cards)
        computer.take_box_turn()
        print(computer.hand)
        self.assertIn(keep_card, computer.hand.cards)

    def test_box_cards_two_jacks_and_a_fifteen_no_box(self):
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        round.player_has_box = True
        keep_cards = [cc(11, CLUBS), cc(11, DIAMONDS)]
        init_cards = keep_cards + [cc(1, HEARTS), cc(7, SPADES), cc(8, CLUBS)]
        computer.receive_cards(init_cards)
        computer.take_box_turn()
        print(computer.hand)
        for c in keep_cards:
            self.assertIn(c, computer.hand.cards)

    def test_box_cards_two_jacks_and_a_fifteen_computer_has_box(self):
        # result is sensitive to changing card order
        computer = Crib.ComputerPlayer()
        round = Crib.Round([computer, Crib.ComputerPlayer()])
        round.player_has_box = False
        discards = [cc(11, CLUBS), cc(11, DIAMONDS)]
        init_cards = [cc(1, HEARTS), cc(7, SPADES), cc(8, CLUBS)] + discards
        computer.receive_cards(init_cards)
        computer.take_box_turn()
        print(computer.hand)
        for c in discards:
            self.assertNotIn(c, computer.hand.cards)

    def test_most_complex_run_in_pegging(self):
        cards_down = [cc(7, CLUBS), cc(5, CLUBS), cc(4, SPADES), cc(2, DIAMONDS), cc(6, HEARTS),
                      cc(3, CLUBS)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in cards_down]
        self.assertEqual(6, ps.run_score())

    def test_broken_run_in_pegging(self):
        cards_down = [cc(2, CLUBS), cc(10, DIAMONDS), cc(11, SPADES), cc(12, HEARTS)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in cards_down]
        self.assertEqual(0, ps.run_score())

    def test_second_phase_run_in_pegging(self):
        cards_down = [cc(10, DIAMONDS), cc(13, SPADES), cc(9, HEARTS), cc(8, CLUBS), cc(6, HEARTS),
                      cc(7, SPADES)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in cards_down]
        self.assertEqual(3, ps.run_score())

    def test_previous_run_in_pegging(self):
        cards_down = [cc(9, SPADES), cc(1, HEARTS), cc(2, CLUBS), cc(3, HEARTS), cc(5, SPADES)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in cards_down]
        self.assertEqual(0, ps.run_score())

    def test_one_card_after_31_not_a_run(self):
        cards_down = [cc(4, HEARTS), cc(2, CLUBS), cc(7, DIAMONDS), cc(8, SPADES), cc(9, CLUBS),
                      cc(10, SPADES)]
        ps = Crib.PeggingSequence()
        [ps.add_card(c) for c in cards_down]
        self.assertEqual(0, ps.run_score())

    def test_results_generator_matches_reference_file(self):
        ref_file = open('Test\\MonteCarloResults2.1.8.csv')
        test_subject = open('MonteCarloResults2.1.8.csv')
        differences = 0
        print('\n')
        for line_no, line in enumerate(test_subject.readlines()):
            if line_no > 10002:
                break
            expected_line = ref_file.readline()
            if line != expected_line:
                differences += 1
                print(f'Line {line_no} does not match: \nMy file:\t{line}Expected:\t{expected_line}')
                if differences > 5:
                    break
        self.assertEqual(0, differences)

    def test_pegging_sequence(self):
        ps = Crib.PeggingSequence()
        self.assertEqual(0, len(ps))

    def test_adding_cards_to_peg_seq(self):
        ps = Crib.PeggingSequence()
        ps.add_card(Crib.Card(5, DIAMONDS))
        ps.add_card(Crib.Card(13, SPADES))
        self.assertEqual(15, ps.running_total)
        self.assertEqual(2, ps.fifteen_or_thirty_one_score())

    def test_pairs_peg_seq(self):
        ps = Crib.PeggingSequence()
        ps.add_card(Crib.Card(6, HEARTS))
        ps.add_card(Crib.Card(6, DIAMONDS))
        ps.add_card(Crib.Card(6, CLUBS))
        self.assertEqual(6, ps.pairs_score())

    def test_thirty_one_peg_seq(self):
        ps = Crib.PeggingSequence()
        ps.add_card(Crib.Card(11, HEARTS))
        ps.add_card(Crib.Card(8, DIAMONDS))
        ps.add_card(Crib.Card(6, CLUBS))
        ps.add_card(Crib.Card(7, CLUBS))
        self.assertEqual(2, ps.fifteen_or_thirty_one_score())

    def test_not_a_pair_after_31_peg_seq(self):
        ps = Crib.PeggingSequence()
        ps.add_card(Crib.Card(11, HEARTS))
        ps.add_card(Crib.Card(8, DIAMONDS))
        ps.add_card(Crib.Card(13, CLUBS))
        ps.add_card(Crib.Card(13, SPADES))
        self.assertEqual(0, ps.pairs_score())

    def test_weird_or_missing_pegging_strings(self):
        return
        def compare_files(two_files):
            suits_regex = '|'.join(Crib.SUITS)
            def is_interesting(raw_line):
                exclude_list = [' box', '===', 'turned up:']
                for exclude in exclude_list:
                    if exclude in raw_line:
                        return False
                return True

            def get_description_string_from(raw_line):
                whole_line = raw_line[:-1]
                if ' : ' in whole_line:
                    start_ind = re.search(suits_regex, whole_line).start() + 1
                    return whole_line[start_ind:]
                if ']' in whole_line:
                    start_ind = whole_line.index(']') + 1
                    return whole_line[start_ind:]
                return whole_line

            unique_strings_found = []
            with open(two_files[0], 'r', encoding='utf-8') as of:
                for line in of.readlines():
                    if is_interesting(line):
                        description = get_description_string_from(line)
                        if description not in unique_strings_found:
                            unique_strings_found.append(description)

            print(f'\n<<BIG TURN DESCRIPTOR TEST>>')
            print(f'{len(unique_strings_found)} unique strings found in {two_files[0]}')
            unique_strings_found.sort()
            # for us in unique_strings_found:
            #     print(us)

            missing_strings = []
            with open(two_files[1], 'r', encoding='utf-8') as ref_file:
                ref_text = ref_file.read()
                for us in unique_strings_found:
                    regex_string = '[' + suits_regex + r'|\n|\]]' + us + '\n'
                    if not re.search(regex_string, ref_text):
                        # make sure search includes possible terminating chars either side
                        # so as to exclude lines where our string is only a partial match
                        # (as happened with 'go' point bug where '0 for 1' was not spotted
                        # because '30 for 1' was also matched)
                        missing_strings.append(us)
            return missing_strings

        latest_mco_file = f'MonteCarloOutput{Crib.VERSION}.txt' #[f for f in os.listdir('.') if 'MonteCarloOutput' in f][0]
        files_to_compare = [latest_mco_file, 'Test\\MonteCarloOutput2.1.8.txt']
        test_passes = True
        for step in range(1, -2, -2):
            missing_from_second_file = compare_files(files_to_compare[::step])
            if missing_from_second_file:
                test_passes = False
            print(f'{len(missing_from_second_file)} missing from {files_to_compare[::step][1]}:')
            for ms in missing_from_second_file:
                print(ms)

        self.assertTrue(test_passes)

    def test_how_many_knobs(self):  # or indeed other searches
        hoped_for_string = "One for his knob is 1"
        CRG().search_for_regex(hoped_for_string)

    def test_smart_computer_does_not_lead_with_a_five(self):
        re_five_lead = f'[{"|".join(Crib.SUITS)}]\nComputer : 5'
        self.assertLessEqual(CRG().search_for_regex(re_five_lead), 20)

    def test_round_searcher(self):
        # print([CRG(version='2.1.2').search_for_regex(f'{v}!') for v in Crib.Round.dict_31.values()])
        CRG().search_for_regex(' is 19')

    def test_gen_speed(self):
        # CRG().generate()
        pass

    def test_monte_carlo_pegging_rounds(self):
        for round_id in range(100):
            player_list = [Crib.ComputerPlayer(name='Comp 1'), Crib.ComputerPlayer()]
            shuffle(player_list)
            next_round = Crib.Round(player_list)
            next_round.interface.update_score_info('=== Monte Carlo round ' +
                                                   str(round_id).rjust(6) + '===')
            next_round.play_round()
        CRG().generate()


if __name__ == '__main__':
    unittest.main()