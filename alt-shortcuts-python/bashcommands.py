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
    def get_running_windows_on_letter(letter, translations, active_window_id, window_id_stack):
        try:
            all_windows = BashCommands.get_all_running_windows()
            all_windows = BashCommands.translate_windows(all_windows, translations)
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
    def get_window_stack_and_active_window():
        try:
            command = "xprop -root | grep '^_NET_CLIENT_LIST_STACKING' | cut -c 48- | tr ', ' ','"
            output = BashCommands.execute_bash_command(command)

            window_ids = output.strip().split(',,')
            window_ids_fixed = []

            for window_id in window_ids:
                while len(window_id) < 10:
                    window_id = window_id.replace("0x", "0x0")
                window_ids_fixed.append(window_id)

            return window_ids_fixed, window_ids_fixed[-1]

        except Exception as e:
            raise Exception(f"Exception occurred: {e}")

    # @staticmethod
    # def close_window(window):
    #     print(f"killing processes with name {window}")
    #     good_processes, _ = Bash_commands.get_running_windows()
    #     zenity_processes = [process for process in good_processes if window in process.pid]
    #     for process in zenity_processes:
    #         print(f'Killing process with id {process}')
    #         try:
    #             command = ["wmctrl", "-i", "-c", process.window_id]
    #             subprocess.run(command, check=True)
    #         except subprocess.CalledProcessError as e:
    #             raise Exception(f"Error: {e}")

    # @staticmethod
    # def filter_window_ids_by_name(name):
    #     try:
    #         command = ["wmctrl", "-lix"]
    #         process = subprocess.Popen(command, stdout=subprocess.PIPE)
    #         grep_process = subprocess.Popen(["grep", name], stdin=process.stdout, stdout=subprocess.PIPE)
    #         process.stdout.close()
    #         output, _ = grep_process.communicate()
    #
    #         if grep_process.returncode == 0:
    #             return output.decode()
    #         else:
    #             raise Exception("Error in grep command")
    #     except Exception as e:
    #         raise Exception(f"Exception occurred: {e}")
    # @staticmethod
    # def extract_window_ids(output):
    #     try:
    #         if output:
    #             lines = output.splitlines()
    #             window_ids = [line.split()[0] for line in lines]
    #             return window_ids
    #         else:
    #             return []
    #     except Exception as e:
    #         raise Exception(f"Exception occurred: {e}")
    #

