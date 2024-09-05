'''This file is for evaluating the log file coming from the simulator.py. Goal is to make sure all features are working correctly'''

import logging
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        log_entries = file.readlines()
    return log_entries

import re

def parse_log_entries(log_file_path):
    log_entries = []
    with open(log_file_path, 'r') as file:
        for line in file:
            log_parts = line.split(" - ", 2)
            if len(log_parts) < 3:
                print(f"Skipping malformed log line: {line.strip()}")
                continue

            timestamp = log_parts[0].strip()
            level = log_parts[1].strip()
            message = log_parts[2].strip()

            log_entries.append({'timestamp': timestamp, 'level': level, 'message': message})
    return log_entries

def update_tracking_betting(entry, player_1_bets, player_1_balances, player_1_sitting_out):
    message = entry['message']

    if "Player 1 is sitting out due to low betting count." in message:
        player_1_sitting_out.append(True)
        return

    if "Player 1 placed a bet of" in message:
        player_1_sitting_out.append(False)
        bet_amount = int(message.split('$')[1].split('.')[0])
        initial_balance = int(message.split('$')[2].split('.')[0])
        player_1_bets.append(bet_amount)
        player_1_balances.append(initial_balance)

    if player_1_sitting_out and player_1_sitting_out[-1]:
        return

    if "Player 1 after DOUBLE:" in message:
        if player_1_bets:
            player_1_balances[-1] -= player_1_bets[-1]
            player_1_bets[-1] *= 2
        else:
            print("Warning: DOUBLE detected without an initial bet")

    elif "Player 1 wins insurance bet" in message:
        if player_1_bets:
            insurance_bet_amount = player_1_bets[-1] / 2
            player_1_balances[-1] += insurance_bet_amount * 2
        else:
            print("Warning: Insurance win detected without an initial bet")

    elif "Player 1 decides to SPLIT." in message:
        if player_1_bets:
            player_1_balances[-1] -= player_1_bets[-1]
            player_1_bets.append(player_1_bets[-1])
        else:
            print("Warning: Split detected without an initial bet")

    elif "Player 1" in message:
        if player_1_bets:
            if "wins" in message:
                bet_amount = player_1_bets.pop(0)
                player_1_balances[-1] += bet_amount * 2  # Winning returns bet + winnings
            elif "loses" in message:
                bet_amount = player_1_bets.pop(0)
                player_1_balances[-1] -= bet_amount  # Losing subtracts bet
            elif "pushes" in message:
                player_1_bets.pop(0)  # No balance change for push
            elif "Blackjack" in message:
                bet_amount = player_1_bets.pop(0)
                player_1_balances[-1] += bet_amount * 1.5  # Blackjack pays 3:2
        else:
            print("Warning: Outcome detected without an initial bet")

def check_payouts(log_file_path):
    log_entries = parse_log_entries(log_file_path)
    player_1_bets, player_1_balances, player_1_sitting_out = initialize_tracking(log_entries)
    payouts_issues = []

    for entry in log_entries:
        if "Player 1" in entry['message']:
            update_tracking_betting(entry, player_1_bets, player_1_balances, player_1_sitting_out)

            if "Player 1 has $" in entry['message']:
                actual_balance = int(entry['message'].split('$')[1].split('.')[0])
                expected_balance = player_1_balances[-1]

                if actual_balance != expected_balance:
                    payouts_issues.append({
                        'entry': entry,
                        'expected_balance': expected_balance,
                        'actual_balance': actual_balance
                    })

    return payouts_issues

# Helper function to initialize tracking from the log entries
def initialize_tracking(log_entries):
    player_1_bets = []
    player_1_balances = []
    player_1_sitting_out = []

    for entry in log_entries:
        if "Player 1 placed a bet of" in entry['message']:
            bet_amount = int(entry['message'].split('$')[1].split('.')[0])
            initial_balance = int(entry['message'].split('$')[2].split('.')[0])
            player_1_bets.append(bet_amount)
            player_1_balances.append(initial_balance)
            player_1_sitting_out.append(False)
            break  # Only need to initialize from the first bet entry

    return player_1_bets, player_1_balances, player_1_sitting_out

if __name__ == "__main__":
    log_file_path = #Removed for Privacy purposes but used as path/to/log_file
    payouts_issues = check_payouts(log_file_path)
    if payouts_issues:
        print(f"Payout issues found: {payouts_issues}")
    else:
        print("No payout issues found.")
