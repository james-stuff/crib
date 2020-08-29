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
NUMBERS = ['zero', 'a', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
           'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen']
VERSION = '2.1.9'
# TODO: box score for ComputerPlayer has gone down slightly.  Is this worthy of investigation?

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
        self.peg_rows = []
        for n in range(2):
            self.peg_rows.append(PegRow(tkinter.Label(info_frame)))
            self.peg_rows[-1].screen_label.grid(row=n)

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
        [pr.reset() for pr in self.peg_rows]

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
        self.players = [HumanPlayer(), ComputerPlayer()]
        for ind, pl in enumerate(self.players[::-1]):
            pl.pegs = self.table.peg_rows[ind]
            pl.pegs.game = self
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

    def record_win(self, calling_peg_row):
        self.win_detected = True
        player = [p for p in self.players if p.pegs is calling_peg_row][0]
        self.table.score_info.set(self.table.score_info.get() +
                                  f' -- {player.ownership_string.upper()} WON!!!')


class Round:
    dict_31 = {1: 'one-ty', 2: 'two\'s in time', 3: 'three\'s awake',
               4: 'four\'s in heaven', 5: 'five\'s a fix', 6: 'six is alive',
               7: 'sevens galore', 8: 'eight\'s a spree', 9: 'nine\'ll do', 10: '31'}

    def __init__(self, players, game=None):
        self.game = game
        self.players = players
        self.box_cards = []
        self.ps = PeggingSequence()
        self.last_score = 0
        self.the_pack = Pack()
        self.box = self.box_owner = self.face_up_card = None
        self.ordered_players = []
        self.last_card_won_game = False

        if any([p for p in players if type(p) is HumanPlayer]):
            self.player_has_box = self.game.player_has_box
            self.interface = RoundVisualInterface(self.game.table)
        else:
            self.interface = RoundTestInterface()
        [p.set_round_and_interface(self) for p in self.players]
        self.deal()

    def play_round(self):
        if self.game is None:
            self.player_has_box = random.choice([True, False])
        self.box_owner = self.players[not self.player_has_box]
        self.interface.set_box_buttons(self.box_owner)
        lead_index = (self.players.index(self.box_owner) + 1) % len(self.players)
        self.ordered_players = self.players[lead_index:] + self.players[:lead_index]
        # TODO: can I get rid of self.ordered_players and just re-order self.players each round?
        self.build_box()
        self.box = Box(self.box_cards, self.box_owner)
        self.turn_up_top_card()
        self.pegging_round()
        self.put_cards_on_table()
        self.interface.end_of_round_tidy_up()
        return self

    def deal(self):
        [p.receive_cards(self.the_pack.deal(5)) for p in self.players]
        [self.interface.allocate_cards_after_deal(p) for p in self.players]

    def build_box(self):
        self.interface.update_score_info(f'{self.box_owner.ownership_string} the box')
        [p.take_box_turn() for p in self.ordered_players]

    def turn_up_top_card(self):
        self.face_up_card = self.the_pack.deal(1)[0]
        self.interface.turn_up_top_card(self.face_up_card)
        if self.face_up_card.rank == 11:
            self.interface.update_score_info('Two for his heels!')
            self.interface.increment_pegs(self.box_owner, 2)

    def pegging_round(self):
            # TODO: does the computer always knock?  It doesn't when I play the 'go' card
            # . . .  This is unchanged, but is it desirable?
        for player in itertools.cycle(self.ordered_players):
            card_to_play = None
            player.knock_if_required()
            if not player.knocked:
                card_to_play = player.pick_card_in_pegging()
            if isinstance(card_to_play, Card):
                self.play_card(player, card_to_play)
                self.interface.update_played_cards(self.ps)

            if self.need_to_turn_over_played_cards(player):
                self.reset_variables_at_31()
            if len(self.ps) == 6:
                break

    def need_to_turn_over_played_cards(self, whose_turn):
        if self.ps.running_total == 31:
            return True
        if all([pl.knocked for pl in self.players]) or len(self.ps) == 6:
            self.award_go_point(whose_turn)
            return True
        return False

    def reset_variables_at_31(self):
        for p in self.players:
            p.knocked = False
        self.interface.turn_over_played_cards_on_next_turn = True
        self.last_score = 0
        self.ps.reset()

    def card_is_small_enough(self, card):
        return self.ps.card_does_not_break_31(card)

    def play_card(self, player, card_played):
        won_already = self.game and self.game.win_detected
        self.ps.add_card(card_played)
        turn_score = self.ps.get_last_card_points()
        score_string = self.compose_score_string(turn_score)
        self.last_score = turn_score
        self.interface.update_score_info(self.interface.log_card_played(player,
                                                                        card_played, score_string))
        self.interface.increment_pegs(player, turn_score)
        if self.game and not won_already and self.game.win_detected:
            self.last_card_won_game = True

    def award_go_point(self, player):
        if self.last_score:
            score_string = f'{self.compose_score_string(self.last_score)} and a go is ' \
                           f'{self.last_score + 1}'
            self.interface.update_score_info(score_string)
            self.interface.move_front_peg_for_additional_go_point(player)
        else:
            score_string = f'{self.ps.running_total} for 1'
            self.interface.update_score_info(score_string)
            self.interface.increment_pegs(player, 1)

        if self.last_card_won_game:
            self.game.win_detected = False
            player.pegs.check_for_win()

    def compose_score_string(self, added_points):
        score_string = f'{self.running_total_or_31_string()}'
        if added_points:
            score_string += f' for {added_points}'
        return score_string

    def running_total_or_31_string(self):
        if self.ps.running_total == 31 and self.ps[-1].value in self.dict_31:
            return f'{31 - self.ps[-1].value}, {self.dict_31[self.ps[-1].value]}!'
        return f'{self.ps.running_total}'

    def put_cards_on_table(self):
        self.evaluate_hand(self.ordered_players[0].hand)
        self.interface.show_cards_in_list(self.ordered_players[1].hand.cards, visible=False)
        self.evaluate_hand(self.ordered_players[1].hand)
        self.evaluate_hand(self.box)

    def evaluate_hand(self, hand_to_score):
        hs = HandScore(hand_to_score, self.face_up_card)
        self.interface.update_score_info(f'{self.interface.hand_display(hand_to_score)}{hs}')
        self.interface.increment_pegs(hand_to_score.owner, hs.points_value)


