import customtkinter as ctk

from ui_elements import create_ui_elements

# window
ctk.set_appearance_mode('dark')
window = ctk.CTk()
window.title("Apriori Algorithm")
window.geometry('800x400')

# Create and layout UI elements
create_ui_elements(window)

window.mainloop()
