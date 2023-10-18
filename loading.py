from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_screen = Builder.load_file("views/loading.kv")
        self.add_widget(self.loading_screen)