class PeggingSequence:
    dict_of_a_kind = {1: 0, 2: 2, 3: 6, 4: 12}

    def __init__(self):
        self.cards_down = []
        self.running_total = 0
        self.cards_of_a_kind = 1

    def __getitem__(self, ind):
        return self.cards_down[ind]

    def __len__(self):
        return len(self.cards_down)

    def __copy__(self):
        ps = PeggingSequence()
        ps.cards_down = self.cards_down
        return ps

    def card_does_not_break_31(self, card):
        return self.running_total + card.value <= 31

    def add_card(self, card):
        self.cards_down.append(card)
        self.running_total += card.value
        if self.running_total > 31:
            self.running_total = card.value
            self.cards_of_a_kind = 0
        if len(self) > 1 and self[-1].rank == self[-2].rank:
            self.cards_of_a_kind += 1
        else:
            self.cards_of_a_kind = 1

    def fifteen_or_thirty_one_score(self):
        return (self.running_total in [15, 31]) * 2

    def pairs_score(self):
        return self.dict_of_a_kind[self.cards_of_a_kind]

    def run_score(self):
        if len(self) >= 3:
            valid_cards = self.cards_down
            if sum([c.value for c in self.cards_down]) > 31:
                if sum([c.value for c in self.cards_down[:4]]) <= 31:
                    return 0
                else:
                    valid_cards = self.cards_down[3:]
            for n_start_card in range(len(valid_cards) - 2):
                if its_a_run(valid_cards[n_start_card:]):
                    return len(valid_cards[n_start_card:])
        return 0

    def get_last_card_points(self):
        return sum([getattr(self, m)() for m in self.__dir__() if '_score' in m])

    def reset(self):
        self.running_total = self.cards_of_a_kind = 0

    def pop_last_card(self):
        self.cards_down.pop()


