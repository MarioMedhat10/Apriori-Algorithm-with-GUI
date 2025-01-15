from tkinter import filedialog, messagebox, Toplevel, ttk
import re

from logic import *

file_contents = ""
filename = ""


def browse_file(label_file_path):
    global file_contents  # Access the global variable to store file contents
    global filename  # Access the global variable to store the file path

    # Show a window to upload the csv file
    filename = filedialog.askopenfilename()

    if filename and filename.split('.').pop() == 'csv':  # Check if the selected file is a CSV file
        # Update the label text with the selected file path
        label_file_path.configure(text=filename)

        # Read and store the contents of the file
        with open(filename, 'r') as file:
            file_contents = file.read()
    else:
        # Display a warning message if the selected file is not a CSV file
        messagebox.showwarning(
            "Invalid File",
            "Please upload a CSV file."
        )


def show_file_contents():
    global file_contents  # Access the global variable to retrieve file contents

    if file_contents:
        # Split the file contents by lines and then by commas to create rows and columns
        rows = [line.split(',') for line in file_contents.split('\n')]

        # Create a new window
        file_window = Toplevel()
        file_window.title(filename.split('/').pop())  # Set the title of the window to the file name
        file_window.geometry('1300x800')  # Set the size of the window

        # Create a Frame to contain Treeview and Scrollbar
        tree_frame = ttk.Frame(file_window)
        tree_frame.pack(fill='both', expand=True)

        # Create a Treeview widget
        tree = ttk.Treeview(tree_frame)
        tree.pack(side='left', fill='both', expand=True)

        # Insert data into the Treeview
        for i, row in enumerate(rows):
            if i == 0:
                # First row contains column headers
                tree['columns'] = row
                tree.heading("#0", text="Row")  # Create a heading for the row numbers
                for col in row:
                    tree.heading(col, text=col)  # Create headings for each column
            else:
                tree.insert('', 'end', text=str(i), values=row)  # Insert each row into the Treeview

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)

        # Run the new window
        file_window.mainloop()
    else:
        # Display a warning message if no file has been uploaded
        messagebox.showwarning(
            "File Not Found",
            "Please upload a CSV file first."
        )


def get_frequent_sets(entry_percentage, entry_min_support):
    global filename  # Access the global variable to retrieve the file path

    if file_contents:
        # Retrieve percentage and minimum support count values from entry widgets
        percentage = entry_percentage.get()
        min_support_count = entry_min_support.get()

        if percentage and min_support_count and percentage != '.' and 0 < float(percentage) <= 100:
            # Call read_transactions function to extract transactions from the CSV file
            transactions = read_transactions(file_contents, float(percentage))

            # Create the list of items for each transaction
            items_list = []
            for transaction_no, items in transactions.items():
                items_list.append(items)

            # Generate frequent item sets based on the provided minimum support count
            frequent_item_sets = generate_frequent_itemsets(items_list, int(min_support_count))

            # Display frequent item sets rules in the console
            # for itemset, supp_count in frequent_item_sets.items():
            #     print(f"{itemset} \t\t {supp_count}")

            # Display frequent item sets in a new window using Treeview widget
            result_window = Toplevel()
            result_window.geometry('800x600')
            result_window.title("Frequent Item Sets")

            # Create a Treeview widget to display frequent item sets and their support counts
            tree = ttk.Treeview(result_window, columns=("Itemset", "Support Count"), show="headings")
            tree.heading("Itemset", text="Itemset")
            tree.heading("Support Count", text="Support Count")

            # Center the columns
            tree.column("Itemset", anchor="center")
            tree.column("Support Count", anchor="center")

            # Add a vertical scrollbar
            scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.config(yscrollcommand=scrollbar.set)
            tree.pack(fill="both", expand=True)

            # Insert frequent item sets and their support counts into the Treeview
            for itemset, supp_count in frequent_item_sets.items():
                tree.insert("", "end", values=(str(itemset), str(supp_count)))

        else:
            # Display warning messages if percentage or minimum support count is missing
            if not percentage:
                messagebox.showwarning(
                    "Missing parameter",
                    "Percentage is empty. Please enter a valid percentage."
                )
            if not min_support_count:
                messagebox.showwarning(
                    "Missing parameter",
                    "Minimum Support Count is empty. Please enter a valid Min Support Count."
                )
    else:
        # Display a warning message if no file has been uploaded
        messagebox.showwarning(
            "File Not Found",
            "Please upload a CSV file first."
        )


