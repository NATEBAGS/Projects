import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import counter
import itertools

#Account 1/2 were updated 13 Feb 10AM
'''These are the returns for a returns on 1000+ blackjack hands'''
returns1000 = [10, -5, 5, -5, 10, 0, -5, -5, -5, -10, 5, 0, 5, -5, 7.50, 10, -5, -5, 5, -15, -20, 16, 0, 0, -5, -5, 10 - 5,
           5, 5, 5, -10, 5, 10, 5, 7.50, 0, -5, -5, 5, 5, 5, -5, 5, -5, 5, 5, -5, 5, 5, 5, -5, -5, 5, -10, -10, -40, -5,
           5, -6, 5, -10, 5, 7.5, 5, 0, 2.5, 5, -5, -5, 5, -5, 5, -5, 0, -5, -5, -5, 0, 5, -5, 7.5, -5, 5, -5, 5, 5, 5,
           7.5, -5, 0, 5, -5, -5, -5, -5, -10, 5, 0, -5, -5, -5, -5, -10, -5, 5, -15, -5, -5, 10, -5, 5, 5, -5, 5, 5,
           -5, 5, 5, -5, -5, -5, 5, -5, 5, -5, 5, 0, 0, 5, 10, 0, 5, -5, 10, 5, 10, 5, -10, -5, 0, 5, -10, -5, -10, 5,
           10, 0, -5, -10, 5, 0, 5, 7.5, 10, 7.5, 30, 20, 0, 0, 0, 5, 25, -15, 15, 10, -10, 5, -2.5, -5, -7.5, 10, 5,
           -10, -2.5, 12.5, -10, 20, 30, -10, -15, 15, -5, 17.5, -5, -5, -10, 5, 10, 7.5, -5, 0, 12.5, -5, -5, 10, 5,
           -5, -5, 7.5, -5, -10, 10, 0, 0, 20, -5, -5, 15, -5, -5, 5, -5, -5, 15, -10, 15, 2.5, -5, 5, -5, 10, -5, -10,
           -10, -5, -5, 0, -10, 0, -20, 5, -5, 17.5, -5, 7.5, -5, -5, 0, 5, -5, -5, -10, -10, 15, 5, -5, 3, 5, 5, -5,
           -5, -10, 7.5, 5, 7.5, 5, -5, -5, -5, 7.5, 10, 0, 10, 15, 0, -20, -5, -5, 7.5, 0, -5, 10, 0, -5, -10, -5, 5,
           5, -5, 5, -5, 10, -5, 0, 5, 5, 2.5, 10, -10, -5, -5, -5, 5, -10, -10, 5, 5, -10, 12.5, 5, 7.5, 5, -5, 5, -10,
           -10, -5, -5, 5, -5, -5, -5, 5, 5, 5, 5, 5, -5, -5, -5, 7.5, 5, 5, -5, 5, -10, -10, 25, -10, -40, -22.5, -10,
           5, 5, -5, -5, 10, 5, -5, -5, -10, 5, -10, 0, 0, 0, -5, 5, -5, 5, 10, 15, 20, 5, 5, -5, -10, -5, -5, 5, -10,
           10, -20, 0, -10, -5, 5, 5, 0, -5, -5, -5, 5, -5, 5, -5, -5, 0, 5, -5, 10, -5, -5, 10, 5, 5, 5, -5, 5, -5, 5,
           5, 5, 5, 5, 5, -10, 10, 5, -5, 7.5, -5, -10, -10, 15, -5, 5, 10, -10, 5, 0, 2.5, -5, 10, -10, 5, -5, 5, 10,
           5, 5, 10, -5, 10, -10, 2.5, 2.5, 5, 5, 5, 5, -5, -5, -5, -5, 5, -5, -10, -5, -15, 7.5, -15, 0, -5, 0, 10, 5
           , -6, 10, -15, 5, -10, -5, -5, -5, -5, -5, 5, 5, 10, 10, 5, 10, 5, 5, 5, -15, 0, -5, 5, 5, -5, 5, 5, -15, 0,
           -5, -5, 10, 5, -10, 0, -5, 5, 0, -5, 5, -5, -5, 0, -5, -5, -10, -10, 5, -5, -5, 7.5, 0, -5, 0, 5, -5, 5, -5,
           5, 10, -10, 0, 15, 10, -5, 5, 7.5, 5, -5, -10, -5, 7.5, -5, -10, 10, 5, -5, 0,-5, 5, -5, -5, -10, 0, 2.5, 0,
           -10, -5, -10, 15, -10, -10, 5, 10, 10, -7.50, 5, 10, 15.01, 0, 2, 0, 5, 5, -5, 5, 0, -5, 5, -5, -5, 5, 5, -5
           -5, 5, -5, 5, -10, -5, 0, 0, 2.5, 5, 5, 5, -5, -5, 7.5, 5, -10, 0, -5, -10, -10, -5, -5, -5, 10, -5, -5, -5,
           -5, 5, 0, -5, -5, 5, -5, -5, -5, 5, 5, 5, 5, 5, -10, -5, -5, -5, 5, 5, -5, -5, 5, -10, 5, -5, 0, 7.5, -10, 5,
           15.01, 15.01, -10, 0, 5, 5, -10, -5, 0, -5, 7.5, 5, 5, 0, 5, -10, -5, -5, -5, 5, -5, 0, -5, 15.01, 5, 5, -10,
           5, 5, -5, 5, -5, 5, -5, -5, -5, 5, -5, 7.5, 5, -5, -10, 5, 5, 5, 7.5, 5, -5, 0, -5, 15.01, 5, 5, -10, 5, 5,
           -5, 5, -5, 5, -5, -5, -5, -5, 5, 7.5, 10, 5, 5, 5, 5, 5, -5, 5, 5, -5, 5, 5, 7.5, 5, -5, 7.5, 5, -5, -10, 5,
           5, 5, 7.5, -5, 2.5, -5, -5, -5, -5, 5, 5, -5, 5, 5, 0, 10, 5, 0, -5, -10, 10, 5, -5, 5, 10, 10, 5, 5, 5, -5,
           10, -5, -5, -5, 0, -5, 5, -5, -5, 5, -5, -5, 0, -5, 5, 5, 0, 5, -5, -5, -5, -5, 5, 10, 5, 5, 5, -5, 0, 5, 5,
           0, 7.5, 5, 5, -5, -5, 7.5, -5, -5, -5, 12.50, -5, 10, -5, -5, 7.5, 5, -5, -5, -5, 7.5, -5, -5, -5, 5, 0, 0,
           5, 5, -5, 5, 5, -10, 5, 5, 5, 5, 5, 7.5, 7.5, 5, 0, 5, 10, -10, 5, -5, 0, -5, 10, 0, 5, 0, 0, 7.5, -5, -5,
           5, 0, 5, -5, -5, -5, 5, 0, -10, 10, -5, 7.5, -5, 0, 10, -5, 5, -5, 5, 10, 7.5, 5, -5, -15, -5, 5, 20, -5, 5,
           -10, 5, -5, -5, -10, -5, 5, 5, -10, -5, 7.5, 5, -5, 5, 5, -5, -5, -5, 5, 5, 0, 10, -5, 5, -5, 5, 0, -10, -5,
           -5, 7.5, 7.5, -5, 0, 0, -5, 5, -5, -5, 0, -5, -10, 0, 7.5, 5, 5, 10, 5, -5, 5, 7.5, 10, 7.5, 10, -5, -5, -5,
           5, -5, 10, -10, 5, -5, 5, 5, 5, 7.5, -5, -5, -5, -5, -10, 5, -5, 5, 5, 5, -5, 5, -5, 5, 5, 10, -5, -5, -10,
           -10, -10, -5, 10, -10, -10, -10, 5, -5, -5, -5, 10, 5, 5, 5, -5, -5, -5, -5, 5, 0, -5, 5, 5, -10, -10, 5, -5,
           10, -5, 5, -10, -10, 5, -5, 5, 0, 5, 0, 5, -5, 5, 5, 0, 5, -5, 7.5, 5, -5, 0, -5, 0, 5, -5, 5, -5, 5, -5, -5,
           -5, -20, 10, 5]

