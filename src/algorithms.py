from TuringMachine import TuringMachine

def binary_inverter(input_tape=""):
    """

    :param input_tape:
    :return:
    """
    tm = TuringMachine(tape=input_tape, blank_symbol="B")

    tm.add_transition("q0", "0", "q0", "1", "R")
    tm.add_transition("q0", "1", "q0", "0", "R")
    tm.add_transition("q0", "B", "q_halt", "B", "S")

    tm.final_states = {"q_halt"}
    return tm

def unary_adder(input_tape=""):
    """

    :param input_tape:
    :return:
    """
    tm = TuringMachine(tape=input_tape, blank_symbol="B")

    tm.add_transition("q0", "1", "q0", "1", "R")
    tm.add_transition("q0", "0", "q1", "1", "R")

    tm.add_transition("q1", "1", "q1", "1", "R")
    tm.add_transition("q1", "B", "q2", "B", "L")

    tm.add_transition("q2", "1", "q_halt", "B", "S")

    tm.final_states = {"q_halt"}
    return tm

def visualize_execution(an: str, tm: TuringMachine, max_steps=1000):
    """

    :param an:
    :param tm:
    :param max_steps:
    :return:
    """
    print(f"=== VISUALIZER {an.upper()} ===")
    print("Initial configuration:")
    print(tm)
    print("\nExecution:")

    steps = 0
    while steps < max_steps:
        if not tm.step():
            break
        steps += 1

        print(f"== Step {steps} ==")
        print(tm)
        print()

    print(f"Execution completed in {steps} steps")
    print(f"Result: {tm}")
