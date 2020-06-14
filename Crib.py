# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:24:44 2019

@author: j_a_c
"""
import random
import tkinter
import itertools

HEARTS = '\u2665'
CLUBS = '\u2663'
DIAMONDS = '\u2666'
SPADES = '\u2660'
SUITS = [HEARTS, CLUBS, DIAMONDS, SPADES]
WIN_SCORE = 121
NUMBERS = ['zero', 'a', 'two', 'three', 'four', 'five', 'six', 'seven',
           'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
           'fourteen', 'fifteen', 'sixteen']
VERSION = '2.1.7'


class Table:
    def __init__(self):
        self.gui = tkinter.Tk()
        self.gui.protocol("WM_DELETE_WINDOW", self.get_me_out_of_here)
        self.gui.title('Crib!          v' + VERSION)
        self.gui.geometry('1270x495')
        self.gui.configure(bg='green')

        self.common_card_frame = tkinter.Frame(self.gui, bg='green', width=405, height=194)
        self.comp_cards_frame = tkinter.Frame(self.gui, bg='green', width=870, height=194)
        self.button_frame = tkinter.Frame(self.gui, bg='green')
        self.player_cards_frame = tkinter.Frame(self.gui, bg='green')
        for ind, fr in enumerate([self.common_card_frame, self.comp_cards_frame,
                                  self.button_frame, self.player_cards_frame]):
            fr.grid(row=(ind // 2) * 2, column=(ind % 2), sticky='w', padx=((ind % 2) + 1) * 10)

        for n in range(4):
            card_in_pack = tkinter.Button(self.common_card_frame, borderwidth=1,
                                          height=174, width=4, relief='raised',
                                          image=tkinter.PhotoImage(file='Images\\blank.png'))
            card_in_pack.grid(column=n, row=0, sticky='w')

        self.common_card_frame.columnconfigure(5, minsize=50)
        self.common_card_frame.columnconfigure(12, minsize=10)
        self.comp_cards_frame.columnconfigure(19, minsize=50)
        self.common_card_frame.grid_propagate(False)
        self.comp_cards_frame.grid_propagate(False)

        self.btControl = tkinter.Button(self.button_frame, text='Start new game',
                                        command=self.new_game, font=('Arial Bold', 12),
                                        wraplength=100, height=4, width=12)
        self.btControl.grid(row=0, pady=40, sticky='e')
        self.button_frame.rowconfigure(0, minsize=174)
        self.button_frame.columnconfigure(0, minsize=360)
        self.player_cards_frame.columnconfigure(6, minsize=50)

        info_frame = tkinter.Frame(self.gui, bg='green')
        info_frame.grid(row=1, columnspan=3, sticky='we', pady=10)
        info_frame.columnconfigure(0, minsize=1270)
        self.score_info = tkinter.StringVar()
        self.l_score = tkinter.Label(info_frame, font=('Helvetica', 12),
                                     textvariable=self.score_info)
        self.peg_board = PegBoard(tkinter.Label(info_frame), tkinter.Label(info_frame))

        self.player_card_buttons = [CardButton(self, self.player_cards_frame, n, 1) for n in range(5)]
        self.face_up_card_buttons = [CardButton(self, self.common_card_frame, 0, 4)]
        self.face_up_card_buttons[0].show()
        self.played_cards_buttons = [CardButton(self, self.common_card_frame, n, 6) for n in range(6)]
        self.comp_card_buttons = [CardButton(self, self.comp_cards_frame, n, 13) for n in range(5)]
        self.player_box_buttons = [CardButton(self, self.player_cards_frame, n, 7) for n in range(4)]
        self.comp_box_buttons = [CardButton(self, self.comp_cards_frame, n, 21) for n in range(4)]
        self.all_cb = self.player_card_buttons + self.face_up_card_buttons + \
                      self.played_cards_buttons + self.comp_card_buttons + \
                      self.player_box_buttons + self.comp_box_buttons

        self.card_var = tkinter.IntVar()
        self.gui.mainloop()

    def new_game(self):
        while self.card_var.get() != 20:
            game = Game(self)
            self.configure_for_new_game()
            try:
                game.play()
            except RuntimeError:
                break
            except tkinter.TclError:
                break

    def configure_for_new_game(self):
        self.btControl.configure(command=lambda: self.card_var.set(19))
        self.score_info.set('')
        self.l_score.configure(bg='green')
        self.peg_board.reset()

    def await_control_button_click(self, instruction):
        self.card_var.set(-1)
        while self.card_var.get() not in [19, 20]:
            self.btControl.configure(text=instruction)
            self.btControl.wait_variable(self.card_var)

    def get_me_out_of_here(self):
        self.card_var.set(20)
        self.gui.destroy()


class CardButton:
    def __init__(self, table, frame, index, col_start):
        self.table = table
        self.card = None
        self.full_width = 110
        self.button = tkinter.Button(frame, width=self.full_width, height=174)
        self.clickable_button_id = index
        self.disp_column = col_start + index
        self.image = None
        self.face_down_image = tkinter.PhotoImage(file='Images\\blank.png')

    def make_clickable(self):
        self.button.configure(command=lambda: self.table.card_var.set(self.clickable_button_id))

    def show(self, face_up=False):
        show_border = False
        if face_up:
            suits_dict = {globals()[g]: g.lower() for g in globals().keys() if globals()[g] in SUITS}
            im_file = 'Images\\' + str(self.card)[:-1] + suits_dict[str(self.card)[-1]] + '.png'
            self.image = tkinter.PhotoImage(file=im_file)
        else:
            self.image = self.face_down_image
            show_border = True
        self.button.configure(image=self.image, border=show_border)
        self.button.grid(row=0, column=self.disp_column, pady=10)

    def reduce_width(self):
        self.button.configure(width=16, anchor='w')

    def show_full_size(self, face_up=True):
        self.show(face_up=face_up)
        self.button.configure(width=self.full_width, anchor='center')

    def remove_from_hand(self):
        self.button.configure(image=None, text='')
        self.button.grid_forget()

    def clear(self):
        self.card = None
        self.remove_from_hand()


class Game:
    def __init__(self, table):
        self.table = table
        self.win_detected = self.is_players_turn = False
        self.players = [HumanPlayer(None), ComputerPlayer(None)]
        self.player_has_box = random.choice([True, False])

    def play(self):
        active_round = None
        while not self.win_detected:
            self.is_players_turn = not self.player_has_box
            self.table.await_control_button_click('Deal for next round')
            if active_round:
                active_round.interface.clear_box()
            active_round = Round(self.players, game=self).play_round()
            self.player_has_box = not self.player_has_box
        active_round.interface.wait_for_ctrl_btn_click('Start new game')
        self.table.face_up_card_buttons[0].show(face_up=False)
        active_round.interface.clear_box()


class Round:
    def __init__(self, players, game=None, cards=None, comp_cards=None):
        self.game = game
        self.players = players
        self.my_cards = cards
        self.comp_cards = comp_cards
        self.box_cards = []
        self.played_cards = []
        self.running_total = 0
        self.of_a_kind_count = 1
        self.is_players_turn = self.comp_knock = self.player_knock = False
        self.last_score_comment = ''
        self.the_pack = Pack()
        self.face_up_card = None
        self.computer = ComputerPlayer(self)
        self.who_has_it = {True: 'You have', False: 'Computer has'}
        self.my_hand = self.comp_hand = self.box = None

        if self.game:
            self.player_has_box = self.game.player_has_box
            self.interface = RoundVisualInterface(self.game.table)
        else:
            self.interface = RoundTestInterface()
        for p in self.players:
            p.round = self
        [p.set_interface(self.interface) for p in self.players]

    def play_round(self):
        self.deal()
        if self.game is None:
            self.player_has_box = random.choice([True, False])
        self.is_players_turn = not self.player_has_box
        self.interface.set_box_buttons(self.player_has_box)
        self.build_box()
        self.my_hand = Hand(self.my_cards, True)
        self.comp_hand = Hand(self.comp_cards, False)
        self.box = Hand(self.box_cards, self.player_has_box)
        self.turn_up_top_card()
        self.pegging_round()
        self.put_cards_on_table()
        self.interface.end_of_round_tidy_up()
        return self

    def deal(self):
        if self.my_cards is None:
            self.my_cards = self.the_pack.deal(5)
        if self.comp_cards is None:
            self.comp_cards = self.the_pack.deal(5)
        # [p.receive_cards(self.the_pack.deal(5)) for p in self.players]
        self.players[0].receive_cards(self.my_cards)
        self.players[1].receive_cards(self.comp_cards)
        # self.interface.allocate_cards_after_deal(self.my_cards, self.comp_cards)
        [self.interface.allocate_cards_after_deal(p) for p in self.players]

    def build_box(self):
        self.interface.update_score_info(self.who_has_it[self.player_has_box] + ' the box')
        turn_order = 1
        if self.player_has_box:
            turn_order = -1
        [p.take_box_turn() for p in self.players[::turn_order]]

    def turn_up_top_card(self):
        # Turn up the next card, Two for his heels check:
        self.face_up_card = self.the_pack.deal(1)[0]
        self.interface.turn_up_top_card(self.face_up_card)
        if self.face_up_card.rank == 11:
            heels_notification = 'Two for his heels!'
            updated_score = self.interface.update_pegs(self.player_has_box, 2)
            heels_notification += self.check_for_win(self.player_has_box, updated_score)
            self.interface.update_score_info(heels_notification)

    def pegging_round(self):
        while len(self.played_cards) < 6:
            self.check_if_knock_required()
            if self.is_players_turn and not self.player_knock:
                card_to_play = self.players[0].pick_card_in_pegging()
            elif not self.is_players_turn and not self.comp_knock:
                card_to_play = self.players[1].pick_card_in_pegging()
            else:
                card_to_play = None

            if type(card_to_play) == Card:
                self.play_card(card_to_play)
                self.interface.update_played_cards(self.played_cards)
            self.is_players_turn = not self.is_players_turn

            # when to reset to zero:
            if self.running_total == 31:
                self.reset_variables_at_31()
            elif len(self.played_cards) == 6:
                self.award_go_point()
            elif self.comp_knock and self.player_knock:
                self.award_go_point()
                self.reset_variables_at_31()
                self.is_players_turn = not self.played_cards[-1] in self.my_cards

    def check_if_knock_required(self):
        if not self.can_go():
            if self.is_players_turn and not self.player_knock:
                if self.my_hand.get_unplayed_cards(self.played_cards):
                    self.interface.wait_for_ctrl_btn_click('Knock')
                self.player_knock = True
            else:
                self.comp_knock = True
                self.interface.update_score_info(self.last_score_comment +
                                                 '\tComputer knocks.')

    def can_go(self):
        turn_dict = {True: self.my_hand, False: self.comp_hand}
        whose_hand = turn_dict[self.is_players_turn]
        return any(self.card_is_small_enough(c) for c in
                   whose_hand.get_unplayed_cards(self.played_cards))

    def card_is_small_enough(self, card):
        return self.running_total + card.value <= 31

    def player_picks_card_in_test_mode(self):
        for card in self.my_hand.get_unplayed_cards(self.played_cards):
            if self.card_is_small_enough(card):
                selected_card = card
                break
        return selected_card

    def play_card(self, card_played):
        ''' see if this card gets any points and show new scores when a valid card is played'''
        for_text = ''
        run_tot_text = str(self.running_total)
        self.update_round_state_with_played_card(card_played)
        turn_score = self.points_scored_by_played_card()
        total_score = self.interface.update_pegs(self.is_players_turn, turn_score)

        if self.running_total == 31:
            for_text = self.congratulations_on_getting_31()
        else:
            run_tot_text = str(self.running_total)

        win_str = ''
        if turn_score > 0:
            for_text += ' for ' + str(turn_score)
            win_str = self.check_for_win(self.is_players_turn, total_score)

        score_string = run_tot_text + for_text + win_str
        self.last_score_comment = score_string
        self.interface.update_score_info(self.interface.log_card_played(self.is_players_turn,
                                                                        card_played, score_string))

    def update_round_state_with_played_card(self, card_played):
        self.played_cards.append(card_played)
        self.running_total += card_played.value

    def points_scored_by_played_card(self):
        added_points = 0
        if self.running_total in [15, 31]:
            added_points = 2
        added_points += self.pairs_in_pegging()
        added_points += runs_in_pegging(self.played_cards)
        return added_points

    def pairs_in_pegging(self):
        if len(self.played_cards) > 1:
            if self.played_cards[-1].rank == self.played_cards[-2].rank:
                self.of_a_kind_count += 1
            else:
                self.of_a_kind_count = 1
        dict_of_a_kind = {1: 0, 2: 2, 3: 6, 4: 12}
        points_for_pairs = dict_of_a_kind[self.of_a_kind_count]
        return points_for_pairs

    def congratulations_on_getting_31(self):
        congrats = ''
        dict_31 = {1: 'one-ty', 2: 'two\'s in time', 3: 'three\'s awake',
                   4: 'four\'s in heaven', 5: 'five\'s a fix',
                   6: 'six is alive', 7: 'sevens galore',
                   8: 'eight\'s a spree', 9: 'nine\'ll do', 10: '31'}
        if self.played_cards[-1].value in dict_31:
            congrats = ', ' + dict_31[self.played_cards[-1].value] + '!'
        return congrats

    def award_go_point(self):
        player_gets_go_point = self.played_cards[-1] in self.my_cards
        just_won = 'WON' in self.last_score_comment
        last_score = 0
        if 'for' in self.last_score_comment:
            start_of_for = self.last_score_comment.index('for')
            last_score = int(self.last_score_comment[start_of_for + 4:start_of_for + 6])
            last_score += 1
            score_string = self.last_score_comment[:start_of_for + 6].rstrip() + ' and a go is ' + str(
                last_score)
            updated_score = self.interface.update_pegs(player_gets_go_point, 1, False)
        else:
            updated_score = self.interface.update_pegs(player_gets_go_point, 1)
            score_string = str(self.running_total) + ' for 1'

        if just_won:
            score_string += ' ' + self.last_score_comment[start_of_for + 6:]
        else:
            score_string += self.check_for_win(player_gets_go_point, updated_score)

        self.interface.update_score_info(score_string)

    def check_for_win(self, player_just_scored, score):
        congrats = ''
        if self.game is not None:
            if score >= WIN_SCORE and not self.game.win_detected:
                self.game.win_detected = True
                congrats = ' -- ' + self.who_has_it[player_just_scored].upper() + ' WON!!!'
        return congrats

    def reset_variables_at_31(self):
        self.running_total = 0
        self.of_a_kind_count = 0
        self.comp_knock = self.player_knock = False
        self.interface.turn_over_played_cards_on_next_turn = True
        self.last_score_comment = ''

    def put_cards_on_table(self):
        hands = [self.my_hand, self.comp_hand]
        display_order = [0, 1]
        if self.player_has_box:
            display_order = display_order[::-1]
        self.evaluate_hand(hands[display_order[0]])
        self.interface.show_cards_in_list(hands[display_order[1]].cards, visible=False)
        self.evaluate_hand(hands[display_order[1]])
        self.evaluate_hand(self.box)

    def evaluate_hand(self, hand_to_score):
        hs = HandScore(hand_to_score, self.face_up_card)
        str_info = str(hs)
        str_info = self.interface.hand_display(hand_to_score) + str_info

        new_score = self.interface.update_pegs(hand_to_score.belongs_to_player, hs.points_value)
        str_info += self.check_for_win(hand_to_score.belongs_to_player, new_score)
        self.interface.update_score_info(str_info)


class RoundInterface():
    def __init__(self):
        self.turn_over_played_cards_on_next_turn = False
        self.active_box_buttons = None

    def update_pegs(self, whose_turn, points_to_add, back_peg_moves=True):
        return 0

    def update_played_cards(self, cards):
        pass

    def update_ctrl_btn_text(self, button_text):
        pass

    def wait_for_ctrl_btn_click(self, blah):
        pass

    def wait_for_card(self, cards=None):
        pass

    def allocate_cards_after_deal(self, player):
        pass

    def set_box_buttons(self, player_has_box):
        pass

    def transfer_card_to_box(self, player, card):
        pass

    def turn_up_top_card(self, top_card):
        pass

    def player_picks_card(self, pegging_round):
        pass

    def log_card_played(self, players_turn, card, score_string):
        return score_string

    def hide_played_card(self, card):
        pass

    def show_cards_in_list(self, card_list, visible=True):
        pass

    def clear_buttons_in(self, card_button_list):
        pass

    def clear_box(self):
        pass

    def hand_display(self, hand):
        pass

    def end_of_round_tidy_up(self):
        pass


class RoundTestInterface(RoundInterface):
    def __init__(self):
        super().__init__()
        self.log_file = open('MonteCarloOutput' + VERSION + '.txt', 'a', encoding='utf-8')

    def update_score_info(self, info_to_display):
        if len(info_to_display) > 0:
            self.log_file.writelines(info_to_display + '\n')

    def wait_for_card(self, player_cards=None):
        return player_cards[-1]

    def turn_up_top_card(self, top_card):
        self.update_score_info('Card turned up: ' + str(top_card))

    def player_picks_card(self, pegging_round):
        return pegging_round.player_picks_card_in_test_mode()

    def log_card_played(self, players_turn, card, score_string):
        dict_who = {True: 'Player  ', False: 'Computer'}
        player = dict_who[players_turn]
        return player + ' : ' + str(card) + '\t' + score_string

    def hand_display(self, hand):
        return str(hand)

    def end_of_round_tidy_up(self):
        self.log_file.close() # without this, Monte Carlo logging skips many rounds


class RoundVisualInterface(RoundInterface):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.button_colour = table.btControl.cget('bg')
        self.all_card_buttons = table.all_cb
        self.table.face_up_card_buttons[0].card = None
        self.table.face_up_card_buttons[0].show(face_up=False)

    def update_pegs(self, whose_turn, points_to_add, back_peg_moves=True):
        return self.table.peg_board.increment_row_by(whose_turn, points_to_add, back_peg_moves)

    def update_played_cards(self, played_cards):
        no_of_cards_down = len(played_cards)
        if no_of_cards_down > 1:
            if self.turn_over_played_cards_on_next_turn:
                # this means 31 or double-knock, so clear previously-played cards here:
                [cb.show(face_up=False) for cb in self.table.played_cards_buttons[:no_of_cards_down]]
                self.turn_over_played_cards_on_next_turn = False
            self.table.played_cards_buttons[no_of_cards_down - 2].reduce_width()
        self.table.played_cards_buttons[no_of_cards_down - 1].card = played_cards[-1]
        self.table.played_cards_buttons[no_of_cards_down - 1].show_full_size()

    def update_score_info(self, info_to_display):
        self.table.score_info.set(info_to_display)
        self.table.l_score.grid(row=2, pady=2)
        self.table.l_score.configure(bg=self.button_colour)
        if len(info_to_display) == 0:
            self.table.l_score.configure(bg='green')

    def update_ctrl_btn_text(self, button_text):
        self.table.btControl.configure(text=button_text)
        
    def wait_for_ctrl_btn_click(self, button_text):
        self.table.await_control_button_click(button_text)

    def wait_for_card(self, player_cards=None):
        self.table.card_var.set(-1)
        while self.table.card_var.get() < 0 or self.table.card_var.get() > 4:
            self.table.btControl.wait_variable(self.table.card_var)
        our_card_number = self.table.card_var.get()
        poss_card = [c for c in self.table.player_card_buttons if c.clickable_button_id == our_card_number]
        return poss_card[0].card

    def allocate_cards_after_deal(self, player):
        is_human = type(player) == HumanPlayer
        for card_button, card in zip(player.card_buttons, player.initial_card_list):
            card_button.card = card
            card_button.show(face_up=is_human)
            if is_human:
                card_button.make_clickable()

    def set_box_buttons(self, player_has_box):
        self.active_box_buttons = self.table.comp_box_buttons
        if player_has_box:
            self.active_box_buttons = self.table.player_box_buttons

    def transfer_card_to_box(self, origin_player, card):
        box_size = len([b for b in self.active_box_buttons if b.card]) + 1
        self.active_box_buttons[box_size - 1].card = card
        self.active_box_buttons[box_size - 1].show(face_up=False)
        if box_size > 1:
            self.active_box_buttons[box_size - 2].reduce_width()
        origin_cb = [cb for cb in origin_player.card_buttons if cb.card == card][0]
        origin_cb.remove_from_hand()
        origin_cb.card = None

    def turn_up_top_card(self, top_card):
        self.table.face_up_card_buttons[0].card = top_card
        self.table.face_up_card_buttons[0].show(face_up=True)

    def player_picks_card(self, pegging_round):
        self.update_ctrl_btn_text('It\'s your turn!  Click a card to play it')
        card_ok = False
        while not card_ok:
            selected_card = self.wait_for_card()
            card_ok = pegging_round.card_is_small_enough(selected_card)
            if not card_ok:
                self.update_score_info('Cannot play this card, too high.')
        self.hide_played_card(selected_card)
        return selected_card

    def hide_played_card(self, card):
        [cb.remove_from_hand() for cb in self.all_card_buttons if cb.card == card]

    def hand_display(self, hand):
        self.wait_for_ctrl_btn_click(hand.display_button_text)
        self.show_cards_in_list(hand.cards)
        if hand.is_box:
            self.clear_buttons_in(self.table.player_card_buttons + self.table.comp_card_buttons)
        else:
            self.clear_buttons_in(self.table.played_cards_buttons)
        return ''

    def show_cards_in_list(self, card_list, visible=True):
        [cb.show_full_size(face_up=visible) for cb in self.all_card_buttons if cb.card in card_list]

    def clear_buttons_in(self, card_button_list):
        [cb.clear() for cb in card_button_list]

    def clear_box(self):
        self.clear_buttons_in(self.table.player_box_buttons + self.table.comp_box_buttons)


class Player:
    def __init__(self, current_round):
        self.interface = None
        self.hand = None
        self.knocked = False
        self.round = current_round
        self.initial_card_list = []
        self.card_buttons = self.box_buttons = None

    def set_interface(self, interface):
        self.interface = interface

    def receive_cards(self, card_list):
        self.initial_card_list = card_list

    def take_box_turn(self):
        self.hand = Hand(self.initial_card_list, True)

    def check_if_knock_required(self):
        if not self.can_go():
            if self.hand.get_unplayed_cards(self.round.played_cards):
                self.knocked = True

    def can_go(self):
        return any(self.round.card_is_small_enough(c) for c in
                   self.hand.get_unplayed_cards(self.round.played_cards))

    def pick_card_in_pegging(self):
        pass



class ComputerPlayer(Player):
    def __init__(self, current_round):
        super(ComputerPlayer, self).__init__(current_round)
        self.name = 'Computer'

    def set_interface(self, interface):
        super(ComputerPlayer, self).set_interface(interface)
        self.card_buttons = interface.table.comp_card_buttons
        self.box_buttons = interface.table.comp_box_buttons

    def take_box_turn(self):
        self.interface.wait_for_ctrl_btn_click('Add cards to box for computer')
        discards = self.two_cards_for_box(self.initial_card_list)
        for disc in discards:
            self.initial_card_list.remove(disc)
            self.round.box_cards.append(disc)
            self.interface.transfer_card_to_box(self, disc)
            self.interface.update_score_info('Computer adds ' + str(disc) + ' to box')
        self.hand = Hand(self.initial_card_list, False)
        self.interface.update_score_info('')
        super(ComputerPlayer, self).take_box_turn()

    def check_if_knock_required(self):
        super(ComputerPlayer, self).check_if_knock_required()
        self.interface.update_score_info(self.round.last_score_comment + '\tComputer knocks.')

    def pick_card_in_pegging(self):
        self.interface.wait_for_ctrl_btn_click(self.name + '\'s turn')
        selected_card = self.card_to_play()
        self.interface.hide_played_card(selected_card)
        return selected_card

    def two_cards_for_box(self, dealt_hand):
        final_selection = []
        all_triplets_scored = []

        all_pairs = find_all_possible_pairs_in(dealt_hand)
        for pair in all_pairs:
            triplet = [c for c in dealt_hand if c not in pair]
            all_triplets_scored.append([triplet, HandScore(Hand(triplet, False)).points_value])

        self.refine_box_selection(all_triplets_scored)
        all_triplets_scored.sort(key=lambda tr: tr[1], reverse=True)

        #        print('All triplets, scored:')
        #        for tr in all_triplets_scored:
        #            print([str(c) for c in tr[0]], str(tr[1]))

        # discard the two cards that are not in the highest-scoring triplet:
        desired_triplet = all_triplets_scored[0][0]
        final_selection = [c for c in dealt_hand if c not in desired_triplet]
        return final_selection

    def refine_box_selection(self, all_trios):
        for sel in all_trios:
            sel[1] += self.evaluate_run_potential(sel[0])
            sel[1] += self.evaluate_flush_extension_potential(sel[0])
            sel[1] += self.evaluate_fifteen_potential(sel[0])
            sel[1] += self.evaluate_knob_potential(sel[0])

    def evaluate_run_potential(self, triplet):
        strong_run_potential = weak_run_potential = 0
        pairs = find_all_possible_pairs_in(triplet)
        for pr in pairs:
            if pr[0].rank + pr[1].rank == 3 or pr[0].rank + pr[1].rank == 25:
                weak_run_potential += 3 * 1 / 13
            #                print('Weak run potential for A2 or QK')
            elif abs(pr[0].rank - pr[1].rank) == 2:
                weak_run_potential += 3 * 1 / 13
            #                print('Weak run potential for two cards 2 apart')
            elif abs(pr[0].rank - pr[1].rank) == 1:
                strong_run_potential += 3 * 2 / 13
        #                print('Strong run potential')
        return strong_run_potential + weak_run_potential

    def evaluate_flush_extension_potential(self, triplet):
        suits_found = set([t.suit for t in triplet])
        if len(suits_found) == 1:
            #            self.round.update_score_info('flush extension potential: ' + str([str(t) for t in triplet]))
            return 10 / 47
        return 0

    def evaluate_fifteen_potential(self, triplet):
        additional_likely_points = len([t for t in triplet if t.value == 5])
        pairs = find_all_possible_pairs_in(triplet)
        additional_likely_points += len([pr for pr in pairs if pr[0].value + pr[1].value == 5])
        #        if additional_likely_points > 0:
        #            self.round.update_score_info(str([str(t) for t in triplet]) + 
        #                                          ' Extra fifteen potential x' + 
        #                                          str(additional_likely_points))
        return additional_likely_points * 2 * 4 / 13

    def evaluate_knob_potential(self, triplet):
        # I am double-rating the score instead of just adding to the score for hands that have the J
        # and taking away from hands that don't.  Only care about RELATIVE value of hands.  Is this right??
        if self.round.player_has_box:
            knob_potential = len([t for t in triplet if t.rank == 11]) * 2 * 12 / 51
            #            self.round.update_score_info('Knob potential: ' + str([str(t) for t in triplet]) + 
            #                                         str(knob_potential))
            return knob_potential
        return 0

    def card_to_play(self):
        cards_down = self.round.played_cards
        available_cards = [c for c in self.round.comp_cards if
                           c not in cards_down and self.round.card_is_small_enough(c)]
        if len(available_cards) == 1:
            return available_cards[0]

        card_scores = []
        of_a_kind_scores = {0: 0, 1: 2, 2: 6, 3: 12}
        for c in available_cards:
            score = 0
            if len(cards_down) > 0 and c.rank == cards_down[-1].rank:
                score += of_a_kind_scores[self.round.of_a_kind_count]
            score += runs_in_pegging(cards_down + [c])
            score += 2 * (self.round.running_total + c.value in [15, 31])
            if self.round.running_total == 0 and c.rank == 5:
                score = -1
            card_scores.append([c, score])
        card_scores.sort(key=lambda i: i[1])
        #        print('card_scores:', [str(cs[0]) + ' ' + str(cs[1]) for cs in card_scores])
        return card_scores[-1][0]


class HumanPlayer(Player):
    def __init__(self, round):
        super(HumanPlayer, self).__init__(round)
        self.name = 'Player'

    def set_interface(self, interface):
        super(HumanPlayer, self).set_interface(interface)
        self.card_buttons = interface.table.player_card_buttons
        self.box_buttons = interface.table.player_box_buttons

    def take_box_turn(self):
        box_string = ''
        for n in range(2):
            self.interface.update_ctrl_btn_text('Click on two cards to add them to the box')
            card_for_box = self.interface.wait_for_card()
            self.initial_card_list.remove(card_for_box)
            self.round.box_cards.append(card_for_box)
            box_string += str(card_for_box)
            self.interface.transfer_card_to_box(self, card_for_box)
            self.interface.update_score_info('Card added to box: ' + box_string)
        self.interface.update_score_info('Cards added to box: ' + box_string)
        super(HumanPlayer, self).take_box_turn()

    def check_if_knock_required(self):
        super(HumanPlayer, self).check_if_knock_required()
        self.interface.wait_for_ctrl_btn_click('Knock')

    def pick_card_in_pegging(self):
        return self.interface.player_picks_card(self.round)


class PegBoard():

    def __init__(self, my_pegs, comp_pegs):
        self.comp_pegs = PegRow(comp_pegs)
        comp_pegs.configure(fg='blue')
        comp_pegs.grid(row=0)
        self.my_pegs = PegRow(my_pegs)
        my_pegs.grid(row=1)

    def increment_row_by(self, is_player, point_incr, back_peg_moves=True):
        pegs_dict = {True: self.my_pegs, False: self.comp_pegs}
        return pegs_dict[is_player].increment_by(point_incr, back_peg_moves)

    def reset(self):
        self.my_pegs.reset()
        self.comp_pegs.reset()


class PegRow():
    empty_peg_row = '¦' + ((WIN_SCORE // 5) * (5 * '.' + '¦'))
    peg = '\u2022'

    def __init__(self, screen_label):
        self.screen_label = screen_label
        self.front_peg = self.back_peg = 0
        self.full_peg_row = ''
        if __name__ == '__main__':
            screen_label.configure(font=('courier', 10))
        self.draw_for_new_game()

    def reset(self):
        self.front_peg = self.back_peg = 0
        self.draw_for_new_game()

    def draw_for_new_game(self):
        self.full_peg_row = (self.peg + ' ' + self.empty_peg_row +
                             '  ' + '0'.rjust(4))
        self.draw()

    def draw(self):
        if __name__ == '__main__':
            self.screen_label.configure(text=self.full_peg_row)

    def increment_by(self, points_to_add, move_back_peg=True):
        if points_to_add == 0:
            return self.front_peg

        if move_back_peg:
            self.back_peg = self.front_peg
        self.front_peg += points_to_add

        self.full_peg_row = '  ' + self.empty_peg_row + '  '
        self.insert_peg_for_score(self.back_peg)
        self.insert_peg_for_score(self.front_peg)

        self.full_peg_row += str(self.front_peg).rjust(4)

        if __name__ == '__main__':
            self.draw()
        return self.front_peg

    def insert_peg_for_score(self, peg_value):
        peg_position = self.calc_peg_pos(peg_value)
        self.full_peg_row = (self.full_peg_row[:peg_position] + self.peg +
                             self.full_peg_row[peg_position + 1:])

    def calc_peg_pos(self, score):
        ''' give the position in an full peg row (with two spaces at each end) for a given absolute score'''
        if score == 0:
            return 0
        if score >= WIN_SCORE:
            return WIN_SCORE + (WIN_SCORE // 5) + 3
        fives = score // 5
        ones = score % 5

        position = (fives * 6) - 1 + ones + 2
        if ones > 0:
            position += 1
        return position


class Pack():
    def __init__(self):
        self.pack = [Card(rank, suit) for rank in range(1, 14) for suit in SUITS]
        random.shuffle(self.pack)

    def deal(self, how_many_cards):
        return [self.pack.pop() for n in range(how_many_cards)]


class Card():
    picdic = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = rank
        if rank in range(11, 14):
            self.value = 10

    def __str__(self):
        if self.rank in self.picdic:
            return self.picdic[self.rank] + self.suit
        return str(self.value) + self.suit


def find_all_possible_pairs_in(hand):
    return list(itertools.combinations(hand, 2))


def pair_counter(list_of_pairs, matching_test, value=0):
    expr = lambda pr: matching_test(pr, value)
    return len([i for i in filter(expr, list_of_pairs)])


def is_pair(two_cards, unused_value=0):
    return two_cards[0].rank == two_cards[1].rank


def its_a_run(card_list):
    no_of_cards = len(card_list)
    ranks = [c.rank for c in card_list]
    if max(ranks) == min(ranks) + no_of_cards - 1:
        if len(set(ranks)) == no_of_cards:
            return True
    return False


def runs_in_pegging(cards_played):
    cumulative = 0
    no_of_cards = len(cards_played)

    if no_of_cards >= 3:
        # check if 31 was reached, and if so, ignore the cards that got there:
        for i, c in enumerate(cards_played):
            cumulative += c.value
            if cumulative == 31 and not len(cards_played) == i + 1:
                # if 31 was reached, use cards starting after the card that
                # got the total to 31 - unless it's the last card played
                cards_played = cards_played[i + 1:]
                break
            elif cumulative > 31:
                cards_played = cards_played[i:]
                break

    no_of_cards = len(cards_played)
    if no_of_cards >= 3:
        for starting_point in range(no_of_cards - 2):
            sequence = cards_played[starting_point:]
            if its_a_run(sequence):
                return len(sequence)
    return 0


def pluralise_if_necessary(word, count):
    if count > 1:
        return word + 's'
    return word


class Hand:
    def __init__(self, cards, belongs_to_player):
        self.cards = cards
        self.belongs_to_player = belongs_to_player
        self.is_box = len(cards) == 4
        self.display_button_text = self.set_display_button_text()

    def set_display_button_text(self):
        owner_dict = {True: 'my', False: 'computer\'s'}
        box_or_hand_dict = {True: 'box', False: 'hand'}
        owner = owner_dict[self.belongs_to_player]
        hand_or_box = box_or_hand_dict[self.is_box]
        return 'Show ' + owner + ' ' + hand_or_box

    def get_unplayed_cards(self, played_already):
        return [c for c in self.cards if c not in played_already]

    def __str__(self):
        return str([str(c) for c in self.cards])


class HandScore:
    def __init__(self, hand, face_up_card=None):
        self.points_value = 0
        self.description = ''
        self.hand_cards = hand.cards
        self.all_cards = hand.cards
        self.face_up_card = face_up_card
        if face_up_card:
            self.all_cards = hand.cards + [face_up_card]
        self.two_pairs = False
        self.calculate()

    def calculate(self):
        [getattr(self, m)() for m in self.__dir__() if 'count' in m]
        if self.points_value in [4, 5] and self.two_pairs:
            self.description = 'Morgan\'s Orchard'
            if self.points_value == 5:
                self.description += ' and one for his knob'
        if self.points_value == 0:
            self.description = 'zero points'
            if not [c for c in self.all_cards if c.rank % 2 == 1]:
                self.description = 'two, four, six, eight, Blotchy Bob!'

    def count_fifteens(self):
        instances = 0
        for combo_length in range(2, len(self.all_cards) + 1):
            for combo in itertools.combinations(self.all_cards, combo_length):
                if sum([card.value for card in list(combo)]) == 15:
                    instances += 1
        self.points_value += instances * 2
        for f in range(1, instances + 1):
            self.description += NUMBERS[15] + ' ' + NUMBERS[f * 2] + ', '
        return

    def count_runs(self):
        # get every combination from length of hand downwards
        # if the whole hand is a run, can stop there
        instances = length = 0
        for run_length in range(len(self.all_cards), 2, -1):
            combos = itertools.combinations(self.all_cards, run_length)
            for comb in combos:
                if its_a_run(comb):
                    instances += 1
                    length = run_length
            if instances:
                self.points_value += instances * length
                run_or_runs = pluralise_if_necessary(' run', instances)
                self.description += NUMBERS[instances] + run_or_runs + ' of ' + NUMBERS[length] + ', '
                break
        return

    def count_flush(self):
        flush_suit = self.all_cards[0].suit
        flush_length = len([c for c in self.all_cards if c.suit == flush_suit])
        points_awarded = 0
        if flush_length == len(self.all_cards):
            points_awarded = flush_length
        if len(self.all_cards) == 4 and flush_length == 3 and self.all_cards[-1].suit != flush_suit:
            points_awarded = 3
        if points_awarded:
            self.points_value += points_awarded
            self.description += 'a flush of ' + NUMBERS[points_awarded] + ', '
        return

    def count_pairs(self):
        ct = pair_counter(find_all_possible_pairs_in(self.all_cards), is_pair)
        self.points_value += ct * 2
        if ct:
            self.two_pairs = ct == 2
            self.description += NUMBERS[ct] + pluralise_if_necessary(' pair', ct) + ', '
        return

    def count_knob(self):
        if self.face_up_card:
            if [c for c in self.hand_cards if c.rank == 11 and c.suit == self.face_up_card.suit]:
                self.points_value += 1
                self.description += 'one for his knob'

    def __str__(self):
        desc = self.description
        if desc[-2:] == ', ':
            desc = desc[:-2]
        last_comma = desc.rfind(',')
        if last_comma > 0:
            if 'Bob' not in desc and desc.split()[-2] != 'fifteen':
                desc = desc[:last_comma] + ' and' + desc[last_comma + 1:]
        desc = desc[0].upper() + desc[1:]
        return desc + ' is ' + str(self.points_value)


if __name__ == '__main__':
    the_table = Table()