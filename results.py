from kivy.uix.screenmanager import Screen
from kivy.app import App
import logging

from kivymd.uix.label import MDLabel


class ResultScreen(Screen):
    def __init__(self, result_data=None, **kwargs):
        super().__init__(**kwargs)
        self.result_data = result_data
        self.display_results()

    def display_results(self):
        if self.result_data:
            app = App.get_running_app()
            results_screen = app.root.get_screen("results")
            results_container = results_screen.ids["results_container"]

            logging.info("Displaying results:", self.result_data)

            maturity_index = self.result_data.get('indiceMaturacao')
            total_samples = self.result_data.get('totalAmostras')

            results_screen.ids["maturity_index"].text = "Índice de Maturação: {}".format(maturity_index)
            results_screen.ids["total_samples"].text = "Total de Amostras: {}".format(total_samples)

            result_labels = self.create_result_labels()
            for label in result_labels:
                results_container.add_widget(label, 3)

            app.root.current = "results"

    def create_result_labels(self):
        result_labels = []

        for index, value in enumerate(self.result_data.get('percentAmostras', [])):
            label = MDLabel(text=f"N{index + 1}: {value}")
            label.id = f"N{index}"
            result_labels.append(label)

        return result_labels
