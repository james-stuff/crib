# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:24:44 2019

@author: j_a_c
"""
import random
import tkinter

HEARTS = '\u2665'
CLUBS = '\u2663'
DIAMONDS = '\u2666'
SPADES = '\u2660'
SUITS = [HEARTS, CLUBS, DIAMONDS, SPADES]
WIN_SCORE = 121
VERSION = '2.0.12'

def make_spacer(owner_frame, text_string, column, min_size):
    my_label = tkinter.Label(owner_frame, text=text_string, fg='green',
                             bg='green')
    my_label.grid(row=0, column=column, sticky='w')
    if min_size > 0:
        owner_frame.grid_columnconfigure(column, minsize=min_size)

class Table():
    colour_dict = {CLUBS: 'black', SPADES: 'black', HEARTS: 'red',
                   DIAMONDS: 'red'}

    def __init__(self):
        self.gui = tkinter.Tk()
        self.gui.title('Crib!          v' + VERSION)
        self.gui.geometry('1250x500')
        self.gui.configure(bg='green')

        # list of the four frames used for showing cards, then lists of their properties that line up:
        self.frame_list = []
        frame_widths = [600, 600, 500, 300]
        frame_rows = [0, 0, 2, 2]
        frame_cols = [0, 1, 0, 2]

        for frm in range(4):
            self.frame_list.append(tkinter.Frame(self.gui, width=frame_widths[frm],
                                            height=150, bg='green'))
            self.frame_list[-1].grid(row=frame_rows[frm],
                      column=frame_cols[frm], sticky='w')

        info_frame = tkinter.Frame(self.gui, bg='green')
        info_frame.grid(row=1, columnspan=3, sticky='we')

        button_frame = tkinter.Frame(self.gui, bg='green', width=220, height=200)
        button_frame.grid(row=2, column=1, sticky='we')
        self.frame_list[2].grid_propagate(False)
        button_frame.grid_propagate(False)
        self.frame_list[3].grid_propagate(False)

        l_pack_cards = []
        for n in range(4):
            l_pack_cards.append(tkinter.Label(self.frame_list[0],
                                              font = ('Arial Bold', 2),
                                              borderwidth=1,
                                              height=29, width=1,
                                              relief='raised'))
            l_pack_cards[-1].grid(column=1 + n, row=0, sticky='w')
        self.bt_blank_card = tkinter.Button(self.frame_list[0],
                                            font=('Arial Bold', 20),
                                            height=3, width=3)
        self.bt_blank_card.grid(column=5, row=0, pady=10)

        make_spacer(self.frame_list[0], '-', 0, 0)
        make_spacer(self.frame_list[0], 20 * '-', 6, 20)
        make_spacer(self.frame_list[1], '-', 19, 200)

        self.btControl = tkinter.Button(button_frame, text='Start new game',
                                        command=self.new_game)
        self.btControl.grid(padx=10, pady=50)

        self.btQuit = tkinter.Button(button_frame, text='Quit',
                                     command=lambda: self.card_var.set(20))
        self.btQuit.grid(row=1, column=0)

        self.score_info = tkinter.StringVar()
        self.l_score = tkinter.Label(info_frame, font=('Helvetica', 12),
                                     textvariable=self.score_info)
        self.peg_board = PegBoard(tkinter.Label(info_frame),
                                  tkinter.Label(info_frame))

        make_spacer(self.frame_list[2], 39 * '-', 0, 0)

        self.card_var = tkinter.IntVar()

        self.gui.mainloop()

    def new_game(self):
        while True:
            game = Game(self)
            game.play()

    def display_card(self, widget, card):
        ''' show a card, making it the right colour, depending on its suit '''
        widget.configure(text=str(card), fg=self.colour_dict[card.suit])

    def await_control_button_click(self, instruction):
        self.card_var.set(-1)
        while self.card_var.get() != 19:
            self.btControl.configure(text=instruction)
            self.btControl.wait_variable(self.card_var)
            if self.card_var.get() == 20:
                self.gui.destroy()
                break

class Game():
    def __init__(self, table):
        self.table = table

    def play(self):
        self.win_detected = False
        self.player_has_box = random.randrange(2)
        self.table.btControl.configure(command=lambda: self.table.card_var.set(19))
        self.table.score_info.set('')
        self.table.l_score.configure(bg='green')
        self.table.peg_board.reset()
        this_round = None

        while not self.win_detected:
            self.is_players_turn = not self.player_has_box
            self.table.await_control_button_click('Deal for new round')
            if this_round != None:
                this_round.btn_box.destroy_cards()
                del(this_round)
            this_round = Round(self)
            this_round.play_round()
            self.player_has_box = not self.player_has_box
        this_round.btn_box.destroy_cards()
        del(this_round)

class ButtonList():
    ''' a list of on-screen card buttons that allows Round to interact with the UI'''
    def __init__(self, table, card_list, buttons, frame_no, first_column, length):
        self.card_list = card_list
        self.first_column = first_column
        self.table = table
        self.buttons = buttons

        for n in range(length):
            self.buttons.append(tkinter.Button(self.table.frame_list[frame_no],
                                     font=('Arial Bold', 20),
                                     height=3, width=3))

    def populate(self, card_list):
        self.card_list = card_list
        self.clickable_cards = list(range(len(card_list)))

    def show_cards(self, index=-1, face_down=False):
        start_index = 0
        end_index = len(self.card_list)
        if index > -1:
            start_index = index
            end_index = index + 1

        for card_index in range(start_index, end_index):
            if face_down:
                self.buttons[card_index].configure(text='')
            else:
                self.table.display_card(self.buttons[card_index],
                                        self.card_list[card_index])
            self.buttons[card_index].grid(row=0, column=self.first_column +
                                            card_index, pady=10)

    def destroy_cards(self, index=-1, destroy_button=True):
        start_index = 0
        end_index = len(self.card_list)
        if index > -1:
            start_index = index
            end_index = index + 1

        for b in self.buttons[start_index:end_index]:
            b.configure(text='')
            b.grid_forget()

        if destroy_button and index > -1:
            del(self.buttons[start_index])
            del(self.clickable_cards[index])

class Round():
    def __init__(self, game=None, cards=[], comp_cards=[]):
        self.real_mode = False

        # gameplay variables:
        self.my_cards = cards
        self.comp_cards = comp_cards
        self.box = []
        self.played_cards = []
        self.running_total = 0
        self.of_a_kind_count = 1
        self.comp_knock = self.player_knock = False
        self.turn_over_played_cards_on_next_turn = False
        self.last_score_comment = ''
        self.the_pack = Pack()
        self.face_up_card = Card(0, '')
        self.computer = SmartComputer(self)
        self.who_has_it = {True: 'You have', False: 'Computer has'}

        if isinstance(game, Game):
            self.real_mode = True
            self.game = game

            self.card_var = tkinter.IntVar()
            self.card_var.set(0)

            self.b_my_cards = []
            self.b_comp_cards = []
            self.b_played_cards = []
            self.b_comp_box = []
            self.b_my_box = []
            self.b_face_up = []

            self.player_has_box = self.game.player_has_box
            tbl = self.game.table
            if self.player_has_box:
                target_box = self.b_my_box
                frame = 3
            else:
                target_box = self.b_comp_box
                frame = 1
            self.btn_box = ButtonList(tbl, self.box, target_box, frame, 21, 4)
            self.btn_played = ButtonList(tbl, self.played_cards,
                                         self.b_played_cards, 1, 12, 6)
            self.btn_player_hand = ButtonList(tbl, self.my_cards, self.b_my_cards,
                                              2, 2, 5)
            self.btn_comp_hand = ButtonList(tbl, self.comp_cards,
                                            self.b_comp_cards, 0, 7, 5)
            tbl.bt_blank_card.grid_forget()
            self.btn_face_up = ButtonList(tbl, [self.face_up_card],
                                          self.b_face_up, 0, 5, 1)
            self.btn_face_up.show_cards(0, True)

            # hard-coding: surely there's a better way to do this?
            self.b_my_cards[0].configure(command=lambda: self.card_var.set(0))
            self.b_my_cards[1].configure(command=lambda: self.card_var.set(1))
            self.b_my_cards[2].configure(command=lambda: self.card_var.set(2))
            self.b_my_cards[3].configure(command=lambda: self.card_var.set(3))
            self.b_my_cards[4].configure(command=lambda: self.card_var.set(4))

            self.button_colour = self.b_my_cards[0].cget('bg')
        else:
            self.output_file = open('MonteCarloOutput' + VERSION + '.txt', 
                                    'a', encoding='utf-8')

    def await_card_click(self):
        ''' wait for player to click a card.  Tell me the index of the card chosen'''
        self.card_var.set(-1)
        while self.card_var.get() < 0 or self.card_var.get() > 4:
            self.b_my_cards[0].wait_variable(self.card_var)
        return self.card_var.get()

    def update_score_info(self, info_to_display):
        ''' update label on table, or print to console if in test mode '''
        if self.real_mode:
            self.game.table.score_info.set(info_to_display)
            self.game.table.l_score.grid(row=2, pady=2)
            self.game.table.l_score.configure(bg=self.button_colour)
            if len(info_to_display) == 0:
                self.game.table.l_score.configure(bg='green')
        elif len(info_to_display) > 0:
            self.output_file.writelines(info_to_display + '\n')

    def ui_btn_update(self, button_text):
        ''' change what is written on the control button'''
        if self.real_mode:
            self.game.table.btControl.configure(text=button_text)

    def ui_wait_for_click(self, button_text):
        ''' change the text on the control button and wait for user to click it '''
        if self.real_mode:
            self.game.table.await_control_button_click(button_text)

    def ui_wait_for_card(self):
        ''' wait for the player to select a card, and tell me what they've chosen'''
        clickable_card = self.await_card_click()
        return self.btn_player_hand.clickable_cards.index(clickable_card)

    def ui_transfer_card_to_box(self, card_index):
        if self.real_mode:
            cards_in_box = len(self.box)
            self.btn_box.show_cards(cards_in_box - 1, True)
            if self.is_players_turn:
                self.btn_player_hand.destroy_cards(card_index)
            else:
                self.btn_comp_hand.destroy_cards(0)

    def ui_update_played_cards(self):
        if self.real_mode:
            no_of_cards_down = len(self.played_cards)
            if no_of_cards_down > 1:
                if self.turn_over_played_cards_on_next_turn:
                    # this means 31 or double-knock, so clear previously-played cards here:
                    self.btn_played.show_cards(face_down=True)
                    self.turn_over_played_cards_on_next_turn = False
                self.btn_played.buttons[no_of_cards_down - 2].configure(width=2,
                                   font=('Arial Bold', 12), anchor='nw',
                                   height=5)
            self.btn_played.show_cards(no_of_cards_down - 1)

    def ui_pegging(self, whose_turn, points_to_add, back_peg_moves=True):
        if self.real_mode:
            return self.game.table.peg_board.increment_row_by(whose_turn,
                                                              points_to_add,
                                                              back_peg_moves)
        return 0

    def play_round(self):
        self.deal()
        if not self.real_mode:
            self.player_has_box = random.randrange(2)
        self.is_players_turn = not self.player_has_box

        self.build_box()
        self.turn_up_top_card()
        self.pegging_round()
        self.hand_display(not self.player_has_box)
        self.hand_display(self.player_has_box)
        self.hand_display(self.player_has_box, is_box=True)
        if self.real_mode and self.game.win_detected:
            self.ui_wait_for_click('Start new game')
            self.btn_face_up.show_cards(face_down=True)
        if not self.real_mode:
            self.output_file.close()

    def deal(self):
        if len(self.my_cards) == 0:
            self.my_cards = self.the_pack.deal(5)
        if len(self.comp_cards) == 0:
            self.comp_cards = self.the_pack.deal(5)

        if self.real_mode:
            self.btn_player_hand.populate(self.my_cards)
            self.btn_player_hand.show_cards()
            self.btn_comp_hand.populate(self.comp_cards)
            self.btn_comp_hand.show_cards(face_down=True)

    def build_box(self):
        who_has_box = self.who_has_it[self.player_has_box] + ' the box'
        self.update_score_info(who_has_box)

        while len(self.box) < 4:
            if self.is_players_turn:
                initial_box_size = len(self.box)
                box_string = ''
                while len(self.box) < initial_box_size + 2:
                    if self.real_mode:
                        self.ui_btn_update('Click on two cards to add them ' +
                                           'to the box')
                        card_for_box = self.my_cards[self.ui_wait_for_card()]
                    else:
                        card_for_box = self.my_cards[-1]
                    self.box.append(card_for_box)
                    # find and remove the card from player's hand
                    ind = self.my_cards.index(card_for_box)
                    del(self.my_cards[ind])
                    box_string += str(card_for_box)
                    if len(box_string) < 4:
                        self.update_score_info('Card added to box: ' + box_string)
                    self.ui_transfer_card_to_box(ind)
                self.update_score_info('Cards added to box: ' + box_string)
                self.is_players_turn = False
            else:
                # computer adds two cards to the box
                self.ui_wait_for_click('Add cards to box for computer')
                discards = self.computer.two_cards_for_box(self.comp_cards)
#                print('computer discards:', [str(d) for d in discards])
#                print('computer still has:', [str(x) for x in self.comp_cards])
                for disc in discards:
                    self.comp_cards.remove(disc)
                    self.box.append(disc)
                    self.ui_transfer_card_to_box(disc)
                    if not self.real_mode:
                        self.update_score_info('Computer adds ' + str(disc) +
                                               ' to box')
                self.update_score_info('')
                self.is_players_turn = True

    def turn_up_top_card(self):
        # Turn up the next card, Two for his heels check:
        self.face_up_card = self.the_pack.deal(1)[0]
        if self.real_mode:
            self.btn_face_up.populate([self.face_up_card])
            self.btn_face_up.show_cards()
        else:
            self.update_score_info('Card turned up: ' + str(self.face_up_card))
        if self.face_up_card.rank == 11:
            heels_notification = 'Two for his heels!'
            updated_score = self.ui_pegging(self.player_has_box, 2)
            heels_notification += self.check_for_win(self.player_has_box, updated_score)
            self.update_score_info(heels_notification)

    def pegging_round(self):
        while len(self.played_cards) < 6:
            self.check_if_knock_required()
            if self.is_players_turn and not self.player_knock:
                card_to_play = self.player_picks_card()
            elif not self.is_players_turn and not self.comp_knock:
                card_to_play = self.computer_picks_card()
            else:
                card_to_play = None
                
            if type(card_to_play) == Card:
                self.play_card(card_to_play)
                self.ui_update_played_cards()
            self.is_players_turn = not self.is_players_turn

            # when to reset to zero:
            if self.running_total == 31:
                self.reset_variables_at_31()
            elif len(self.played_cards) == 6:
                self.award_go_point()
            elif self.comp_knock == self.player_knock == True:
                self.award_go_point()
                self.reset_variables_at_31()
                self.is_players_turn = not self.played_cards[-1] in self.my_cards
                
    def check_if_knock_required(self):
        if not self.can_go():
            if self.is_players_turn:
                self.ui_wait_for_click('Knock')
                self.player_knock = True
            else:
                self.comp_knock = True
                self.update_score_info(self.last_score_comment +
                                       '\tComputer knocks.')

    def can_go(self):
        turn_dict = {True: self.my_cards, False: self.comp_cards}
        whose_hand = turn_dict[self.is_players_turn]
        return any(c not in self.played_cards and self.can_play_card(c) 
                   for c in whose_hand)

    def can_play_card(self, card):
        return self.running_total + card.value <= 31
    
    def player_picks_card(self):
        self.ui_btn_update('It\'s your turn!  Click a card to play it')
        if self.real_mode:
            card_ok = False
            while not card_ok:
                card_index = self.ui_wait_for_card()
                selected_card = self.my_cards[card_index]
                card_ok = self.can_play_card(selected_card)
                if not card_ok:
                    self.update_score_info('Cannot play this card, too high.')
            self.btn_player_hand.destroy_cards(card_index, False)
        else:
            available_cards = [c for c in self.my_cards if c not in self.played_cards]
            for card in available_cards:
                if self.can_play_card(card):
                    selected_card = card
                    break
        return selected_card

    def computer_picks_card(self):
        self.ui_wait_for_click('Computer\'s turn')
        if self.real_mode:
            # remove the right-most computer card button from screen:
            comp_cards_left = 2
            for cd in self.comp_cards:
                if cd in self.played_cards:
                    comp_cards_left -= 1
            self.btn_comp_hand.destroy_cards(comp_cards_left, False)
        return self.computer.card_to_play()

    def play_card(self, card_played):
        ''' see if this card gets any points and show new scores when a valid card is played'''
        for_text = ''
        run_tot_text = str(self.running_total)
        self.update_round_state_with_played_card(card_played)
        turn_score = self.points_scored_by_played_card()
        total_score = self.ui_pegging(self.is_players_turn, turn_score)

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
        if not self.real_mode:
            dict_who = {True: 'Player  ', False: 'Computer'}
            player = dict_who[self.is_players_turn]
            score_string = player + ' : ' + str(card_played) + '\t' + score_string
        self.update_score_info(score_string)

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
        points_for_pairs = 0
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
            score_string = self.last_score_comment[:start_of_for + 6].rstrip() + ' and a go is ' + str(last_score)
            updated_score = self.ui_pegging(player_gets_go_point, 1, False)
        else:
            updated_score = self.ui_pegging(player_gets_go_point, 1)
            score_string = str(self.running_total) + ' for 1'

        if just_won:
            score_string += ' ' + self.last_score_comment[start_of_for + 6:]
        else:
            score_string += self.check_for_win(player_gets_go_point, updated_score)

        self.update_score_info(score_string)

    def check_for_win(self, player_just_scored, score):
        congrats = ''
        if self.real_mode:
            if score >= WIN_SCORE and not self.game.win_detected:
                self.game.win_detected = True
                congrats = ' -- ' + self.who_has_it[player_just_scored].upper() + ' WON!!!'
        return congrats

    def reset_variables_at_31(self):
        self.running_total = 0
        self.of_a_kind_count = 0
        self.comp_knock = self.player_knock = False
        self.turn_over_played_cards_on_next_turn = True
        self.last_score_comment = ''

    def hand_display(self, is_player, is_box=False):
        if is_player:
            card_list = self.my_cards
            owner = 'my'
            if self.real_mode:
                button_list = self.btn_player_hand
        else:
            card_list = self.comp_cards
            owner = 'computer\'s'
            if self.real_mode:
                button_list = self.btn_comp_hand

        if is_box:
            hand_or_box = ' box'
            card_list = self.box
            if self.real_mode:
                button_list = self.btn_box
        else:
            hand_or_box = ' hand'

        self.ui_wait_for_click('Show ' + owner + hand_or_box)
        int_score, text_score = score_hand(card_list + [self.face_up_card],
                                          is_box)
        str_info = text_score + ' is ' + str(int_score)
        if not self.real_mode:
            str_info = str([str(c) for c in card_list]) + str_info

        if self.real_mode:
            # clear the played cards (and if appropriate, hands), before displaying the cards:
            self.btn_played.destroy_cards()
            if is_box:
                self.btn_player_hand.destroy_cards()
                self.btn_comp_hand.destroy_cards()
            button_list.show_cards()

        new_score = self.ui_pegging(is_player, int_score)
        str_info += self.check_for_win(is_player, new_score)
        self.update_score_info(str_info)

class SmartComputer():

    def __init__(self, current_round):
        self.round = current_round

    def two_cards_for_box(self, dealt_hand):
        final_selection = []
        all_triplets_scored = []

        all_pairs = find_all_possible_pairs_in(dealt_hand)
        for pair in all_pairs:
            triplet = [c for c in dealt_hand if c not in pair]
            all_triplets_scored.append([triplet, score_hand(triplet)[0]])
           
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
                weak_run_potential += 3 * 1/13
#                print('Weak run potential for A2 or QK')
            elif abs(pr[0].rank - pr[1].rank) == 2:
                weak_run_potential += 3 * 1/13
#                print('Weak run potential for two cards 2 apart')
            elif abs(pr[0].rank - pr[1].rank) == 1:
                strong_run_potential += 3 * 2/13
#                print('Strong run potential')
        return strong_run_potential + weak_run_potential
    
    def evaluate_flush_extension_potential(self, triplet):
        suits_found = set([t.suit for t in triplet])
        if len(suits_found) == 1:
#            self.round.update_score_info('flush extension potential: ' + str([str(t) for t in triplet]))
            return 10/47
        return 0
    
    def evaluate_fifteen_potential(self, triplet):
        additional_likely_points = len([t for t in triplet if t.value == 5])
        pairs = find_all_possible_pairs_in(triplet)
        additional_likely_points += len([pr for pr in pairs if pr[0].value + pr[1].value == 5])
#        if additional_likely_points > 0:
#            self.round.update_score_info(str([str(t) for t in triplet]) + 
#                                          ' Extra fifteen potential x' + 
#                                          str(additional_likely_points))
        return additional_likely_points * 2 * 4/13
    
    def evaluate_knob_potential(self, triplet):
        # I am double-rating the score instead of just adding to the score for hands that have the J
        # and taking away from hands that don't.  Only care about RELATIVE value of hands.  Is this right??
        if self.round.player_has_box:
            knob_potential = len([t for t in triplet if t.rank == 11]) * 2 * 12/51
#            self.round.update_score_info('Knob potential: ' + str([str(t) for t in triplet]) + 
#                                         str(knob_potential))
            return knob_potential
        return 0
        

    def card_to_play(self):
        cards_down = self.round.played_cards
        available_cards = [c for c in self.round.comp_cards if 
                           c not in cards_down and self.round.can_play_card(c)]
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
                            '  ' +  '0'.rjust(4))
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
        # generate the pack of 52 cards:
        self.pack = []

        for suit in SUITS:
            for number in range(1, 14):
                self.pack.append(Card(number, suit))
        random.shuffle(self.pack)

    def deal(self, how_many_cards):
        return [self.pack.pop() for n in range(how_many_cards)]

class Card():
    picdic = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

        if rank <= 10:
            self.value = rank
        elif rank in range(11, 14):
            self.value = 10

    def __str__(self):
        if self.rank in self.picdic:
            return self.picdic[self.rank] + self.suit
        return str(self.value) + self.suit

def find_all_possible_pairs_in(hand):
    pairs = []
    for ind, card in enumerate(hand[:-1]):
        for c in hand[ind + 1:]:
            pairs.append([card, c])
    return pairs

def pair_counter(list_of_pairs, matching_test, value=0):
    expr = lambda pr: matching_test(pr, value)
    return len([i for i in filter(expr, list_of_pairs)])

def is_pair(two_cards, unused_value=0):
    return two_cards[0].rank == two_cards[1].rank

def adds_up_to(two_cards, target_value):
    return two_cards[0].value + two_cards[1].value == target_value

def find_runs(cards):
    result = []
    run_structure = [1]  # for a run, will be no. of each rank in run
                        # e.g. for A,2,2,3 will be [1, 2, 1]
    last_card = cards[0].rank
    for c in cards[1:]:
        this_card = c.rank
        if this_card == last_card:
            run_structure[-1] += 1
        elif this_card == last_card + 1:
            run_structure.append(1)
        elif len(run_structure) >= 3:
            break
        else:
            run_structure = [1]
        last_card = this_card

    if len(run_structure) >= 3:
        number_of_runs = 1
        for r in run_structure:
            number_of_runs *= r
        result = [number_of_runs, len(run_structure)]

    return result

def runs_in_pegging(cards_played):
    run_length = cumulative = 0
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
        for l in range(no_of_cards - 2):
            seq = [c.rank for c in cards_played[l:]]
            if max(seq) == min(seq) + len(seq) - 1 and \
                    len(set(seq)) == len(seq):
                return len(seq)
    return run_length

def flush_points(hand):
    flush_suit = hand[0].suit
    flush_length = len([c for c in hand if c.suit == flush_suit])
    if flush_length == len(hand):
        return flush_length
    if len(hand) == 4 and flush_length == 3 and hand[-1].suit != flush_suit:
        return 3
    return 0

def score_hand(hand, is_box=False):
    score_int = 0
    score_text = ''
    numbers = ['zero', 'a', 'two', 'three', 'four', 'five', 'six', 'seven',
               'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 
               'fourteen', 'fifteen', 'sixteen']

    all_pairs = find_all_possible_pairs_in(hand)

    # how many fifteens?
    fifteens = pair_counter(all_pairs, adds_up_to, 15) # any pairs that add up to 15?
    for index, card in enumerate(hand[:-1]): # any triplets?
        first_card_value = card.value
        pairs_to_make_triplets = find_all_possible_pairs_in(hand[index + 1:])
        fifteens += pair_counter(pairs_to_make_triplets, adds_up_to, 15 - first_card_value)
    if len(hand) > 4: # box scenario, do any combos of four cards add up to 15?
        for card in hand:
            reduced_hand = hand.copy()
            reduced_hand.remove(card)
            fifteens += sum([c.value for c in reduced_hand]) == 15
    if len(hand) > 3: # do all the cards in the hand add up to 15?
        fifteens += sum([c.value for c in hand]) == 15

    score_int = fifteens * 2
    for f in range(1, fifteens + 1):
        score_text += what_to_append_to_score_text(score_text, numbers[15] + 
                                                   ' ' + numbers[f*2])

    # Any runs?
    sorted_hand = sorted(hand, key = lambda c: c.rank)
    run_results = find_runs(sorted_hand)
    if len(run_results):
        score_int += run_results[0] * run_results[1]
        if run_results[0] == 1:
            score_text += what_to_append_to_score_text(score_text, 'a run of ')
        elif run_results[0] > 1:
            score_text += what_to_append_to_score_text(score_text, 
                                                       numbers[run_results[0]] + ' runs of ')
        score_text += numbers[run_results[1]]

    # Any flushes?
    flush_length = flush_points(hand)
    if flush_length > 2:
        score_int += flush_length
        score_text += what_to_append_to_score_text(score_text, 'a flush of ' + 
                                                   numbers[flush_length])

    # How many pairs?
    pairs = pair_counter(all_pairs, is_pair)
    score_int += pairs * 2
    if pairs > 0:
        score_text += what_to_append_to_score_text(score_text, numbers[pairs] + ' pair')
        if pairs > 1:
            score_text += 's'

    if score_int == 4 and pairs == 2:
        score_text = 'Morgan\'s Orchard'

    # one for his knob (assumes face-up card was appended to hand)
    if len(hand) > 3:
        knob = [c for c in hand[:-1] if c.rank == 11 and c.suit == hand[-1].suit]
        if len(knob) == 1:
            score_int += 1
            score_text += what_to_append_to_score_text(score_text, 'one for his knob')

    if score_int == 0:
        odd_card_found = len([c for c in hand if c.rank % 2 == 1])
        if not odd_card_found:
            score_text = 'two, four, six, eight, Blotchy Bob!'
        else:
            score_text = 'zero points'

    score_text = score_text[0].upper() + score_text[1:]

    # slip in an 'and' at the end if there are multiple scoring types
    last_comma = score_text.rfind(',')
    if last_comma > 0:
        if 'Bob' not in score_text and not score_int == fifteens * 2:
            score_text = score_text[:last_comma] + ' and' + score_text[last_comma + 1:]

    return (score_int, score_text)

def what_to_append_to_score_text(score_string, latest_addition):
    if len(score_string) > 0:
        return ', ' + latest_addition
    return latest_addition

if __name__ == '__main__':
    the_table = Table()