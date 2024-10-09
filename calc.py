import tkinter as tk
from tkinter import messagebox
import math
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced GUI Calculator")
        self.master.geometry("400x600")
        self.master.configure(bg="#f0f0f0")  # Light background color

        self.result_var = tk.StringVar()
        self.memory = 0  # Memory variable
        self.history = []  # To keep track of operations
        self.is_dark_mode = False  # Dark mode flag

        self.create_widgets()

    def create_widgets(self):
        # Entry for result display
        result_entry = tk.Entry(self.master, textvariable=self.result_var, font=("Arial", 24), justify='right', bd=5)
        result_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('√', 5, 0), ('^', 5, 1), ('%', 5, 2), ('M+', 5, 3),
            ('MC', 6, 0), ('MR', 6, 1), ('sin', 6, 2), ('cos', 6, 3),
            ('tan', 7, 0), ('C', 7, 1), ('History', 7, 2, 2), ('Exit', 7, 3),
            ('Dark/Light', 8, 0, 4)
        ]

        for (text, row, col, *span) in buttons:
            span = span[0] if span else 1
            button = tk.Button(self.master, text=text, font=("Arial", 18), command=lambda t=text: self.on_button_click(t),
                               bg="#e7e7e7", activebackground="#d3d3d3", bd=2)
            button.grid(row=row, column=col, columnspan=span, sticky='nsew')

        # Configure grid weights
        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char.isdigit() or char == '.':
            current_text = self.result_var.get()
            self.result_var.set(current_text + char)
        elif char in {'+', '-', '*', '/'}:
            self.perform_operation(char)
        elif char == '=':
            self.calculate_result()
        elif char == 'C':
            self.clear()
        elif char == '√':
            self.calculate_sqrt()
        elif char == '^':
            self.perform_exponentiation()
        elif char == '%':
            self.calculate_percentage()
        elif char == 'M+':
            self.store_in_memory()
        elif char == 'MC':
            self.clear_memory()
        elif char == 'MR':
            self.retrieve_from_memory()
        elif char in {'sin', 'cos', 'tan'}:
            self.calculate_trig_function(char)
        elif char == 'History':
            self.show_history()
        elif char == 'Dark/Light':
            self.toggle_theme()
        elif char == 'Exit':
            self.master.quit()

    def perform_operation(self, operator):
        current_text = self.result_var.get()
        if current_text:
            self.history.append(current_text + " " + operator)
            self.result_var.set(current_text + " " + operator + " ")

    def calculate_result(self):
        try:
            expression = self.result_var.get().replace('^', '**')  # Replace ^ with ** for exponentiation
            expression = re.sub(r'\s+', '', expression)  # Remove whitespace
            result = eval(expression)  # Safely evaluate the expression
            self.result_var.set(result)
            self.history.append(str(result))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def clear(self):
        self.result_var.set("")

    def calculate_sqrt(self):
        try:
            number = float(self.result_var.get())
            result = math.sqrt(number)
            self.result_var.set(result)
            self.history.append(f"√{number} = {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def perform_exponentiation(self):
        current_text = self.result_var.get()
        if current_text:
            self.history.append(current_text + " ^ ")
            self.result_var.set(current_text + " ^ ")

    def calculate_percentage(self):
        try:
            number = float(self.result_var.get())
            result = number / 100
            self.result_var.set(result)
            self.history.append(f"{number}% = {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def store_in_memory(self):
        try:
            self.memory = float(self.result_var.get())
            messagebox.showinfo("Memory", f"Stored {self.memory} in memory.")
        except ValueError:
            messagebox.showerror("Error", "Invalid number to store in memory.")

    def clear_memory(self):
        self.memory = 0
        messagebox.showinfo("Memory", "Memory cleared.")

    def retrieve_from_memory(self):
        self.result_var.set(self.memory)

    def calculate_trig_function(self, func):
        try:
            number = float(self.result_var.get())
            if func == 'sin':
                result = math.sin(math.radians(number))
                self.history.append(f"sin({number}) = {result}")
            elif func == 'cos':
                result = math.cos(math.radians(number))
                self.history.append(f"cos({number}) = {result}")
            elif func == 'tan':
                result = math.tan(math.radians(number))
                self.history.append(f"tan({number}) = {result}")
            self.result_var.set(result)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_history(self):
        history_text = "\n".join(self.history)
        if not history_text:
            history_text = "No operations performed yet."
        messagebox.showinfo("Operation History", history_text)

    def toggle_theme(self):
        if self.is_dark_mode:
            self.master.configure(bg="#f0f0f0")  # Light background
            for widget in self.master.winfo_children():
                widget.configure(bg="#e7e7e7", fg="black")
            self.is_dark_mode = False
        else:
            self.master.configure(bg="#2e2e2e")  # Dark background
            for widget in self.master.winfo_children():
                widget.configure(bg="#3e3e3e", fg="white")
            self.is_dark_mode = True

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
