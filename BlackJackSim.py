import random
import math
import matplotlib.pyplot as plt
import statistics

HIOPT2_SPLITTING = {
    'A': ['Y'] * 9 + ['N'],
    '10': ['N'] * 2 + ['10+', '8+', '7+'] + ['N'] * 5,
    '9': ['Y'] * 5 + ['14+', 'Y', '-25+', 'N', '11+'],
    '8': ['Y'] * 7 + ['31-'] + ['N'] * 2,
    '7': ['Y'] * 6 + ['N'] * 4,
    '6': ['4+'] + ['-1+', '-4+', '-8+', '-11+'] + ['N'] * 5,
    '5': ['N'] * 10,
    '4': ['N'] * 10,
    '3': ['13+', '6+', '0+'] + ['Y'] * 3 + ['N'] * 4,
    '2': ['12+', '4+'] + ['Y'] * 4 + ['N'] * 4,
}

HIOPT2_SOFT = {
    20: ['18+'] + ['15+', '12+', '10+', '9+'] + ['S'] * 5,
    19: ['14+', '8+', '6+', '3+'] + ['D'] + ['27+'] + ['S'] * 4,
    18: ['2+'] + ['D'] * 4 + ['28+'] + ['S'] + ['H'] * 3,
    17: ['2+'] + ['D'] * 4 + ['22+'] + ['H'] * 4,
    16: ['19+'] + ['6+'] + ['D'] * 3 + ['H'] * 5,
    15: ['20+'] + ['8+'] + ['D'] * 3 + ['H'] * 5,
    14: ['18+'] + ['9+'] + ['2+'] + ['D'] * 2 + ['H'] * 5,
    13: ['18+'] + ['10+'] + ['5+'] + ['D'] * 2 + ['H'] * 5,
}

HIOPT2_HARD = {
    17: ['S'] * 10,
    16: ['S'] * 5 + ['14-', '13-', '7-'] + ['S'] + ['13-'],
    15: ['S'] * 5 + ['H'] * 2 + ['14-', '6-'] + ['H'],
    14: ['S'] * 5 + ['H'] * 3 + ['14-'] + ['H'],
    13: ['S'] * 5 + ['H'] * 5,
    12: ['5-'] + ['2-'] + ['0-'] + ['-2-'] * 2 + ['H'] * 5,
}

# Hard Doubling (easier than having hit,stand,double [above] in the same deviation chart)
HIOPT2_HARDDUB = {
    11: ['D'] * 8 + ['H'] * 2,
    10: ['D'] * 8 + ['H'] * 2,
    9: ['3+'] + ['D'] * 4 + ['6+', '15+'] + ['H'] * 3,
    8: ['H'] * 2 + ['11+', '6+', '4+'] + ['H'] * 5,
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

UPCARD_MAPPING = {
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    '10': 8,
    'J': 8,
    'K': 8,
    'Q': 8,
    'A': 9
}

STRATEGY = (0, 1, 1, 2, 2, 1, 1, 0, 0, -2, -2, -2, -2)
INSURANCE_STRAT = (1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2)

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

INSURANCE_COUNT_MAP = {
    'A': INSURANCE_STRAT[0],
    '2': INSURANCE_STRAT[1],
    '3': INSURANCE_STRAT[2],
    '4': INSURANCE_STRAT[3],
    '5': INSURANCE_STRAT[4],
    '6': INSURANCE_STRAT[5],
    '7': INSURANCE_STRAT[6],
    '8': INSURANCE_STRAT[7],
    '9': INSURANCE_STRAT[8],
    '10': INSURANCE_STRAT[9],
    'J': INSURANCE_STRAT[10],
    'Q': INSURANCE_STRAT[11],
    'K': INSURANCE_STRAT[12],
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
        self.betting_count = 0
        self.insurance_count = 0
        self.initialize_deck()

    def initialize_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank) for rank in ranks for _ in range(4 * self.num_decks)]
        self.reshuffle()
        self.set_cut_card_position()

    def update_count(self, card):
        self.count += COUNT_MAP[card.rank]
        self.insurance_count += INSURANCE_COUNT_MAP[card.rank]

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
        self.count = 0  # Reset the running count
        self.true_count = 0  # Reset the true count
        self.betting_count = 0  # Reset the betting count
        self.insurance_count = 0  # Reset the insurance count

    def set_cut_card_position(self):
        self.cut_card_position = len(self.cards) - random.randint(190, 235)

    def deal_card(self):
        if not self.cards:
            #print("Reshuffling deck as cards have run out.")
            self.initialize_deck()
        card = self.cards.pop()
        self.update_count(card)
        return card

    def get_count(self):
        return self.count

    def get_true_count(self):
        remaining_decks = len(self.cards) / 52
        self.true_count = self.count / remaining_decks
        return self.true_count

    def get_betting_count(self):
        # Calculate aces removed from the deck
        aces_in_deck = sum(1 for card in self.cards if card.rank == 'A')
        # Calculate the expected aces in the remaining deck
        expected_aces = math.floor(len(self.cards) / 13)
        # Calculate the ace deficit
        ace_deficit = aces_in_deck - expected_aces
        # Calculate the remaining decks
        remaining_decks = len(self.cards) / 52
        # Calculate the betting count using the ace deficit
        self.betting_count = (self.count + (ace_deficit * 2)) / remaining_decks
        return self.betting_count

    def get_insurance_strat(self):
        insurance = False
        if (self.insurance_count - (self.num_decks * 4)) > 0:
            print("Insurance count: ", self.insurance_count)
            insurance = True
        return insurance

    def cards_left(self):
        return len(self.cards)

