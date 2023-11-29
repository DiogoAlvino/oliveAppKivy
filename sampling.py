from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from plyer import filechooser
from processYOLO import ProcessYOLO
import os

Window.size = (350, 600)
dirname = os.path.dirname(__file__)


class BatchValidator:
    def __init__(self, screen):
        self.screen = screen

    def validate_input(self, user_input, element_id):
        element = self.screen.ids[element_id]
        if not user_input:
            element.required = True
            raise ValueError(f"Input required for {element_id}")
        element.required = False
        return True

    def validate_batch(self):
        app = App.get_running_app()
        sampling_screen = app.root.get_screen("sampling")

        inputs_to_validate = [
            ("input_batch_name", self.screen.ids.input_batch_name.text),
            ("input_sample_count", self.screen.ids.input_sample_count.text),
            ("input_color_pattern", self.screen.ids.input_color_pattern.text),
            ("input_predictive_model", self.screen.ids.input_predictive_model.text),
        ]

        for element_id, user_input in inputs_to_validate:
            if not self.validate_input(user_input, element_id):
                return False

        num_images = len(self.screen.selected_images)
        if num_images < int(self.screen.ids.input_sample_count.text):
            print("Quantidade de imagens inferior a de amostras")
            sampling_screen.ids["input_sample_count"].helper_text = f"Quantidade de imagens inferior a de amostras"
            sampling_screen.ids["input_sample_count"].helper_text_mode = "persistent"
            return False

        return True


class SamplingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_images = []
        self.batch_validator = BatchValidator(self)

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected_image, multiple=True, filters=[("Comma-separated Values", "*.png", "*.jpeg", "*.jpg")])

    def selected_image(self, image):
        self.selected_images.extend(image)
        print(self.selected_images)

    def create_batch(self):
        if self.batch_validator.validate_batch():
            app = App.get_running_app()
            app.root.current = "loading"
            Clock.schedule_once(self.start_yolo_process, 0.2)

    def start_yolo_process(self, dt):
        process_yolo = ProcessYOLO(selected_images=self.selected_images)
        process_yolo.start_yolo()
