from TuringMachine import TuringMachine


def binary_inverter(input_tape=""):
    """
    Создает машину Тьюринга для инвертирования бинарной строки
    Работает с любыми последовательностями из 0 и 1
    """
    tm = TuringMachine(tape=input_tape, blank_symbol="B")

    tm.add_transition("q0", "0", "q0", "1", "R")
    tm.add_transition("q0", "1", "q0", "0", "R")
    tm.add_transition("q0", "B", "q_hast", "", "S")

    tm.final_states = {"q_hast"}
    return tm


def palindrome_checker(input_tape=""):
    """
    Исправленный алгоритм проверки палиндрома для бинарных строк
    Возвращает '1' если палиндром, '0' если нет
    """
    tm = TuringMachine(tape=input_tape, blank_symbol="B")

    # Начало: ищем первый непомеченный символ
    tm.add_transition("q0", "0", "q_mark_0", "X", "R")  # Помечаем первый 0
    tm.add_transition("q0", "1", "q_mark_1", "Y", "R")  # Помечаем первый 1
    tm.add_transition("q0", "X", "q0", "X", "R")  # Уже помечен, идем дальше
    tm.add_transition("q0", "Y", "q0", "Y", "R")  # Уже помечен, идем дальше
    tm.add_transition("q0", "B", "q_accept", "1", "R")  # Все символы проверены - палиндром!

    # Пометили 0, идем к концу
    tm.add_transition("q_mark_0", "0", "q_mark_0", "0", "R")
    tm.add_transition("q_mark_0", "1", "q_mark_0", "1", "R")
    tm.add_transition("q_mark_0", "X", "q_mark_0", "X", "R")
    tm.add_transition("q_mark_0", "Y", "q_mark_0", "Y", "R")
    tm.add_transition("q_mark_0", "B", "q_check_last_0", "B", "L")

    # Пометили 1, идем к концу
    tm.add_transition("q_mark_1", "0", "q_mark_1", "0", "R")
    tm.add_transition("q_mark_1", "1", "q_mark_1", "1", "R")
    tm.add_transition("q_mark_1", "X", "q_mark_1", "X", "R")
    tm.add_transition("q_mark_1", "Y", "q_mark_1", "Y", "R")
    tm.add_transition("q_mark_1", "B", "q_check_last_1", "B", "L")

    # Проверяем последний символ для 0
    tm.add_transition("q_check_last_0", "0", "q_return", "X", "L")  # Совпало
    tm.add_transition("q_check_last_0", "1", "q_reject", "0", "R")  # Не совпало
    tm.add_transition("q_check_last_0", "X", "q_check_last_0", "X", "L")
    tm.add_transition("q_check_last_0", "Y", "q_check_last_0", "Y", "L")
    tm.add_transition("q_check_last_0", "B", "q_accept", "1", "R")  # Достигли начала - палиндром!

    # Проверяем последний символ для 1
    tm.add_transition("q_check_last_1", "1", "q_return", "Y", "L")  # Совпало
    tm.add_transition("q_check_last_1", "0", "q_reject", "0", "R")  # Не совпало
    tm.add_transition("q_check_last_1", "X", "q_check_last_1", "X", "L")
    tm.add_transition("q_check_last_1", "Y", "q_check_last_1", "Y", "L")
    tm.add_transition("q_check_last_1", "B", "q_accept", "1", "R")  # Достигли начала - палиндром!

    # Возвращаемся к началу
    tm.add_transition("q_return", "0", "q_return", "0", "L")
    tm.add_transition("q_return", "1", "q_return", "1", "L")
    tm.add_transition("q_return", "X", "q_return", "X", "L")
    tm.add_transition("q_return", "Y", "q_return", "Y", "L")
    tm.add_transition("q_return", "B", "q0", "B", "R")

    tm.final_states = {"q_accept", "q_reject"}
    return tm

def visualize_execution(an: str, tm: TuringMachine, max_steps=50):
    """Визуализирует выполнение машины Тьюринга"""
    print(f"=== {an.upper()} ===")
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
    print(f"Result: {tm.get_tape_string()}")


def test_palindrome():
    """Тестирование исправленного палиндром-чекера"""

    test_cases = [
        ("101", True),  # Палиндром
        ("1001", True),  # Палиндром
        ("10101010101", True),  # Палиндром (11 символов)
        ("101010101010", False),  # Не палиндром (12 символов)
        ("110", False),  # Не палиндром
        ("1", True),  # Один символ
        ("0", True),  # Один символ
        ("", True),  # Пустая строка
        ("11", True),  # Два одинаковых
        ("10", False),  # Два разных
    ]

    print("=== Тестирование палиндром-чекера ===\n")

    for test_input, expected in test_cases:
        tm = palindrome_checker(test_input)
        completed = tm.run(max_steps=1000, verbose=False)

        if completed:
            result_tape = tm.get_tape_string()
            # Определяем результат по наличию 1 или 0 в результате
            if "1" in result_tape and "0" not in result_tape:
                result = True
            elif "0" in result_tape:
                result = False
            else:
                result = None

            status = "✓" if result == expected else "✗"
            print(
                f"{status} '{test_input}' -> {'палиндром' if result else 'не палиндром'} (ожидалось: {'палиндром' if expected else 'не палиндром'})")
        else:
            print(f"✗ '{test_input}' -> НЕ ЗАВЕРШЕНО")


if __name__ == "__main__":
    test_palindrome()