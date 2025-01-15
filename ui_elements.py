import customtkinter as ctk

from ui_trigger_functions import *


def create_ui_elements(window):
    # Create and style widgets
    label_file = ctk.CTkLabel(window, text="Upload CSV File:")
    button_browse = ctk.CTkButton(window, text="Browse", command=lambda: browse_file(label_file_path))
    label_file_path = ctk.CTkLabel(window, text="")
    button_show_contents = ctk.CTkButton(window, text="Show File Contents", command=show_file_contents)
    label_percentage = ctk.CTkLabel(window, text="Percentage to read (%):")
    validate_decimal_percentage = window.register(validate_decimal_input)
    entry_percentage = ctk.CTkEntry(window, validate="key", validatecommand=(validate_decimal_percentage, '%P'))
    label_min_support = ctk.CTkLabel(window, text="Minimum Support Count:")
    validate_numeric_support = window.register(validate_numeric_input)
    entry_min_support = ctk.CTkEntry(window, validate="key", validatecommand=(validate_numeric_support, '%P'))
    label_min_confidence = ctk.CTkLabel(window, text="Minimum Confidence (%):")
    validate_decimal_confidence = window.register(validate_decimal_input)
    entry_min_confidence = ctk.CTkEntry(window, validate="key", validatecommand=(validate_decimal_confidence, '%P'))
    button_calc_frequent_sets = ctk.CTkButton(window, text="Calculate Frequent Sets",
                                              command=lambda: get_frequent_sets(entry_percentage, entry_min_support, ))
    button_calc_association_rules = ctk.CTkButton(window, text="Calculate Association Rules",
                                                  command=lambda: get_strong_association_rules(entry_percentage,
                                                                                               entry_min_support,
                                                                                               entry_min_confidence))

    # Layout widgets
    label_file.grid(row=1, column=0, pady=5, padx=10)
    button_browse.grid(row=1, column=1, pady=5, padx=10)
    label_file_path.grid(row=1, column=2, pady=5, padx=10)
    button_show_contents.grid(row=2, column=1, pady=5, padx=10)
    label_percentage.grid(row=3, column=0, pady=5, padx=10)
    entry_percentage.grid(row=3, column=1, pady=5, padx=10)
    label_min_support.grid(row=4, column=0, pady=5, padx=10)
    entry_min_support.grid(row=4, column=1, pady=5, padx=10)
    label_min_confidence.grid(row=5, column=0, pady=5, padx=10)
    entry_min_confidence.grid(row=5, column=1, pady=5, padx=10)
    button_calc_frequent_sets.grid(row=6, column=0, columnspan=2, pady=20, padx=10)
    button_calc_association_rules.grid(row=7, column=0, columnspan=2, padx=10)
