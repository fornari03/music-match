from kivymd.uix.screen import MDScreen

class LoginScreen(MDScreen):
    def login(self):
        # TODO: implementar lógica de login com o API do backend
        self.manager.current = "home_screen"

    def sign_up(self):
        self.manager.current = "sign_up_screen"