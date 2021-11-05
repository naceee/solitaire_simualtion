class Card:
    def __init__(self, card_id):
        self.card_id = card_id
        self.suit = card_id // 13
        self.number = card_id % 13 + 1

    def __str__(self):
        if self.suit == 0:
            s = '\u2665'  # heart
        elif self.suit == 1:
            s = '\u2660'  # spade
        elif self.suit == 2:
            s = '\u2666'  # diamond
        elif self.suit == 3:
            s = '\u2663'  # club
        else:
            raise ValueError('suit error')

        if self.number == 1:
            s = s + ' A'
        elif self.number < 10:
            s = s + ' ' + str(self.number)
        elif self.number == 10:
            s = s + '10'
        elif self.number == 11:
            s = s + ' J'
        elif self.number == 12:
            s = s + ' Q'
        elif self.number == 13:
            s = s + ' K'
        else:
            raise ValueError('suit error')

        return s

    def can_move_to(self, cards):
        if cards == []:
            if self.number == 13:
                return True
            return False
        if self.number == 1:
            return False
        if self.suit % 2 == cards.suit % 2:
            return False
        if self.number == cards.number - 1:
            return True
        return False

    def can_move_to_ace(self, aces):
        if len(aces) == 0:
            if self.number == 1:
                return True
            return False
        if self.suit == aces[-1].suit and self.number == aces[-1].number + 1:
            return True
        return False
