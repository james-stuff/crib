# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:57:50 2019

@author: j_a_c
"""

import Crib
import unittest
import tkinter

HEARTS = '\u2665'
CLUBS = '\u2663'
DIAMONDS = '\u2666'
SPADES = Crib.SPADES#'\u2660'

class CribTest(unittest.TestCase):
    
    def testFifteenTwo(self):
        h = self.CardsFromTupleHand([(5, HEARTS), (10, SPADES)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 2)
        print(score[1])
        
    def testFifteenEight(self):
        h = self.CardsFromTupleHand([(5, HEARTS), (10, SPADES), (5, DIAMONDS), 
                                     (10, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 12)
        print(score[1])
        
    def testLongFifteen(self):
        h = self.CardsFromTupleHand([('A', HEARTS), ('Q', SPADES), 
                                     (2, DIAMONDS), (2, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 4)
        print(score[1])
        
    def testLongFifteensInTheBox(self):
        h = self.CardsFromTupleHand([('A', CLUBS), (9, SPADES), (3, HEARTS), 
                                     (2, DIAMONDS), (2, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 12)
        print(score[1])
        
    def testTripletFifteen(self):
        h = self.CardsFromTupleHand([('A', HEARTS), ('K', SPADES), 
                                     (2, DIAMONDS), (4, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 2)
        print(score[1])
               
    def testFlush(self):
        h = self.CardsFromTupleHand([('K', CLUBS), ('Q', CLUBS), (2, DIAMONDS),
                                     (2, CLUBS), (6, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 6)
        print(score[1])
        
    def testMultiplePairs(self):
        h = self.CardsFromTupleHand([('Q', CLUBS), (6, HEARTS), 
                                     ('Q', DIAMONDS), ('Q', HEARTS), 
                                     (6, DIAMONDS), ('Q', SPADES), (6, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 18)
        print(score[1])
        
    def testBlotchy(self):
        h = self.CardsFromTupleHand([(6, HEARTS), (4, SPADES), (8, DIAMONDS), 
                                     (2, CLUBS)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 0)
        print(score[1])
        
    def testMegaRuns(self):
        h = self.CardsFromTupleHand([(9, HEARTS), (4, SPADES), (10, DIAMONDS),
                                     ('J', CLUBS), ('Q', DIAMONDS), 
                                     (10, HEARTS), ('J', CLUBS), (3, SPADES)])
        score = Crib.score_hand(h)
        self.assertEqual(score[0], 20)
        print(score[1])
        
    def testPegs(self):
        row = Crib.PegRow(tkinter.Label())
        expected = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19]
        for n in range(len(expected)):
            self.assertEqual(row.calc_peg_pos(n + 1), expected[n])
            
    def testFlushInBox(self):
        hand = [Crib.Card(10, CLUBS), Crib.Card(3, CLUBS), Crib.Card(6, CLUBS),
                Crib.Card(12, CLUBS), Crib.Card(13, CLUBS)]
        score = Crib.score_hand(hand, True)
        self.assertEqual(score[0], 5)
        print(score[1])
        
    def testNotAFlushInBox(self):
        hand = [Crib.Card(10, CLUBS), Crib.Card(3, CLUBS), Crib.Card(6, CLUBS),
                Crib.Card(12, HEARTS), Crib.Card(13, CLUBS)]
        score = Crib.score_hand(hand, True)
        self.assertEqual(score[0], 0)
        print(score[1])
        
    def testRunsInPegging(self):
        played_cards = [Crib.Card(2, CLUBS), Crib.Card(3, HEARTS),
                                   Crib.Card(4, DIAMONDS)]
        self.assertEqual(Crib.runs_in_pegging(played_cards), 3)
        
    def testComplexRunInPegging(self):
        played_cards = [Crib.Card(10, CLUBS), Crib.Card(3, HEARTS), 
                        Crib.Card(5, DIAMONDS), Crib.Card(6, CLUBS), 
                        Crib.Card(4, SPADES)]#, Crib.Card(11, CLUBS)]
        self.assertEqual(Crib.runs_in_pegging(played_cards), 4)
        
    def testShouldntBeARun(self):   
        played_cards = [Crib.Card(9, DIAMONDS), Crib.Card(11, HEARTS),
                        Crib.Card(11, DIAMONDS)]#['9♦', 'J♥', 'J♦']
        self.assertEqual(Crib.runs_in_pegging(played_cards), 0)
        
    def testTwentyNine(self):
        hand = [Crib.Card(11, CLUBS), Crib.Card(5, DIAMONDS), 
                Crib.Card(5, HEARTS), Crib.Card(5, SPADES), Crib.Card(5, CLUBS)]
        score = Crib.score_hand(hand, True)
        self.assertEqual(score[0], 29)
        print(score[1])
        
    def testThreeCardsForscore_hand(self):
        hand = [Crib.Card(7, HEARTS), Crib.Card(7, SPADES), Crib.Card(8, DIAMONDS)]
        score = Crib.score_hand(hand)
        self.assertEqual(score[0], 6)
        print(score)
        
    def testThreeCardsLongFifteen(self):
        hand = [Crib.Card(6, HEARTS), Crib.Card(7, SPADES), Crib.Card(2, DIAMONDS)]
        score = Crib.score_hand(hand)
        self.assertEqual(score[0], 2)
        print(score)
        
    def testThreeCardsKnobCheck(self):
        # shouldn't give one for his knob
        hand = [Crib.Card(11, HEARTS), Crib.Card(7, SPADES), Crib.Card(2, HEARTS)]
        score = Crib.score_hand(hand)
        self.assertEqual(score[0], 0)
        print(score)

    def testThreeCardsFlush(self):
        hand = [Crib.Card(11, HEARTS), Crib.Card(6, HEARTS), Crib.Card(13, HEARTS)]
        score = Crib.score_hand(hand)
        self.assertEqual(score[0], 3)
        print(score)
        
    def testHowManyPairsInFiveCards(self):
        # shouldn't give one for his knob
        hand = [Crib.Card(7, SPADES), Crib.Card(7, HEARTS), 
                Crib.Card(7, SPADES), Crib.Card(7, SPADES), Crib.Card(7, SPADES)]
        score = Crib.score_hand(hand, True)
        self.assertEqual(score[0], 20)
        print(score)
        
     # NB for these tests, both players put last two cards in list in box, 
    # then player plays 2, 1, 0 and computer 0, 1, 2 in their remaining card lists
    def testBoxCreation(self):
        player = [Crib.Card(6, CLUBS), Crib.Card(5, DIAMONDS), 
                Crib.Card(5, HEARTS), Crib.Card(5, SPADES), Crib.Card(5, CLUBS)]
        comp = [Crib.Card(11, CLUBS), Crib.Card(10, DIAMONDS), 
                Crib.Card(12, HEARTS), Crib.Card(13, SPADES), Crib.Card(11, CLUBS)]
        crib_round = Crib.Round(game=None, cards=player, comp_cards=comp)
        crib_round.update_score_info('=== testBoxCreation ===')
        crib_round.play_round()
        print('=' * 23)
        
    def testDozenInPairsPegging(self):
        player = [Crib.Card(2, CLUBS), Crib.Card(2, DIAMONDS), 
                Crib.Card(10, HEARTS), Crib.Card(5, SPADES), Crib.Card(5, CLUBS)]
        comp = [Crib.Card(12, CLUBS), Crib.Card(2, SPADES), 
                Crib.Card(2, HEARTS), Crib.Card(13, SPADES), Crib.Card(11, CLUBS)]
        crib_round = Crib.Round(game=None, cards=player, comp_cards=comp)
        crib_round.update_score_info('=== testDozenInPairsPegging ===')
        crib_round.play_round()
        print('=' * 23)
        
    def testMonteCarloPeggingRounds(self):
        for monte_carlo in range(10):
            next_round = Crib.Round()
            next_round.update_score_info('=== Monte Carlo round ' + 
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
        
    def CardsFromTupleHand(self, hand):
        cards = []
        picdic = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
        rank = 0
        for c in hand:
            if type(c[0]) == int:
                rank = c[0]
            elif c[0] in picdic:
                rank = picdic[c[0]]
            cards.append(Crib.Card(rank, c[1]))
        return cards

if __name__ == '__main__':
    unittest.main()