from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from plyer import filechooser
from yoloutils.index import generate_and_overlay_mask
import os
from scripts.oliveClassification import olivindex2

Window.size = (350, 600)
dirname = os.path.dirname(__file__)

class ProcessYOLO(Screen):
    def __init__(self, selected_images=None, **kwargs):
        super().__init__(**kwargs)
        self.yolo_screen = Builder.load_file("views/processYOLO.kv")
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.add_widget(self.yolo_screen)
        self.classification_results = ""
        self.selected_images = selected_images
        if selected_images:
            self.iniciar_yolo()

    def iniciar_yolo(self):
        counter = 0
        results = []

        if(len(self.selected_images) > 0):
            for path in self.selected_images:
                counter += 1
                output_path = f"{dirname}\\results\\result{counter}.png"
                results.append(output_path)
                generate_and_overlay_mask(path, output_path)
            self.classification_results = olivindex2(results)
            print(self.classification_results)
