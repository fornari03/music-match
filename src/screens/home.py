from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
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