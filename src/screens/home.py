from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDRoundFlatIconButton, MDIconButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList
import webbrowser

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_icons = {}
        self.showing_users_connected = True
        self.showing_evaluated_musics = True

    ############################## Tela de Início ##############################

    def on_pre_enter(self):
        """Método de entrada da tela de início, chamado antes da tela ser exibida. Deve receber todas as informações que serão mostradas nas telas de início, eventos, conexões e perfil."""
        # TODO: implementar lógica de receber todas as músicas ainda não avaliadas com a API do backend (ordem aleatoria)
        # TODO: implementar lógica de receber os dados do usuário que fez o login com a API do backend
        # TODO: implementar lógica de receber os usuários conectados com a API do backend
        # TODO: implementar lógica de receber os usuários não conectados com a API do backend

        self.evaluated = [
            {"id": 4, "capa": "https://via.placeholder.com/150", "titulo": "musica 4", "artista": "artista 4", "genero": "MPB", "spotify_link": "https://open.spotify.com"},
            {"id": 5, "capa": "https://via.placeholder.com/150", "titulo": "musica 5", "artista": "artista 5", "genero": "Pop", "spotify_link": "https://open.spotify.com"},
            {"id": 6, "capa": "https://via.placeholder.com/150", "titulo": "musica 6", "artista": "artista 6", "genero": "Rock", "spotify_link": "https://open.spotify.com"},
        ]

        self.not_evaluated = [
            {"id": 1, "capa": "https://via.placeholder.com/150", "titulo": "musica 1", "artista": "artista 1", "genero": "MPB", "spotify_link": "https://open.spotify.com/intl-pt/track/3eW8Di8rolVzktc3xW7hba?si=156bacc4d77c4f1c"},
            {"id": 2, "capa": "https://via.placeholder.com/150", "titulo": "musica 2", "artista": "artista 2", "genero": "Pop", "spotify_link": "https://open.spotify.com"},
            {"id": 3, "capa": "https://via.placeholder.com/150", "titulo": "musica 3", "artista": "artista 3", "genero": "Rock", "spotify_link": "https://open.spotify.com"},
        ]

        self.changed_evaluation = {}       # dicionario de músicas que sofreram alteração na avaliação no formato id_musica: 'CHAR_AVALIACAO'

        self.show_music_list()

        self.connected = [
            {"id": 2, "name": "João Silva", "social_media": ["Instagram: @joaosilva", "Twitter: @jsilva12", "Facebook: /joaosilvaa"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 87, "artists": ["artista 1", "artista 2", "artista 3"]},
            {"id": 3, "name": "Maria Souza", "social_media": ["Twitter: @mariasouza"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 75, "artists": ["artista 1", "artista 2", "artista 3"]},
            {"id": 4, "name": "Pedro Oliveira", "social_media": ["Facebook: /pedro.oliveira"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 65, "artists": ["artista 1", "artista 2", "artista 3"]},
        ]

        self.not_connected = [
            {"id": 5, "name": "Henrique Vale", "social_media": ["Facebook: /h.valee"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 12, "artists": ["artista 1", "artista 2", "artista 3"]},
        ]
        self.show_grid()

    def add_music_item(self, music):
        item = TwoLineAvatarIconListItem(text=f"{music['titulo']} - {music['genero']}", secondary_text=f"{music['artista']}")
        
        capa = ImageLeftWidget(source=music['capa'])
        item.add_widget(capa)
        
        like_icon = IconRightWidget(icon="thumb-up-outline")

        dislike_icon = IconRightWidget(icon="thumb-down-outline")

        like_icon.on_release = lambda: self.like_music(like_icon, dislike_icon, music['id'])
        item.add_widget(like_icon)
        
        dislike_icon.on_release = lambda: self.dislike_music(dislike_icon, like_icon, music['id'])
        item.add_widget(dislike_icon)

        self.music_icons[music['id']] = {
            'like': like_icon,
            'dislike': dislike_icon
        }
        
        # abre o spotify na musica clicada
        item.on_release = lambda: webbrowser.open(music['spotify_link'])
        
        self.ids.music_list.add_widget(item)


    def like_music(self, like_icon, dislike_icon, music_id):
        if like_icon.icon == "thumb-up":
            like_icon.icon = "thumb-up-outline"
            self.changed_evaluation[music_id] = 'N'
        else:
            like_icon.icon = "thumb-up"
            self.changed_evaluation[music_id] = 'L'
        dislike_icon.icon = "thumb-down-outline"

    def dislike_music(self, dislike_icon, like_icon, music_id):
        if dislike_icon.icon == "thumb-down":
            dislike_icon.icon = "thumb-down-outline"
            self.changed_evaluation[music_id] = 'N'
        else:
            dislike_icon.icon = "thumb-down"
            self.changed_evaluation[music_id] = 'D'
        like_icon.icon = "thumb-up-outline"


    def show_music_list(self, search_string=None):
        self.ids.music_list.clear_widgets()
        if not self.showing_evaluated_musics:
            for music in self.not_evaluated:
                if search_string is None or search_string.lower().strip() in music['titulo'].lower().strip() or search_string.lower().strip() in music['artista'] or search_string.lower().strip() in music['genero'] or search_string.lower().strip() == "":
                    self.add_music_item(music)

        else:
            for music in self.evaluated:
                if search_string is None or search_string.lower().strip() in music['titulo'].lower().strip() or search_string.lower().strip() in music['artista'] or search_string.lower().strip() in music['genero'] or search_string.lower().strip() == "":
                    self.add_music_item(music)

    def switch_musics_view(self):
        self.showing_evaluated_musics = not self.showing_evaluated_musics
        self.show_music_list()

    def show_musics_search(self):
        self.dialog = MDDialog(
            title="Buscar Música",
            type="custom",
            content_cls=
                MDBoxLayout(
                    MDTextField(id="barra_pesquisa", hint_text="Nome da Música"),
                    MDRaisedButton(text="Buscar", on_release=lambda x: self.search_music(self.dialog.content_cls.children[1].text.strip())),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp"
                )        
        )
        self.dialog.open()

    def search_music(self, search_string):
        self.show_music_list(search_string)
        self.dialog.dismiss()

    def save_evaluations(self):
        # TODO: ver se vale a pena verificar se houve alguma alteração de fato
        self.dialog = MDDialog(
            text="Salvar avaliações?",
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Salvar",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.confirm_save())]
        )
        self.dialog.open()

    def confirm_save(self):
        # TODO: implementar lógica de salvar alterações das avaliações com o API do backend
        # TODO: bloquear a interface por um tempo até receber tudo do banco de dados de novo
        self.dialog.dismiss()
        self.show_music_list()
        print(self.changed_evaluation)      # dicionario com alterações de avaliação no formato id_musica: 'CHAR_AVALIAÇÃO'


    ############################## Tela de Eventos ##############################


    ############################## Tela de Conexões ##############################

    def add_connection_banner(self, connection, status):
        banner = MDCard(orientation="vertical", size_hint=(0.5, None), size=(300, 200), md_bg_color=(0.2, 0.22, 0.2, 1), radius=[15], padding=[10], spacing=300, on_release=lambda x: self.open_profile(connection))

        box_layout = MDBoxLayout(orientation="vertical", padding=[10], spacing=10)

        box_layout.add_widget(MDLabel(text=connection['name'], size_hint=(None, 0.1)))

        box_layout.add_widget(MDLabel(text="    //    ".join(connection['social_media']), size_hint=(0.9, 0.2)))

        box_layout.add_widget(MDLabel(text=f"Gosto musical: {', '.join([': '.join([genero, str(perc)+'%']) for [genero, perc] in connection['musical_taste']])}", size_hint=(0.9, 0.1)))

        box_layout.add_widget(MDLabel(text=f"Artistas: {', '.join(connection['artists'])}", size_hint=(0.9, 0.2)))

        box_layout.add_widget(MDLabel(text=f"Music Match: {connection['music_match']}%", size_hint=(0.3, 0.1)))

        if status == "connected":
            disconnectButton = MDRoundFlatIconButton(text="Desconectar", size_hint=(0.25, None), icon="account-minus", icon_color="red", text_color="red", line_color="red")
            disconnectButton.on_release = lambda: self.remove_connection(banner)
        else:
            disconnectButton = MDRoundFlatIconButton(text="Conectar", size_hint=(0.25, None), icon="account-plus", icon_color="green", text_color="green", line_color="green")
            disconnectButton.on_release = lambda: self.add_connection(banner)

        box_layout.add_widget(disconnectButton)

        banner.add_widget(box_layout)

        self.ids.connections_grid.add_widget(banner)

    def remove_connection(self, banner):
        for i in range(len(self.ids.connections_grid.children)-1, -1, -1):
            if self.ids.connections_grid.children[i] == banner:
                self.dialog = MDDialog(
                    text=f"Deseja se desconectar de {banner.children[0].children[4].text}?",
                    buttons=[
                        MDFlatButton(
                            text="Cancelar",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.dialog.dismiss()
                        ),
                        MDFlatButton(
                            text="Desconectar",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.confirm_disconect(i))])
                
                self.dialog.open()
                break

    def confirm_disconect(self, idx):
        """Método que apaga o MDCard da conexão com o usuário de índice idx no grid."""
        self.dialog.dismiss()
        self.ids.connections_grid.remove_widget(self.ids.connections_grid.children[idx])
        idx = len(self.connected) - idx - 1
        user = self.connected[idx]
        self.not_connected.append(user)
        self.connected.pop(idx)
        self.show_grid()
        # TODO: implementar lógica de remoção de conexão com o API do backend

    def add_connection(self, banner):
        for i in range(len(self.ids.connections_grid.children)-1, -1, -1):
            if self.ids.connections_grid.children[i] == banner:
                self.dialog = MDDialog(
                    text=f"Deseja se conectar com {banner.children[0].children[4].text}?",
                    buttons=[
                        MDFlatButton(
                            text="Cancelar",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.dialog.dismiss()
                        ),
                        MDFlatButton(
                            text="Conectar",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.confirm_connect(i))])
                
                self.dialog.open()
                break

    def confirm_connect(self, idx):
        """Método que adiciona o MDCard da conexão com o usuário de índice idx no grid."""
        self.dialog.dismiss()
        self.ids.connections_grid.remove_widget(self.ids.connections_grid.children[idx])
        idx = len(self.not_connected) - idx - 1
        user = self.not_connected[idx]
        self.connected.append(user)
        self.not_connected.pop(idx)
        self.show_grid()
        # TODO: implementar lógica de adição de conexão com o API do backend

    def open_profile(self, user):
        # TODO: verificar se é plausível abrir o perfil do usuário em um dialog ou outra tela
        # self.dialog = MDDialog(
        #         title="Ver Perfil",
        #         type="custom",
        #         size_hint=(0.8, 0.8),
        #         content_cls=
        #             MDBoxLayout(
        #                 MDLabel(text=user['name']),
        #                 MDLabel(text="    //    ".join(user['social_media'])),
        #                 MDLabel(text=f"Gosto musical: {', '.join([': '.join([genero, str(perc)+'%']) for [genero, perc] in user['musical_taste']])}"),
        #                 MDLabel(text=f"Music Match: {user['music_match']}%"),
        #                 orientation="vertical",
        #                 padding=[10],
        #                 spacing=10,
        #                 size_hint=(0.8, 0.8)
        #             )        
        #     )
        # self.dialog.open()
        pass

    def show_grid(self, search_string=None):
        # TODO: melhorar algoritmo de mostrar usuários conectados e não conectados,
        # calcular e ordenar por music_match
        self.ids.connections_grid.clear_widgets()
        if self.showing_users_connected:
            for connection in self.connected:
                if search_string is None or search_string.lower().strip() in connection['name'].lower().strip() or search_string.lower().strip() in connection['social_media'] or search_string.lower().strip() == "":
                    self.add_connection_banner(connection, "connected")
        else:
            for connection in self.not_connected:
                if search_string is None or search_string.lower().strip() in connection['name'].lower().strip() or search_string.lower().strip() in connection['social_media'] or search_string.lower().strip() == "":
                    self.add_connection_banner(connection, "not_connected")

    def switch_users_view(self):
        self.showing_users_connected = not self.showing_users_connected
        self.show_grid()

    def show_users_search(self):
        self.dialog = MDDialog(
            title="Buscar Usuário",
            type="custom",
            content_cls=
                MDBoxLayout(
                    MDTextField(id="barra_pesquisa", hint_text="Nome do Usuário"),
                    MDRaisedButton(text="Buscar", on_release=lambda x: self.search_user(self.dialog.content_cls.children[1].text.strip())),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp"
                )        
        )
        self.dialog.open()

    def search_user(self, search_string):
        self.show_grid(search_string)
        self.dialog.dismiss()

    ############################## Tela de Perfil ##############################

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()
        date_dialog.bind(on_save=self.on_save)

    def on_save(self, instance, value, date_range):
        self.ids.data_nascimento.text = value.strftime("%d/%m/%Y")

    def save(self):
        # TODO: verificar se campos estão preenchidos e são válidos
        nome = self.ids.nome.text.strip()
        email = self.ids.email.text.strip()
        data_nascimento = self.ids.data_nascimento.text.strip()
        senha = self.ids.senha.text.strip()
        lista_redes_sociais = [(child.children[0].hint_text.strip(), child.children[0].text.strip()) for child in self.ids.lista_opcoes.children if child.children[1].active and child.children[0].text.strip() != ""] # lista de tuplas (nome_rede_social, usuario) habilitados e preenchidos
        # TODO: implementar lógica de edição dos dados com o API do backend
        pass

    def delete_account(self):
        self.dialog = MDDialog(
            text="Deseja excluir sua conta?",
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Excluir",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.confirm_delete())]
        )
        self.dialog.open()

    def confirm_delete(self):
        self.dialog.dismiss()
        self.dialog = MDDialog(
            text="Conta excluída com sucesso!",
            buttons=[
                MDFlatButton(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                )]
        )
        self.dialog.open()
        self.ids.home_screen_bottom_nav.switch_tab("inicio")
        self.manager.current = "login_screen"
        # TODO: implementar lógica de exclusão de conta com o API do backend

    def set_profile_pic(self):
        # TODO: possibilitar abrir arquivos de imagem do dispositivo
        pass

    def add_social_media_item(self, social_media: str):
        new_item = OneLineIconListItem(on_press=lambda x: self.checkbox_selected(len(self.ids.lista_opcoes.children)))
        
        new_item.add_widget(MDCheckbox(size_hint_x=None, pos_hint={"center_y": 0.5}))
        new_item.add_widget(MDTextField(hint_text=social_media, size_hint_x=0.6, pos_hint={"center_y": 0.5, "center_x": 0.5}))
        
        self.ids.lista_opcoes.add_widget(new_item)

        self.ids.nova_rede_social.text = ""

    def checkbox_selected(self, item_id):
        pass