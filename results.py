from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.app import App
from kivy.lang import Builder

class ResultScreen(Screen):
    def __init__(self, results=None, **kwargs):
        super().__init__(**kwargs)
        self.results = results
        self.result_screen = Builder.load_file("views/results.kv")
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.add_widget(self.result_screen)
        self.show_results()

    def show_results(self):
        if self.results:
            app = App.get_running_app()
            print("RESULTS DA TELA RESULTS >>> ", self.results)
            
            percentAmostras = self.results.get('percentAmostras', [])
            self.result_screen.ids['N0'].text = "N0: "+str(percentAmostras[0])
            print(self.result_screen.ids['N0'].text)
            app.root.current = "results"