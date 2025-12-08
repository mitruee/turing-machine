class TuringMachine:
    """

    """

    def __init__(self, tape="", blank_symbol=" ", initial_state="q0", final_states=None):
        """

        :param tape:
        :param blank_symbol:
        :param initial_state:
        :param final_states:
        """
        self.tape = list(tape) if tape else [blank_symbol]
        self.head_position = 0
        self.current_state = initial_state
        self.blank_symbol = blank_symbol
        self.final_states = final_states if final_states else set()
        self.transitions = {}

    def add_transition(self, state: str, read_symbol: str, next_state: str, write_symbol: str, direction: str):
        """

        :param state:
        :param read_symbol:
        :param next_state:
        :param write_symbol:
        :param direction:
        :return:
        """

        key = (state, read_symbol)
        self.transitions[key] = (next_state, write_symbol, direction)

    def step(self):
        if self.current_state in self.final_states:
            return False

        if self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)

        current_symbol = self.tape[self.head_position]
        transition_key = (self.current_state, current_symbol)

        if transition_key not in self.transitions:
            return False

        next_state, write_symbol, direction = self.transitions[transition_key]

        self.tape[self.head_position] = write_symbol

        self.current_state = next_state

        if self.current_state not in self.final_states:
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1

        return True

    def run(self, max_steps=1000):
        """

        :param max_steps:
        :return:
        """
        step_count = 0

        while step_count < max_steps:
            if not self.step():
                break
            step_count += 1

        return step_count < max_steps

    def __str__(self):
        """

        :return:
        """
        tape_str = ''.join(self.tape)

        if self.head_position < 0:
            marker = '^' + ' ' * (abs(self.head_position) - 1)
            tape_display = self.blank_symbol * abs(self.head_position) + tape_str
        elif self.head_position >= len(tape_str):
            extra_spaces = self.head_position - len(tape_str) + 1
            marker = ' ' * len(tape_str) + '^' + ' ' * (extra_spaces - 1)
            tape_display = tape_str + self.blank_symbol * extra_spaces
        else:
            marker = ' ' * self.head_position + '^'
            tape_display = tape_str

        return f"State: {self.current_state}\nTape: {tape_display}\n      {marker}"
