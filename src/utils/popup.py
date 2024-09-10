from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.lang import Builder

# Provisório
KV = '''
<CustomPopup@Popup>:
    size_hint: None, None
    size: 400, 200
    title: root.popup_title
    background_color: app.theme_cls.bg_dark  
    separator_color: app.theme_cls.primary_color  

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        MDLabel:
            id: message_label
            text: root.popup_message
            halign: 'center'
            valign: 'middle'
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color  # Texto na cor primária
            text_size: self.size

        MDRaisedButton:
            text: "OK"
            md_bg_color: app.theme_cls.primary_color  # Botão na cor primária
            text_color: app.theme_cls.opposite_text_color  # Cor do texto do botão
            size_hint: None, None
            size: dp(100), dp(40)
            pos_hint: {"center_x": 0.5}
            on_release: root.dismiss()
'''

Builder.load_string(KV)

class CustomPopup(Popup):
    popup_title = StringProperty()
    popup_message = StringProperty()

def show_popup(title, message):
    popup = CustomPopup(popup_title=title, popup_message=message)
    popup.open()
