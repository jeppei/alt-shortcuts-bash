import subprocess
import time

from window import Window


class BashCommands:
    window_title = "Choose an app to start"

    @staticmethod
    def execute_bash_command(command):
        print(f'Executing command: {command}')
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Command '{command}' failed with error: {e}"  # Return

    @staticmethod
    def activate_window_by_match(window):
        print(f'Will switch focus to window {window}')
        BashCommands.execute_bash_command(f"wmctrl -ia {window.window_id}")

    @staticmethod
    def get_all_running_windows():
        print(f'Getting all running windows')
        output = BashCommands.execute_bash_command("wmctrl -xl")
        return BashCommands.parse_wmctrl_output(output)

    @staticmethod
    def close_window(window):
        print(f"Closing window {window}")
        command = f"wmctrl -ic {window.window_id}"
        BashCommands.execute_bash_command(command)

    @staticmethod
    def get_running_windows_on_letter(
        letter,
        translations,
        active_window_id,
        window_id_stack
    ):
        try:
            all_windows = BashCommands.get_active_windows_translated(translations)
            active_window = BashCommands.get_active_window(all_windows, active_window_id)
            good_windows = []
            for window_id_in_stack in window_id_stack:
                window = next((window for window in all_windows if window.window_id == window_id_in_stack), None)
                if window.class_name.startswith(letter):
                    good_windows.append(window)

            if active_window is None:
                raise Exception(f'Could not find the active window with id {active_window_id}')
            return good_windows, active_window
        except Exception as e:
            raise Exception(f"Exception occurred: {e}")

    @staticmethod
    def get_active_window(all_windows, active_window_id):
        for window in all_windows:
            if window.window_id == active_window_id:
                return window
        raise Exception(f"Could the active window with id {active_window_id}")

    @staticmethod
    def get_active_windows_translated(translations):
        all_windows = BashCommands.get_all_running_windows()
        all_windows_translated = BashCommands.translate_windows(all_windows, translations)
        return all_windows_translated

    @staticmethod
    def translate_windows(all_windows, translations):
        for window in all_windows:
            if window.class_name in translations:
                window.class_name = translations[window.class_name]
        return all_windows

    @staticmethod
    def close_windows_with_suggestions():
        try:
            all_windows = BashCommands.get_all_running_windows()
            for window in all_windows:
                class_name_matches = window.class_name == "tk.Tk"
                window_title_matches = window.window_title == BashCommands.window_title
                if class_name_matches and window_title_matches:
                    BashCommands.close_window(window)
                    time.sleep(0.05)
        except Exception as e:
            raise Exception(f"Exception occurred: {e}")

    @staticmethod
    def parse_wmctrl_output(output):
        windows = []
        lines = output.splitlines()
        for line in lines:
            parts = line.split()
            window_id = parts[0]
            class_name = parts[2]
            window_name = ' '.join(parts[4:])
            window = Window(window_id, class_name, window_name)
            windows.append(window)
        return windows

    @staticmethod
    def get_window_stack_and_active_window(ignored_windows, translations):
        try:
            command = "xprop -root | grep '^_NET_CLIENT_LIST_STACKING' | cut -c 48- | tr ', ' ','"
            output = BashCommands.execute_bash_command(command)

            window_ids = output.strip().split(',,')
            window_ids_fixed = []

            for window_id in window_ids:
                while len(window_id) < 10:
                    window_id = window_id.replace("0x", "0x0")
                window_ids_fixed.append(window_id)

            all_windows = BashCommands.get_active_windows_translated(translations)
            active_window_id = None
            for i in range(len(window_ids_fixed) - 1, -1, -1):
                current_window_id = window_ids_fixed[i]
                current_window = BashCommands.get_active_window(all_windows, current_window_id)
                if current_window.class_name != 'IGNORE':
                    active_window_id = window_ids_fixed[i]
                    break

            if active_window_id is None:
                print('Could not find an active window after ignoring, will ignore the ignored list')
                active_window_id = window_ids_fixed[-1]

            return window_ids_fixed, active_window_id

        except Exception as e:
            raise Exception(f"Exception occurred: {e}")