def get_strong_association_rules(entry_percentage, entry_min_support, entry_min_confidence):
    global filename  # Access the global variable to retrieve the file path

    if file_contents:
        # Filling the variables with entry buttons content
        percentage = entry_percentage.get()
        min_support_count = entry_min_support.get()
        min_confidence = entry_min_confidence.get()

        if percentage and min_support_count and min_confidence and percentage != '.' and 0 < float(
                percentage) <= 100 and 0 <= float(min_confidence) <= 100:
            # Call read_transactions function to extract transactions from the CSV file
            transactions = read_transactions(file_contents, float(percentage))

            # Create the list of items for each transaction
            items_list = []
            for transaction_no, items in transactions.items():
                items_list.append(items)

            # Generate frequent item sets based on the provided minimum support count
            frequent_item_sets = generate_frequent_itemsets(items_list, int(min_support_count))

            # Generate association rules based on the frequent item sets and minimum confidence
            association_rules = generate_association_rules(frequent_item_sets, float(min_confidence) / 100, items_list)

            # Ensure association_rules is not None before iterating over it
            if association_rules is not None:
                # Display association rules in the console
                # for rule in association_rules:
                #     print(str(rule[0]) + ' => ' + str(rule[1]) + ' has confidence = ' + str(rule[2] * 100) + ' %')

                # Create a new window to display association rules using Treeview widget
                rules_window = Toplevel()
                rules_window.title("Strong Association Rules")
                rules_window.geometry('1000x600')

                # Create a Treeview widget to display association rules and their confidence
                tree = ttk.Treeview(rules_window, columns=("Antecedent", "", "Consequent", "Confidence"),
                                    show="headings")
                tree.heading("Antecedent", text="Antecedent")
                tree.heading("", text="")
                tree.heading("Consequent", text="Consequent")
                tree.heading("Confidence", text="Confidence (%)")

                # Center the columns
                tree.column("Antecedent", anchor="center")
                tree.column("", anchor="center")
                tree.column("Consequent", anchor="center")
                tree.column("Confidence", anchor="center")

                # Add a vertical scrollbar
                scrollbar = ttk.Scrollbar(rules_window, orient="vertical", command=tree.yview)
                scrollbar.pack(side="right", fill="y")

                tree.config(yscrollcommand=scrollbar.set)
                tree.pack(fill="both", expand=True)

                # Insert association rules and their confidence into the Treeview
                for rule in association_rules:
                    tree.insert("", "end", values=(str(rule[0]), "=>", str(rule[1]), str(rule[2] * 100)))

            else:
                # Handle the case where association_rules is None
                messagebox.showwarning(
                    "Error",
                    "Failed to generate association rules. Make sure that Frequent Sets has records."
                )

        else:
            # Display warning messages if percentage, minimum support count, or minimum confidence is missing
            if not percentage:
                messagebox.showwarning(
                    "Missing parameter",
                    "Percentage is empty. Please enter a valid percentage."
                )
            if not min_support_count:
                messagebox.showwarning(
                    "Missing parameter",
                    "Minimum Support Count is empty. Please enter a valid Min Support Count."
                )
            if not min_confidence:
                messagebox.showwarning(
                    "Missing parameter",
                    "Minimum Confidence is empty. Please enter a valid Min Confidence."
                )
    else:
        # Display a warning message if no file has been uploaded
        messagebox.showwarning(
            "File Not Found",
            "Please upload a CSV file first."
        )


# Function to validate numeric input
def validate_numeric_input(input):
    return re.match(r'^[0-9]*$', input) is not None


# Function to validate decimal input
def validate_decimal_input(input):
    return re.match(r'^[0-9]*\.?[0-9]*$', input) is not None
