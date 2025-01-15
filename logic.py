from itertools import combinations
import pandas as pd

from io import StringIO


# Function to read transactions from a CSV file and filter based on percentage
def read_transactions(file_contents, percentage=100.0):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(StringIO(file_contents))

    # print(pd.isnull(df).sum().sum())
    df.dropna(axis=0, how='any', inplace=True)

    # Calculate the number of unique transactions
    num_transactions = df['TransactionNo'].nunique()

    # Calculate the number of transactions to read based on the percentage
    num_transactions_to_read = int(num_transactions * (percentage / 100))

    # Get the unique transaction numbers to read
    unique_transactions = df['TransactionNo'].unique()[:num_transactions_to_read]

    # Select transactions subset based on the unique transaction numbers
    transactions_subset = df[df['TransactionNo'].isin(unique_transactions)]

    # Convert the transactions subset DataFrame into a dictionary of transactions
    transactions = {}
    for _, row in transactions_subset.iterrows():
        transaction_no = row['TransactionNo']
        item = row['Items']
        if transaction_no in transactions:
            transactions[transaction_no].append(item)
        else:
            transactions[transaction_no] = [item]

    return transactions


# Function to generate candidate itemsets of a given size
def generate_candidate_itemsets(transactions, frequent_itemsets, size):
    candidate_itemsets = []
    if size == 1:
        # If generating itemsets of size 1, create singleton itemsets from unique items in transactions
        unique_items = set()
        for items in transactions:
            for item in items:
                unique_items.add(item)

        candidate_itemsets = []
        for item in unique_items:
            candidate_itemsets.append((item,))  # Store as singe item

    else:
        # For larger itemset sizes, combine frequent itemsets of size k-1 to generate candidates
        for itemset1 in frequent_itemsets:
            for itemset2 in frequent_itemsets:
                # Combine two frequent itemsets if the first k-1 items are equal and check that last item in set1
                # comes before the last item in set2 to prevent duplicate combinations
                if itemset1[:-1] == itemset2[:-1] and itemset1[-1] < itemset2[-1]:

                    # Combine itemsets by taking their union and sorting the result
                    combined_set = set(itemset1) | set(itemset2)  # Union
                    sorted_combined_set = sorted(combined_set)  # Sort
                    candidate = tuple(sorted_combined_set)  # Store as tuple

                    # Add the candidate to the list if it is of the desired size and not already present
                    if len(candidate) == size and candidate not in candidate_itemsets:
                        candidate_itemsets.append(candidate)
    return candidate_itemsets


# Generate frequent itemsets using the Apriori algorithm.
def generate_frequent_itemsets(transactions, min_support_count):
    frequent_itemsets = {}  # Store frequent itemsets as Dictionary (Map)
    k = 1  # Initialize itemset size
    highest_order_with_min_support = 1  # Keep track of the highest order itemset with min support

    # Iterate until no more frequent itemsets can be found
    while True:
        # Generate candidate itemsets of size k
        candidate_itemsets = generate_candidate_itemsets(transactions, frequent_itemsets, k)

        # If no candidate itemsets are generated, terminate the loop
        if not candidate_itemsets:
            break

        # Calculate the support Count for each candidate itemset in the transactions
        support_counts = {}
        for transaction in transactions:
            for candidate in candidate_itemsets:
                # Check if the candidate itemset is a subset of the transaction
                if set(candidate).issubset(set(transaction)):
                    # Increment support count for the candidate itemset
                    if candidate in support_counts:
                        support_counts[candidate] += 1
                    else:
                        support_counts[candidate] = 1

        # Filter candidate itemsets to obtain frequent itemsets with support_count >= min_support
        frequent_candidate_itemsets = {}
        for itemset, support_count in support_counts.items():
            if support_count >= min_support_count:
                frequent_candidate_itemsets[itemset] = support_count

        # If any frequent itemsets are found, update the frequent itemsets dictionary
        if frequent_candidate_itemsets:
            frequent_itemsets.update(frequent_candidate_itemsets)
        else:
            # If no frequent itemsets are found, terminate the loop
            break

        # Update the highest order itemset with min support count
        if k >= highest_order_with_min_support:
            if frequent_candidate_itemsets:
                highest_order_with_min_support = k
            else:
                break

        # Increment itemset size for the next iteration
        k += 1

    return frequent_itemsets


# Function to calculate the support count of an itemset in transactions
def support_count(itemset, transactions):
    count = 0  # Initialize support count

    # Iterate through each transaction in the list of transactions
    for transaction in transactions:
        if isinstance(itemset, tuple):  # Check if the itemset is a tuple (multiple items)
            # Check if the itemset is a subset of the transaction
            if set(itemset).issubset(set(transaction)):
                count += 1  # Increment support count if the itemset is found in the transaction
        else:  # If the itemset is not a tuple (single item)
            # Check if the single item is present in the transaction
            if itemset in transaction:
                count += 1  # Increment support count if the item is found in the transaction

    return count


# Function to generate association rules with minimum confidence
def generate_association_rules(frequent_itemsets, min_confidence, transactions):
    association_rules = []  # List to store generated association rules

    if not frequent_itemsets:
        return  # Return early if frequent_itemsets is empty

    # Find the maximum length among frequent itemsets
    max_length = max(len(itemset) for itemset in frequent_itemsets)

    # Filter frequent itemsets to include only those with the maximum length
    highest_order_frequent_itemsets = [itemset for itemset in frequent_itemsets if len(itemset) == max_length]

    # Generate association rules for each highest order itemset
    for itemset in highest_order_frequent_itemsets:
        if len(itemset) > 1:
            # Generate all possible antecedents of the itemset
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    # If antecedent is single item, convert it to a tuple
                    if isinstance(antecedent, str):
                        antecedent = (antecedent,)

                    # List to store consequent items
                    consequent_items = []

                    # Iterate over each item in the itemset
                    for item in itemset:
                        # Check if the item is not in the antecedent
                        if item not in antecedent:
                            # If not, add it to the list of consequent items
                            consequent_items.append(item)

                    # Convert the filtered items into a tuple to represent the consequent
                    consequent = tuple(consequent_items)

                    # Calculate confidence measures for the association rule
                    # Confidence of antecedent => consequent
                    confidence_antecedent_to_consequent = support_count(itemset, transactions) / support_count(
                        antecedent, transactions)

                    # Confidence of consequent => antecedent
                    confidence_consequent_to_antecedent = support_count(itemset, transactions) / support_count(
                        consequent, transactions)

                    # Check if confidence meets the minimum threshold for both directions
                    if confidence_antecedent_to_consequent >= min_confidence:
                        # Check if the association rule is unique and add it to the list
                        if (antecedent, consequent) not in [(rule[0], rule[1]) for rule in association_rules]:
                            association_rules.append((antecedent, consequent, confidence_antecedent_to_consequent))
                    if confidence_consequent_to_antecedent >= min_confidence:
                        # Check if the association rule is unique and add it to the list
                        if (consequent, antecedent) not in [(rule[0], rule[1]) for rule in association_rules]:
                            association_rules.append((consequent, antecedent, confidence_consequent_to_antecedent))

    return association_rules
