from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from functools import partial
import requests

import src.parse_ui
import src

#bot_token = ""

ui_dict = {}

status_text = None

gen_ui_container = None


class MyApp(App):
    def build(self):
        return MainView()


def connect_to_bot(pop, form_layout, *args):

    src.bot_port = form_layout.children[2].text
    src.bot_ip = form_layout.children[3].text
    src.bot_pwd = form_layout.children[1].text

    print(form_layout.children)

    status_text.text = "Connecting to bot..."

    r = requests.post("http://{}:{}/m/login".format(src.bot_ip,src.bot_port), data={"pass": src.bot_pwd})

    if r.text == "pwd_err":
        status_text.text = "Password incorrect"
        pop.dismiss()
        return

    src.bot_token = r.text

    status_text.text = "Connected to bot: {}".format(src.bot_token)

    print(src.bot_port, src.bot_ip, src.bot_pwd, src.bot_token)

    pop.dismiss()

    #Get the UI
    r2 = requests.post("http://{}:{}/m/get_ui".format(src.bot_ip,src.bot_port), data={"t": src.bot_token})
    print(r2.text)

    gen_ui_container.clear_widgets()
    src.parse_ui.build_ui(gen_ui_container, r2.text)


class MainView(BoxLayout):

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)

        global status_text, gen_ui_container, ui_dict

        self.orientation = "vertical"

        # Code for connection popup

        self.bot_connect_layout = BoxLayout()
        self.bot_connect_layout.orientation = "vertical"

        self.details_popup = Popup(title='Connect to a bot', content=self.bot_connect_layout,
                                   auto_dismiss=False, size_hint=(0.5, 0.5))

        bot_connect_btn = Button(text="Connect", size_hint=(1, 0.1))
        bot_connect_btn.bind(on_press=partial(connect_to_bot, self.details_popup, self.bot_connect_layout))

        self.bot_connect_layout.add_widget(TextInput(multiline=False, hint_text="Bot IP", size_hint=(1, 0.1), text="192.168.1.42"))
        self.bot_connect_layout.add_widget(TextInput(multiline=False, hint_text="Bot port", size_hint=(1, 0.1), input_filter="int", text="5000"))
        self.bot_connect_layout.add_widget(TextInput(multiline=False, hint_text="Bot password", size_hint=(1, 0.1), text="notsecurepassword", password=True, password_mask="*"))
        self.bot_connect_layout.add_widget(bot_connect_btn)

        # Code for group at top

        self.menu_layout = BoxLayout(size_hint=(1, 0.1))
        self.menu_layout.orientation = "vertical"

        status_text = Label(text="Not connected to a bot", size_hint=(1, 0.5))
        self.menu_layout.add_widget(status_text)

        self.btn_connect = Button(text="Connect to a bot", size_hint=(1, 0.5))
        self.menu_layout.add_widget(self.btn_connect)

        gen_ui_container = BoxLayout(size_hint=(1, 0.8))
        gen_ui_container.orientation = "vertical"

        self.btn_connect.bind(on_press=self.details_popup.open)
        self.add_widget(self.menu_layout)
        self.add_widget(gen_ui_container)


if __name__ == '__main__':
    MyApp().run()
