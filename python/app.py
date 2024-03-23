import os
import bashcommands

bash = bashcommands.BashCommands

class App:
    def __init__(
        self,
        window_name,
        translation,
        command_to_launch,
        ask_before_launch,
        ignored,
    ):
        self.window_name = window_name
        self.translation = translation
        self.command_to_launch = command_to_launch
        self.ask_before_launch = ask_before_launch
        self.ignored = ignored

    def __str__(self):
        return (
            f'window_name={self.window_name}, '
            f'translation={self.translation}, '
            f'command_to_launch={self.command_to_launch}, '
            f'ignored={self.ignored}, '
            f'ask_before_launch={self.ask_before_launch}, '
        )

    def run_app(self):
        bash.execute_bash_command(self.command_to_launch)

    @staticmethod
    def get_suggestions_and_translations(letter):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, 'apps.csv')
        suggestions = []
        translations = {}
        ignored = []
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    app_properties = line.split(';')
                    window_name = app_properties[0].strip()
                    translation = app_properties[1].strip()
                    command_to_launch = app_properties[2].strip()
                    ignore = app_properties[3].strip()
                    ask_before_launch = app_properties[4].strip()

                    translations[window_name] = translation
                    app = App(window_name, translation, command_to_launch, ask_before_launch, ignore)
                    if ignore == '1':
                        ignored.append(app)
                    else:
                        if letter is None or translation.startswith(letter):
                            suggestions.append(app)

        except FileNotFoundError:
            raise Exception(f"The file '{file_path}' was not found.")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

        return suggestions, translations, ignored