class RoundInterface:
    def __init__(self):
        self.turn_over_played_cards_on_next_turn = False
        self.active_box_buttons = None

    def increment_pegs(self, whose_turn, points_to_add):
        return 0

    def move_front_peg_for_additional_go_point(self, player):
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
        self.update_score_info(f'Card turned up: {top_card}')

    def log_card_played(self, player, card, score_string):
        return f'{player.name} : {card}\t{score_string}'

    def hand_display(self, hand):
        return str(hand)

    def end_of_round_tidy_up(self):
        self.log_file.close()  # without this, Monte Carlo logging skips many rounds


class RoundVisualInterface(RoundInterface):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.button_colour = table.btControl.cget('bg')
        self.all_card_buttons = table.all_cb
        self.table.face_up_card_buttons[0].card = None
        self.table.face_up_card_buttons[0].show(face_up=False)

    def increment_pegs(self, whose_turn, points_to_add):
        return whose_turn.pegs.increment_by(points_to_add)

    def move_front_peg_for_additional_go_point(self, whose_turn):
        return whose_turn.pegs.extend_for_go_point()

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

    def set_box_buttons(self, player):
        self.active_box_buttons = self.table.comp_box_buttons
        if type(player) == HumanPlayer:
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
        if type(hand) is Box:
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
    def __init__(self, name=None):
        self.interface = None
        self.hand = None
        self.knocked = False
        self.round = None
        self.initial_card_list = []
        self.card_buttons = self.box_buttons = self.pegs = None

    def set_round_and_interface(self, round):
        self.round = round
        self.interface = round.interface

    def receive_cards(self, card_list):
        self.initial_card_list = card_list

    def take_box_turn(self):
        self.hand = Hand(self.initial_card_list, self)

    def knock_if_required(self):
        if not self.get_playable_cards():
            self.knocked = True

    def get_playable_cards(self):
        return [c for c in self.get_unplayed_cards() if self.round.card_is_small_enough(c)]

    def get_unplayed_cards(self):
        return set(self.hand) - set(self.round.ps)

    def pick_card_in_pegging(self):
        pass


class ComputerPlayer(Player):
    def __init__(self, name=None):
        super(ComputerPlayer, self).__init__()
        self.name = 'Computer'
        if name:
            self.name = name
        self.ownership_string = self.name + ' has'
        self.possessive = self.name.lower() + '\'s'

    def set_round_and_interface(self, round):
        super(ComputerPlayer, self).set_round_and_interface(round)
        if type(self.interface) is RoundVisualInterface:
            self.card_buttons = self.interface.table.comp_card_buttons
            self.box_buttons = self.interface.table.comp_box_buttons

    def take_box_turn(self):
        self.interface.wait_for_ctrl_btn_click('Add cards to box for computer')
        discards = self.two_cards_for_box(self.initial_card_list)
        for disc in discards:
            self.initial_card_list.remove(disc)
            self.round.box_cards.append(disc)
            self.interface.transfer_card_to_box(self, disc)
            self.interface.update_score_info(f'{self.name} adds {disc} to box')
        self.interface.update_score_info('')
        super(ComputerPlayer, self).take_box_turn()

    def knock_if_required(self):
        super(ComputerPlayer, self).knock_if_required()
        if self.knocked:
            prev_comment = f'{self.round.ps.running_total}'
            prev_comment += f' for {self.round.last_score}' if self.round.last_score > 0 else ''
            self.interface.update_score_info(f'{prev_comment}\t{self.name} knocks.')

    def pick_card_in_pegging(self):
        self.interface.wait_for_ctrl_btn_click(f'{self.name}\'s turn')
        selected_card = self.select_card_to_play()
        self.interface.hide_played_card(selected_card)
        return selected_card

    def two_cards_for_box(self, dealt_hand):
        triplets = find_all_combos(dealt_hand, 3)
        all_triplets_scored = [[t, HandScore(Hand(t, self)).points_value] for t in triplets]
        self.refine_box_selection(all_triplets_scored)
        desired_triplet = max(all_triplets_scored, key=lambda tr: tr[1])[0]
        return [c for c in dealt_hand if c not in desired_triplet]

    def refine_box_selection(self, all_tr_scored):
        for tr in all_tr_scored:
            tr[1] += sum([getattr(self, m)(tr[0]) for m in self.__dir__() if 'evaluate' in m])

    def evaluate_run_potential(self, triplet):
        strong_run_potential = weak_run_potential = 0
        pairs = find_all_combos(triplet)
        for pr in pairs:
            rank_sum = pr[0].rank + pr[1].rank
            rank_diff = abs(pr[0].rank - pr[1].rank)
            if rank_sum in [3, 25] or rank_diff == 2:#    A2 / QK or cards two apart
                weak_run_potential += 3 * 1 / 13
            elif rank_diff == 1:
                strong_run_potential += 3 * 2 / 13
        return strong_run_potential + weak_run_potential

    def evaluate_flush_extension_potential(self, triplet):
        suits_found = set([c.suit for c in triplet])
        if len(suits_found) == 1:
            return 10 / 47
        return 0

    def evaluate_fifteen_potential(self, triplet):
        fives = len([c for c in triplet if c.value == 5])
        pairs = find_all_combos(triplet)
        fives += len([pr for pr in pairs if sum([c.value for c in pr]) == 5])
        return fives * 2 * 4 / 13

    def evaluate_knob_potential(self, triplet):
        # I am double-rating the score instead of just adding to the score for hands that have the J
        # and taking away from hands that don't.  Only care about RELATIVE value of hands.  Is this right??
        if self.round.player_has_box:
            knob_potential = len([t for t in triplet if t.rank == 11]) * 2 * 12 / 51
            return knob_potential
        return 0

    def select_card_to_play(self):
        test_ps = self.round.ps.__copy__()
        available_cards = self.get_playable_cards()
        if len(available_cards) == 1:   # TODO: Computer IS LEADING WITH A 5
            return available_cards[0]
        card_scores = []
        for c in available_cards:
            test_ps.add_card(c)
            score = -1 if test_ps.running_total == c.rank == 5 else test_ps.get_last_card_points()
            test_ps.pop_last_card()
            card_scores.append([c, score])
        card_scores.sort(key=lambda i: i[1])
        return card_scores[-1][0]


