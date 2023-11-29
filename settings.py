from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

Window.size = (350, 600)


class SettingScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