class Player:
    def __init__(self, name, game, initial_balance=1000):
        self.name = name
        self.game = game
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
            print(f"{self.name} placed a bet of ${amount}. New balance: ${self.balance}")
        else:
            print(f"Ran out of balance. Cannot place bet of ${amount}. Current balance: ${self.balance}")
            self.bet = 0  # Set bet to 0 if the player can't afford it

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
        print(f"{self.name} won ${win_amount} on hand {hand_index}. New balance: ${self.balance}")

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
                if len(hand) == 2:
                    return 'DOUBLE'
                else:
                    return 'HIT'
            elif play == 'H':
                return 'HIT'
            else:
                return 'STAND'
        return 'STAND' if not soft and hand_sum > 15 else 'HIT'

    def bestMove(self, upcard: str, hand_index: int) -> str:
        """Returns the best move as a capitalized string."""

        def isValidTC(tc: str):
            try:
                n, sym = tc[:-1], tc[-1]
                if sym == '+':
                    print("Deviation + is", self.game.deck.get_true_count() >= float(n))
                    return self.game.deck.get_true_count() >= float(n)
                elif sym == '-':
                    print("Deviation - is", self.game.deck.get_true_count() <= float(n))
                    return self.game.deck.get_true_count() <= float(n)
                else:
                    # Return false for letters
                    return False
            except ValueError:
                return False

        i = UPCARD_MAPPING[upcard.upper()]
        hand = [card.rank for card in self.hands[hand_index]]  # Get ranks of the cards in hand
        handSum, soft = Counter.sumHand(hand)

        # Check for soft 21 (blackjack)
        if soft and handSum == 21:
            return 'STAND'

        # Hard Doubles (moved above Split because these are never split, rather doubled (4,4) = 8 and (5,5) = 10)
        if not soft and handSum in HIOPT2_HARDDUB.keys():
            play = HIOPT2_HARDDUB[handSum][i]
            if (play == 'D' or isValidTC(play)) and len(hand) == 2:
                return 'DOUBLE'
            else:
                return 'HIT'

        # Split logic
        if len(hand) == 2 and hand[0] == hand[1]:  # Compare ranks directly
            card = hand[0].upper()
            if card in ('K', 'J', 'Q'):
                card = '10'
            play = HIOPT2_SPLITTING[card][i]
            if play == 'Y' or isValidTC(play):
                return 'SPLIT'

        # Soft decision logic
        if soft and handSum in HIOPT2_SOFT.keys():
            play = HIOPT2_SOFT[handSum][i]
            if play == 'S':
                return 'STAND'
            elif play == 'H':
                return 'HIT'
            elif play == 'D' or isValidTC(play):
                if len(hand) == 2:
                    return 'DOUBLE'
                else:
                    return 'HIT'
            if handSum >= 19:
                return 'STAND'
        # Hard decision logic
        elif not soft and handSum in HIOPT2_HARD.keys():
            play = HIOPT2_HARD[handSum][i]
            if play == 'D':
                if len(hand) == 2:
                    return 'DOUBLE'
                else:
                    return 'HIT'
            elif play == 'H' or isValidTC(play):
                return 'HIT'
            else:
                return 'STAND'
        return 'STAND' if not soft and handSum > 15 else 'HIT'

    def show_hand(self, hand_index=0):
        hand_description = " ".join(str(card) for card in self.hands[hand_index])
        total, is_soft = self.hand_total(hand_index)
        soft_display = "Soft" if is_soft else "Hard"
        print(f"{self.name}'s hand ({soft_display} {total}): {hand_description}")

    def _get_balance(self):
        return self.balance

