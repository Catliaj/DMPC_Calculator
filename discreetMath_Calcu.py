import tkinter as tk
from tkinter import ttk, messagebox
import math
import mysql.connector

# Probability Calculator
class ProbabilityCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Probability Calculator")
        self.root.geometry("705x744")
        self.root.resizable(False, False)
        self.center_window()

        # MySQL Connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="probncomb"
        )
        self.db_cursor = self.db_connection.cursor()

        # Panel 1: Header
        self.panel1 = tk.Frame(root, width=687, height=90, bg="#630606")
        self.panel1.place(x=9, y=18)

        # Panel 2: Left Side Panel
        self.panel2 = tk.Frame(root, width=254, height=605, bg="#919191")
        self.panel2.place(x=8, y=120)

        # Scrollable Pane
        self.scrollable_frame = tk.Frame(self.panel2, width=219, height=427, bg="#fff5f5")
        self.scrollable_frame.place(x=7, y=102)

        self.canvas = tk.Canvas(self.scrollable_frame, bg="#fff5f5", width=219, height=427)
        self.vertical_scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.inner_frame = tk.Frame(self.canvas, bg="#fff5f5")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate Scrollable Pane
        self.populate_scrollable_pane()

        # FunctionsComboBox
        self.calculator_switch = ttk.Combobox(
            self.panel2, values=["Probability Calculator", "Combinatorics Calculator"], state="readonly"
        )
        self.calculator_switch.set("Probability Calculator")
        self.calculator_switch.bind("<<ComboboxSelected>>", self.switch_calculator)
        self.calculator_switch.place(x=70, y=20, width=120)

        # Exit Button
        self.exit_button = tk.Button(self.panel2, text="Exit", command=root.quit)
        self.exit_button.place(x=66, y=556, width=120)

        # Panel 3: Inputs Panel
        self.panel3 = tk.Frame(root, width=427, height=295, bg="#630606")
        self.panel3.place(x=270, y=120)

        tk.Label(self.panel3, text="Total Outcomes (n(S)):", bg="#630606", fg="white").place(x=30, y=30)
        self.entry_total_outcomes = tk.Entry(self.panel3)
        self.entry_total_outcomes.place(x=190, y=30, width=100)

        tk.Label(self.panel3, text="Favorable Outcomes for A (n(A)):", bg="#630606", fg="white").place(x=30, y=70)
        self.entry_event_a = tk.Entry(self.panel3)
        self.entry_event_a.place(x=190, y=70, width=100)

        tk.Label(self.panel3, text="Favorable Outcomes for B (n(B)):", bg="#630606", fg="white").place(x=30, y=110)
        self.entry_event_b = tk.Entry(self.panel3)
        self.entry_event_b.place(x=190, y=110, width=100)

        self.calculate_button = tk.Button(self.panel3, text="Calculate", command=self.calculate_probability)
        self.calculate_button.place(x=160, y=150, width=100)

        # Panel 4: Outputs Panel
        self.panel4 = tk.Frame(root, width=427, height=301, bg="#630606")
        self.panel4.place(x=270, y=425)

        self.simple_prob_label = tk.Label(self.panel4, text="Simple Probability: 0.0000", anchor="w", bg="#630606", fg="white")
        self.simple_prob_label.place(x=10, y=10, width=400)

        self.complementary_prob_label = tk.Label(self.panel4, text="Complementary Probability: 0.0000", anchor="w", bg="#630606", fg="white")
        self.complementary_prob_label.place(x=10, y=40, width=400)

        self.conditional_prob_label = tk.Label(self.panel4, text="Conditional Probability: 0.0000", anchor="w", bg="#630606", fg="white")
        self.conditional_prob_label.place(x=10, y=70, width=400)

        self.addition_rule_label = tk.Label(self.panel4, text="Addition Rule (P(A or B)): 0.0000", anchor="w", bg="#630606", fg="white")
        self.addition_rule_label.place(x=10, y=100, width=400)

        self.multiplication_rule_label = tk.Label(self.panel4, text="Multiplication Rule (P(A and B)): 0.0000", anchor="w", bg="#630606", fg="white")
        self.multiplication_rule_label.place(x=10, y=130, width=400)

    def center_window(self):
        window_width = 705
        window_height = 744
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    def populate_scrollable_pane(self):
        query = "SELECT `n(S)`, `n(A)`, `n(B)`, `Simple_P`, `Complementary_P`, `Conditional_P`, `Addition_R`, `Multiplication_R` FROM probability_history ORDER BY `Prob_HistoryID` DESC"
        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()

        for row in rows:
            tk.Label(self.inner_frame, text=f"n(S) = {row[0]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"n(A) = {row[1]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"n(B) = {row[2]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Simple = {row[3]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Complementary = {row[4]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Conditional = {row[5]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Addition Rule = {row[6]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Multiplication Rule = {row[7]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text="-" * 50, bg="#fff5f5").pack(anchor="w")

    def calculate_probability(self):
        try:
            total_outcomes = float(self.entry_total_outcomes.get())
            event_a = float(self.entry_event_a.get())
            event_b = float(self.entry_event_b.get())

            simple_prob = event_a / total_outcomes
            complementary_prob = 1 - simple_prob
            conditional_prob = event_a / event_b if event_b != 0 else 0
            addition_prob = simple_prob + (event_b / total_outcomes)
            multiplication_prob = simple_prob * (event_b / total_outcomes)

            self.simple_prob_label.config(text=f"Simple Probability: {simple_prob:.4f}")
            self.complementary_prob_label.config(text=f"Complementary Probability: {complementary_prob:.4f}")
            self.conditional_prob_label.config(text=f"Conditional Probability: {conditional_prob:.4f}")
            self.addition_rule_label.config(text=f"Addition Rule (P(A or B)): {addition_prob:.4f}")
            self.multiplication_rule_label.config(text=f"Multiplication Rule (P(A and B)): {multiplication_prob:.4f}")

            query = """
                INSERT INTO probability_history (`n(S)`, `n(A)`, `n(B)`, `Simple_P`, `Complementary_P`, `Conditional_P`, `Addition_R`, `Multiplication_R`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (total_outcomes, event_a, event_b, simple_prob, complementary_prob, conditional_prob, addition_prob, multiplication_prob)
            self.db_cursor.execute(query, values)
            self.db_connection.commit()

            messagebox.showinfo("Success", "Probability results saved to the database.")
            self.populate_scrollable_pane()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def switch_calculator(self, event):
        if self.calculator_switch.get() == "Combinatorics Calculator":
            self.root.destroy()
            main(CombinatoricsCalculator)

# Combinatorics Calculator and main function follow...
# Combinatorics Calculator
class CombinatoricsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Combinatorics Calculator")
        self.root.geometry("705x744")
        self.root.resizable(False, False)
        self.center_window()

        # Panel 1: Header
        self.panel1 = tk.Frame(root, width=687, height=90, bg="#630606")
        self.panel1.place(x=9, y=18)

        # Panel 2: Left Side Panel
        self.panel2 = tk.Frame(root, width=254, height=605, bg="#919191")
        self.panel2.place(x=8, y=120)

        # Calculator Switch
        self.calculator_switch = ttk.Combobox(
            self.panel2, values=["Probability Calculator", "Combinatorics Calculator"], state="readonly"
        )
        self.calculator_switch.set("Combinatorics Calculator")
        self.calculator_switch.bind("<<ComboboxSelected>>", self.switch_calculator)
        self.calculator_switch.place(x=70, y=20, width=120)

        # Exit Button
        self.exit_button = tk.Button(self.panel2, text="Exit", command=root.quit)
        self.exit_button.place(x=66, y=556, width=120)

        # Panel 3: Inputs Panel
        self.panel3 = tk.Frame(root, width=427, height=295, bg="#630606")
        self.panel3.place(x=270, y=120)

        tk.Label(self.panel3, text="n:", bg="#630606", fg="white").place(x=30, y=30)
        self.entry_n = tk.Entry(self.panel3)
        self.entry_n.place(x=80, y=30, width=100)

        tk.Label(self.panel3, text="r:", bg="#630606", fg="white").place(x=30, y=70)
        self.entry_r = tk.Entry(self.panel3)
        self.entry_r.place(x=80, y=70, width=100)

        self.calculate_button = tk.Button(self.panel3, text="Calculate", command=self.calculate_combinatorics)
        self.calculate_button.place(x=60, y=120, width=100)

        # Panel 4: Outputs Panel
        self.panel4 = tk.Frame(root, width=427, height=301, bg="#630606")
        self.panel4.place(x=270, y=425)

        self.combination_label = tk.Label(self.panel4, text="Combination: 0", anchor="w", bg="#630606", fg="white")
        self.combination_label.place(x=10, y=10, width=400)

        self.permutation_label = tk.Label(self.panel4, text="Permutation: 0", anchor="w", bg="#630606", fg="white")
        self.permutation_label.place(x=10, y=40, width=400)

    def center_window(self):
        window_width = 705
        window_height = 744
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    def calculate_combinatorics(self):
        try:
            n = int(self.entry_n.get())
            r = int(self.entry_r.get())
            if n < r:
                raise ValueError("n must be greater than or equal to r.")

            combination = math.comb(n, r)
            permutation = math.perm(n, r)

            self.combination_label.config(text=f"Combination: {combination}")
            self.permutation_label.config(text=f"Permutation: {permutation}")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def switch_calculator(self, event):
        if self.calculator_switch.get() == "Probability Calculator":
            self.root.destroy()
            main(ProbabilityCalculator)

# Main function to initialize the app
def main(calculator_class):
    root = tk.Tk()
    app = calculator_class(root)
    root.mainloop()

# Launch the app with the desired calculator
if __name__ == "__main__":
    main(ProbabilityCalculator)
