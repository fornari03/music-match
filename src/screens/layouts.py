KV = '''
#: import WipeTransition kivy.uix.screenmanager.WipeTransition


MDScreenManager:
    LoginScreen:
    HomeScreen:
    SignUpScreen:

<LoginScreen>:
    name: "login_screen"
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(40)
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(5)
            MDLabel:
                text: "TuneLink"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (1, 0, 1, 1)
                font_style: "H2"
            MDLabel:
                text: "Conecte-se pela música!"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (1, 0, 1, 1)
                font_size: "20sp"
        MDLabel:
            text: "Login"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (1, 0, 1, 1)
            font_style: "H4"
        MDTextField:
            id: email
            hint_text: "Email"
            icon_right: "email"
            mode: "rectangle"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: senha
            hint_text: "Senha"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
        MDRaisedButton:
            text: "Login"
            md_bg_color: (1, 0, 1, 1)
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            on_release: 
                root.manager.transition = WipeTransition()
                root.login()
        MDTextButton:
            text: "Sign Up"
            theme_text_color: "Custom"
            text_color: (1, 0, 1, 1)
            pos_hint: {"center_x": 0.5}
            on_release: 
                root.manager.transition = WipeTransition()
                root.sign_up()

<HomeScreen>:
    name: "home_screen"
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: 'inicio'
            text: 'Início'
            icon: 'music-circle'
            MDScrollView:
                MDList:
                    id: music_list

        MDBottomNavigationItem:
            name: 'buscar'
            text: 'Buscar'
            icon: 'magnify'
            MDLabel:
                text: "Buscar"
                halign: "center"

        MDBottomNavigationItem:
            name: 'eventos'
            text: 'Eventos'
            icon: 'calendar-month'
            MDLabel:
                text: "Eventos"
                halign: "center"

        MDBottomNavigationItem:
            name: 'conexoes'
            text: 'Conexões'
            icon: 'account-group'
            MDLabel:
                text: "Conexões"
                halign: "center"

        MDBottomNavigationItem:
            name: 'perfil'
            text: 'Perfil'
            icon: 'account'
            MDLabel:
                text: "Perfil"
                halign: "center"

<SignUpScreen>:
    name: "sign_up_screen"
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(40)
        
        MDLabel:
            text: "Crie sua conta"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (1, 0, 1, 1)
            font_style: "H4"
        
        MDTextField:
            id: nome
            hint_text: "Nome"
            icon_right: "account"
            mode: "rectangle"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}

        MDTextField:
            id: email
            hint_text: "Email"
            icon_right: "email"
            mode: "rectangle"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}

        MDTextField:
            id: nascimento
            hint_text: "Data de Nascimento"
            icon_right: "calendar"
            mode: "rectangle"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            on_focus: if self.focus: root.show_date_picker()

        MDTextField:
            id: senha
            hint_text: "Senha"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Adicionar Foto de Perfil"
            md_bg_color: (1, 0, 1, 1)
            size_hint_x: 0.3
            pos_hint: {"center_x": 0.5}
            on_release: root.set_profile_pic()

        MDRaisedButton:
            text: "Cadastrar"
            md_bg_color: (1, 0, 1, 1)
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            on_release: root.sign_up()    
'''