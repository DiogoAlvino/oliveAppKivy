from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooser
from kivy.uix.popup import Popup
import base64

Window.size = (350, 600)

class SamplingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_screen = Builder.load_file("views/sampling.kv")
        self.screen_manager = ScreenManager()
        self.add_widget(self.menu_screen)
    """
    def open_image_dialog(self):
        file_chooser = FileChooser(filters=["*.jpg", "*.jpeg", "*.png"])
        file_chooser.bind(on_submit=self.load_image)

        popup = Popup(title="Escolha uma imagem", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_image(self, instance, value):
        selected_file = value[0]
        # Verifique se um arquivo foi selecionado
        if selected_file:
            with open(selected_file, "rb") as file:
                # Leia o conteúdo do arquivo
                image_data = file.read()
                
                # Codifique o conteúdo em base64
                base64_data = base64.b64encode(image_data).decode("utf-8")
                
                # Imprima o resultado em base64 no console
                print(base64_data)
    """