from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from plyer import filechooser
from yoloutils.index import generate_and_overlay_mask
import os
from scripts.oliveClassification import olivindex2
from kivy.app import App
from processYOLO import ProcessYOLO

Window.size = (350, 600)
dirname = os.path.dirname(__file__)

class SamplingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sampling_screen = Builder.load_file("views/sampling.kv")
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.add_widget(self.sampling_screen)
        self.selected_images = []

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected_image, multiple=True, filters=[("Comma-separated Values", "*.png", "*.jpeg", "*.jpg")])

    def selected_image(self, image):
        self.selected_images.extend(image)
        print(self.selected_images)
    
    def create_batch(self):
        if self.validate_batch():
            process_yolo = ProcessYOLO(selected_images=self.selected_images, name="processYOLO")
            self.screen_manager.add_widget(process_yolo)
            self.screen_manager.current = "processYOLO"
            return self.screen_manager

    def validate_input(self, user_input, elementID):
        element = self.sampling_screen.ids[elementID]
        if(not user_input):
            print(elementID)
            element.required = True
            return False
        
        element.required = False
        return True
    
    def validate_batch(self):
        nome_lote = self.sampling_screen.ids.nome_lote.text
        num_amostras = self.sampling_screen.ids.num_amostras.text
        padrao_cor = self.sampling_screen.ids.padrao_cor.text
        modelo_preditivo = self.sampling_screen.ids.modelo_preditivo.text
        informacoes = self.sampling_screen.ids.informacoes.text
        numero_imagens = len(self.selected_images)

        if not self.validate_input(nome_lote, "nome_lote"):
            return False

        if not self.validate_input(num_amostras, "num_amostras"):
            return False

        if not self.validate_input(padrao_cor, "padrao_cor"):
            return False

        if not self.validate_input(modelo_preditivo, "modelo_preditivo"):
            return False

        if numero_imagens < int(num_amostras):
            self.sampling_screen.ids.num_amostras.helper_text = "Quantidade de imagens inferior a de amostras"
            self.sampling_screen.ids.num_amostras.helper_text_mode = "persistent"
            return False
        
        return True