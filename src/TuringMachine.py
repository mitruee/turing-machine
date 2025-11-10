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
        self.history = []

    def add_transition(self, state, read_symbol, next_state, write_symbol, direction):
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

        # Расширяем ленту только когда это действительно необходимо
        if self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
        elif self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0

        current_symbol = self.tape[self.head_position]
        transition_key = (self.current_state, current_symbol)

        if transition_key not in self.transitions:
            return False

        next_state, write_symbol, direction = self.transitions[transition_key]

        self.tape[self.head_position] = write_symbol

        self.history.append({
            'state': self.current_state,
            'head_position': self.head_position,
            'tape': self.tape.copy(),
            'read_symbol': current_symbol,
            'write_symbol': write_symbol,
            'direction': direction
        })

        self.current_state = next_state

        # Двигаем головку только если не в финальном состоянии
        if self.current_state not in self.final_states:
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1

        return True

    def run(self, max_steps=1000, verbose=False):
        """

        :param max_steps:
        :param verbose:
        :return:
        """
        step_count = 0

        while step_count < max_steps:
            if not self.step():
                break
            step_count += 1

        return step_count < max_steps

    def get_tape_string(self):
        """
        Возвращает строковое представление ленты, обрезая пустые символы с обоих концов
        """
        tape_str = ''.join(self.tape)

        # Находим первый и последний не-пустые символы
        first_non_blank = 0
        last_non_blank = len(tape_str) - 1

        # Ищем первый не-пустой символ слева
        while first_non_blank <= last_non_blank and tape_str[first_non_blank] == self.blank_symbol:
            first_non_blank += 1

        # Ищем последний не-пустой символ справа
        while last_non_blank >= first_non_blank and tape_str[last_non_blank] == self.blank_symbol:
            last_non_blank -= 1

        # Если все символы пустые, возвращаем пустую строку
        if first_non_blank > last_non_blank:
            return ""

        return tape_str[first_non_blank:last_non_blank + 1]

    def __str__(self):
        """
        Улучшенное строковое представление с обработкой всех крайних случаев
        """
        tape_str = ''.join(self.tape)

        # Определяем позицию для отображения головки
        if self.head_position < 0:
            # Головка слева от видимой ленты
            marker = '^' + ' ' * (abs(self.head_position) - 1)
            tape_display = self.blank_symbol * abs(self.head_position) + tape_str
        elif self.head_position >= len(tape_str):
            # Головка справа от видимой ленты
            extra_spaces = self.head_position - len(tape_str) + 1
            marker = ' ' * len(tape_str) + '^' + ' ' * (extra_spaces - 1)
            tape_display = tape_str + self.blank_symbol * extra_spaces
        else:
            # Головка в пределах ленты
            marker = ' ' * self.head_position + '^'
            tape_display = tape_str

        return f"State: {self.current_state}\nTape: {tape_display}\n      {marker}"
