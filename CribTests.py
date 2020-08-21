# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:57:50 2019

@author: j_a_c
"""

import Crib
import unittest
import tkinter
from Crib import Card as cc

HEARTS = '\u2665'
CLUBS = '\u2663'
DIAMONDS = '\u2666'
SPADES = Crib.SPADES#'\u2660'

class CribTest(unittest.TestCase):
    
    def testFifteenTwo(self):
        h = Crib.Hand([cc(5, HEARTS), cc(10, SPADES)], Crib.ComputerPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(2, score.points_value)
        print('\n', score)
        
    def testFifteenEight(self):
        h = Crib.Hand([cc(5, HEARTS), cc(10, SPADES), cc(5, DIAMONDS), cc(10, CLUBS)], Crib.ComputerPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(12, score.points_value)
        print('\n', score)
        
    def testLongFifteen(self):
        h = Crib.Hand([cc(1, HEARTS), cc(12, SPADES), cc(2, DIAMONDS), cc(2, CLUBS)], Crib.HumanPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(4, score.points_value)
        print('\n', score)
        
    def testLongFifteensInTheBox(self):
        h = Crib.Hand([cc(1, CLUBS), cc(9, SPADES), cc(3, HEARTS), cc(2, DIAMONDS), cc(2, CLUBS)], Crib.HumanPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(12, score.points_value)
        print('\n', score)
        
    def testTripletFifteen(self):
        h = Crib.Hand([cc(1, HEARTS), cc(13, SPADES), cc(2, DIAMONDS), cc(4, CLUBS)], Crib.ComputerPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(2, score.points_value)
        print('\n', score)
               
    def testFlushInHand(self):
        h = Crib.Hand([cc(13, CLUBS), cc(12, CLUBS), cc(6, CLUBS), cc(2, DIAMONDS)], Crib.HumanPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testNotAFlushInHand(self):
        h = Crib.Hand([cc(13, CLUBS), cc(12, CLUBS), cc(2, DIAMONDS), cc(4, CLUBS)], Crib.ComputerPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(0, score.points_value)
        print('\n', score)

    def testMultiplePairs(self):
        h = Crib.Hand([cc(12, CLUBS), cc(6, HEARTS), cc(12, DIAMONDS), cc(12, HEARTS),
                       cc(6, DIAMONDS), cc(12, SPADES), cc(6, CLUBS)], Crib.ComputerPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(18, score.points_value)
        print('\n', score)
        
    def testBlotchy(self):
        h = Crib.Hand([cc(6, HEARTS), cc(4, SPADES), cc(8, DIAMONDS), cc(2, CLUBS)], Crib.HumanPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testMegaRuns(self):
        h = Crib.Hand([cc(9, HEARTS), cc(4, SPADES), cc(10, DIAMONDS), cc(11, CLUBS),
                       cc(12, DIAMONDS), cc(10, HEARTS), cc(11, CLUBS), cc(3, SPADES)], Crib.ComputerPlayer())
        score = Crib.HandScore(h)
        self.assertEqual(20, score.points_value)
        print('\n', score)
        
    def testPegs(self):
        row = Crib.PegRow(tkinter.Label())
        expected = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19]
        for n in range(len(expected)):
            self.assertEqual(row.calc_peg_pos(n + 1), expected[n])
            
    def testFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, CLUBS), cc(6, CLUBS), cc(12, CLUBS)], Crib.HumanPlayer())
        score = Crib.HandScore(hand, cc(13, CLUBS))
        self.assertEqual(5, score.points_value)
        print('\n', score)
        
    def testNotAFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, CLUBS), cc(6, CLUBS), cc(12, CLUBS)], Crib.ComputerPlayer())
        score = Crib.HandScore(hand, cc(13, HEARTS))
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testDefinitelyNotAFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, SPADES), cc(6, CLUBS), cc(12, CLUBS)], Crib.HumanPlayer())
        score = Crib.HandScore(hand, cc(13, CLUBS))
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testRunsInPegging(self):
        played_cards = [cc(2, CLUBS), cc(3, HEARTS), cc(4, DIAMONDS)]
        self.assertEqual(3, Crib.runs_in_pegging(played_cards))
        
    def testComplexRunInPegging(self):
        played_cards = [cc(10, CLUBS), cc(3, HEARTS), cc(5, DIAMONDS), cc(6, CLUBS), cc(4, SPADES)]
        self.assertEqual(4, Crib.runs_in_pegging(played_cards))
        
    def testShouldntBeARun(self):   
        played_cards = [cc(9, DIAMONDS), cc(11, HEARTS), cc(11, DIAMONDS)]
        self.assertEqual(0, Crib.runs_in_pegging(played_cards))
        
    def testTwentyNine(self):
        hand = Crib.Hand([cc(11, CLUBS), cc(5, DIAMONDS), cc(5, HEARTS), cc(5, SPADES)], Crib.HumanPlayer())
        score = Crib.HandScore(hand, cc(5, CLUBS))
        self.assertEqual(29, score.points_value)
        print('\n', score)
        
    def testThreeCardsForHandScore(self):
        hand = Crib.Hand([cc(7, HEARTS), cc(7, SPADES), cc(8, DIAMONDS)], Crib.ComputerPlayer())
        score = Crib.HandScore(hand)
        self.assertEqual(6, score.points_value)
        print('\n', score)
        
    def testThreeCardsLongFifteen(self):
        hand = Crib.Hand([cc(6, HEARTS), cc(7, SPADES), cc(2, DIAMONDS)], Crib.ComputerPlayer())
        score = Crib.HandScore(hand)
        self.assertEqual(2, score.points_value)
        print('\n', score)
        
    def testThreeCardsKnobCheck(self):
        # shouldn't give one for his knob
        hand = Crib.Hand([cc(11, HEARTS), cc(7, SPADES), cc(2, HEARTS)], Crib.HumanPlayer())
        score = Crib.HandScore(hand)
        self.assertEqual(0, score.points_value)
        print('\n', score)

    def testThreeCardsFlush(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(6, HEARTS), cc(13, HEARTS)], Crib.HumanPlayer())
        score = Crib.HandScore(hand)
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testHowManyPairsInFiveCards(self):
        hand = Crib.Hand([cc(7, SPADES), cc(7, HEARTS), cc(7, SPADES), cc(7, SPADES)], Crib.ComputerPlayer())
        score = Crib.HandScore(hand, cc(7, SPADES))
        self.assertEqual(20, score.points_value)
        print('\n', score)
        
    def testRunsSimple(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS)], Crib.ComputerPlayer())
        score = Crib.HandScore(hand, cc(3, CLUBS))
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testTwoRunsOfFour(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)], Crib.HumanPlayer())
        score = Crib.HandScore(hand, cc(9, DIAMONDS))
        self.assertEqual(10, score.points_value)
        print('\n', score)
        
    def testNoRuns(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(7, HEARTS), cc(3, CLUBS)], Crib.ComputerPlayer())
        score = Crib.HandScore(hand)
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testBoxCreation(self):
        p_cards = [cc(6, CLUBS), cc(5, DIAMONDS), cc(5, HEARTS), cc(5, SPADES), cc(5, CLUBS)]
        c_cards = [cc(11, CLUBS), cc(10, DIAMONDS), cc(12, HEARTS), cc(13, SPADES), cc(11, CLUBS)]
        player, computer = Crib.ComputerPlayer('P'), Crib.ComputerPlayer('C')
        crib_round = Crib.Round([player, computer], game=None)
        crib_round.interface.update_score_info('=== testBoxCreation ===')
        player.receive_cards(p_cards)
        computer.receive_cards(c_cards)
        crib_round.play_round()
        print('=' * 23)
        
    def testDozenInPairsPegging(self):
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
        
    def testMonteCarloPeggingRounds(self):
        for round_id in range(10):
            next_round = Crib.Round([Crib.ComputerPlayer(name='Comp 1'), Crib.ComputerPlayer()])
            next_round.interface.update_score_info('=== Monte Carlo round ' +
                                                   str(round_id).rjust(6) + '===')
            next_round.play_round()
            
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
        
    def test_player_hand(self):
        hand = Crib.Hand([cc(3, HEARTS), cc(6, DIAMONDS), cc(10, CLUBS)], Crib.HumanPlayer())
        self.assertEqual('Show my hand', hand.display_button_text)

    def test_computer_box(self):
        hand = Crib.Box([cc(7, HEARTS), cc(8, DIAMONDS), cc(11, CLUBS),
                          cc(13, HEARTS)], Crib.ComputerPlayer())
        self.assertEqual('Show computer\'s box', hand.display_button_text)

    def test_no_cards_left(self):
        hand = Crib.Hand([cc(3, HEARTS), cc(6, DIAMONDS), cc(10, CLUBS)], Crib.HumanPlayer())
        played_cards = [cc(2, HEARTS), cc(1, CLUBS)] + hand.cards
        self.assertFalse(hand.get_unplayed_cards(played_cards))

    def test_three_cards_left(self):
        hand = Crib.Hand([cc(3, HEARTS), cc(6, DIAMONDS), cc(10, CLUBS)], Crib.HumanPlayer())
        played_cards = [cc(2, HEARTS), cc(1, CLUBS)]
        self.assertEqual(3, len(hand.get_unplayed_cards(played_cards)))

    def test_hand_score(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)], Crib.HumanPlayer())
        hs = Crib.HandScore(hand, cc(9, DIAMONDS))
        print('\n', hs)
        self.assertEqual(10, hs.points_value)

    def test_hand_score_fifteens(self):
        hand = Crib.Hand([cc(5, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)], Crib.HumanPlayer())
        hs = Crib.HandScore(hand, cc(5, DIAMONDS))
        print('\n', hs)
        self.assertEqual(17, hs.points_value)

    def test_hand_score_fifteens_and_nothing_else(self):
        hand = Crib.Hand([cc(5, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(13, CLUBS)], Crib.HumanPlayer())
        hs = Crib.HandScore(hand, cc(2, DIAMONDS))
        print('\n', hs)
        self.assertEqual(6, hs.points_value)

    def test_morgans_orchard_and_one_for_his_knob(self):
        hand = Crib.Hand([cc(4, HEARTS), cc(11, HEARTS), cc(11, CLUBS)], Crib.ComputerPlayer())
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

    def test_box_object(self):
        player = Crib.HumanPlayer()
        box = Crib.Box([cc(1, SPADES)], player)
        print(box.set_display_button_text())

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
        self.assertEqual(6, Crib.runs_in_pegging(cards_down))

    def test_broken_run_in_pegging(self):
        cards_down = [cc(2, CLUBS), cc(10, DIAMONDS), cc(11, SPADES), cc(12, HEARTS)]
        self.assertEqual(0, Crib.runs_in_pegging(cards_down))

    def test_second_phase_run_in_pegging(self):
        cards_down = [cc(10, DIAMONDS), cc(13, SPADES), cc(9, HEARTS), cc(8, CLUBS), cc(6, HEARTS),
                      cc(7, SPADES)]
        self.assertEqual(3, Crib.runs_in_pegging(cards_down))

    def test_previous_run_in_pegging(self):
        cards_down = [cc(9, SPADES), cc(1, HEARTS), cc(2, CLUBS), cc(3, HEARTS), cc(5, SPADES)]
        self.assertEqual(0, Crib.runs_in_pegging(cards_down))


if __name__ == '__main__':
    unittest.main()