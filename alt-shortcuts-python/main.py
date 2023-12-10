import sys

from app import App
from window_with_suggestions import WindowWithSuggestions
import bashcommands


class Main:
    def __init__(self):
        self.bash = bashcommands.BashCommands()

    def run(self, letter):
        print("\n\n\
             █████╗ ██╗  ████████╗    ███████╗██╗  ██╗ ██████╗ ██████╗ ████████╗ ██████╗██╗   ██╗████████╗███████╗ \n\
            ██╔══██╗██║  ╚══██╔══╝    ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██║   ██║╚══██╔══╝██╔════╝ \n\
            ███████║██║     ██║       ███████╗███████║██║   ██║██████╔╝   ██║   ██║     ██║   ██║   ██║   ███████╗ \n\
            ██╔══██║██║     ██║       ╚════██║██╔══██║██║   ██║██╔══██╗   ██║   ██║     ██║   ██║   ██║   ╚════██║ \n\
            ██║  ██║███████╗██║       ███████║██║  ██║╚██████╔╝██║  ██║   ██║   ╚██████╗╚██████╔╝   ██║   ███████║ \n\
            ╚═╝  ╚═╝╚══════╝╚═╝       ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝ \n\
            \n\n"
        )

        self.bash.close_windows_with_suggestions()

        print(letter)

        window_id_stack, active_window_id = self.bash.get_window_stack_and_active_window()
        print(f'Window stack: {window_id_stack}')
        print(f'Active window id: {active_window_id}')

        suggestions, translations = App.get_suggestions_and_translations(letter)
        self.print_list(suggestions, f'Suggestions')
        self.print_map(translations, "Translations")

        running_windows_on_letter, active_window = self.bash.get_running_windows_on_letter(
            letter,
            translations,
            active_window_id,
            window_id_stack
        )
        self.print_list(running_windows_on_letter, "Running windows on letter")
        print(f'Active window: {active_window}')

        no_running_windows_on_letter = len(running_windows_on_letter) == 0
        current_window_is_the_only_one_on_letter = (
            active_window.class_name.startswith(letter) and
            len(running_windows_on_letter) == 1
        )

        print(f'\n\n\nRESULT:')
        if no_running_windows_on_letter:
            print(f"Couldn't find a window on letter {letter}")
            self.print_list(suggestions, "Here are some suggestions")
            WindowWithSuggestions(suggestions).run()

        elif current_window_is_the_only_one_on_letter:
            print(f"Current window is the only on letter {letter}")
            self.print_list(suggestions, "Here are some suggestions")
            WindowWithSuggestions(suggestions).run()

        elif active_window.class_name.startswith(letter):
            print(f"Current window starts on {letter}. Will activate the oldest window on letter {letter}")
            self.bash.activate_window_by_match(running_windows_on_letter[0])

        else:
            print(f"Current window does not starts on {letter}. Will activate the most recent window on letter {letter}")
            self.bash.activate_window_by_match(running_windows_on_letter[-1])

    @staticmethod
    def print_list(list_of_items, list_name):
        print(f'{list_name}:')
        for item in list_of_items:
            print(f'    {item}')
        print()

    @staticmethod
    def print_map(map, map_name):
        print(f'{map_name}:')
        for key, value in map.items():
            print(f"    {key}-->{value}")


def main():
    if len(sys.argv) != 2:
        print("This script only supports one argument which should be a single character")
        return

    letter = sys.argv[1]

    m = Main()
    m.run(letter)


if __name__ == "__main__":
    main()
