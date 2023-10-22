from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from scripts.oliveClassification import olivindex2
from yoloutils.index import generate_and_overlay_mask
from results import ResultScreen
import os

Window.size = (350, 600)
dirname = os.path.dirname(__file__)

class ProcessYOLO(Screen):
    def __init__(self, selected_images=None, **kwargs):
        super().__init__(**kwargs)
        self.selected_images = selected_images
        self.classification_results = None

    def start_yolo(self):
        counter = 0
        results = []

        if(len(self.selected_images) > 0):
            for path in self.selected_images:
                counter += 1
                output_path = f"{dirname}\\results\\result{counter}.png"
                results.append(output_path)
                generate_and_overlay_mask(path, output_path)
            self.classification_results = olivindex2(results)
            self.show_results()

    def show_results(self):
        result_screen = ResultScreen(results=self.classification_results)
        result_screen.show_results()