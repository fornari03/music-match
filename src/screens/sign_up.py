from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.filechooser import FileChooserIconView
from src.models.usuario import Usuario
from src.utils.popup import show_popup
from re import match

class SignUpScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()
        date_dialog.bind(on_save=self.on_save)

    def on_save(self, instance, value, date_range):
        self.ids.data_nascimento.text = value.strftime("%d/%m/%Y")

    def sign_up(self):
        nome = self.ids.nome.text.strip()
        email = self.ids.email.text.strip()
        data_nascimento = self.ids.data_nascimento.text.strip()
        senha = self.ids.senha.text.strip()

        # Verificar se os campos estão preenchidos
        if not nome or not email or not data_nascimento or not senha:
            show_popup("Campo vazio", "Todos os campos devem ser preenchidos!")
            return

        # Verificar o nome (máximo 10 caracteres)
        if len(nome) > 10:
            show_popup("Limite de caracteres atingido", "O nome deve ter no máximo 10 caracteres!")
            return

        # Validar email (expressão regular para verificar formato)
        if not match(r"[^@]+@[^@]+\.[^@]+", email):
            show_popup("Email inválido", "Insira um email válido!")
            return

        # Verificar a data de nascimento
        if len(data_nascimento) < 8:  
            show_popup("Data de nascimento inválida", "Insira uma Data de nascimento válida!")
            return

        # Verificar senha (mínimo 6 caracteres e máximo de 10)
        if len(senha) < 6 or len(senha) > 10:
            show_popup("Senha inválida", "A senha deve ter entre 6 e 10 caracteres!")
            return

        data = {
                'nome': nome,
                'email': email,
                'data_nascimento': data_nascimento,
                'senha': senha
                }
        
        user = Usuario()
        verify_email = user.where({'email':data['email']})
        
        if verify_email == -1:
            show_popup("Erro no banco de dados", "Erro ao salvar os dados, tente novamente!")
            return

        if len(verify_email) > 0:
            show_popup("Erro: Email já cadastrado", "O email informado já foi cadastrado anteriormente!")
            return
        
        user.change_values(data)
        if user.save() != -1:
            show_popup("Sucesso", "Cadastro realizado com sucesso!")
            self.manager.current = "login_screen"
        else:
            show_popup("Erro no banco de dados", "Erro ao salvar os dados, tente novamente!")