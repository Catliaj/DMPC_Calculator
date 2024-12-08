import tkinter as tk
from tkinter import ttk, messagebox
import math
import mysql.connector



#Probability Calculator_______________________________________________________________________________
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
            password="",  # Replace with your MySQL password
            database="probncomb"
        )
        self.db_cursor = self.db_connection.cursor()


        # Panel 1: Header----------------------------------------------------------------------
        self.panel1 = tk.Frame(root, width=687, height=90, bg="#630606")
        self.panel1.place(x=9, y=18)

        title_label = tk.Label(
            self.panel1,
            text="PROBABILITY CALCULATOR",
            font=("Arial", 18, "bold"),
            bg="#630606",
            fg="white"
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")


        # Panel 2: Left Side Panel----------------------------------------------------------------------
        self.panel2 = tk.Frame(root, width=254, height=605, bg="#919191")
        self.panel2.place(x=8, y=120)


        # FunctionsComboBox
        self.calculator_switch = ttk.Combobox(
            self.panel2, values=["Probability Calculator", "Combinatorics Calculator"], state="readonly"
        )
        self.calculator_switch.set("Probability Calculator")
        self.calculator_switch.bind("<<ComboboxSelected>>", self.switch_calculator)
        self.calculator_switch.place(x=10, y=15, width=230, height=50)


        # History Label
        history_label = tk.Label(
            self.panel2,
            text="History:",
            bg="#919191",
            fg="white",
            font=("Arial", 14, "bold")
        )
        history_label.place(x=7, y=70)  # Position the label above the scrollable frame

        # Scrollable Pane
        self.scrollable_frame = tk.Frame(self.panel2, width=219, height=427, bg="#fff5f5")
        self.scrollable_frame.place(x=7, y=102)

        # Add a canvas to the scrollable frame
        self.canvas = tk.Canvas(self.scrollable_frame, bg="#fff5f5", width=219, height=427)
        self.vertical_scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.horizontal_scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.inner_frame = tk.Frame(self.canvas, bg="#fff5f5")

        # Configure the scrollable area
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        # Adjust the placement of the horizontal scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontal_scrollbar.place(x=0, y=414, width=219)

        # Populate Scrollable Pane
        self.populate_scrollable_pane()


        # Exit Button
        self.exit_button = tk.Button(self.panel2, text="Exit", command=root.quit,  font=("Arial", 10, "bold"), fg="black")
        self.exit_button.place(x=66, y=556, width=120)



        # Panel 3: Inputs Panel----------------------------------------------------------------------
        self.panel3 = tk.Frame(root, width=427, height=235, bg="#630606")
        self.panel3.place(x=270, y=120)


        # Input Fields
        tk.Label(
            self.panel3, 
            text="Total Outcomes (n(S)):", 
            bg="#630606", 
            fg="white", 
            font=("Arial", 12, "bold")
        ).place(relx=0.5, rely=0.15, anchor="center")  # Lowered by increasing rely

        self.entry_total_outcomes = tk.Entry(self.panel3, font=("Arial", 12))
        self.entry_total_outcomes.place(relx=0.5, rely=0.25, anchor="center", width=250, height=30)  # Adjusted lower


        tk.Label(
            self.panel3, 
            text="Favorable Outcomes for A (n(A)):", 
            bg="#630606", 
            fg="white", 
            font=("Arial", 12, "bold")
        ).place(relx=0.5, rely=0.35, anchor="center")

        self.entry_event_a = tk.Entry(self.panel3, font=("Arial", 12))
        self.entry_event_a.place(relx=0.5, rely=0.45, anchor="center", width=250, height=30)  # Adjusted lower


        tk.Label(
            self.panel3, 
            text="Favorable Outcomes for B (n(B)):", 
            bg="#630606", 
            fg="white", 
            font=("Arial", 12, "bold")
        ).place(relx=0.5, rely=0.55, anchor="center")  # Lowered by increasing rely

        self.entry_event_b = tk.Entry(self.panel3, font=("Arial", 12))
        self.entry_event_b.place(relx=0.5, rely=0.65, anchor="center", width=250, height=30)  # Adjusted lower



        # Calculate Button
        self.calculate_button = tk.Button(
            self.panel3, 
            text="Calculate", 
            command=self.calculate_probability,
            font=("Arial", 12, "bold"), 
            fg="black"
        )
        self.calculate_button.place(relx=0.35, rely=0.80, anchor="center", width=120, height=25)  # Lowered button



        # Clear Button
        self.clear_button = tk.Button(
            self.panel3, 
            text="Clear", 
            command=self.clear_fields,
            font=("Arial", 12, "bold"), 
            fg="black"
        )
        self.clear_button.place(relx=0.65, rely=0.80, anchor="center", width=120, height=25)  # Lowered button



        # Panel 4: Outputs Panel----------------------------------------------------------------------
        self.panel4 = tk.Frame(root, width=427, height=361, bg="#630606")
        self.panel4.place(x=270, y=365)

        # Output Fields
        self.simple_prob_label = tk.Label(self.panel4, text="Simple Probability:", bg="#630606", fg="white", font=("Arial", 12, "bold"))
        self.simple_prob_label.place(relx=0.5, rely=0.15, anchor="center")

        self.simple_prob_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 12))
        self.simple_prob_result.place(relx=0.5, rely=0.21, anchor="center", width=300)


        self.complementary_prob_label = tk.Label(self.panel4, text="Complementary Probability:", bg="#630606", fg="white", font=("Arial", 12, "bold"))
        self.complementary_prob_label.place(relx=0.5, rely=0.30, anchor="center")

        self.complementary_prob_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 12))
        self.complementary_prob_result.place(relx=0.5, rely=0.36, anchor="center", width=300)


        self.conditional_prob_label = tk.Label(self.panel4, text="Conditional Probability:", bg="#630606", fg="white", font=("Arial", 12, "bold"))
        self.conditional_prob_label.place(relx=0.5, rely=0.45, anchor="center")

        self.conditional_prob_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 12))
        self.conditional_prob_result.place(relx=0.5, rely=0.51, anchor="center", width=300)


        self.addition_rule_label = tk.Label(self.panel4, text="Addition Rule (P(A or B)):", bg="#630606", fg="white", font=("Arial", 12, "bold"))
        self.addition_rule_label.place(relx=0.5, rely=0.60, anchor="center")

        self.addition_rule_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 12))
        self.addition_rule_result.place(relx=0.5, rely=0.66, anchor="center", width=300)


        self.multiplication_rule_label = tk.Label(self.panel4, text="Multiplication Rule (P(A and B)):", bg="#630606", fg="white", font=("Arial", 12, "bold"))
        self.multiplication_rule_label.place(relx=0.5, rely=0.75, anchor="center")

        self.multiplication_rule_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 12))
        self.multiplication_rule_result.place(relx=0.5, rely=0.81, anchor="center", width=300)

    def center_window(self):
        window_width = 705
        window_height = 744
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    def populate_scrollable_pane(self):
        # Fetch probability history from the database
        query = "SELECT `n(S)`, `n(A)`, `n(B)`, `Simple_P`, `Complementary_P`, `Conditional_P`, `Addition_R`, `Multiplication_R` FROM probability_history ORDER BY `Prob_HistoryID` DESC"
        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()

        # Clear the previous content in the scrollable frame before adding new data
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Display data in scrollable frame
        for i, row in enumerate(rows):
            tk.Label(self.inner_frame, text=f"n(S) = {row[0]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"n(A) = {row[1]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"n(B) = {row[2]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Simple = {row[3]:.4f} or {row[3]*100:.2f}%", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Complementary = {row[4]:.4f} or {row[4]*100:.2f}%", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Conditional = {row[5]:.4f} or {row[5]*100:.2f}%", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Addition Rule = {row[6]:.4f} or {row[6]*100:.2f}%", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Multiplication Rule = {row[7]:.4f} or {row[7]*100:.2f}%", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text="-" * 50, bg="#fff5f5").pack(anchor="w")

    def calculate_probability(self):
        try:
            event_a = float(self.entry_event_a.get())
            event_b = float(self.entry_event_b.get())
            total_outcomes = float(self.entry_total_outcomes.get())

            # Calculate probabilities
            simple_prob = event_a / total_outcomes

            complementary_prob = 1 - simple_prob
            
            conditional_prob = event_a / event_b if event_b != 0 else 0

            addition_prob = simple_prob + (event_b / total_outcomes)

            multiplication_prob = simple_prob * (event_b / total_outcomes)

            # Update result labels
            self.simple_prob_result.delete(0, tk.END)
            self.simple_prob_result.insert(0, str(f"{round(simple_prob,2)} or {round(simple_prob*100,2)}%"))

            self.complementary_prob_result.delete(0, tk.END)
            self.complementary_prob_result.insert(0, str(f"{round(complementary_prob,2)} or {round(complementary_prob*100,2)}%"))

            self.conditional_prob_result.delete(0, tk.END)
            self.conditional_prob_result.insert(0, str(f"{round(conditional_prob,2)} or {round(conditional_prob*100,2)}%"))

            self.addition_rule_result.delete(0, tk.END)
            self.addition_rule_result.insert(0, str(f"{round(addition_prob,2)} or {round(addition_prob*100,2)}%"))

            self.multiplication_rule_result.delete(0, tk.END)
            self.multiplication_rule_result.insert(0, str(f"{round(multiplication_prob,2)} or {round(multiplication_prob*100,2)}%"))


        # Insert into the database
            insert_query = """
                INSERT INTO probability_history (`n(S)`, `n(A)`, `n(B)`, `Simple_P`, `Complementary_P`, `Conditional_P`, `Addition_R`, `Multiplication_R`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (total_outcomes, event_a, event_b, simple_prob, complementary_prob, conditional_prob, addition_prob, multiplication_prob)
            self.db_cursor.execute(insert_query, values)
            self.db_connection.commit()

            messagebox.showinfo("Success", "Probability results saved to the database.")
            self.populate_scrollable_pane()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def clear_fields(self):
        # Clear the input fields and result text fields
        self.entry_total_outcomes.delete(0, tk.END)
        self.entry_event_a.delete(0, tk.END)
        self.entry_event_b.delete(0, tk.END)
        self.simple_prob_result.delete(0, tk.END)
        self.complementary_prob_result.delete(0, tk.END)
        self.conditional_prob_result.delete(0, tk.END)
        self.addition_rule_result.delete(0, tk.END)
        self.multiplication_rule_result.delete(0, tk.END)

    def switch_calculator(self, event):
        selection = self.calculator_switch.get()
        if selection == "Combinatorics Calculator":
            self.root.destroy()
            main(CombinatoricsCalculator)




#Combinatronics Calculator_______________________________________________________________________________
class CombinatoricsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Combinatorics Calculator")
        self.root.geometry("705x744")
        self.root.resizable(False, False)
        self.center_window()

        # MySQL Connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="probncomb"
        )
        self.db_cursor = self.db_connection.cursor()


        # Panel 1: Header----------------------------------------------------------------------
        self.panel1 = tk.Frame(root, width=687, height=90, bg="#630606")
        self.panel1.place(x=9, y=18)

# Adding a title label to self.panel1
        title_label = tk.Label(
            self.panel1,
            text="COMBINATORICS CALCULATOR",
            font=("Arial", 18, "bold"),
            bg="#630606",
            fg="white"
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Panel 2: Left Side Panel---------------------------------------------------------------------- 
        self.panel2 = tk.Frame(root, width=254, height=605, bg="#919191")
        self.panel2.place(x=8, y=120)

        # History Label
        history_label = tk.Label(
            self.panel2,
            text="History:",
            bg="#919191",
            fg="white",
            font=("Arial", 14, "bold")
        )
        history_label.place(x=7, y=70)  # Position the label above the scrollable frame

        # Scrollable Pane
        self.scrollable_frame = tk.Frame(self.panel2, width=219, height=427, bg="#fff5f5")
        self.scrollable_frame.place(x=7, y=102)

        # Add a canvas to the scrollable frame
        self.canvas = tk.Canvas(self.scrollable_frame, bg="#fff5f5", width=219, height=427)
        self.vertical_scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.horizontal_scrollbar = ttk.Scrollbar(
            self.scrollable_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.inner_frame = tk.Frame(self.canvas, bg="#fff5f5")

        # Configure the scrollable area
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        # Adjust the placement of the horizontal scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontal_scrollbar.place(x=0, y=414, width=219)

        # Populate Scrollable Pane
        self.populate_scrollable_pane()

        # FunctionsComboBox
        self.calculator_switch = ttk.Combobox(
            self.panel2, values=["Probability Calculator", "Combinatorics Calculator"], state="readonly"
        )
        self.calculator_switch.set("Combinatorics Calculator")
        self.calculator_switch.bind("<<ComboboxSelected>>", self.switch_calculator)
        self.calculator_switch.place(x=10, y=15, width=230, height=50)

        # Exit Button
        self.exit_button = tk.Button(self.panel2, text="Exit", command=root.quit, font=("Arial", 10, "bold"), fg="black")
        self.exit_button.place(x=66, y=556, width=120)

        # Panel 3: Inputs Panel---------------------------------------------------------------------- 
        self.panel3 = tk.Frame(root, width=427, height=295, bg="#630606")  # Increased height of the panel
        self.panel3.place(x=270, y=120)

        # Input Fields
        tk.Label(
            self.panel3, 
            text="Total Number of items in a set (n):", 
            bg="#630606", 
            fg="white", 
            font=("Arial", 12, "bold")
        ).place(relx=0.5, rely=0.15, anchor="center")  # Lowered by increasing rely

        self.entry_n = tk.Entry(self.panel3, font=("Arial", 12))
        self.entry_n.place(relx=0.5, rely=0.25, anchor="center", width=250, height=30)  # Adjusted lower

        tk.Label(
            self.panel3, 
            text="Number of items to arrange in the set (r):", 
            bg="#630606", 
            fg="white", 
            font=("Arial", 12, "bold")
        ).place(relx=0.5, rely=0.45, anchor="center")  # Lowered by increasing rely

        self.entry_r = tk.Entry(self.panel3, font=("Arial", 12))
        self.entry_r.place(relx=0.5, rely=0.55, anchor="center", width=250, height=30)  # Adjusted lower

        # Calculate Button
        self.calculate_button = tk.Button(
            self.panel3, 
            text="Calculate", 
            command=self.calculate_combinatorics,
            font=("Arial", 12, "bold"), 
            fg="black"
        )
        self.calculate_button.place(relx=0.35, rely=0.80, anchor="center", width=120, height=40)  # Lowered button

        # Clear Button
        self.clear_button = tk.Button(
            self.panel3, 
            text="Clear", 
            command=self.clear_fields,
            font=("Arial", 12, "bold"), 
            fg="black"
        )
        self.clear_button.place(relx=0.65, rely=0.80, anchor="center", width=120, height=40)  # Lowered button


        # Panel 4: Outputs Panel---------------------------------------------------------------------- 
        self.panel4 = tk.Frame(root, width=427, height=301, bg="#630606")
        self.panel4.place(x=270, y=425)

        # Output Labels with Text Fields beneath them
        self.factorial_label = tk.Label(self.panel4, text="Factorial | n! :", bg="#630606", fg="white", font=("Arial", 14, "bold"))
        self.factorial_label.place(relx=0.5, rely=0.2, anchor="center")

        self.factorial_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 14))
        self.factorial_result.place(relx=0.5, rely=0.3, anchor="center", width=300)

        self.npr_label = tk.Label(self.panel4, text="Permutation | nPr = n! / (n-r)! :", bg="#630606", fg="white", font=("Arial", 14, "bold"))
        self.npr_label.place(relx=0.5, rely=0.4, anchor="center")

        self.npr_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 14))
        self.npr_result.place(relx=0.5, rely=0.5, anchor="center", width=300)

        self.ncr_label = tk.Label(self.panel4, text="Combination | nCr = n! / (n-r)! * r! :", bg="#630606", fg="white", font=("Arial", 14, "bold"))
        self.ncr_label.place(relx=0.5, rely=0.6, anchor="center")

        self.ncr_result = tk.Entry(self.panel4, bg="white", fg="black", font=("Arial", 14))
        self.ncr_result.place(relx=0.5, rely=0.7, anchor="center", width=300)

    def center_window(self):
        window_width = 705
        window_height = 744
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    def populate_scrollable_pane(self):
        # Fetch combinatorics history from the database
        query = "SELECT `(n)`, `(r)`, `Factorial_R`, `Permutation_R`, `Combination_R` FROM combinatronics_history ORDER BY `Comb_HistoryID` DESC"
        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()

        # Clear the previous content in the scrollable frame before adding new data
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Display data in scrollable frame
        for i, row in enumerate(rows):
            tk.Label(self.inner_frame, text=f"(n) = {row[0]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"(r) = {row[1]}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Factorial = {row[2]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Permutation = {row[3]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text=f"Combination = {row[4]:.4f}", bg="#fff5f5").pack(anchor="w")
            tk.Label(self.inner_frame, text="-" * 50, bg="#fff5f5").pack(anchor="w")

    def calculate_combinatorics(self):
        try:
            n = int(self.entry_n.get())
            r = int(self.entry_r.get())

            # Calculations for factorial, permutations, and combinations
            n_fact = math.factorial(n)

            npr = math.factorial(n) / math.factorial(n - r) if r <= n else 0

            ncr = math.factorial(n) / (math.factorial(r) * math.factorial(n - r)) if r <= n else 0

            # Update result labels
            self.factorial_label.config(text=f"n! = {n_fact}")

            self.npr_label.config(text=f"nPr = {npr}")

            self.ncr_label.config(text=f"nCr = {ncr}")
            
        # Insert into the database
            insert_query = """
                INSERT INTO combinatronics_history (n, r, Factorial_R, Permutation_R, Combination_R)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (n, r, n_fact, npr, ncr)
            self.db_cursor.execute(insert_query, values)
            self.db_connection.commit()

            messagebox.showinfo("Success", "Combinatorics results saved to the database.")
            self.populate_scrollable_pane()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers.")

    def clear_fields(self):
        # Clear the input fields and result text fields
        self.entry_n.delete(0, tk.END)
        self.entry_r.delete(0, tk.END)
        self.factorial_result.delete(0, tk.END)
        self.npr_result.delete(0, tk.END)
        self.ncr_result.delete(0, tk.END)

    def switch_calculator(self, event):
        selection = self.calculator_switch.get()
        if selection == "Probability Calculator":
            self.root.destroy()
            main(ProbabilityCalculator)
            



# Function to initialize the selected calculator
def main(calculator_class): 
    root = tk.Tk()
    calculator_class(root)
    root.mainloop()

# Start with the Probability Calculator
if __name__ == "__main__":
    main(ProbabilityCalculator)
