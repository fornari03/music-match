from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
import webbrowser

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_icons = {}

    def on_pre_enter(self):
        """Método para colocar todas as músicas do banco de dados na lista da tela"""

        # TODO: implementar lógica de receber todas as músicas ainda não avaliadas com a API do backend (ordem aleatoria)
        
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