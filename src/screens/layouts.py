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
        id: home_screen_bottom_nav
        MDBottomNavigationItem:
            name: 'inicio'
            text: 'Início'
            icon: 'music-circle'
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0,0,0,10]
                MDTopAppBar:
                    title: "Músicas"
                    md_bg_color: (1, 0, 1, 1)
                    left_action_items: [["order-bool-ascending", lambda x: root.switch_musics_view()]]
                    right_action_items: [["magnify", lambda x: root.show_musics_search()]]
                MDScrollView:
                    MDList:
                        id: music_list
                MDRaisedButton:
                    text: "Salvar"
                    md_bg_color: (0.31, 0.78, 0.47, 1)
                    size_hint_x: None
                    width: 300
                    pos_hint: {"center_x": 0.5}
                    on_release: root.save_evaluations()
                    

        MDBottomNavigationItem:
            name: 'eventos'
            text: 'Eventos'
            icon: 'calendar-month'
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(0)
                MDTopAppBar:
                    title: "Eventos"
                    md_bg_color: (1, 0, 1, 1)
                    left_action_items: [["calendar-clock", lambda x: root.switch_events_view()]]
                    right_action_items: [["magnify", lambda x: root.show_events_search()]]

                MDScrollView:
                    MDGridLayout:
                        id: events_grid
                        cols: 1
                        row_default_height: dp(260)
                        row_force_default: True
                        spacing: dp(80)
                        padding: dp(50)
                        size_hint_y: None
                        height: self.minimum_height
                        adaptive_height: True

        MDBottomNavigationItem:
            name: 'conexoes'
            text: 'Conexões'
            icon: 'account-group'
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(0)
                MDTopAppBar:
                    title: "Conexões"
                    md_bg_color: (1, 0, 1, 1)
                    left_action_items: [["order-bool-ascending", lambda x: root.switch_users_view()]]
                    right_action_items: [["magnify", lambda x: root.show_users_search()]]

                MDScrollView:
                    MDGridLayout:
                        id: connections_grid
                        cols: 1
                        row_default_height: dp(150)
                        row_force_default: True
                        spacing: dp(80)
                        padding: dp(50)
                        size_hint_y: None
                        height: self.minimum_height
                        adaptive_height: True

        MDBottomNavigationItem:
            name: 'perfil'
            text: 'Perfil'
            icon: 'account'
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                padding: dp(20)
                MDLabel:
                    text: "Seu perfil"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: (1, 0, 1, 1)
                    font_style: "H4"
                MDGridLayout:
                    cols: 2
                    row_default_height: dp(60)
                    row_force_default: True
                    spacing: dp(20)
                    padding: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    adaptive_height: True
                    MDTextField:
                        id: nome
                        hint_text: "Nome"
                        icon_right: "account"
                        mode: "rectangle"
                        size_hint_x: 0.4
                        pos_hint: {"center_x": 0.5}
                    MDTextField:
                        id: email
                        hint_text: "Email"
                        icon_right: "email"
                        mode: "rectangle"
                        size_hint_x: 0.4
                        pos_hint: {"center_x": 0.5}
                    MDTextField:
                        id: data_nascimento
                        hint_text: "Data de Nascimento"
                        icon_right: "calendar"
                        mode: "rectangle"
                        size_hint_x: 0.4
                        pos_hint: {"center_x": 0.5}
                        on_focus: if self.focus: root.show_date_picker()
                    MDTextField:
                        id: senha
                        hint_text: "Senha"
                        icon_right: "lock"
                        password: True
                        mode: "rectangle"
                        size_hint_x: 0.4
                        pos_hint: {"center_x": 0.5}
                MDScrollView:
                    MDList:
                        id: lista_opcoes
                        OneLineIconListItem:
                            on_press: root.checkbox_selected(1)
                            MDCheckbox:
                                id: checkbox_1
                                size_hint_x: None
                                pos_hint: {"center_y": 0.5}
                            MDTextField:
                                hint_text: "Facebook"
                                size_hint_x: 0.6
                                pos_hint: {"center_y": 0.5, "center_x": 0.5}
                        OneLineIconListItem:
                            on_press: root.checkbox_selected(2)
                            MDCheckbox:
                                id: checkbox_2
                                size_hint_x: None
                                pos_hint: {"center_y": 0.5}
                            MDTextField:
                                hint_text: "Instagram"
                                size_hint_x: 0.6
                                pos_hint: {"center_y": 0.5, "center_x": 0.5}
                        OneLineIconListItem:
                            on_press: root.checkbox_selected(3)
                            MDCheckbox:
                                id: checkbox_3
                                size_hint_x: None
                                pos_hint: {"center_y": 0.5}
                            MDTextField:
                                hint_text: "Twitter"
                                size_hint_x: 0.6
                                pos_hint: {"center_y": 0.5, "center_x": 0.5}
                MDGridLayout:
                    cols: 3
                    spacing: dp(20)
                    padding: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    adaptive_height: True
                    MDRaisedButton:
                        text: "Adicionar Nova Rede"
                        on_release: root.add_social_media_item(root.ids.nova_rede_social.text)
                        size_hint_x: 0.1
                        pos_hint: {"center_x": 0.15}
                    MDTextField:
                        id: nova_rede_social
                        hint_text: "Nome da rede social"
                        size_hint_x: 0.6
                        pos_hint: {"center_x": 0.85}
                    MDLabel:
                        text: "" # gambiarra total para ajustar o layout
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(180)
                    padding: [dp(200), dp(30), dp(200), dp(20)]
                    pos_hint: {"center_y": 0.5}
                    MDRaisedButton:
                        text: "Salvar"
                        md_bg_color: (0.31, 0.78, 0.47, 1)
                        size_hint_x: None
                        width: 300
                        pos_hint: {"center_x": 0.5}
                        on_release: root.save()
                    MDRaisedButton:
                        text: "Excluir conta"
                        md_bg_color: (1, 0, 0, 1)
                        size_hint_x: None
                        width: 300
                        pos_hint: {"center_x": 0.5}
                        on_release: root.delete_account()


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
            id: data_nascimento
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
            text: "Cadastrar"
            md_bg_color: (1, 0, 1, 1)
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}
            on_release: root.sign_up()    
'''