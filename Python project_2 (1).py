# ============================================================
# Scientific Calculator
# Course: Object-Oriented Programming (Python)
# Concepts used: Classes, __init__, Instance Methods,
#                Attributes, Inheritance, Polymorphism, Tkinter
# ============================================================

import tkinter as tk   # tkinter is Python's built-in GUI library
import math            # math gives us sin, cos, sqrt, etc.


# ============================================================
# CLASS 1: Calculator (Base / Parent Class)
# This handles only the basic four operations.
# Think of it as the "simple" calculator your phone has.
# ============================================================

class Calculator:

    def __init__(self):
        # self.result stores the answer of the last calculation
        self.result = 0

    # Each method below takes two numbers and returns the answer.
    # These are instance methods because they belong to this class.

    def add(self, a, b):
        self.result = a + b
        return self.result

    def subtract(self, a, b):
        self.result = a - b
        return self.result

    def multiply(self, a, b):
        self.result = a * b
        return self.result

    def divide(self, a, b):
        # We must handle division by zero — it would crash the program
        if b == 0:
            return "Error: Cannot divide by zero"
        self.result = a / b
        return self.result


# ============================================================
# CLASS 2: ScientificCalculator (Child / Subclass)
# This INHERITS everything from Calculator (all 4 operations)
# and ADDS new scientific methods on top.
# This is exactly the inheritance from Lecture 7.
# ============================================================

class ScientificCalculator(Calculator):  # <-- inherits from Calculator

    def __init__(self):
        super().__init__()   # calls Calculator's __init__ to set self.result = 0
        self.angle_mode = "DEG"   # we start in degree mode (not radians)

    # ---- Helper: convert degrees to radians if needed ----
    # sin/cos/tan in Python's math module always expects RADIANS.
    # So if the user is working in degrees, we must convert first.
    def to_radians(self, angle):
        if self.angle_mode == "DEG":
            return math.radians(angle)  # converts degrees → radians
        return angle  # already in radians, no change needed

    # ---- Scientific Methods (Method Override + New Methods) ----

    def sine(self, angle):
        self.result = math.sin(self.to_radians(angle))
        return round(self.result, 10)  # round to avoid tiny floating errors

    def cosine(self, angle):
        self.result = math.cos(self.to_radians(angle))
        return round(self.result, 10)

    def tangent(self, angle):
        self.result = math.tan(self.to_radians(angle))
        return round(self.result, 10)

    def square_root(self, a):
        if a < 0:
            return "Error: No real root"
        self.result = math.sqrt(a)
        return self.result

    def power(self, base, exponent):
        self.result = base ** exponent   # ** means "to the power of" in Python
        return self.result

    def logarithm(self, a):
        if a <= 0:
            return "Error: Log undefined"
        self.result = math.log10(a)      # log base 10
        return self.result

    def toggle_angle_mode(self):
        # Switches between DEG and RAD mode
        if self.angle_mode == "DEG":
            self.angle_mode = "RAD"
        else:
            self.angle_mode = "DEG"
        return self.angle_mode


# ============================================================
# CLASS 3: CalculatorApp (GUI Class)
# This class builds the visual window using tkinter.
# It USES a ScientificCalculator object to do all the math.
# Notice: this class does NOT inherit from anything —
# it just CREATES and USES a ScientificCalculator.
# ============================================================

