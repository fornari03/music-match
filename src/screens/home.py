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
from kivymd.uix.fitimage import FitImage
import webbrowser
from datetime import datetime, timedelta

from ..models.musica import Musica
from ..models.usuario import Usuario
from ..models.evento import Evento
import src.screens.login as login

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_icons = {}
        self.showing_users_connected = False
        self.showing_evaluated_musics = False
        self.showing_future_events = True

    def on_pre_enter(self):
        """Método de entrada da tela de início, chamado antes da tela ser exibida. Deve receber todas as informações que serão mostradas nas telas de início, eventos, conexões e perfil."""
        musicas = Musica.getEvaluatedAndNotEvaluatedMusics(login.usuario_logado.id)
        if musicas == False:
            self.dialog = MDDialog(text="Erro ao buscar as músicas do usuário.").open()
            self.manager.current = "login_screen"
            return
        self.evaluated, self.not_evaluated = musicas
        self.connected = Usuario.get_connections(login.usuario_logado.id)
        if self.connected == False:
            self.dialog = MDDialog(text="Erro ao buscar as conexões do usuário.").open()
            self.manager.current = "login_screen"
            return
        self.not_connected = Usuario.get_not_connections(login.usuario_logado.id)
        if self.not_connected == False:
            self.dialog = MDDialog(text="Erro ao buscar as conexões do usuário.").open()
            self.manager.current = "login_screen"
            return

        # informacoes do perfil
        self.ids.nome.text = login.usuario_logado.nome
        self.ids.email.text = login.usuario_logado.email
        self.ids.data_nascimento.text = login.usuario_logado.data_nascimento.strftime("%d/%m/%Y")
        self.data_nascimento = login.usuario_logado.data_nascimento
        self.ids.senha.text = ""
        self.user_redes_sociais = Usuario.findSocialMedia(login.usuario_logado.id)
        if self.user_redes_sociais == False:
            self.dialog = MDDialog(text="Erro ao buscar os dados do usuário.").open()
            self.manager.current = "login_screen"
            return
        for rede_social in self.user_redes_sociais:
            self.add_social_media_item(rede_social[0].capitalize(), rede_social[1], True)

        self.changed_evaluation = {}       # dicionario de músicas que sofreram alteração na avaliação no formato id_musica: 'CHAR_AVALIACAO'
        self.events = Evento.get_eventos(login.usuario_logado.id, self.connected)
        if self.events == False:
            self.dialog = MDDialog(text="Erro ao buscar os eventos.").open()
            self.manager.current = "login_screen"
            return

        self.show_music_list()

        self.show_connections_grid()

        self.show_events_grid()










    ############################## Tela de Início ##############################

    def add_music_item(self, music):
        """
        Adiciona um item de música à lista de músicas.
        """
        item = TwoLineAvatarIconListItem(text=f"{music['nome']} - {', '.join(music['estilo'])}", secondary_text=f"{', '.join(music['artista'])}")
        
        capa = ImageLeftWidget(source=music['capa'])
        item.add_widget(capa)
        
        if music.get("evaluation") == 'L' or (music['id'], 'L') in self.changed_evaluation.items():
            like_icon = IconRightWidget(icon="thumb-up")
            dislike_icon = IconRightWidget(icon="thumb-down-outline")
        elif music.get("evaluation") == 'D' or (music['id'], 'D') in self.changed_evaluation.items():
            like_icon = IconRightWidget(icon="thumb-up-outline")
            dislike_icon = IconRightWidget(icon="thumb-down")
        else:
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
        item.on_release = lambda: webbrowser.open(music['link_spotify'])
        
        self.ids.music_list.add_widget(item)


    def like_music(self, like_icon, dislike_icon, music_id):
        """
        Altera o ícone de like e dislike da música de id music_id, dando like.
        """
        if like_icon.icon == "thumb-up":
            like_icon.icon = "thumb-up-outline"
            self.changed_evaluation[music_id] = 'N'
        else:
            like_icon.icon = "thumb-up"
            self.changed_evaluation[music_id] = 'L'
        dislike_icon.icon = "thumb-down-outline"

    def dislike_music(self, dislike_icon, like_icon, music_id):
        """
        Altera o ícone de like e dislike da música de id music_id, dando dislike.
        """
        if dislike_icon.icon == "thumb-down":
            dislike_icon.icon = "thumb-down-outline"
            self.changed_evaluation[music_id] = 'N'
        else:
            dislike_icon.icon = "thumb-down"
            self.changed_evaluation[music_id] = 'D'
        like_icon.icon = "thumb-up-outline"


    def show_music_list(self, search_string=None):
        """
        Mostra a lista de músicas na tela de início.
        """
        self.ids.music_list.clear_widgets()
        if not self.showing_evaluated_musics:
            for music in self.not_evaluated:
                if search_string is None or search_string.lower().strip() in music['nome'].lower().strip() or search_string.lower().strip() in " ".join(music['artista']).lower().strip() or search_string.lower().strip() in music['estilo'] or search_string.lower().strip() == "":
                    self.add_music_item(music)

        else:
            for music in self.evaluated:
                if search_string is None or search_string.lower().strip() in music['nome'].lower().strip() or search_string.lower().strip() in " ".join(music['artista']).lower().strip() or search_string.lower().strip() in music['estilo'] or search_string.lower().strip() == "":
                    self.add_music_item(music)

    def switch_musics_view(self):
        """
        Troca a visualização entre músicas avaliadas e não avaliadas.	
        """
        self.showing_evaluated_musics = not self.showing_evaluated_musics
        self.show_music_list()

    def show_musics_search(self):
        """
        Mostra a barra de pesquisa de músicas.
        """
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
        """
        Faz a busca de músicas na lista de músicas.
        """
        self.show_music_list(search_string)
        self.dialog.dismiss()

    def save_evaluations(self):
        """
        Salva as avaliações feitas pelo usuário.
        """
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
        """
        Confirma a ação de salvar as avaliações feitas pelo usuário.
        """
        erro = False
        for music_id, evaluation in self.changed_evaluation.items():
            achou = False
            for music in self.evaluated:
                if music['id'] == music_id:
                    if music['evaluation'] != evaluation:
                        if evaluation != 'N':
                            ret = Musica.updateFeedback(music_id, login.usuario_logado.id, True if evaluation == 'L' else False)
                            if not ret:
                                erro = True
                        else:
                            ret = Musica.removeFeedback(music_id, login.usuario_logado.id)
                            if not ret:
                                erro = True
                    achou = True
                    break
            if not achou:
                if evaluation == 'L':
                    ret = Musica.createFeedback(music_id, login.usuario_logado.id, True)
                    if not ret:
                        erro = True
                elif evaluation == 'D':
                    ret = Musica.createFeedback(music_id, login.usuario_logado.id, False)
                    if not ret:
                        erro = True
        self.dialog.dismiss()

        if erro:
            self.dialog = MDDialog(text="Ocorreu um erro ao salvar uma ou mais operações.").open()
            
        self.on_pre_enter()










    ############################## Tela de Eventos ##############################

    def add_event_banner(self, event):
        """
        Adiciona um banner de evento à lista de eventos.
        """
        banner = MDCard(id=f"banner_{event['id']}", orientation="vertical", size_hint=(0.5, None), size=(350, 300), md_bg_color=(0.2, 0.22, 0.2, 1), radius=[15], padding=[10], spacing=300)

        grid_layout = MDGridLayout(cols=2, padding=[5, 10, 5, 10], spacing=10)

        grid_layout.add_widget(FitImage(source=f"images/imagem_evento_{event['id']}.jpg", size_hint_y=None, height="260dp", radius=[15]))

        box_layout = MDBoxLayout(orientation="vertical", spacing=5)

        box_layout.add_widget(MDLabel(text=event['nome'], size_hint=(1, 0.4), bold=True))

        box_layout.add_widget(MDLabel(text=event['descricao'], size_hint=(1, 0.7)))

        box_layout.add_widget(MDLabel(text=f"Data: {event['data_realizacao'].strftime('%d/%m/%Y - %H:%M')}", size_hint=(1, 0.6)))

        box_layout.add_widget(MDLabel(text=f"Local: {event['localizacao']}", size_hint=(1, 0.6)))

        box_layout.add_widget(MDLabel(text=f"Artistas: {', '.join(event['artistas'])}", size_hint=(1, 0.6)))

        box_layout.add_widget(MDLabel(text=f"Estilos: {', '.join(event['estilos'])}", size_hint=(1, 0.6)))

        if event['data_realizacao'] >= datetime.now():
            if len(event['conexoes_interessadas']) == 0:
                texto = "Nenhuma conexão se interessou neste evento."
            elif len(event['conexoes_interessadas']) == 1:
                texto = f"{event['conexoes_interessadas'][0]['nome']} se interessou neste evento."
            else:
                texto = f"{event['conexoes_interessadas'][0]['nome']} e mais {len(event['conexoes_interessadas'])-1} conexões se interessaram neste evento."
            box_layout.add_widget(MDLabel(text=texto, size_hint=(1, 0.6), italic=True))
            if event['status'] == "I":
                interest_button = MDRoundFlatIconButton(id="interest_button", text="Sem interesse", size_hint=(0.25, None), icon="alarm-note")
            else:
                interest_button = MDRoundFlatIconButton(id="interest_button", text="Tenho interesse", size_hint=(0.25, None), icon="alarm-note")

        else:
            if len(event['conexoes_foram']) == 0:
                texto = "Nenhuma conexão foi para este evento."
            elif len(event['conexoes_foram']) == 1:
                texto = f"{event['conexoes_foram'][0]['nome']} foi para este evento."
            else:
                texto = f"{event['conexoes_foram'][0]['nome']} e mais {len(event['conexoes_foram'])-1} conexões foram para este evento."
            box_layout.add_widget(MDLabel(text=texto, size_hint=(1, 0.6), italic=True))
            if event['status'] == "P":
                interest_button = MDRoundFlatIconButton(id="interest_button", text="Marcar ausência", size_hint=(0.25, None), icon="account-check")
            else:
                interest_button = MDRoundFlatIconButton(id="interest_button", text="Marcar presença", size_hint=(0.25, None), icon="account-check")

        grid_layout_baixo = MDGridLayout(cols=2, spacing=5)

        if interest_button.text == "Tenho interesse":
            # se o evento é futuro e o usuário não se interessou
            interest = MDLabel(id="label_interest", text="Você não demonstrou interesse no evento.", size_hint=(1, 0.6), italic=True)
            grid_layout_baixo.add_widget(interest)
            interest_button.on_release = lambda: self.mark_interest(banner, interest_button, interest)
        elif interest_button.text == "Marcar presença":
            # se o evento já passou e o usuário não foi
            interest = MDLabel(id="label_interest", text="Você não marcou presença no evento.", size_hint=(1, 0.6), italic=True)
            grid_layout_baixo.add_widget(interest)
            interest_button.on_release = lambda: self.mark_presence(banner, interest_button, interest)
        elif interest_button.text == "Sem interesse":
            # se o evento é futuro e o usuário se interessou
            interest = MDLabel(id="label_interest", text="Você demonstrou interesse no evento.", size_hint=(1, 0.6), italic=True)
            grid_layout_baixo.add_widget(interest)
            interest_button.on_release = lambda: self.mark_interest(banner, interest_button, interest)
        else:
            # se o evento já passou e o usuário foi
            interest = MDLabel(id="label_interest", text="Você marcou presença no evento.", size_hint=(1, 0.6), italic=True)
            grid_layout_baixo.add_widget(interest)
            interest_button.on_release = lambda: self.mark_presence(banner, interest_button, interest)

        grid_layout_baixo.add_widget(interest_button)

        box_layout.add_widget(grid_layout_baixo)

        grid_layout.add_widget(box_layout)

        banner.add_widget(grid_layout)

        self.ids.events_grid.add_widget(banner)

    def mark_interest(self, banner, interest_button, interest_label):
        """
        Marca ou desmarca interesse no evento.
        """
        if interest_button.text == "Tenho interesse":
            marca_interesse = Evento.addTemInteresse(login.usuario_logado.id, int(banner.id.split("_")[1]))
            if not marca_interesse:
                self.dialog = MDDialog(
                    text="Ocorreu um erro ao marcar interesse no evento.",
                    buttons=[MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    )]
                )
                self.dialog.open()
                return
            interest_label.text = "Você demonstrou interesse no evento."
            interest_button.text = "Sem interesse"
            for event in self.events:
                if event['id'] == int(banner.id.split("_")[1]):
                    event['status'] = "I"
                    break
        else:
            marca_desinteresse = Evento.deleteTemInteresse(login.usuario_logado.id, int(banner.id.split("_")[1]))
            if not marca_desinteresse:
                self.dialog = MDDialog(
                    text="Ocorreu um erro ao desmarcar interesse no evento.",
                    buttons=[MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    )]
                )
                self.dialog.open()
                return
            interest_label.text = "Você não demonstrou interesse no evento."
            interest_button.text = "Tenho interesse"
            for event in self.events:
                if event['id'] == int(banner.id.split("_")[1]):
                    event['status'] = "N"
                    break

    def mark_presence(self, banner, interest_button, interest_label):
        """
        Marca ou desmarca presença no evento.
        """
        if interest_button.text == "Marcar presença":
            marca_presenca = Evento.addParticipouDe(login.usuario_logado.id, int(banner.id.split("_")[1]))
            if not marca_presenca:
                self.dialog = MDDialog(
                    text="Ocorreu um erro ao marcar presença no evento.",
                    buttons=[MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    )]
                )
                self.dialog.open()
                return
            interest_label.text = "Você marcou presença no evento."
            interest_button.text = "Marcar ausência"
            for event in self.events:
                if event['id'] == int(banner.id.split("_")[1]):
                    event['status'] = "P"
                    break
        else:
            marca_ausencia = Evento.deleteParticipouDe(login.usuario_logado.id, int(banner.id.split("_")[1]))
            if not marca_ausencia:
                self.dialog = MDDialog(
                    text="Ocorreu um erro ao desmarcar presença no evento.",
                    buttons=[MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    )]
                )
                self.dialog.open()
                return
            interest_label.text = "Você não marcou presença no evento."
            interest_button.text = "Marcar presença"
            for event in self.events:
                if event['id'] == int(banner.id.split("_")[1]):
                    event['status'] = "N"
                    break

    def show_events_grid(self, search_string=None):
        """
        Mostra a lista de eventos na tela de eventos.
        """
        self.ids.events_grid.clear_widgets()
        if self.showing_future_events:
            for event in self.events:
                if event['data_realizacao'] >= datetime.now():
                    if search_string is None or search_string.lower().strip() in event['nome'].lower().strip() or search_string.lower().strip() in event['descricao'] or search_string.lower().strip() == "" or search_string.lower().strip() in event['localizacao'].lower().strip() or search_string.lower().strip() in event['data_realizacao'].strftime('%d/%m/%Y - %H:%M'):
                        self.add_event_banner(event)
        else:
            for event in self.events:
                if event['data_realizacao'] < datetime.now():
                    if search_string is None or search_string.lower().strip() in event['nome'].lower().strip() or search_string.lower().strip() in event['descricao'] or search_string.lower().strip() == "" or search_string.lower().strip() in event['localizacao'].lower().strip() or search_string.lower().strip() in event['data_realizacao'].strftime('%d/%m/%Y - %H:%M'):
                        self.add_event_banner(event)

    def switch_events_view(self):
        """
        Troca a visualização entre eventos futuros e passados.
        """
        self.showing_future_events = not self.showing_future_events
        self.show_events_grid()

    def show_events_search(self):
        """
        Mostra a barra de pesquisa de eventos.
        """
        self.dialog = MDDialog(
            title="Buscar Evento",
            type="custom",
            content_cls=
                MDBoxLayout(
                    MDTextField(id="barra_pesquisa", hint_text="Nome do Evento"),
                    MDRaisedButton(text="Buscar", on_release=lambda x: self.search_event(self.dialog.content_cls.children[1].text.strip())),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp"
                )        
        )
        self.dialog.open()

    def search_event(self, search_string):
        """
        Faz a busca de eventos na lista de eventos.
        """
        self.show_events_grid(search_string)
        self.dialog.dismiss()










    ############################## Tela de Conexões ##############################

    def add_connection_banner(self, connection, status):
        """
        Adiciona um banner de conexão à lista de conexões.
        """
        banner = MDCard(orientation="vertical", size_hint=(0.5, None), size=(300, 200), md_bg_color=(0.2, 0.22, 0.2, 1), radius=[15], padding=[10], spacing=300)

        box_layout = MDBoxLayout(orientation="vertical", padding=[10], spacing=10)

        box_layout.add_widget(MDLabel(text=connection['nome'], size_hint=(0.9, 0.1), bold=True))

        box_layout.add_widget(MDLabel(text="Redes:" + "    //    ".join([": ".join([rd, ru]) for rd, ru in connection['redes_sociais']]), size_hint=(0.9, 0.2)))

        box_layout.add_widget(MDLabel(text=f"Gosto musical: {', '.join([genero for genero in connection['musical_taste']])}", size_hint=(0.9, 0.1)))

        box_layout.add_widget(MDLabel(text=f"Artistas: {', '.join(connection['artists'])}", size_hint=(0.9, 0.2)))

        box_layout.add_widget(MDLabel(text=f"Music Match: {connection['sintonia']:.1f}%", size_hint=(0.3, 0.1)))

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
        """
        Remove a conexão com o usuário do banner.
        """
        for i in range(len(self.ids.connections_grid.children)-1, -1, -1):
            if self.ids.connections_grid.children[i] == banner:
                self.dialog = MDDialog(
                    text=f"Deseja se desconectar de {banner.children[0].children[5].text}?",
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
        """
        Confirma a ação de desconectar do usuário de banner de índice idx.
        """
        self.dialog.dismiss()
        i = len(self.connected) - idx - 1
        user = self.connected[i]
        query_ret = Usuario.disconnect(login.usuario_logado.id, user['id'])
        if not query_ret:
            self.dialog = MDDialog(
                text="Ocorreu um erro ao desconectar do usuário.",
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    )])
            self.dialog.open()
            return
    
        self.ids.connections_grid.remove_widget(self.ids.connections_grid.children[idx])
        self.not_connected.append(user)
        self.not_connected.sort(key=lambda x: x['sintonia'], reverse=True)
        self.connected.pop(i)
        self.show_connections_grid()

    def add_connection(self, banner):
        """
        Adiciona a conexão com o usuário do banner.
        """
        for i in range(len(self.ids.connections_grid.children)-1, -1, -1):
            if self.ids.connections_grid.children[i] == banner:
                self.dialog = MDDialog(
                    text=f"Deseja se conectar com {banner.children[0].children[5].text}?",
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
        """
        Confirma a ação de conectar com o usuário de banner de índice idx.
        """
        self.dialog.dismiss()
        i = len(self.not_connected) - idx - 1
        user = self.not_connected[i]
        query_ret = Usuario.connect(login.usuario_logado.id, user['id'])
        if not query_ret:
            self.dialog = MDDialog(
                text="Ocorreu um erro ao conectar com o usuário.",
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    )]
            )
            self.dialog.open()
            return

        self.ids.connections_grid.remove_widget(self.ids.connections_grid.children[idx])
        self.connected.append(user)
        self.connected.sort(key=lambda x: x['sintonia'], reverse=True)
        self.not_connected.pop(i)
        self.show_connections_grid()

    def show_connections_grid(self, search_string=None):
        """
        Mostra a lista de conexões na tela de conexões.
        """
        self.ids.connections_grid.clear_widgets()
        if self.showing_users_connected:
            for connection in self.connected:
                if search_string is None or search_string.lower().strip() in connection['nome'].lower().strip() or search_string.lower().strip() in connection['redes_sociais'] or search_string.lower().strip() == "":
                    self.add_connection_banner(connection, "connected")
        else:
            for connection in self.not_connected:
                if search_string is None or search_string.lower().strip() in connection['nome'].lower().strip() or search_string.lower().strip() in connection['redes_sociais'] or search_string.lower().strip() == "":
                    self.add_connection_banner(connection, "not_connected")

    def switch_users_view(self):
        """
        Troca a visualização entre usuários conectados e não conectados.
        """
        self.showing_users_connected = not self.showing_users_connected
        self.show_connections_grid()

    def show_users_search(self):
        """
        Mostra a barra de pesquisa de usuários.
        """
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
        """
        Busca usuários na lista de conexões.
        """
        self.show_connections_grid(search_string)
        self.dialog.dismiss()










    ############################## Tela de Perfil ##############################

    def show_date_picker(self):
        """
        Mostra o seletor de data para a data de nascimento.
        """
        date_dialog = MDDatePicker()
        date_dialog.open()
        date_dialog.bind(on_save=self.on_save)

    def on_save(self, instance, value, date_range):
        """
        Salva a data de nascimento selecionada.
        """
        self.ids.data_nascimento.text = value.strftime("%d/%m/%Y")
        try:
            self.data_nascimento = value
        except:
            self.data_nascimento = None

    def save(self):
        """
        Salva as informações do perfil do usuário.
        """
        if self.ids.nome.text.strip() == "" or self.ids.email.text.strip() == "" or self.ids.data_nascimento.text.strip() == "":
            self.dialog = MDDialog(text="Preencha o nome, email e data de nascimento atualizada.").open()
            return
        
        if self.ids.senha.text.strip() != "":
            self.dialog = MDDialog(
                text="Deseja mudar sua senha?",
                buttons=[
                    MDFlatButton(
                        text="Não",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Sim",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.confirm_save_perfil())]
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(text="Ocorreu um erro inesperado.")
            self.confirm_save_perfil()

    def confirm_save_perfil(self):
        """
        Confirma a ação de salvar as informações do perfil do usuário.
        """
        self.dialog.dismiss()
        
        nome = self.ids.nome.text.strip()
        email = self.ids.email.text.strip()
        data_nascimento = self.data_nascimento
        senha = self.ids.senha.text.strip()
        lista_redes_sociais = [(child.children[0].hint_text.strip(), child.children[0].text.strip(), child.children[1].active) for child in self.ids.lista_opcoes.children]
        for rede_social in lista_redes_sociais:
            if rede_social[2]:
                if rede_social[0].strip() == "" or rede_social[1].strip() == "":
                    self.dialog = MDDialog(text="Preencha todos os campos das redes sociais marcadas para salvar.").open()
                    return
                else:
                    if (rede_social[0], rede_social[1]) not in self.user_redes_sociais:
                        if rede_social[0] in [rs[0] for rs in self.user_redes_sociais]:
                            ret = Usuario.editSocialMediaUsername(login.usuario_logado.id, rede_social[0], rede_social[1])
                            if not ret:
                                self.dialog = MDDialog(text="Erro ao salvar os dados no banco de dados.").open()
                                return
                        else:
                            ret = Usuario.addSocialMedia(login.usuario_logado.id, rede_social[0], rede_social[1])
                            if not ret:
                                self.dialog = MDDialog(text="Erro ao salvar os dados no banco de dados.").open()
                                return
            else:
                if (rede_social[0], rede_social[1]) in self.user_redes_sociais:
                    ret = Usuario.deleteSocialMedia(login.usuario_logado.id, rede_social[0])
                    if not ret:
                        self.dialog = MDDialog(text="Erro ao salvar os dados no banco de dados.").open()


        changes = {}
        if nome != login.usuario_logado.nome:
            changes["nome"] = nome
        
        if email != login.usuario_logado.email:
            changes["email"] = email

        if data_nascimento != login.usuario_logado.data_nascimento:
            changes["data_nascimento"] = data_nascimento

        if senha != "":
            changes["nova_senha"] = senha
        
        login.usuario_logado.change_values(changes)
        if not login.usuario_logado.save():
            self.dialog = MDDialog(text="Erro ao salvar os dados no banco de dados.").open()
            return

        self.ids.lista_opcoes.clear_widgets()
        self.user_redes_sociais = Usuario.findSocialMedia(login.usuario_logado.id)
        if self.user_redes_sociais == False:
            self.dialog = MDDialog(text="Erro ao buscar as redes sociais do usuário.").open()
        else:
            for rede_social in self.user_redes_sociais:
                self.add_social_media_item(rede_social[0].capitalize(), rede_social[1], True)

        # nao precisa reescrever os campos pq eh literalmente o que ja ta escrito la
        login.usuario_logado = Usuario.where({"id": login.usuario_logado.id})[0]
        self.user_redes_sociais = Usuario.findSocialMedia(login.usuario_logado.id)

        self.dialog = MDDialog(text="Dados atualizados com sucesso!").open()

    def delete_account(self):
        """
        Deleta a conta do usuário.
        """
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
        """
        Confirma a ação de deletar a conta do usuário.
        """
        self.dialog.dismiss()

        if not Usuario.delete(login.usuario_logado.id):
            self.dialog = MDDialog(text="Ocorreu um erro ao deletar o usuario.").open()
            return

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

    def add_social_media_item(self, social_media: str, user_social_media: str="", checked: bool=False):
        """
        Adiciona um item de rede social à lista de redes sociais.
        """
        new_item = OneLineIconListItem(on_press=lambda x: self.checkbox_selected(len(self.ids.lista_opcoes.children)))

        new_item.add_widget(MDCheckbox(size_hint_x=None, pos_hint={"center_y": 0.5}, active=checked))
        new_item.add_widget(MDTextField(hint_text=social_media.strip(), text=user_social_media.strip(), size_hint_x=0.6, pos_hint={"center_y": 0.5, "center_x": 0.5}))
        
        self.ids.lista_opcoes.add_widget(new_item)

        self.ids.nova_rede_social.text = ""

    def checkbox_selected(self, item_id):
        pass