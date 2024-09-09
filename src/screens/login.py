from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog

from src.models.usuario import Usuario

class LoginScreen(MDScreen):
    def login(self):
        global usuario_logado
        usuario_logado = Usuario.where({"email": email})

        email = self.ids.email.text
        senha = self.ids.senha.text
        if usuario_logado == False:
            self.dialog = MDDialog(title="Erro", text="Email não cadastrado", size_hint=(0.7, 0.2))
            self.dialog.open()
            self.ids.email.text = ""
            self.ids.senha.text = ""
        else:
            if usuario_logado[0].senha != senha:
                self.dialog = MDDialog(title="Erro", text="Senha incorreta", size_hint=(0.7, 0.2))
                self.dialog.open()
                self.ids.senha.text = ""
            else:
                self.manager.current = "home_screen"

    def sign_up(self):
        self.manager.current = "sign_up_screen"