class BlackjackGame:
    def __init__(self, num_decks=1, num_players=1):
        self.deck = Deck(num_decks)
        self.players = [Player(f"Player {i + 1}", self, initial_balance=500) for i in range(num_players)]
        self.dealer = Player("Dealer", self)
        self.round_results = []
        self.num_rounds = 0
        self.hands_played_player_1 = 0

    def play(self, num_rounds=1):
        self.num_rounds = num_rounds
        for _ in range(num_rounds):
            if self.deck.cards_left() <= self.deck.cut_card_position:
                print("Cut card reached, reshuffling the deck.")
                self.deck.print_deck()
                self.deck.initialize_deck()

            self.reset_hands()
            self.collect_bets()
            self.deal_initial_cards()
            if self.check_dealer_blackjack():
                self.resolve_dealer_blackjack()
            else:
                self.player_actions()
                self.dealer_actions()
                self.summarize_round()
            if self.players[0].bet > 0:  # Only increment if Player 1 is playing
                self.hands_played_player_1 += 1
            print(f"Running count: {self.deck.get_count()}")
            print(f"True count: {self.deck.get_true_count()}")
            print(f"Betting Count: {self.deck.get_betting_count()}")
            print(f"Insurance count: {self.deck.insurance_count}")


    def reset_hands(self):
        for player in self.players:
            player.reset_hands()
        self.dealer.reset_hands()

    def reset_game(self):
        self.deck = Deck(self.deck.num_decks)  # Reset the deck
        for player in self.players:
            player.balance = 500  # Reset balance
            player.wins = 0
            player.losses = 0
            player.pushes = 0
            player.blackjacks = 0
            player.reset_hands()
        self.dealer.reset_hands()
        self.round_results = []
        self.hands_played_player_1 = 0  # Reset hands played

    def collect_bets(self):
        for player in self.players:
            if player.name == "Player 1":
                 if self.deck.get_betting_count() < 0.5:
                     print(f"{player.name} is sitting out due to low betting count.")
                     player.bet = 0
                     continue
                 balance = player._get_balance()
                 bet_amt = 5  # Flat bet by default
                 if balance != -1:
                     kelly_bet = round(((self.deck.get_betting_count() - 0.5) / 200) * 0.77 * balance)
                     bet_amt = max(bet_amt, kelly_bet)
                 player.place_bet(bet_amt)
                 #print(f"{player.name}'s initial bet: ${bet_amt}")
            else:
                bet_amount = 5  # Set bet amount for each player
                player.place_bet(bet_amount)

    def set_test_hands(self, player_hands, dealer_upcard):
        self.test_player_hands = player_hands
        self.test_dealer_upcard = dealer_upcard

    def deal_initial_cards(self):
        if hasattr(self, 'test_player_hands') and hasattr(self, 'test_dealer_upcard'):
            # Set player hands
            for player, hand in zip(self.players, self.test_player_hands):
                if player.name == "Player 1" and player.bet == 0:
                    continue
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
            if player.name == "Player 1" and player.bet == 0:
                continue  # Skip showing hand for Player 1 if sitting out
            player.show_hand()

        print("\nDealer's upcard:")
        print(self.dealer.hands[0][0])

        if self.dealer.hands[0][0].rank == 'A':  # Fixed typo here
            self.offer_insurance()

    def check_dealer_blackjack(self):
        dealer_upcard = self.dealer.hands[0][0].rank
        dealer_downcard = self.dealer.hands[0][1].rank
        return dealer_upcard == 'A' and dealer_downcard in ['10', 'J', 'Q', 'K']

    def resolve_dealer_blackjack(self):
        print("Dealer has blackjack!")
        for player in self.players:
            if player.name == "Player 1" and player.bet == 0:
                continue
            if hasattr(player, 'insurance_bet') and player.insurance_bet > 0:
                player.balance += player.insurance_bet * 2  # Pay 2:1 on insurance bet
                print(f"{player.name} wins insurance bet of ${player.insurance_bet * 2}.")
            if not player.has_blackjack():
                player.add_loss()
                print(f"{player.name} loses to dealer blackjack.")
            else:
                player.add_push(0)  # Assuming single hand, index 0
                print(f"{player.name} pushes with dealer blackjack.")

    def offer_insurance(self):
        for player in self.players:
            if player.name == "Player 1" and player.bet == 0:
                continue
            if player.name != "Player 1":
                continue
            else:
                ensure = self.deck.get_insurance_strat()  # Fixed reference here
                if ensure:
                    insurance_bet = player.bet / 2
                    if insurance_bet <= player.balance:
                        player.balance -= insurance_bet
                        player.insurance_bet = insurance_bet
                        print(f"{player.name} takes insurance bet of ${insurance_bet}.")
                    else:
                        player.insurance_bet = 0
                        #print(f"{player.name} cannot afford insurance.")

    def player_actions(self):
        for player in self.players:
            if player.name == "Player 1" and player.bet == 0:
                continue  # Skip actions for Player 1 if sitting out
            hands_to_play = [(0, False)]  # (hand_index, was_split)

            while hands_to_play:
                new_hands = []
                for hand_index, was_split in hands_to_play:
                    while True:
                        dealer_upcard = self.dealer.hands[0][0].rank if self.dealer.hands[0] else 'Unknown'
                        if player.name == "Player 1":
                            # Player 1 has the deviations
                            move = player.bestMove(dealer_upcard, hand_index)
                        else:
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
                            print(
                                f"{player.name} after DOUBLE: {' '.join(str(card) for card in player.hands[hand_index])}")
                            break
                        elif move == 'DOUBLE' and was_split:  # Prevent doubling after a split
                            print(f"{player.name} decides to DOUBLE, but doubling after a split is not allowed.")
                            move = 'HIT'  # Force a HIT instead of DOUBLE
                            player.add_card_to_hand(self.deck.deal_card(), hand_index)
                            print(
                                f"{player.name} HIT instead of DOUBLE -> {' '.join(str(card) for card in player.hands[hand_index])}")
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
        round_result = {}

        for player in self.players:
            if player.name == "Player 1" and player.bet == 0:
                round_result[player.name] = 0  # Player 1 sits out
                continue  # Skip summary for Player 1 if sitting out

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

            # Update player statistics
            player.wins += (total_win > 0)
            player.losses += (total_loss > 0)
            player.pushes += (total_push > 0 and total_win == 0 and total_loss == 0)

            # Summary for the player
            result_summary = "wins" if total_win > 0 else "loses" if total_loss > 0 else "pushes"
            print(f"{player.name} {result_summary}.")
            print(
                f"{player.name} has {player.wins} wins, {player.losses} losses, and {player.pushes} pushes. Also {player.blackjacks} Blackjacks")
            print(f"{player.name} has ${player.balance}\n")

            if player.name == "Player 1":
                round_result[player.name] = player.balance - initial_bet
        self.round_results.append(round_result)

    def print_summary_statistics(self):
        # Calculate and store returns for Player 1
        self.player_returns = []

        print(f"\nSummary Statistics after {self.num_rounds} rounds:")
        for player in self.players:
            if player.name == "Player 1":
                player_returns = []
                for round_result in self.round_results:  # Iterate through round results
                    if player.name in round_result:
                        player_returns.append(round_result[player.name])
                self.player_returns.extend(player_returns)

                # Calculate key statistics
                wins = player.wins
                losses = player.losses
                pushes = player.pushes
                total_hands = wins + losses + pushes

                # Calculate additional statistics
                win_rate = (wins / total_hands) * 100 if total_hands > 0 else 0
                loss_rate = (losses / total_hands) * 100 if total_hands > 0 else 0
                push_rate = (pushes / total_hands) * 100 if total_hands > 0 else 0
                blackjack_percentage = (player.blackjacks / total_hands) * 100 if total_hands > 0 else 0

                print(
                    f"{player.name} - Balance: ${player.balance}, Wins: {wins}, Losses: {losses}, Pushes: {pushes}, Blackjacks: {player.blackjacks}")
                print(
                    f"  - Win Rate: {win_rate:.2f}%, Loss Rate: {loss_rate:.2f}%, Push Rate: {push_rate:.2f}%, Blackjack Percentage: {blackjack_percentage:.2f}%, Hands Played: {total_hands}")

                # Additional statistics for Player 1 (card counter)
                returns = [x for x in self.player_returns]  # Calculate returns for each round
                if returns:
                    avg_return = statistics.mean(returns)
                    std_dev_return = statistics.stdev(returns) if len(returns) > 1 else 0  # Avoid division by zero
                    min_return = min(returns)
                    max_return = max(returns)
                    print(
                        f"  - Avg Return: ${avg_return:.2f}, Std Dev Return: ${std_dev_return:.2f}, Min Return: ${min_return:.2f}, Max Return: ${max_return:.2f}")

                    # Plot the returns over time
                    plt.figure(figsize=(10, 6))
                    plt.plot(returns, marker='o')
                    plt.title(f"{player.name}'s Returns Over Time")
                    plt.xlabel("Round")
                    plt.ylabel("Return ($)")
                    plt.grid(axis='y')
                    plt.show()
                else:
                    print("  - No returns to display")

