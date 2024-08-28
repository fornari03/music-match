from kivymd.app import MDApp
from kivy.lang import Builder
from screens.layouts import KV
from screens.login import *
from screens.home import *
from screens.sign_up import *

class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Modo escuro
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV)

if __name__ == "__main__":
    App().run()