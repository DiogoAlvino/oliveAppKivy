from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from plyer import filechooser
from yoloutils.index import generate_and_overlay_mask
import os

Window.size = (350, 600)
dirname = os.path.dirname(__file__)

class SamplingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_screen = Builder.load_file("views/sampling.kv")
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.add_widget(self.menu_screen)
        self.selected_images = []

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected_image, multiple=True, filters=[("Comma-separated Values", "*.png", "*.jpeg", "*.jpg")])

    def selected_image(self, image):
        self.selected_images.extend(image)
        print(self.selected_images)
    
    def create_batch(self):
        if(len(self.selected_images) != 0):
            self.iniciar_yolo()

    def iniciar_yolo(self):
        counter = 0
        for path in self.selected_images:
            counter += 1
            output_path = f"{dirname}\\results\\result{counter}.png"
            generate_and_overlay_mask(path, output_path)