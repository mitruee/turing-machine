import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import algorithms

class TuringMachineApp:
    """

    """
    def __init__(self, root):
        """

        :param root:
        """
        self.root = root
        self.root.title("Turing Machine")
        self.root.geometry("900x700")

        self.tm = None
        self.current_algorithm = None
        self.input_tape = ""
        self.step_count = 0

        self.create_widgets()

        self.algorithms = {
            "Binary Inverter": algorithms.binary_inverter,
            "Unary Adder": algorithms.unary_adder
        }

        self.update_algorithm_list()

    def create_widgets(self):
        """

        :return:
        """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Select algorithm:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.algorithm_var = tk.StringVar()
        self.algorithm_combo = ttk.Combobox(main_frame, textvariable=self.algorithm_var, state="readonly")
        self.algorithm_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.algorithm_combo.bind('<<ComboboxSelected>>', self.on_algorithm_select)

        ttk.Label(main_frame, text="Input tape:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))

        self.tape_entry = ttk.Entry(main_frame)
        self.tape_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 5))
        self.tape_entry.insert(0, "0011")
        self.tape_entry.bind('<KeyRelease>', self.on_tape_change)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Initialize", command=self.initialize_tm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Step Forward", command=self.step_forward).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Run to End", command=self.run_to_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_tm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="5")
        info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))

        self.state_label = ttk.Label(info_frame, text="State: Not initialized")
        self.state_label.pack(anchor=tk.W)

        self.steps_label = ttk.Label(info_frame, text="Steps executed: 0")
        self.steps_label.pack(anchor=tk.W)

        self.tape_label = ttk.Label(info_frame, text="Tape: ")
        self.tape_label.pack(anchor=tk.W)

        tape_frame = ttk.LabelFrame(main_frame, text="Tape Visualization", padding="10")
        tape_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 5))

        tape_frame.columnconfigure(0, weight=1)
        tape_frame.rowconfigure(0, weight=1)

        self.tape_canvas = tk.Canvas(tape_frame, height=100, bg="white", relief=tk.SUNKEN)
        self.tape_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        log_frame = ttk.LabelFrame(main_frame, text="Execution Log", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 5))

        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        desc_frame = ttk.LabelFrame(main_frame, text="Algorithm Description", padding="5")
        desc_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        self.desc_text = tk.Text(desc_frame, height=4, width=80, wrap=tk.WORD)
        self.desc_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.desc_text.config(state=tk.DISABLED)

        self.algorithm_descriptions = {
            "Binary Inverter": "Inverts binary string (0 → 1, 1 → 0). Example: '0011' → '1100'",
            "Unary Adder": "Adds two unary numbers (represented by ones). Numbers separated by zero. Example: '111011' → '111111' (3 + 2 = 5)"
        }

    def update_algorithm_list(self):
        """

        :return:
        """
        algorithms_list = list(self.algorithms.keys())
        self.algorithm_combo['values'] = algorithms_list
        if algorithms_list:
            self.algorithm_combo.current(0)
            self.update_algorithm_description()

    def update_algorithm_description(self):
        """

        :return:
        """
        algo_name = self.algorithm_var.get()
        if algo_name in self.algorithm_descriptions:
            self.desc_text.config(state=tk.NORMAL)
            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(1.0, self.algorithm_descriptions[algo_name])
            self.desc_text.config(state=tk.DISABLED)

    def on_algorithm_select(self, event):
        """

        :param event:
        :return:
        """
        self.update_algorithm_description()
        self.clear_log()

    def on_tape_change(self, event):
        """

        :param event:
        :return:
        """
        self.clear_log()

    def clear_log(self):
        """

        :return:
        """
        self.log_text.delete(1.0, tk.END)

    def initialize_tm(self):
        """

        :return:
        """
        algo_name = self.algorithm_var.get()
        input_tape = self.tape_entry.get().strip()

        if not algo_name:
            messagebox.showwarning("Warning", "Select algorithm!")
            return

        if algo_name not in self.algorithms:
            messagebox.showerror("Error", "Selected algorithm not found!")
            return

        try:
            algo_func = self.algorithms[algo_name]

            self.tm = algo_func(input_tape)
            self.current_algorithm = algo_name
            self.input_tape = input_tape
            self.step_count = 0

            self.update_display()

            self.log(f"Initialized algorithm: {algo_name}")
            self.log(f"Input tape: '{input_tape}'")
            self.log(f"Initial state: {self.tm.current_state}")

        except Exception as e:
            messagebox.showerror("Error", f"Initialization error: {str(e)}")

    def step_forward(self):
        """

        :return:
        """
        if not self.tm:
            messagebox.showwarning("Warning", "Initialize Turing Machine first!")
            return

        if self.tm.current_state in self.tm.final_states:
            self.log("Machine already in final state!")
            return

        try:
            result = self.tm.step()
            self.step_count += 1

            if result:
                self.log(f"Step {self.step_count}: moved to state {self.tm.current_state}")
            else:
                if self.tm.current_state in self.tm.final_states:
                    self.log(f"Step {self.step_count}: reached final state {self.tm.current_state}")
                else:
                    self.log(f"Step {self.step_count}: no transition rule for state {self.tm.current_state}")

            self.update_display()

        except Exception as e:
            messagebox.showerror("Error", f"Step execution error: {str(e)}")

    def run_to_end(self):
        """

        :return:
        """
        if not self.tm:
            messagebox.showwarning("Warning", "Initialize Turing Machine first!")
            return

        try:
            max_steps = 1000
            steps_before = self.step_count

            while self.step_count - steps_before < max_steps:
                if not self.tm.step():
                    break
                self.step_count += 1

            self.log(f"Executed {self.step_count - steps_before} steps until completion")
            self.update_display()

        except Exception as e:
            messagebox.showerror("Error", f"Execution error: {str(e)}")

    def reset_tm(self):
        if self.current_algorithm and self.input_tape:
            algo_func = self.algorithms[self.current_algorithm]
            self.tm = algo_func(self.input_tape)
            self.step_count = 0
            self.update_display()
            self.log("Turing Machine reset")

    def update_display(self):
        """

        :return:
        """
        if not self.tm:
            self.state_label.config(text="State: Not initialized")
            self.steps_label.config(text="Steps executed: 0")
            self.tape_label.config(text="Tape: ")
            self.draw_tape()
            return

        self.state_label.config(text=f"State: {self.tm.current_state}")
        self.steps_label.config(text=f"Steps executed: {self.step_count}")

        tape_str = ''.join(self.tm.tape)
        head_pos = self.tm.head_position

        display_pos = head_pos
        if head_pos < 0:
            tape_str = self.tm.blank_symbol * abs(head_pos) + tape_str
            display_pos = 0
        elif head_pos >= len(tape_str):
            tape_str = tape_str + self.tm.blank_symbol * (head_pos - len(tape_str) + 1)

        self.tape_label.config(text=f"Tape: {tape_str}")

        self.draw_tape(tape_str, display_pos)

    def draw_tape(self, tape_str="", head_pos=0):
        """

        :param tape_str:
        :param head_pos:
        :return:
        """
        self.tape_canvas.delete("all")

        if not tape_str:
            return

        cell_width = 40
        cell_height = 60
        start_x = 20
        start_y = 20

        for i, symbol in enumerate(tape_str):
            x1 = start_x + i * cell_width
            y1 = start_y
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            self.tape_canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")

            self.tape_canvas.create_text(x1 + cell_width / 2, y1 + cell_height / 2,
                                         text=symbol, font=("Arial", 14, "bold"))

            self.tape_canvas.create_text(x1 + cell_width / 2, y2 + 10,
                                         text=str(i), font=("Arial", 10))

        if 0 <= head_pos < len(tape_str):
            x_head = start_x + head_pos * cell_width + cell_width / 2
            y_head = y1 - 10

            self.tape_canvas.create_polygon(
                x_head - 10, y_head,
                x_head + 10, y_head,
                x_head, y_head - 10,
                fill="red"
            )

            self.tape_canvas.create_text(x_head, y_head - 25,
                                         text="Head", font=("Arial", 10, "bold"))

    def log(self, message):
        """

        :param message:
        :return:
        """
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

def main():
    """

    :return:
    """
    root = tk.Tk()
    TuringMachineApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()