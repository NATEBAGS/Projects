import random

UPCARD_MAPPING = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    '10': 9,
    'J': 9,
    'K': 9,
    'Q': 9,
    'A': 0
}

STRATEGY = (0, 1, 1, 2, 2, 1, 1, 0, 0, -2, -2, -2, -2)

COUNT_MAP = {
    'A': STRATEGY[0],
    '2': STRATEGY[1],
    '3': STRATEGY[2],
    '4': STRATEGY[3],
    '5': STRATEGY[4],
    '6': STRATEGY[5],
    '7': STRATEGY[6],
    '8': STRATEGY[7],
    '9': STRATEGY[8],
    '10': STRATEGY[9],
    'J': STRATEGY[10],
    'Q': STRATEGY[11],
    'K': STRATEGY[12],
}

SPLITTING = {
    'A': ['Y'] * 9 + ['N'],
    '10': ['N'] * 10,
    '9': ['Y'] * 5 + ['N'] + ['Y'] * 2 + ['N'] * 2,
    '8': ['Y'] * 8 + ['N'] * 2,
    '7': ['Y'] * 6 + ['N'] * 4,
    '6': ['Y'] * 5 + ['N'] * 5,
    '5': ['N'] * 10,
    '4': ['N'] * 3 + ['Y'] * 2 + ['N'] * 5,
    '3': ['Y'] * 6 + ['N'] * 4,
    '2': ['Y'] * 6 + ['N'] * 4,
}

SOFT = {
    21: ['S'] * 10,
    20: ['S'] * 10,
    19: ['S'] * 10,
    18: ['S'] * 7 + ['H'] * 3,
    17: ['H'] * 10,
    16: ['H'] * 10,
    15: ['H'] * 10,
    14: ['H'] * 10,
    13: ['H'] * 10,
}

HARD = {
    17: ['S'] * 10,
    16: ['S'] * 5 + ['H'] * 5,
    15: ['S'] * 5 + ['H'] * 5,
    14: ['S'] * 5 + ['H'] * 5,
    13: ['S'] * 5 + ['H'] * 5,
    12: ['H'] * 2 + ['S'] * 3 + ['H'] * 5,
}

HARDDUB = {
    11: ['D'] * 8 + ['H'] * 2,
    10: ['D'] * 8 + ['H'] * 2,
    9: ['H'] + ['D'] * 4 + ['H'] * 5,
    8: ['H'] * 10,
}

class Card:
    def __init__(self, rank):
        self.rank = rank

    def __str__(self):
        return self.rank

