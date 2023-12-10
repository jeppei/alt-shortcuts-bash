import ttkbootstrap as tkb
from screeninfo import get_monitors
import bashcommands

bash = bashcommands.BashCommands


class WindowWithSuggestions:

    def __init__(self, apps):
        if len(apps) == 0:
            return
        self.apps = apps
        self.root = tkb.Window(themename='darkly')
        self.center_window()
        self.root.title(bash.window_title)
        self.buttons = []
        self.create_buttons()
        self.current_button_index = 0
        self.buttons[self.current_button_index].focus_set()
        self.bind_keys()

    def close_window_and_print(self, command):
        bash.execute_bash_command(command)
        self.root.destroy()

    def create_buttons(self):
        for app in self.apps:
            button = tkb.Button(
                self.root,
                text=app.translation,
                command=lambda cmd=app.command_to_launch: self.close_window_and_print(cmd),
                style='primary.TButton'
            )
            button.pack(padx=10, pady=5)
            self.buttons.append(button)

    def center_window(self):
        window_width = 300
        window_height = 200

        monitors = get_monitors()

        primary_monitor = next((monitor for monitor in monitors if monitor.is_primary), monitors[0])
        screen_width = primary_monitor.width
        screen_height = primary_monitor.height

        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def focus_next_button(self, _):
        self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
        self.buttons[self.current_button_index].focus_set()

    def focus_prev_button(self, _):
        self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
        self.buttons[self.current_button_index].focus_set()

    def click_focused_button(self, _):
        self.buttons[self.current_button_index].invoke()

    def close_window_on_escape(self, _):
        self.root.destroy()

    def bind_keys(self):
        self.root.bind("<Up>", self.focus_prev_button)
        self.root.bind("<Down>", self.focus_next_button)
        self.root.bind("<Return>", self.click_focused_button)
        self.root.bind("<Return>", self.click_focused_button)
        self.root.bind("<Escape>", self.close_window_on_escape)

    def run(self):
        self.root.mainloop()