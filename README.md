### README

# Apriori Algorithm Project

## Overview

This project implements the Apriori algorithm for mining frequent itemsets and generating strong association rules from a CSV file containing transaction data. The application is built using Python and the `customtkinter` library for the graphical user interface (GUI).

## Features

- **Upload CSV File**: Allows users to upload a CSV file containing transaction data.
- **Show File Contents**: Displays the contents of the uploaded CSV file in a new window.
- **Calculate Frequent Sets**: Computes frequent itemsets based on a specified percentage of transactions and minimum support count.
- **Calculate Association Rules**: Generates strong association rules based on the frequent itemsets and a specified minimum confidence.

## Project Structure

```
.
├── main.py
├── ui_elements.py
├── ui_trigger_functions.py
├── validation_functions.py
├── logic.py
└── README.md
```

### `main.py`

This is the entry point of the application. It sets up the main window and calls the function to create and layout the UI elements.

### `ui_elements.py`

Contains the function to create and layout the UI elements in the main window.

### `ui_trigger_functions.py`

Contains the functions that are triggered by the UI elements, such as browsing for a file, showing file contents, calculating frequent sets, and generating association rules.

### `validation_functions.py`

Contains functions to validate user input for numeric and decimal values.

### `logic.py`

Contains the core logic for reading transactions from the CSV file, generating frequent itemsets, and generating association rules.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/apriori-algorithm.git
    cd apriori-algorithm
    ```

2. **Install the required packages**:
    ```sh
    pip install customtkinter pandas
    ```

## Usage

1. **Run the application**:
    ```sh
    python main.py
    ```

2. **Upload a CSV file**: Click the "Browse" button and select a CSV file containing transaction data.

3. **Show File Contents**: Click the "Show File Contents" button to display the contents of the uploaded CSV file.

4. **Calculate Frequent Sets**: Enter the percentage of transactions to read and the minimum support count, then click the "Calculate Frequent Sets" button to compute the frequent itemsets.

5. **Calculate Association Rules**: Enter the percentage of transactions to read, the minimum support count, and the minimum confidence, then click the "Calculate Association Rules" button to generate strong association rules.

## CSV File Format

The CSV file should contain transaction data with the following columns:
- `TransactionNo`: The transaction number.
- `Items`: The items in the transaction.

Example:
```
TransactionNo,Items
1,Milk
1,Bread
2,Butter
2,Milk
3,Bread
3,Butter
```

## Functions

### `ui_elements.py`

- `create_ui_elements(window)`: Creates and layouts the UI elements in the main window.

### `ui_trigger_functions.py`

- `browse_file(label_file_path)`: Opens a file dialog to select a CSV file and updates the label with the file path.
- `show_file_contents()`: Displays the contents of the uploaded CSV file in a new window.
- `get_frequent_sets(entry_percentage, entry_min_support)`: Computes frequent itemsets based on the specified percentage of transactions and minimum support count.
- `get_strong_association_rules(entry_percentage, entry_min_support, entry_min_confidence)`: Generates strong association rules based on the frequent itemsets and specified minimum confidence.

### `validation_functions.py`

- `validate_numeric_input(input)`: Validates that the input is a numeric value.
- `validate_decimal_input(input)`: Validates that the input is a decimal value.

### `logic.py`

- `read_transactions(file_contents, percentage)`: Reads transactions from the CSV file based on the specified percentage.
- `generate_frequent_itemsets(items_list, min_support_count)`: Generates frequent itemsets based on the specified minimum support count.
- `generate_association_rules(frequent_item_sets, min_confidence, items_list)`: Generates strong association rules based on the frequent itemsets and specified minimum confidence.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- The `customtkinter` library for providing the GUI components.
- The `pandas` library for data manipulation and analysis.