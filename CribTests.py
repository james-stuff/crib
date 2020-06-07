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
        h = Crib.Hand([cc(5, HEARTS), cc(10, SPADES)], True)
        score = Crib.HandScore(h)
        self.assertEqual(2, score.points_value)
        print('\n', score)
        
    def testFifteenEight(self):
        h = Crib.Hand([cc(5, HEARTS), cc(10, SPADES), cc(5, DIAMONDS), cc(10, CLUBS)], False)
        score = Crib.HandScore(h)
        self.assertEqual(12, score.points_value)
        print('\n', score)
        
    def testLongFifteen(self):
        h = Crib.Hand([cc(1, HEARTS), cc(12, SPADES), cc(2, DIAMONDS), cc(2, CLUBS)], True)
        score = Crib.HandScore(h)
        self.assertEqual(4, score.points_value)
        print('\n', score)
        
    def testLongFifteensInTheBox(self):
        h = Crib.Hand([cc(1, CLUBS), cc(9, SPADES), cc(3, HEARTS), cc(2, DIAMONDS), cc(2, CLUBS)], True)
        score = Crib.HandScore(h)
        self.assertEqual(12, score.points_value)
        print('\n', score)
        
    def testTripletFifteen(self):
        h = Crib.Hand([cc(1, HEARTS), cc(13, SPADES), cc(2, DIAMONDS), cc(4, CLUBS)], False)
        score = Crib.HandScore(h)
        self.assertEqual(2, score.points_value)
        print('\n', score)
               
    def testFlushInHand(self):
        h = Crib.Hand([cc(13, CLUBS), cc(12, CLUBS), cc(6, CLUBS), cc(2, DIAMONDS)], True)
        score = Crib.HandScore(h)
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testNotAFlushInHand(self):
        h = Crib.Hand([cc(13, CLUBS), cc(12, CLUBS), cc(2, DIAMONDS), cc(4, CLUBS)], False)
        score = Crib.HandScore(h)
        self.assertEqual(0, score.points_value)
        print('\n', score)

    def testMultiplePairs(self):
        h = Crib.Hand([cc(12, CLUBS), cc(6, HEARTS), cc(12, DIAMONDS), cc(12, HEARTS),
                       cc(6, DIAMONDS), cc(12, SPADES), cc(6, CLUBS)], False)
        score = Crib.HandScore(h)
        self.assertEqual(18, score.points_value)
        print('\n', score)
        
    def testBlotchy(self):
        h = Crib.Hand([cc(6, HEARTS), cc(4, SPADES), cc(8, DIAMONDS), cc(2, CLUBS)], True)
        score = Crib.HandScore(h)
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testMegaRuns(self):
        h = Crib.Hand([cc(9, HEARTS), cc(4, SPADES), cc(10, DIAMONDS), cc(11, CLUBS),
                       cc(12, DIAMONDS), cc(10, HEARTS), cc(11, CLUBS), cc(3, SPADES)], False)
        score = Crib.HandScore(h)
        self.assertEqual(20, score.points_value)
        print('\n', score)
        
    def testPegs(self):
        row = Crib.PegRow(tkinter.Label())
        expected = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19]
        for n in range(len(expected)):
            self.assertEqual(row.calc_peg_pos(n + 1), expected[n])
            
    def testFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, CLUBS), cc(6, CLUBS), cc(12, CLUBS)], True)
        score = Crib.HandScore(hand, cc(13, CLUBS))
        self.assertEqual(5, score.points_value)
        print('\n', score)
        
    def testNotAFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, CLUBS), cc(6, CLUBS), cc(12, CLUBS)], False)
        score = Crib.HandScore(hand, cc(13, HEARTS))
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
    def testDefinitelyNotAFlushInBox(self):
        hand = Crib.Hand([cc(10, CLUBS), cc(3, SPADES), cc(6, CLUBS), cc(12, CLUBS)], True)
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
        hand = Crib.Hand([cc(11, CLUBS), cc(5, DIAMONDS), cc(5, HEARTS), cc(5, SPADES)], True)
        score = Crib.HandScore(hand, cc(5, CLUBS))
        self.assertEqual(29, score.points_value)
        print('\n', score)
        
    def testThreeCardsForHandScore(self):
        hand = Crib.Hand([cc(7, HEARTS), cc(7, SPADES), cc(8, DIAMONDS)], False)
        score = Crib.HandScore(hand)
        self.assertEqual(6, score.points_value)
        print('\n', score)
        
    def testThreeCardsLongFifteen(self):
        hand = Crib.Hand([cc(6, HEARTS), cc(7, SPADES), cc(2, DIAMONDS)], False)
        score = Crib.HandScore(hand)
        self.assertEqual(2, score.points_value)
        print('\n', score)
        
    def testThreeCardsKnobCheck(self):
        # shouldn't give one for his knob
        hand = Crib.Hand([cc(11, HEARTS), cc(7, SPADES), cc(2, HEARTS)], True)
        score = Crib.HandScore(hand)
        self.assertEqual(0, score.points_value)
        print('\n', score)

    def testThreeCardsFlush(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(6, HEARTS), cc(13, HEARTS)], True)
        score = Crib.HandScore(hand)
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testHowManyPairsInFiveCards(self):
        hand = Crib.Hand([cc(7, SPADES), cc(7, HEARTS), cc(7, SPADES), cc(7, SPADES)], False)
        score = Crib.HandScore(hand, cc(7, SPADES))
        self.assertEqual(20, score.points_value)
        print('\n', score)
        
    def testRunsSimple(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS)], False)
        score = Crib.HandScore(hand, cc(3, CLUBS))
        self.assertEqual(3, score.points_value)
        print('\n', score)
        
    def testTwoRunsOfFour(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)], True)
        score = Crib.HandScore(hand, cc(9, DIAMONDS))
        self.assertEqual(10, score.points_value)
        print('\n', score)
        
    def testNoRuns(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(7, HEARTS), cc(3, CLUBS)], False)
        score = Crib.HandScore(hand)
        self.assertEqual(0, score.points_value)
        print('\n', score)
        
     # NB for these tests, both players put last two cards in list in box, 
    # then player plays 2, 1, 0 and computer 0, 1, 2 in their remaining card lists
    def testBoxCreation(self):
        player = [cc(6, CLUBS), cc(5, DIAMONDS), 
                cc(5, HEARTS), cc(5, SPADES), cc(5, CLUBS)]
        comp = [cc(11, CLUBS), cc(10, DIAMONDS), 
                cc(12, HEARTS), cc(13, SPADES), cc(11, CLUBS)]
        crib_round = Crib.Round(game=None, cards=player, comp_cards=comp)
        crib_round.interface.update_score_info('=== testBoxCreation ===')
        crib_round.play_round()
        print('=' * 23)
        
    def testDozenInPairsPegging(self):
        player = [cc(2, CLUBS), cc(2, DIAMONDS), 
                cc(10, HEARTS), cc(5, SPADES), cc(5, CLUBS)]
        comp = [cc(12, CLUBS), cc(2, SPADES), 
                cc(2, HEARTS), cc(7, SPADES), cc(11, CLUBS)]
        crib_round = Crib.Round(game=None, cards=player, comp_cards=comp)
        crib_round.interface.update_score_info('=== testDozenInPairsPegging ===')
        crib_round.play_round()
        print('=' * 23)
        
    def testMonteCarloPeggingRounds(self):
        for monte_carlo in range(10):
            next_round = Crib.Round()
            next_round.interface.update_score_info('=== Monte Carlo round ' +
                                         str(monte_carlo).rjust(6) + '===')
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
        hand = Crib.Hand([cc(3, HEARTS), cc(6, DIAMONDS), cc(10, CLUBS)], True)
        self.assertEqual('Show my hand', hand.display_button_text)

    def test_computer_box(self):
        hand = Crib.Hand([cc(7, HEARTS), cc(8, DIAMONDS), cc(11, CLUBS),
                          cc(13, HEARTS)], False)
        self.assertEqual('Show computer\'s box', hand.display_button_text)

    def test_no_cards_left(self):
        hand = Crib.Hand([cc(3, HEARTS), cc(6, DIAMONDS), cc(10, CLUBS)], True)
        played_cards = [cc(2, HEARTS), cc(1, CLUBS)] + hand.cards
        self.assertFalse(hand.get_playable_cards(played_cards))

    def test_three_cards_left(self):
        hand = Crib.Hand([cc(3, HEARTS), cc(6, DIAMONDS), cc(10, CLUBS)], True)
        played_cards = [cc(2, HEARTS), cc(1, CLUBS)]
        self.assertEqual(3, len(hand.get_playable_cards(played_cards)))

    def test_hand_score(self):
        hand = Crib.Hand([cc(11, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)], True)
        hs = Crib.HandScore(hand, cc(9, DIAMONDS))
        print('\n', hs)
        self.assertEqual(10, hs.points_value)

    def test_hand_score_fifteens(self):
        hand = Crib.Hand([cc(5, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(11, CLUBS)], True)
        hs = Crib.HandScore(hand, cc(5, DIAMONDS))
        print('\n', hs)
        self.assertEqual(17, hs.points_value)

    def test_hand_score_fifteens_and_nothing_else(self):
        hand = Crib.Hand([cc(5, HEARTS), cc(10, CLUBS), cc(12, HEARTS), cc(13, CLUBS)], True)
        hs = Crib.HandScore(hand, cc(2, DIAMONDS))
        print('\n', hs)
        self.assertEqual(6, hs.points_value)

    def test_morgans_orchard_and_one_for_his_knob(self):
        hand = Crib.Hand([cc(4, HEARTS), cc(11, HEARTS), cc(11, CLUBS)], False)
        hs = Crib.HandScore(hand, cc(4, CLUBS))
        print('\n', hs)
        self.assertEqual(5, hs.points_value)


if __name__ == '__main__':
    unittest.main()