returns1124 = [0, -10, -10, -10, -5, 10, -5, 5, 5, 5, 5, 10, -5, -5, 5, 0, -5, 0, -5, 5, -15, -5, -5, -5, 5, -5, -5, -5,
               -5, -5, -5, -5, 5, -5, 5, -5, 5, -5, -5, -5, -10, -5, 7.5, -5, -5, -5, -5, -5, -5, -5, -5, 5, 5, 0, 5, -5,
               5, -5, -5, -5, -5, 5, -5, 5, -5, 7.5, -5, 5, -5, 5, -5, 5, -5, 7.5, -5, 5, -5, 10, 5, 5, 5, 5, 5, -10, -5,
               5, -5, -5, -5, 5, -5, -5, 5, 0, -5, -5, 10, -5, -5, -5, 5, 5, 0, -5, -5, -5, -5, -10, 7.5, -5, 5, 5, 5, 5,
               -10, 5, 10, -5, 5, 5, -10, 10, 0, -5]

kelly_returns =[-5, -5, 0, -5, -5, 0, -10, -13, 7.5, -5, 5, -20, -15, -15, -22.5, 15, 20, 10, 5, 0, 5, 5, -10, 5, -5, -5,
                -15, 0, 22.5, -5, -5, 5, -6, 6, 0, 10, -10, -15, 15, 10, -10, 5, 7.5, -5, -10, -5, -5, -10, 5, 6, -5, 10,
                5, 0, 7.5, -5, -10, -5, -5, 5, -5, 5, 7.5, 10, 15, -10, -6, 5, 5, -8, 5, -5, 7.5, -7, -7, 5, -6, -5, -6,
                0, -5, -5, -5, 5, -5, 10, 10, 0, 5, 6, 7, 0, -10, -15, 6, -5, 9.01, 5, 5, -5, -10, 5, 10, 5, 5, -5, -5,
                5, -10, 0, -6, -5, -5, -5, 7, -10, 5, -10, 6, -6, -10, -10, -5, -5, 5, -5, -5, 5, -7, 5, 0, -12, -7, -12,
                10, -10, -6, 5, -6, -5, -5, -6, 5, 5, 0, 6, -5, 14, 6, -10, -15, -12, 0, -9, -5, -5, 5, -5, 5, 5, 0, -10,
                6, -5, 5, -5, 6, 5, 6, -5, -10, -10, 0, -12, -14, -10, 5,  -5, 0, 5, -14, 0, 0, -5, 5, 5, -5, 10.5, 15, 0,
                -10, 0, 8, 5, 7.5, 5, 5, -5, -5, 10, 5, 0, 0, -5, 0, -5, 0, 5, 5, 0, -6, 5, -18, -10, -6, -5, 5, 5, -5, -5,
                10, 7.5, -5, -5, -6, -5, 12, -8, 10, 10, -10, 0, -9, 7.5, -5, -10, 10, 0, -5, 5, -5, 5, -5, -5, 0, -5, -5,
                0, -7, -6, 6, 6, 0, -5, 5, -6, 0, 10, -15, 10, 0, -5, 5, -8, 10, -10, 10, 10] #03/08/24 16:46:43
