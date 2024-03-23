class Window:
    def __init__(
        self,
        window_id,
        class_name,
        window_title
    ):
        self.window_id = window_id
        self.class_name = class_name
        self.window_title = window_title

    def __str__(self):
        return (
            f"window_id: {self.window_id}, "
            f"wm_class_name: {self.class_name}, "
            f"window_title: {self.window_title}"
        )
