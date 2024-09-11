from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog

from src.models.usuario import Usuario
from ..utils.encrypt import encrypt_password

class LoginScreen(MDScreen):
    def login(self):
        """
        Realiza o login do usuário
        """
        global usuario_logado

        email = self.ids.email.text
        senha = encrypt_password(self.ids.senha.text)

        usuario_logado = Usuario.where({"email": f"'{email}'"})
        if usuario_logado == False or len(usuario_logado) == 0:
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
                usuario_logado = usuario_logado[0]
                self.manager.current = "home_screen"

    def sign_up(self):
        """
        Troca para a tela de cadastro
        """
        self.manager.current = "sign_up_screen"