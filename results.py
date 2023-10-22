from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.app import App
from kivy.lang import Builder

class ResultScreen(Screen):
    def __init__(self, results=None, **kwargs):
        super().__init__(**kwargs)
        self.result_screen = Builder.load_file("views/results.kv")
        self.add_widget(self.result_screen)
        self.results = results

    def show_results(self):
        if self.results:
            app = App.get_running_app()
            app.root.current = "results"
            print("RESULTS DA TELA RESULTS >>> ", self.results)
