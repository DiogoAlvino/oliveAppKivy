from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screenmanager import MDScreenManager
from menu import MenuScreen
from sampling import SamplingScreen
from loading import LoadingScreen
from results import ResultScreen
from settings import SettingScreen
from kivy.core.window import Window


Window.size = (350, 600)


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.screen_manager = MDScreenManager(transition=NoTransition())

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        self.title = "Olive App"

        self.screen_manager.add_widget(MenuScreen())
        self.screen_manager.add_widget(SamplingScreen())
        self.screen_manager.add_widget(LoadingScreen())
        self.screen_manager.add_widget(ResultScreen())
        self.screen_manager.add_widget(SettingScreen())

        return self.screen_manager

    def go_to_menu(self):
        self.screen_manager.current = "menu"


if __name__ == '__main__':
    LabelBase.register(name='Rawline_Bold', fn_regular='./assets/rawline-700.ttf')
    MainApp().run()
