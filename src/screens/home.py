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
import webbrowser

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_icons = {}

    ############################## Tela de Início ##############################

    def on_pre_enter(self):
        """Método de entrada da tela de início, chamado antes da tela ser exibida. Deve receber todas as informações que serão mostradas nas telas de início, eventos, conexões e perfil."""

        # TODO: implementar lógica de receber todas as músicas ainda não avaliadas com a API do backend (ordem aleatoria)
        # TODO: implementar lógica de receber os dados do usuário que fez o login com a API do backend

        musics_example = [
            {"id": 1, "capa": "https://via.placeholder.com/150", "titulo": "musica 1", "artista": "artista 1", "genero": "MPB", "spotify_link": "https://open.spotify.com/intl-pt/track/3eW8Di8rolVzktc3xW7hba?si=156bacc4d77c4f1c"},
            {"id": 2, "capa": "https://via.placeholder.com/150", "titulo": "musica 2", "artista": "artista 2", "genero": "Pop", "spotify_link": "https://open.spotify.com"},
            {"id": 3, "capa": "https://via.placeholder.com/150", "titulo": "musica 3", "artista": "artista 3", "genero": "Rock", "spotify_link": "https://open.spotify.com"},
        ]
        
        for music in musics_example:
            self.add_music_item(music)

        connections = [
            {"id": 2, "name": "João Silva", "social_media": ["Instagram: @joaosilva", "Twitter: @jsilva12", "Facebook: /joaosilvaa"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 87},
            {"id": 3, "name": "Maria Souza", "social_media": ["Twitter: @mariasouza"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 75},
            {"id": 4, "name": "Pedro Oliveira", "social_media": ["Facebook: /pedro.oliveira"], "musical_taste": [["Pop", 43], ["Rock", 33], ["Jazz", 11]], "music_match": 65}
        ]

        for connection in connections:
            self.add_connection_banner(connection)

    def add_music_item(self, music):
        item = TwoLineAvatarIconListItem(text=f"{music['titulo']} - {music['genero']}", secondary_text=f"{music['artista']}")
        
        capa = ImageLeftWidget(source=music['capa'])
        item.add_widget(capa)
        
        like_icon = IconRightWidget(icon="thumb-up-outline")

        dislike_icon = IconRightWidget(icon="thumb-down-outline")

        like_icon.on_release = lambda: self.like_music(like_icon, dislike_icon)
        item.add_widget(like_icon)
        
        dislike_icon.on_release = lambda: self.dislike_music(dislike_icon, like_icon)
        item.add_widget(dislike_icon)

        self.music_icons[music['id']] = {
            'like': like_icon,
            'dislike': dislike_icon
        }
        
        # abre o spotify na musica clicada
        item.on_release = lambda: webbrowser.open(music['spotify_link'])
        
        self.ids.music_list.add_widget(item)


    def like_music(self, like_icon, dislike_icon):
        if like_icon.icon == "thumb-up":
            like_icon.icon = "thumb-up-outline"
        else:
            like_icon.icon = "thumb-up"
        dislike_icon.icon = "thumb-down-outline"
        # TODO: implementar lógica de avaliação com a API do backend

    def dislike_music(self, dislike_icon, like_icon):
        if dislike_icon.icon == "thumb-down":
            dislike_icon.icon = "thumb-down-outline"
        else:
            dislike_icon.icon = "thumb-down"
        like_icon.icon = "thumb-up-outline"
        # TODO: implementar lógica de avaliação com a API do backend


    ############################## Tela de Eventos ##############################


    ############################## Tela de Conexões ##############################

    def add_connection_banner(self, connection):
        banner = MDCard(orientation="vertical", size_hint=(0.5, None), size=(300, 200), md_bg_color=(0.2, 0.22, 0.2, 1), radius=[15], padding=[10], spacing=300, on_release=lambda x: self.open_profile(connection['id']))

        box_layout = MDBoxLayout(orientation="vertical", padding=[10], spacing=10)

        box_layout.add_widget(MDLabel(text=connection['name'], size_hint=(None, 0.1)))

        box_layout.add_widget(MDLabel(text="    //    ".join(connection['social_media']), size_hint=(0.9, 0.2)))

        box_layout.add_widget(MDLabel(text=f"Gosto musical: {', '.join([': '.join([genero, str(perc)+'%']) for [genero, perc] in connection['musical_taste']])}", size_hint=(0.9, 0.1)))

        box_layout.add_widget(MDLabel(text=f"Music Match: {connection['music_match']}%", size_hint=(0.3, 0.1)))

        disconnectButton = MDRoundFlatIconButton(text="Desconectar", size_hint=(0.25, None), icon="account-minus", icon_color="red", text_color="red", line_color="red")

        disconnectButton.on_release = lambda: self.remove_connection(banner)

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
        # TODO: implementar lógica de remoção de conexão com o API do backend

    def confirm_disconect(self, idx):
        """Método que apaga o MDCard da conexão com o usuário de índice idx no grid."""
        self.dialog.dismiss()
        self.ids.connections_grid.remove_widget(self.ids.connections_grid.children[idx])

    def open_profile(self, connection_id):
        pass


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