class Simulation:
    def __init__(self, num_simulations=100, hands_per_simulation=10000):
        self.num_simulations = num_simulations
        self.hands_per_simulation = hands_per_simulation
        self.results_player_1 = []
        self.results_player_2 = []
        self.hands_played_stats_player_1 = []  # Track hands played for Player 1
        self.hands_played_stats_player_2 = []  # Track hands played for Player 2
        self.returns_player_1 = []  # Track returns for Player 1
        self.returns_player_2 = []  # Track returns for Player 2
        self.total_wins_player_1 = 0
        self.total_losses_player_1 = 0
        self.total_pushes_player_1 = 0
        self.total_blackjacks_player_1 = 0
        self.total_wins_player_2 = 0
        self.total_losses_player_2 = 0
        self.total_pushes_player_2 = 0
        self.total_blackjacks_player_2 = 0

    def run_simulation(self):
        for i in range(self.num_simulations):
            game = BlackjackGame(num_decks=8, num_players=3)
            game.play(num_rounds=self.hands_per_simulation)
            final_balance_player_1 = game.players[0]._get_balance()
            final_balance_player_2 = game.players[1]._get_balance()
            initial_balance = 500  # Initial balance for players
            self.results_player_1.append(final_balance_player_1)
            self.results_player_2.append(final_balance_player_2)
            self.hands_played_stats_player_1.append(game.hands_played_player_1)  # Track hands played for Player 1
            self.hands_played_stats_player_2.append(self.hands_per_simulation)  # Track hands played for Player 2
            self.returns_player_1.append(final_balance_player_1 - initial_balance)  # Calculate and store the return for Player 1
            self.returns_player_2.append(final_balance_player_2 - initial_balance)  # Calculate and store the return for Player 2

            # Accumulate wins, losses, and pushes
            self.total_wins_player_1 += game.players[0].wins
            self.total_losses_player_1 += game.players[0].losses
            self.total_pushes_player_1 += game.players[0].pushes
            self.total_blackjacks_player_1 += game.players[0].blackjacks
            self.total_wins_player_2 += game.players[1].wins
            self.total_losses_player_2 += game.players[1].losses
            self.total_pushes_player_2 += game.players[1].pushes
            self.total_blackjacks_player_2 += game.players[1].blackjacks

            print(f"Simulation {i + 1}/{self.num_simulations} completed. Player 1 balance: ${final_balance_player_1}, Player 2 balance: ${final_balance_player_2}")
            game.reset_game()  # Reset the game state for the next simulation

        self.analyze_results()

    def analyze_results(self):
        if not self.results_player_1 or not self.hands_played_stats_player_1 or not self.returns_player_1:
            print("No results to analyze.")
            return

        # Player 1 statistics
        avg_balance_player_1 = statistics.mean(self.results_player_1)
        std_dev_balance_player_1 = statistics.stdev(self.results_player_1) if len(self.results_player_1) > 1 else 0
        min_balance_player_1 = min(self.results_player_1)
        max_balance_player_1 = max(self.results_player_1)
        median_balance_player_1 = statistics.median(self.results_player_1)

        avg_hands_played_player_1 = statistics.mean(self.hands_played_stats_player_1)
        std_dev_hands_played_player_1 = statistics.stdev(self.hands_played_stats_player_1) if len(self.hands_played_stats_player_1) > 1 else 0
        min_hands_played_player_1 = min(self.hands_played_stats_player_1)
        max_hands_played_player_1 = max(self.hands_played_stats_player_1)
        median_hands_played_player_1 = statistics.median(self.hands_played_stats_player_1)

        total_hands_possible = self.num_simulations * self.hands_per_simulation
        avg_hands_played_percentage_player_1 = (avg_hands_played_player_1 / total_hands_possible) * 100  # Calculate percentage

        avg_return_player_1 = statistics.mean(self.returns_player_1)
        std_dev_return_player_1 = statistics.stdev(self.returns_player_1) if len(self.returns_player_1) > 1 else 0
        min_return_player_1 = min(self.returns_player_1)
        max_return_player_1 = max(self.returns_player_1)
        median_return_player_1 = statistics.median(self.returns_player_1)

        # Calculate total hands played
        total_hands_player_1 = self.total_wins_player_1 + self.total_losses_player_1 + self.total_pushes_player_1

        # Calculate win rate, loss rate, and push rate
        win_rate_player_1 = (self.total_wins_player_1 / total_hands_player_1) * 100 if total_hands_player_1 > 0 else 0
        loss_rate_player_1 = (self.total_losses_player_1 / total_hands_player_1) * 100 if total_hands_player_1 > 0 else 0
        push_rate_player_1 = (self.total_pushes_player_1 / total_hands_player_1) * 100 if total_hands_player_1 > 0 else 0
        blackjack_rate_player_1 = (self.total_blackjacks_player_1 / total_hands_player_1) * 100 if total_hands_player_1 > 0 else 0

        # Player 2 statistics
        avg_balance_player_2 = statistics.mean(self.results_player_2)
        std_dev_balance_player_2 = statistics.stdev(self.results_player_2) if len(self.results_player_2) > 1 else 0
        min_balance_player_2 = min(self.results_player_2)
        max_balance_player_2 = max(self.results_player_2)
        median_balance_player_2 = statistics.median(self.results_player_2)

        avg_return_player_2 = statistics.mean(self.returns_player_2)
        std_dev_return_player_2 = statistics.stdev(self.returns_player_2) if len(self.returns_player_2) > 1 else 0
        min_return_player_2 = min(self.returns_player_2)
        max_return_player_2 = max(self.returns_player_2)
        median_return_player_2 = statistics.median(self.returns_player_2)

        # Calculate total hands played
        total_hands_player_2 = self.total_wins_player_2 + self.total_losses_player_2 + self.total_pushes_player_2

        # Calculate win rate, loss rate, and push rate
        win_rate_player_2 = (self.total_wins_player_2 / total_hands_player_2) * 100 if total_hands_player_2 > 0 else 0
        loss_rate_player_2 = (self.total_losses_player_2 / total_hands_player_2) * 100 if total_hands_player_2 > 0 else 0
        push_rate_player_2 = (self.total_pushes_player_2 / total_hands_player_2) * 100 if total_hands_player_2 > 0 else 0
        blackjack_rate_player_2 = (self.total_blackjacks_player_2 / total_hands_player_2) * 100 if total_hands_player_2 > 0 else 0

        print(f"\nSimulation Results after {self.num_simulations} simulations:")
        print(f"  - Average Balance Player 1: ${avg_balance_player_1:.2f}")
        print(f"  - Standard Deviation Player 1: ${std_dev_balance_player_1:.2f}")
        print(f"  - Minimum Balance Player 1: ${min_balance_player_1:.2f}")
        print(f"  - Maximum Balance Player 1: ${max_balance_player_1:.2f}")
        print(f"  - Median Balance Player 1: ${median_balance_player_1:.2f}")
        print(f"  - Average Balance Player 2: ${avg_balance_player_2:.2f}")
        print(f"  - Standard Deviation Player 2: ${std_dev_balance_player_2:.2f}")
        print(f"  - Minimum Balance Player 2: ${min_balance_player_2:.2f}")
        print(f"  - Maximum Balance Player 2: ${max_balance_player_2:.2f}")
        print(f"  - Median Balance Player 2: ${median_balance_player_2:.2f}")

        print(f"\nHands Played Statistics for Player 1:")
        print(f"  - Average Hands Played: {avg_hands_played_player_1:.2f}")
        print(f"  - Standard Deviation: {std_dev_hands_played_player_1:.2f}")
        print(f"  - Minimum Hands Played: {min_hands_played_player_1}")
        print(f"  - Maximum Hands Played: {max_hands_played_player_1}")
        print(f"  - Median Hands Played: {median_hands_played_player_1}")
        print(f"  - Average Hands Played per 100 Simulations (Percentage): {avg_hands_played_percentage_player_1:.2f}%")

        print(f"\nReturn Statistics for Player 1:")
        print(f"  - Average Return: ${avg_return_player_1:.2f}")
        print(f"  - Standard Deviation: ${std_dev_return_player_1:.2f}")
        print(f"  - Minimum Return: ${min_return_player_1:.2f}")
        print(f"  - Maximum Return: ${max_return_player_1:.2f}")
        print(f"  - Median Return: ${median_return_player_1:.2f}")

        print(f"\nOverall Win/Loss/Push Statistics for Player 1:")
        print(f"  - Win Rate: {win_rate_player_1:.2f}%")
        print(f"  - Loss Rate: {loss_rate_player_1:.2f}%")
        print(f"  - Push Rate: {push_rate_player_1:.2f}%")
        print(f"  - Blackjack Rate: {blackjack_rate_player_1:.2f}%")

        print(f"\nReturn Statistics for Player 2:")
        print(f"  - Average Return: ${avg_return_player_2:.2f}")
        print(f"  - Standard Deviation: ${std_dev_return_player_2:.2f}")
        print(f"  - Minimum Return: ${min_return_player_2:.2f}")
        print(f"  - Maximum Return: ${max_return_player_2:.2f}")
        print(f"  - Median Return: ${median_return_player_2:.2f}")

        print(f"\nOverall Win/Loss/Push Statistics for Player 2:")
        print(f"  - Win Rate: {win_rate_player_2:.2f}%")
        print(f"  - Loss Rate: {loss_rate_player_2:.2f}%")
        print(f"  - Push Rate: {push_rate_player_2:.2f}%")
        print(f"  - Blackjack Rate: {blackjack_rate_player_2:.2f}%")

        # Plot the results for Player 1
        plt.figure(figsize=(10, 6))
        plt.plot(self.results_player_1, marker='o')
        plt.title("Player 1's Balance After Each Simulation")
        plt.xlabel("Simulation")
        plt.ylabel("Balance ($)")
        plt.grid(axis='y')
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(self.hands_played_stats_player_1, marker='o')
        plt.title("Number of Hands Played by Player 1 After Each Simulation")
        plt.xlabel("Simulation")
        plt.ylabel("Hands Played")
        plt.grid(axis='y')
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(self.returns_player_1, marker='o')
        plt.title("Player 1's Return After Each Simulation")
        plt.xlabel("Simulation")
        plt.ylabel("Return ($)")
        plt.grid(axis='y')
        plt.show()


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
    simulation = Simulation(num_simulations=40, hands_per_simulation=6000)
    simulation.run_simulation()
    # game = BlackjackGame(num_decks=8, num_players=3)
    # game.play(num_rounds=300000)
    # game.print_summary_statistics()
