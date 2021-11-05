import random
from card import Card


class Solitaire:
    def __init__(self):
        self.piles = [[], [], [], [], [], [], []]
        self.num_closed_cards = [0, 1, 2, 3, 4, 5, 6]
        self.num_cards = [1, 2, 3, 4, 5, 6, 7]
        self.cards_in_hand = []
        self.card_in_hand_idx = 2
        self.aces = [[], [], [], []]

        idx = list(range(0, 52))
        random.shuffle(idx)
        st = 0
        for i in range(7):
            for j in range(i, 7):
                self.piles[j].append(Card(idx[st]))
                st += 1

        for i in range(st, 52):
            self.cards_in_hand.append(Card(idx[st]))
            st += 1

    def __str__(self):
        """ return printable string of table with cards
        """
        s = ''
        for i in range(4):
            if len(self.aces[i]) > 0:
                s = s + str(self.aces[i][-1]) + '   '
            else:
                s = s + 'XXX   '
        s = s + '\n\n'

        m = 0
        for i in range(7):
            if len(self.piles[i]) > m:
                m = len(self.piles[i])

        for i in range(m):
            for j in range(7):
                if self.num_cards[j] > i:
                    if self.num_closed_cards[j] > i:
                        s = s + 'XXX '
                    else:
                        s = s + str(self.piles[j][i]) + ' '
                else:
                    s = s + '    '
            s = s + '\n'
        s = s + '\n'
        offset = self.card_in_hand_idx // 8
        s = s + '  -  ' * self.card_in_hand_idx + ' ' * offset + '___\n'
        for r in self.cards_in_hand:
            s = s + str(r) + ', '
        s = s[:-1] + '\n'
        return s

    def higher_cards(self):
        """ return a list of cards, where i-th card in the list is the highest open card in the i-th
        pile. If a pile is empty, put a None in its place.
        """
        cards = []
        for k in range(7):
            if self.num_cards[k] > 0:
                cards.append(self.piles[k][self.num_closed_cards[k]])
            else:
                cards.append(None)
        return cards

    def lower_cards(self):
        """ return a list of cards, where i-th card in the list is the lowest open card in the i-th
        pile. If a pile is empty, put a None in its place.
        """
        cards = []
        for k in range(7):
            if self.num_cards[k] > 0:
                cards.append(self.piles[k][self.num_cards[k] - 1])
            else:
                cards.append(None)
        return cards

    def make_a_move(self, show_prints=False):
        """ function that tries to make a good move.
        :return:
         *  1 if the game is won
         * -1 if the game is lost
         *  0 otherwise
        """
        if show_prints:
            input()

        higher_visible_cards = self.higher_cards()
        lower_visible_cards = self.lower_cards()
        for i in range(7):
            if self.num_closed_cards[i] < 0:
                self.num_closed_cards[i] = 0

        # if all the cards are on the aces, then the game is won
        if len(self.aces[0]) + len(self.aces[1]) + len(self.aces[2]) + len(self.aces[3]) == 52:
            if show_prints:
                print('YOU WIN :)')
            return 1

        # if there is an ace open in the pile, put it to the place with aces
        # if there is a card, that can be put on the aces pile, also put it there
        for i in range(7):
            if lower_visible_cards[i] is not None:
                for j in range(4):
                    if lower_visible_cards[i].can_move_to_ace(self.aces[j]):
                        if show_prints:
                            print(f'{lower_visible_cards[i]} goes to ace {j}')
                        moving_cards = self.piles[i].pop()
                        self.num_cards[i] -= 1
                        if self.num_cards[i] == self.num_closed_cards[i]:
                            self.num_closed_cards[i] -= 1
                        self.aces[j].append(moving_cards)
                        return 0

        # move one card (or whole pile of open cards) from one pile to the other
        for i in range(6, -1, -1):
            if higher_visible_cards[i] is not None:
                for j in range(6, -1, -1):
                    if lower_visible_cards[j] is not None:
                        if higher_visible_cards[i].can_move_to(lower_visible_cards[j]):
                            if show_prints:
                                print(f'{higher_visible_cards[i]} goes to {lower_visible_cards[j]}')
                            moving_cards = self.piles[i][self.num_closed_cards[i]:self.num_cards[i]]
                            for k in range(len(moving_cards)):
                                self.piles[i].pop()
                            self.num_cards[i] -= len(moving_cards)
                            if self.num_closed_cards[i] > 0:
                                self.num_closed_cards[i] -= 1
                            self.piles[j] = self.piles[j] + moving_cards
                            self.num_cards[j] += len(moving_cards)
                            return 0
                    # move the kings to an empty pile
                    else:
                        if higher_visible_cards[i].number == 13 and self.num_closed_cards[i] > 0:
                            if show_prints:
                                print(f'{higher_visible_cards[i]} goes to empty pile')
                            moving_cards = self.piles[i][self.num_closed_cards[i]:self.num_cards[i]]
                            for k in range(len(moving_cards)):
                                self.piles[i].pop()
                            self.num_cards[i] -= len(moving_cards)
                            if self.num_closed_cards[i] > 0:
                                self.num_closed_cards[i] -= 1
                            self.piles[j] = self.piles[j] + moving_cards
                            self.num_cards[j] += len(moving_cards)
                            return 0

        # turn the cards in the hand until one can move onto a card on the table
        remaining_circles = 2
        while remaining_circles > 0 and len(self.cards_in_hand) > 0:
            for i in range(7):
                if lower_visible_cards[i] is not None:
                    if self.cards_in_hand[self.card_in_hand_idx].can_move_to(
                            lower_visible_cards[i]):
                        if show_prints:
                            print(f'{self.cards_in_hand[self.card_in_hand_idx]} goes to '
                                  f'{lower_visible_cards[i]}')
                        moving_cards = self.cards_in_hand.pop(self.card_in_hand_idx)
                        self.piles[i].append(moving_cards)
                        self.num_cards[i] += 1
                        if self.card_in_hand_idx > 0:
                            self.card_in_hand_idx -= 1
                        return 0
                    for j in range(4):
                        if self.cards_in_hand[self.card_in_hand_idx].can_move_to_ace(self.aces[j]):
                            if show_prints:
                                print(f'{self.cards_in_hand[self.card_in_hand_idx]} goes to ace '
                                      f'{j}')
                            moving_cards = self.cards_in_hand.pop(self.card_in_hand_idx)
                            self.aces[j].append(moving_cards)
                            if self.card_in_hand_idx > 0:
                                self.card_in_hand_idx -= 1
                            return 0
                else:
                    if self.cards_in_hand[self.card_in_hand_idx].number == 13:
                        if show_prints:
                            print(f'{self.cards_in_hand[self.card_in_hand_idx]} '
                                  f'goes to the empty pile')
                        moving_cards = self.cards_in_hand.pop(self.card_in_hand_idx)
                        self.piles[i].append(moving_cards)
                        self.num_cards[i] += 1
                        if self.card_in_hand_idx > 0:
                            self.card_in_hand_idx -= 1
                        return 0

            if self.card_in_hand_idx == len(self.cards_in_hand) - 1:
                remaining_circles -= 1
                self.card_in_hand_idx = min(2, len(self.cards_in_hand) - 1)
            else:
                self.card_in_hand_idx += 3
                if self.card_in_hand_idx >= len(self.cards_in_hand):
                    self.card_in_hand_idx = len(self.cards_in_hand) - 1

            if show_prints:
                print('move to the next 3 cards in the hand')
                print(self)
                input()
        return -1
