from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from sampling import SamplingScreen
from kivy.core.window import Window

Window.size = (350, 600)

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.title = "Olive App"
        
        self.screen_manager = ScreenManager(transition=NoTransition())
        
        self.menu_screen = Builder.load_file("views/menu.kv")
        menu = Screen(name="menu")
        menu.add_widget(self.menu_screen)
        self.screen_manager.add_widget(menu)
        
        novas_amostragens = SamplingScreen(name="sampling")
        self.screen_manager.add_widget(novas_amostragens)

        return self.screen_manager

    def on_start(self):
        super().on_start()

if __name__ == '__main__':
    LabelBase.register(name='Rawline_Bold', fn_regular='./assets/rawline-700.ttf')
    MainApp().run()