returns = returns1000 + returns1124 + kelly_returns

'''Chunk the list into sessions of (returns, x) rounds each'''

Account_3 = [10, 5, 5, 5, -5, 7.5, 5, 15, -5, -10, -5, 0, -5, -5, -5, -5, -6, 10, 5, 0, 10, 5, 7.5, 7.5, 5, 10.5, -15, -5, 5,
                 -7, 7.5, 10, -10, 10, -5, -5, -5, -5, 10, -7, 10, -10, 10]

def chunk_sessions(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
'''This prints every session and can be changed with the session variable (chunk_size)'''
def print_sessions(sessions):
    # Initialize counters
    test_W = 0
    test_L = 0
    test_P = 0
    test_BJ = 0
    sum_T = 0
    # Iterate over each session
    for session in sessions:
        for i in session:
            sum_T += i
            if i > 0:
                test_W += 1
            if i < 0:
                test_L += 1
            if i == 0:
                test_P += 1
            if i > 0 and isinstance(i, float):
                test_BJ += 1
        print("Wins:", test_W)
        print("Losses:", test_L)
        print("Pushes:", test_P)
        print("Blackjacks", test_BJ)
        print("Session AV:", sum_T)
        print("Session EV:", (test_W - test_BJ + test_L) + (test_BJ * 1.5) * 5)
        test_W = 0
        test_L = 0
        test_P = 0
        sum_T = 0
        test_BJ = 0

# Function to calculate standard deviation
def calculate_standard_deviation(returns):
    # Calculate mean
    returns_mean = np.mean(returns)

    # Calculate squared differences
    squared_diff = (returns - returns_mean) ** 2
    #print(squared_diff)

    # Calculate variance
    global variance
    variance = np.sum(squared_diff) / len(returns)

    # Calculate standard deviation
    standard_deviation = np.sqrt(variance)


    return standard_deviation

def plot_blackjack_results(returns):
    # Create a list to store the cumulative sum of returns
    cumulative_returns = [returns[0]]

    # Calculate cumulative returns
    for i in range(1, len(returns)):
        cumulative_returns.append(cumulative_returns[-1] + returns[i])

        # Perform linear regression
        x = np.arange(len(cumulative_returns))
        y = np.array(cumulative_returns)
        slope, intercept = np.polyfit(x, y, 1)

    # Plot the cumulative returns
    plt.plot(cumulative_returns, label='Cumulative Returns')
    plt.plot(x, slope * x + intercept, color='red', linestyle='-', label='Line of best Fit')

    # Highlight winning streaks and losing streaks
    # for i in range(1, len(cumulative_returns) - 5):
    #      if returns[i] > 0 and returns[i + 1] > 0 and returns[i + 2] > 0 and returns[i + 3] > 0 and returns[i + 4] > 0 and returns[i + 5] > 0:
    #           plt.axvline(x=i, color='green', linestyle='--', alpha=0.5)#label='Winning Streak
    #      if returns[i] < 0 and returns[i + 1] < 0 and returns[i + 2] < 0 and returns[i + 3] < 0 and returns[i + 4] < 0 and returns[i + 5] < 0:
    #          plt.axvline(x=i, color='red', linestyle='--', alpha=0.5)#label='Losing Streak'
    last_round = len(cumulative_returns) - 1  # Assuming cumulative_returns contains the data
    expected_value = slope * last_round + intercept


    # Customize the plot
    plt.title('Blackjack History of returns')
    plt.xlabel('Round')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()

    return expected_value

def plot_blackjack_GrossWL(x):
    plt.hist(x, bins=50, edgecolor='black')
    plt.title('Distribution of Returns')
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    plt.show()

def printGeneralstats(x, wins, losses, push, bjCount, EV, AV, std_deviation, z_score, mean):
    print(f'Number of rounds thus far: {x}')
    print(f'We have {wins} wins, {losses} losses, and {push} pushes. {bjCount} of the wins were blackjacks')
    print(f'Our win percentage is {(wins / x) * 100}%   ')
    print(f"Blackjack Percentage:, {(bjCount / x) * 100}%")
    print(f'Our loss percentage is {(losses / x) * 100}%')
    print(f'Our Push percentage is {(push / x) * 100}%')
    print(f'Expected Value: {EV}')
    print(f'Actual Value: {AV}')
    print('Variance:', variance)
    print("Standard Deviation:", std_deviation)
    print("Z-Score:", z_score)
    print("Mean:", mean)
    print(f"Average Advantage: {average_advantage * 100}%")
    print("Total Stake:", total_staked)

'''General Code'''
#Expected Value calculation
cumulative_returns = [returns[0]]

# Calculate cumulative returns
for i in range(1, len(returns)):
    cumulative_returns.append(cumulative_returns[-1] + returns[i])
    x = np.arange(len(cumulative_returns))
    y = np.array(cumulative_returns)
    #Creating a linear regression of our AP model
    slope, intercept = np.polyfit(x, y, 1)
last_round = len(cumulative_returns) - 1  # Assuming cumulative_returns contains the data
EV = slope * last_round + intercept
rounds = len(returns)
AV = 0
insurance_losses = 4
bjCount = 0
#Iterating through returns to find our outcomes and number of blackajacks
for i in returns:
    AV += i
    if isinstance(i, float):
        bjCount += 1

bjCount = bjCount - insurance_losses
#Calculating Wins, Losses, Push
losses = 0
wins = 0
push = 0
for i in returns:
    if i > 0:
        wins += 1
    if i < 0:
        losses += 1
    if i == 0:
        push += 1

std_deviation = calculate_standard_deviation(returns)
mean = np.mean(returns)
std_rounds = std_deviation * np.sqrt(rounds)
#Calculating estimated z-score
blackjack_zscore = ((AV - EV) / std_rounds)#bj_SD

sessions = list(chunk_sessions(returns, 50))
total_staked = 0
for i in returns:
    if i == 0:
        total_staked += 5
    if i == 7.5:
        total_staked -= 2.5
    total_staked += abs(i)
total_staked = total_staked - ((bjCount / 2) * 5)
average_advantage = (EV / total_staked) #Multiplied by 100 in the print func
counter = 0
largest = 0
win_streak = 0
# for i in range(len(returns)):
#     if returns[i] > 0:
#         win_streak += 1
#     if largest < win_streak:
#         largest = win_streak
#     if returns[i] == 0:
#         pass
#     if returns[i] < 0:
#         win_streak = 0
#     if win_streak == 7:
#         counter += 1
# print(largest)
# print(counter)
'''All testsing code for now'''
deck = {
    'A': 32,   # Four Aces per deck, so 32 in total
    '2': 32,   # Four 2s per deck, so 32 in total
    '3': 32,   # Four 3s per deck, so 32 in total
    '4': 32,   # Four 4s per deck, so 32 in total
    '5': 32,   # Four 5s per deck, so 32 in total
    '6': 32,   # Four 6s per deck, so 32 in total
    '7': 32,   # Four 7s per deck, so 32 in total
    '8': 32,   # Four 8s per deck, so 32 in total
    '9': 32,   # Four 9s per deck, so 32 in total
    '10': 128, # Four 10s (including J, Q, K) per deck, so 128 in total
}

num_A = deck['A']
num_2 = deck['2']
num_3 = deck['3']
num_4 = deck['4']
num_5 = deck['5']
num_6 = deck['6']
num_7 = deck['7']
num_8 = deck['8']
num_9 = deck['9']
num_10 = deck['10']

#num_10 = len(counter.deck['10']) + len(counter.deck['j']) + len(counter.deck['q']) + len(counter.deck['k'])
card_counts = [num_A, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9, num_10]
def probability_bust(self, sumHand):
    bustCount = 0
    num_A = len(self.deck['a'])
    num_2 = len(self.deck['2'])
    num_3 = len(self.deck['3'])
    num_4 = len(self.deck['4'])
    num_5 = len(self.deck['5'])
    num_6 = len(self.deck['6'])
    num_7 = len(self.deck['7'])
    num_8 = len(self.deck['8'])
    num_9 = len(self.deck['9'])
    num_10 = len(self.deck['10']) + len(self.deck['j']) + len(self.deck['q']) + len(self.deck['k'])

    safe_cards = 21 - sumHand
    bust_cards = 10 - safe_cards

    card_counts = [num_A, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9, num_10]

    #Counts the number of bust cards
    for i in range(bust_cards, len(card_counts)):
        bustCount += card_counts[i]

    #Calculates the bust probability
    totalCardsLeft = sum(card_counts)
    bustProbability = bustCount / totalCardsLeft

    return bustProbability

def x_choose_y(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1

    numerator = 1
    denominator = 1
    for i in range(k):
        numerator *= n - i
        denominator *= i + 1

    return numerator // denominator

answer = x_choose_y(200, 2)

def get_blackjack_combinations(number):
    tens = 128#len(counter.deck['10']) + len(counter.deck['j']) + len(counter.deck['q']) + len(counter.deck['k'])
    aces = 32#len(counter.deck['a'])

    return (tens * aces) / number

def dealer_odds(upcard, cards_remaining):
    if upcard == 10:
        winning_combinations = x_choose_y(cards_remaining, 5)
    if upcard == 9:
        winning_combinations = x_choose_y(cards_remaining, 4)
    if upcard == 8:
        winning_combinations = x_choose_y(cards_remaining, 3)
    if upcard == 7:
        winning_combinations = x_choose_y(cards_remaining, 2)
    if upcard == 6:
        winning_combinations = x_choose_y(cards_remaining, 1)
    return winning_combinations

def p(outcome):
    pass
    return 0


def calculate_bust_probability(upcard, card_counts):
    bust_count = 0
    total_combinations = 0
    max_cards_per_hand = 6

    # All possible combinations of card draws up to a maximum of six cards per hand
    for hand_size in range(2, max_cards_per_hand + 1):
        for draw_sequence in itertools.combinations_with_replacement(range(1, 11), hand_size):
            dealer_total = upcard + sum(draw_sequence)

            # Check for soft hands (Ace being counted as 11 without busting)
            if 1 in draw_sequence and dealer_total + 10 <= 21:
                dealer_total += 10

            # Check if the dealer can use Ace as 1 to avoid busting
            if 1 in draw_sequence and dealer_total > 21:
                dealer_total -= 10

            if dealer_total >= 17 and dealer_total <= 21:
                bust_count += 1

            total_combinations += 1

    #Calculates the probability of reaching {17, 18, 19, 20, 21} without busting
    bust_probability = bust_count / total_combinations
    return bust_probability

if __name__ == "__main__":
    plot_blackjack_results(returns)
    printGeneralstats(rounds, wins, losses, push, bjCount, EV, AV, std_deviation, blackjack_zscore, mean)
    #print_sessions(sessions)
    #plot_blackjack_GrossWL(returns)
    #print(get_blackjack_combinations(answer))