class Deck:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = []
        self.cut_card_position = None
        self.count = 0
        self.true_count = 0
        self.initialize_deck()

    def initialize_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank) for rank in ranks for _ in range(4 * self.num_decks)]
        self.reshuffle()
        self.set_cut_card_position()

    def update_count(self, card):
        self.count += COUNT_MAP[card.rank]

    def print_deck(self):
        num = 0
        totalCards = 0
        ranks_count = {rank: 0 for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']}
        for card in self.cards:
            ranks_count[card.rank] += 1
        print("\nCount of all ranks:")
        for rank, count in ranks_count.items():
            totalCards += count
            print(f"{rank}: {count}")
        print(f'Cards left: {totalCards}')

    def reshuffle(self):
        random.shuffle(self.cards)

    def set_cut_card_position(self):
        self.cut_card_position = len(self.cards) - random.randint(190, 235)

    def deal_card(self):
        if not self.cards:
            print("Reshuffling deck as cards have run out.")
            self.initialize_deck()
        card = self.cards.pop()
        self.update_count(card)
        return card

    def get_count(self):
        return self.count

    def get_true_count(self):
        remaining_decks = (self.num_decks * 52 - len(self.cards)) / 52
        self.true_count = self.count / remaining_decks
        return self.true_count

    def get_ace_deficit(self):
        aces_in_deck = sum(1 for card in self.cards if card.rank == 'A')
        aces_removed = (4 * self.num_decks) - aces_in_deck
        ace_deficit = (len(self.cards) / 13) - aces_removed
        remaining_decks = (self.num_decks * 52 - len(self.cards)) / 52
        self.betting_count = (self.count + (ace_deficit * 2)) / remaining_decks
        return self.betting_count

    def cards_left(self):
        return len(self.cards)

class Player:
    def __init__(self, name, initial_balance=500):
        self.name = name
        self.hands = [[]]
        self.hand_bets = [0]
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.balance = initial_balance
        self.bet = 0
        self.doubleWager = False

    def reset_hands(self):
        self.hands = [[]]
        self.hand_bets = [0]
        self.doubleWager = False

    def place_bet(self, amount):
        if amount <= self.balance:
            self.bet = amount
            self.hand_bets[0] = amount
            self.balance -= amount
        else:
            print("Ran out of balance")

    def double_down(self, hand_index):
        if self.hand_bets[hand_index] <= self.balance:
            self.balance -= self.hand_bets[hand_index]
            self.hand_bets[hand_index] *= 2
            self.doubleWager = True
        else:
            print("Ran out of balance")

    def add_win(self, hand_index, multiplier=1):
        self.wins += 1
        win_amount = self.hand_bets[hand_index] * (2 * multiplier)
        self.balance += win_amount

    def add_loss(self):
        self.losses += 1

    def add_push(self, hand_index):
        self.pushes += 1
        self.balance += self.hand_bets[hand_index]  # Refund the bet amount on push

    def add_blackjack(self):
        self.blackjacks += 1
        self.balance += self.bet * 2.5

    def add_card_to_hand(self, card, hand_index=0):
        self.hands[hand_index].append(card)

    def has_blackjack(self, hand_index=0):
        ranks = [card.rank for card in self.hands[hand_index]]
        return len(self.hands[hand_index]) == 2 and 'A' in ranks and any(rank in ['10', 'J', 'Q', 'K'] for rank in ranks)

    def is_busted(self, hand_index=0):
        total, _ = self.hand_total(hand_index)
        return total > 21

    def hand_total(self, hand_index=0):
        hand_ranks = [card.rank for card in self.hands[hand_index]]
        return Counter.sumHand(hand_ranks)

    def basic_best_move(self, upcard, hand_index=0):
        hand = self.hands[hand_index]
        i = UPCARD_MAPPING[upcard.upper()]
        hand_ranks = [card.rank for card in hand]
        hand_sum, soft = Counter.sumHand(hand_ranks)

        if not soft and hand_sum in HARDDUB.keys():
            play = HARDDUB[hand_sum][i]
            if play == 'D' and len(hand) == 2:
                return 'DOUBLE'
            else:
                return 'HIT'

        if len(hand) == 2 and hand[0].rank == hand[1].rank:
            card = hand[0].rank
            if card in ('K', 'J', 'Q'):
                card = '10'
            play = SPLITTING[card][i]
            if play == 'Y':
                return 'SPLIT'

        if soft and hand_sum in SOFT.keys():
            play = SOFT[hand_sum][i]
            if play == 'S':
                return 'STAND'
            elif play == 'H':
                return 'HIT'
            elif play == 'D':
                return 'DOUBLE'
            if hand_sum >= 19:
                return 'STAND'
        elif not soft and hand_sum in HARD.keys():
            play = HARD[hand_sum][i]
            if play == 'D':
                return 'DOUBLE'
            elif play == 'H':
                return 'HIT'
            else:
                return 'STAND'
        return 'STAND' if not soft and hand_sum > 15 else 'HIT'

    def show_hand(self, hand_index=0):
        hand_description = " ".join(str(card) for card in self.hands[hand_index])
        total, is_soft = self.hand_total(hand_index)
        soft_display = "Soft" if is_soft else "Hard"
        print(f"{self.name}'s hand ({soft_display} {total}): {hand_description}")


class BlackjackGame:
    def __init__(self, num_decks=1, num_players=1):
        self.deck = Deck(num_decks)
        self.players = [Player(f"Player {i + 1}", initial_balance=500) for i in range(num_players)]
        self.dealer = Player("Dealer")

    def play(self):
        while self.deck.cards_left() > self.deck.cut_card_position:
            self.reset_hands()
            self.collect_bets()
            self.deal_initial_cards()
            self.player_actions()
            self.dealer_actions()
            self.summarize_round()
            print(f"Running count: {self.deck.get_count()}")
            print(f"True count: {self.deck.get_true_count()}")
            print(f"Betting Count: {self.deck.get_ace_deficit()}")


            if self.deck.cards_left() <= self.deck.cut_card_position:
                print("Cut card reached, reshuffling the deck.")
                self.deck.print_deck()
                self.deck.initialize_deck()
                break

    def reset_hands(self):
        for player in self.players:
            player.reset_hands()
        self.dealer.reset_hands()

    def collect_bets(self):
        for player in self.players:
            bet_amount = 5  # Set bet amount for each player
            player.place_bet(bet_amount)

    def set_test_hands(self, player_hands, dealer_upcard):
        self.test_player_hands = player_hands
        self.test_dealer_upcard = dealer_upcard

    def deal_initial_cards(self):
        if hasattr(self, 'test_player_hands') and hasattr(self, 'test_dealer_upcard'):
            # Set player hands
            for player, hand in zip(self.players, self.test_player_hands):
                for card in hand:
                    player.add_card_to_hand(Card(card))
            # Set dealer hand
            self.dealer.add_card_to_hand(Card(self.test_dealer_upcard))
            self.dealer.add_card_to_hand(self.deck.deal_card())  # Deal the second card normally
        else:
            for _ in range(2):
                for player in self.players:
                    player.add_card_to_hand(self.deck.deal_card())
                self.dealer.add_card_to_hand(self.deck.deal_card())

        for player in self.players:
            player.show_hand()

        print("\nDealer's upcard:")
        print(self.dealer.hands[0][0])

    def player_actions(self):
        for player in self.players:
            hands_to_play = [(0, False)]  # (hand_index, was_split)

            while hands_to_play:
                new_hands = []
                for hand_index, was_split in hands_to_play:
                    while True:
                        dealer_upcard = self.dealer.hands[0][0].rank if self.dealer.hands[0] else 'Unknown'
                        move = player.basic_best_move(dealer_upcard, hand_index)
                        if move == 'SPLIT' and not was_split:  # Prevent splitting again after a split
                            print(f"{player.name} decides to SPLIT.")
                            was_aces = player.hands[hand_index][0].rank == 'A'
                            hand_1 = [player.hands[hand_index][0], self.deck.deal_card()]
                            hand_2 = [player.hands[hand_index][1], self.deck.deal_card()]
                            player.hands[hand_index] = hand_1
                            player.hands.append(hand_2)

                            # Track the bets for split hands
                            player.hand_bets.append(player.hand_bets[hand_index])
                            player.balance -= player.hand_bets[hand_index]

                            # Print the hands after the split
                            hand_1_str = " ".join(str(card) for card in hand_1)
                            hand_2_str = " ".join(str(card) for card in hand_2)
                            print(f"{player.name}'s 1st hand: {hand_1_str}")
                            print(f"{player.name}'s 2nd hand: {hand_2_str}")

                            new_hands.extend([(hand_index, True), (len(player.hands) - 1, True)])
                            if was_aces:
                                break
                        elif move == 'HIT':
                            player.add_card_to_hand(self.deck.deal_card(), hand_index)
                            print(f"{player.name} HIT -> {' '.join(str(card) for card in player.hands[hand_index])}")
                            if player.is_busted(hand_index):
                                print(f"{player.name} Busted!")
                                break
                        elif move == 'STAND':
                            print(f"{player.name} decides to STAND.")
                            break
                        elif move == 'DOUBLE' and not was_split:  # Handle doubling
                            player.double_down(hand_index)
                            player.add_card_to_hand(self.deck.deal_card(), hand_index)
                            print(f"{player.name} after DOUBLE: {' '.join(str(card) for card in player.hands[hand_index])}")
                            break
                        elif move == 'DOUBLE' and was_split:  # Prevent doubling after a split
                            print(f"{player.name} decides to DOUBLE, but doubling after a split is not allowed.")
                            move = 'HIT'  # Force a HIT instead of DOUBLE
                            player.add_card_to_hand(self.deck.deal_card(), hand_index)
                            print(f"{player.name} HIT instead of DOUBLE -> {' '.join(str(card) for card in player.hands[hand_index])}")
                            if player.is_busted(hand_index):
                                print(f"{player.name} Busted!")
                                break
                        elif move == 'SPLIT' and was_split:  # Prevent splitting again after a split
                            print(f"{player.name} decides to SPLIT, but splitting again after a split is not allowed.")
                            move = 'HIT'  # Force a HIT instead of SPLIT
                            player.add_card_to_hand(self.deck.deal_card(), hand_index)
                            print(f"{player.name} HIT instead of SPLIT -> {' '.join(str(card) for card in player.hands[hand_index])}")
                            if player.is_busted(hand_index):
                                print(f"{player.name} Busted!")
                                break

                    hands_to_play = new_hands

    def dealer_actions(self):
        while True:
            dealer_total, _ = self.dealer.hand_total()
            if dealer_total >= 17:
                break
            self.dealer.add_card_to_hand(self.deck.deal_card())
        print("\nDealer's final hand:")
        for card in self.dealer.hands[0]:
            print(card)

    def summarize_round(self):
        dealer_total, _ = self.dealer.hand_total()
        print(f"\nDealer's final hand total: {dealer_total}\n")

        for player in self.players:
            total_win = 0
            total_loss = 0
            total_push = 0

            for hand_index in range(len(player.hands)):
                player_total, _ = player.hand_total(hand_index)
                initial_bet = player.hand_bets[hand_index]
                hand_result = ''

                if player.has_blackjack(hand_index) and hand_index == 0 and len(player.hands) == 1:
                    if dealer_total == 21 and len(self.dealer.hands[0]) == 2:
                        hand_result = 'push'
                        total_push += initial_bet
                    else:
                        player.add_blackjack()
                        hand_result = 'blackjack'
                elif player_total > 21:
                    hand_result = 'loss'
                    total_loss += initial_bet
                elif dealer_total > 21 or player_total > dealer_total:
                    hand_result = 'win'
                    if player.doubleWager:
                        total_win += initial_bet * 2
                    else:
                        total_win += initial_bet * 2
                elif player_total < dealer_total:
                    hand_result = 'loss'
                    total_loss += initial_bet
                else:
                    hand_result = 'push'
                    total_push += initial_bet

                print(f"{player.name}'s hand ({player_total}): {hand_result}")

            # Adjust player's balance based on results
            player.balance += total_push
            player.balance += total_win
            # player.balance -= total_loss

            # Update player statistics
            player.wins += (total_win > 0)
            player.losses += (total_loss > 0)
            player.pushes += (total_push > 0 and total_win == 0 and total_loss == 0)

            # Summary for the player
            result_summary = "wins" if total_win > 0 else "loses" if total_loss > 0 else "pushes"
            print(f"{player.name} {result_summary}.")
            print(f"{player.name} has {player.wins} wins, {player.losses} losses, and {player.pushes} pushes. Also {player.blackjacks} Blackjacks")
            print(f"{player.name} has ${player.balance}\n")


class Counter:
    @staticmethod
    def sumHand(hand_ranks):
        total = 0
        aces = 0
        for rank in hand_ranks:
            if rank in 'JQK10':
                total += 10
            elif rank == 'A':
                total += 11
                aces += 1
            else:
                total += int(rank)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        is_soft = aces > 0
        return total, is_soft

if __name__ == "__main__":
    game = BlackjackGame(num_decks=8, num_players=1)
    # Example test hands
    # player_hands = [
    #     ['A', 'J'],  # Player 1 hand
    # ]
    # dealer_upcard = 'A'  # Dealer's upcard

    # game.set_test_hands(player_hands, dealer_upcard)
    game.play()