class CalculatorApp:

    def __init__(self, window):
        # 'window' is the main tkinter window passed in from outside
        self.window = window
        self.window.title("Scientific Calculator")
        self.window.configure(bg="#1e1e2e")   # dark background colour
        self.window.resizable(False, False)    # window can't be resized

        # Create ONE ScientificCalculator object to use throughout the app
        self.calc = ScientificCalculator()

        # self.current_input stores what the user is typing
        self.current_input = ""

        # self.waiting_for_second tells us if we've already entered the first number
        # and are now waiting for the second (used for +, -, *, /)
        self.waiting_for_second = False
        self.first_number = 0
        self.operation = ""   # stores which operation was pressed (+, -, etc.)

        # Now build the screen display and buttons
        self.build_display()
        self.build_buttons()

    # ----------------------------------------------------------
    # build_display: creates the text screen at the top
    # ----------------------------------------------------------
    def build_display(self):
        # Frame = a container that holds other widgets
        display_frame = tk.Frame(self.window, bg="#11111b")
        display_frame.pack(fill="x", padx=10, pady=10)

        # Label showing DEG or RAD mode
        self.mode_label = tk.Label(
            display_frame,
            text="Mode: DEG",
            bg="#11111b",
            fg="#6c7086",
            font=("Consolas", 11),
            anchor="e"   # anchor="e" means text is right-aligned
        )
        self.mode_label.pack(fill="x", padx=10)

        # The main display screen — shows numbers and results
        self.display_var = tk.StringVar()
        self.display_var.set("0")   # starts showing 0

        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,   # links to display_var above
            bg="#11111b",
            fg="#cdd6f4",
            font=("Consolas", 32, "bold"),
            anchor="e",
            height=2,
            padx=10
        )
        self.display.pack(fill="x")

    # ----------------------------------------------------------
    # build_buttons: creates all the buttons on the calculator
    # ----------------------------------------------------------
    def build_buttons(self):
        # Frame to hold all buttons
        button_frame = tk.Frame(self.window, bg="#1e1e2e")
        button_frame.pack(padx=10, pady=10)

        # Button layout: each inner list = one row of buttons
        # Format: ("Label", background_colour)
        button_rows = [
            [("DEG/RAD", "#4a3728"), ("C",   "#f38ba8"), ("⌫",  "#45475a"), ("÷",  "#45475a")],
            [("sin",     "#1e3a5f"), ("cos", "#1e3a5f"), ("tan","#1e3a5f"), ("√",  "#1e3a5f")],
            [("xⁿ",      "#1e3a5f"), ("log", "#1e3a5f"), ("(",  "#45475a"), (")",  "#45475a")],
            [("7",       "#313244"), ("8",   "#313244"), ("9",  "#313244"), ("×",  "#45475a")],
            [("4",       "#313244"), ("5",   "#313244"), ("6",  "#313244"), ("−",  "#45475a")],
            [("1",       "#313244"), ("2",   "#313244"), ("3",  "#313244"), ("+",  "#45475a")],
            [("±",       "#313244"), ("0",   "#313244"), (".",  "#313244"), ("=",  "#89b4fa")],
        ]

        # Loop through each row and each button to create them
        for row_index, row in enumerate(button_rows):
            for col_index, (label, colour) in enumerate(row):

                # For the "=" button, use dark text; others use light text
                if label == "=":
                    text_colour = "#1e1e2e"
                else:
                    text_colour = "#cdd6f4"

                # Create the button widget
                btn = tk.Button(
                    button_frame,
                    text=label,
                    bg=colour,
                    fg=text_colour,
                    font=("Consolas", 14, "bold"),
                    width=5,
                    height=2,
                    bd=0,                    # bd=0 removes the button border
                    relief="flat",
                    cursor="hand2",          # cursor becomes a hand when hovering
                    command=lambda l=label: self.on_click(l)
                    # ↑ This calls on_click() with the button's label when clicked.
                    # We use "l=label" to "freeze" the label value for each button.
                )
                btn.grid(row=row_index, column=col_index, padx=3, pady=3)

                # Save a reference to the DEG/RAD button so we can update its text later
                if label == "DEG/RAD":
                    self.mode_btn = btn

    # ----------------------------------------------------------
    # on_click: this runs every time a button is pressed
    # It checks which button was pressed and reacts accordingly
    # ----------------------------------------------------------
    def on_click(self, label):

        # ── CLEAR button ──────────────────────────────
        if label == "C":
            self.current_input = ""
            self.first_number = 0
            self.operation = ""
            self.waiting_for_second = False
            self.display_var.set("0")

        # ── BACKSPACE button ──────────────────────────
        elif label == "⌫":
            # Remove the last character from input
            self.current_input = self.current_input[:-1]
            if self.current_input == "":
                self.display_var.set("0")
            else:
                self.display_var.set(self.current_input)

        # ── PLUS/MINUS toggle ─────────────────────────
        elif label == "±":
            if self.current_input != "" and self.current_input != "0":
                if self.current_input[0] == "-":
                    self.current_input = self.current_input[1:]  # remove minus
                else:
                    self.current_input = "-" + self.current_input  # add minus
                self.display_var.set(self.current_input)

        # ── DEGREE/RADIAN toggle ──────────────────────
        elif label == "DEG/RAD":
            new_mode = self.calc.toggle_angle_mode()
            self.mode_label.config(text="Mode: " + new_mode)

        # ── EQUALS button ─────────────────────────────
        elif label == "=":
            self.calculate_result()

        # ── BASIC OPERATOR buttons (+, −, ×, ÷) ──────
        elif label in ["+", "−", "×", "÷"]:
            # Save the first number and the operation, then wait for the second
            if self.current_input != "":
                self.first_number = float(self.current_input)
                self.operation = label
                self.current_input = ""
                self.waiting_for_second = True

        # ── POWER button (xⁿ) ────────────────────────
        elif label == "xⁿ":
            if self.current_input != "":
                self.first_number = float(self.current_input)
                self.operation = "xⁿ"
                self.current_input = ""
                self.waiting_for_second = True

        # ── SCIENTIFIC SINGLE-NUMBER buttons ──────────
        # These work on just one number — the one currently on screen
        elif label in ["sin", "cos", "tan", "√", "log"]:
            self.calculate_scientific(label)

        # ── DIGIT, DOT, BRACKET buttons ───────────────
        else:
            # Only allow one decimal point
            if label == "." and "." in self.current_input:
                return  # do nothing if there's already a dot

            self.current_input += label
            self.display_var.set(self.current_input)

    # ----------------------------------------------------------
    # calculate_result: runs when "=" is pressed
    # Uses the saved operation and numbers to get a result
    # ----------------------------------------------------------
    def calculate_result(self):
        # If there's no second number entered yet, do nothing
        if not self.waiting_for_second or self.current_input == "":
            return

        second_number = float(self.current_input)
        result = ""

        # Check which operation was saved and call the right method
        if self.operation == "+":
            result = self.calc.add(self.first_number, second_number)

        elif self.operation == "−":
            result = self.calc.subtract(self.first_number, second_number)

        elif self.operation == "×":
            result = self.calc.multiply(self.first_number, second_number)

        elif self.operation == "÷":
            result = self.calc.divide(self.first_number, second_number)

        elif self.operation == "xⁿ":
            result = self.calc.power(self.first_number, second_number)

        # If result is a whole number (e.g. 6.0), show it as 6, not 6.0
        if isinstance(result, float) and result == int(result):
            result = int(result)

        self.display_var.set(str(result))
        self.current_input = str(result)
        self.waiting_for_second = False
        self.operation = ""

    # ----------------------------------------------------------
    # calculate_scientific: for sin, cos, tan, sqrt, log
    # These only need ONE number (the one on the display)
    # ----------------------------------------------------------
    def calculate_scientific(self, func_name):
        if self.current_input == "":
            return   # nothing to calculate

        number = float(self.current_input)
        result = ""

        if func_name == "sin":
            result = self.calc.sine(number)

        elif func_name == "cos":
            result = self.calc.cosine(number)

        elif func_name == "tan":
            result = self.calc.tangent(number)

        elif func_name == "√":
            result = self.calc.square_root(number)

        elif func_name == "log":
            result = self.calc.logarithm(number)

        # Clean up the display the same way
        if isinstance(result, float) and result == int(result):
            result = int(result)

        self.display_var.set(str(result))
        self.current_input = str(result)


# ============================================================
# ENTRY POINT — this is where the program starts running
# ============================================================

window = tk.Tk()             # create the main window
app = CalculatorApp(window)  # create our app, passing the window in
window.mainloop()            # start the GUI loop (keeps window open)