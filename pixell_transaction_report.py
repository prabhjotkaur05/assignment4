"""This module contains a program that reads through transaction records
and reports the results.

Example:
    $ python pixell_transaction_report.py
"""

__author__ = "ACE Faculty"
__version__ = "0.11.2024"

import csv
import os

valid_transaction_types = ['deposit', 'withdraw']
customer_data = {}
rejected_transactions = []
transaction_count = 0
transaction_counter = 0
total_transaction_amount = 0
is_valid_record = True
error_message = ''

# Clears the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Get the directory the script is saved to
SCRIPT_DIRECTORY = os.path.dirname(__file__)

# The name of the data file
DATA_FILENAME = "bank_data.csv"

# The absolute path to the data file
DATA_FILE_PATH = f"{SCRIPT_DIRECTORY}/{DATA_FILENAME}"

if not os.path.exists(DATA_FILE_PATH):
    print(f"The bank data file ({DATA_FILENAME}) cannot be found.")
    exit()

with open(DATA_FILE_PATH, 'r') as csv_file:
    reader = csv.reader(csv_file)

    # Place breakpoint here
    next(reader)

    # Skip heading line
    next(reader)

    for transaction in reader:
        # Reset valid record and error message for each iteration
        is_valid_record = True
        error_message = ''

        # Gets the customer ID from the first column
        customer_id = transaction[0]
        
        # Gets the transaction type from the second column
        transaction_type = transaction[1]

        ### VALIDATION 1 ###
        if transaction_type not in valid_transaction_types:
            is_valid_record = False
            error_message = f'The transaction type "{transaction_type}" is invalid.'

        ### VALIDATION 2 ###
        try:
            transaction_amount = float(transaction[2])
        except ValueError:
            is_valid_record = False
            error_message = f'"{transaction[2]}" is an invalid transaction amount.'

        if is_valid_record:
            # Initialize the customer's account balance if it doesn't 
            # already exist
            if customer_id not in customer_data:
                customer_data[customer_id] = {'balance': 0, 'transactions': []}
            # Update the customer's account balance based on the 
            # transaction type
            elif transaction_type == 'deposit':
                customer_data[customer_id]['balance'] += transaction_amount
                transaction_count += 1
                total_transaction_amount += transaction_amount
            elif transaction_type == 'withdraw':
                customer_data[customer_id]['balance'] -= transaction_amount
                transaction_count += 1
                total_transaction_amount += transaction_amount
            
            # Record transactions in the customer's transaction history
            customer_data[customer_id]['transactions'].append(
                (transaction_amount, transaction_type)
                )
        else:
            ### COLLECT INVALID RECORDS ###
            rejected_transactions.append((transaction, error_message))
        
report_title = "PiXELL River Transaction Report"
print(report_title)
print('=' * len(report_title))

# Print the final account balances for each customer
for customer_id, data in customer_data.items():
    balance = data['balance']

    print(f"Customer {customer_id} has a balance of {balance}.")
    
    # Print the transaction history for the customer
    print("Transaction History:")

    for transaction in data['transactions']:
        amount, type = transaction
        print(f"{type.capitalize():>16}:{amount:>12}")

average_transaction_amount = total_transaction_amount / transaction_count
print(f"AVERAGE TRANSACTION AMOUNT: {average_transaction_amount}")

rejected_report_title = "REJECTED RECORDS"
print(rejected_report_title)
print('=' * len(rejected_report_title))

for rejected_transaction in rejected_transactions:
    print("REJECTED:", rejected_transaction)