class HumanPlayer(Player):
    def __init__(self, name=None):
        super(HumanPlayer, self).__init__()
        self.name = 'Player'
        self.ownership_string = 'You have'
        self.possessive = 'my'

    def set_round_and_interface(self, round):
        super(HumanPlayer, self).set_round_and_interface(round)
        if type(self.interface) is RoundVisualInterface:
            self.card_buttons = self.interface.table.player_card_buttons
            self.box_buttons = self.interface.table.player_box_buttons

    def take_box_turn(self):
        box_string = ''
        for n in range(2):
            self.interface.update_ctrl_btn_text('Click on two cards to add them to the box')
            card_for_box = self.interface.wait_for_card()
            self.initial_card_list.remove(card_for_box)
            self.round.box_cards.append(card_for_box)
            box_string += str(card_for_box)
            self.interface.transfer_card_to_box(self, card_for_box)
            self.interface.update_score_info(f'Card added to box: {box_string}')
        self.interface.update_score_info(f'Cards added to box: {box_string}')
        super(HumanPlayer, self).take_box_turn()

    def knock_if_required(self):
        if not self.knocked and not self.get_playable_cards():
            if self.get_unplayed_cards():
                self.interface.wait_for_ctrl_btn_click('Knock')
            self.knocked = True

    def pick_card_in_pegging(self):
        return self.interface.player_picks_card(self.round)


