from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.filechooser import FileChooserIconView

class SignUpScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.screen.ids.text_field_error.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )

        return self.screen

    def set_error_message(self, instance_textfield):
        self.screen.ids.text_field_error.error = True

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()
        date_dialog.bind(on_save=self.on_save)

    def on_save(self, instance, value, date_range):
        self.ids.data_nascimento.text = value.strftime("%d/%m/%Y")

    def sign_up(self):
        # TODO: verificar se campos estão preenchidos e são válidos
        nome = self.ids.nome.text.strip()
        email = self.ids.email.text.strip()
        data_nascimento = self.ids.data_nascimento.text.strip()
        senha = self.ids.senha.text.strip()
        # TODO: implementar lógica de sign up com o API do backend
        self.manager.current = "login_screen"