class PegRow:
    win_score = 121
    empty_peg_row = '¦' + ((win_score // 5) * (5 * '.' + '¦'))
    peg = '\u2022'

    def __init__(self, screen_label):
        self.screen_label = screen_label
        self.front_peg = self.back_peg = 0
        self.full_peg_row = ''
        self.game = None
        if __name__ == '__main__':  # there are unit tests specifically for PegRow
            screen_label.configure(font=('courier', 10))
        self.draw_for_new_game()

    def increment_by(self, points_to_add):
        if points_to_add > 0:
            self.back_peg = self.front_peg
            self.front_peg += points_to_add
            self.move_peg_or_pegs()
        return self.front_peg

    def extend_for_go_point(self):
        self.front_peg += 1
        self.move_peg_or_pegs()
        return self.front_peg

    def move_peg_or_pegs(self):
        self.full_peg_row = f'  {self.empty_peg_row}  '
        self.insert_peg_for_score(self.back_peg)
        self.insert_peg_for_score(self.front_peg)
        self.full_peg_row += str(self.front_peg).rjust(4)
        self.check_for_win()
        self.draw()

    def draw(self):
        if __name__ == '__main__':
            self.screen_label.configure(text=self.full_peg_row)

    def check_for_win(self):
        if self.game:
            if not self.game.win_detected and self.front_peg >= self.win_score:
                self.game.record_win(self)

    def insert_peg_for_score(self, peg_value):
        peg_position = self.calc_peg_pos(peg_value)
        self.full_peg_row = (self.full_peg_row[:peg_position] + self.peg +
                             self.full_peg_row[peg_position + 1:])

    def calc_peg_pos(self, score):
        ''' give the position in an full peg row (with two spaces at each end) for a given absolute score'''
        if score == 0:
            return 0
        if score >= self.win_score:
            return self.win_score + (self.win_score // 5) + 3
        fives = score // 5
        ones = score % 5

        position = (fives * 6) - 1 + ones + 2
        if ones > 0:
            position += 1
        return position

    def reset(self):
        self.front_peg = self.back_peg = 0
        self.draw_for_new_game()

    def draw_for_new_game(self):
        self.full_peg_row = f'{self.peg} {self.empty_peg_row} {"0".rjust(5)}'
        self.draw()


class Pack:
    def __init__(self):
        self.pack = [Card(rank, suit) for rank in range(1, 14) for suit in SUITS]
        random.shuffle(self.pack)

    def deal(self, how_many_cards):
        return [self.pack.pop() for n in range(how_many_cards)]


class Card:
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


def find_all_combos(hand, length=2):
    return list(itertools.combinations(hand, length))


def its_a_run(card_list):
    no_of_cards = len(card_list)
    if no_of_cards >= 3:
        ranks = [c.rank for c in card_list]
        if max(ranks) == min(ranks) + no_of_cards - 1:
            if len(set(ranks)) == no_of_cards:
                return True
    return False


def pluralise_if_necessary(word, count):
    if count != 1:
        return f'{word}s'
    return word


class Hand:
    def __init__(self, cards, owner):
        self.cards = cards
        self.owner = owner
        self.display_button_text = self.set_display_button_text()

    def __getitem__(self, index):
        return self.cards[index]

    def __len__(self):
        return len(self.cards)

    def set_display_button_text(self):
        return f'Show {self.owner.possessive} {type(self).__name__.lower()}'

    def __str__(self):
        return f'{[str(c) for c in self.cards]}'


class Box(Hand):
    def __init__(self, cards, owner):
        super(Box, self).__init__(cards, owner)


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
        for fifteen_instance in range(1, instances + 1):
            self.description += f'{NUMBERS[15]} {NUMBERS[fifteen_instance * 2]}, '

    def count_runs(self):
        for run_length in range(len(self.all_cards), 2, -1):
            combos = itertools.combinations(self.all_cards, run_length)
            runs = [comb for comb in combos if its_a_run(comb)]
            if runs:
                self.points_value += len(runs) * run_length
                self.description += f'{NUMBERS[len(runs)]} {pluralise_if_necessary("run", len(runs))}' \
                                    f' of {NUMBERS[run_length]}, '
                break

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
            self.description += f'a flush of {NUMBERS[points_awarded]}, '

    def count_pairs(self):
        ct = len([pr for pr in find_all_combos(self.all_cards) if pr[0].rank == pr[1].rank])
        self.points_value += ct * 2
        if ct:
            self.two_pairs = ct == 2
            self.description += f'{NUMBERS[ct]} {pluralise_if_necessary("pair", ct)}, '

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
                desc = f'{desc[:last_comma]} and {desc[last_comma + 2:]}'
        desc = desc[0].upper() + desc[1:]
        return f'{desc} is {self.points_value}'


if __name__ == '__main__':
    the_table = Table()
