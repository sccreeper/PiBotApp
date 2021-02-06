from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button

from src.command_parser import execute_command
import src

from functools import partial
import json

def build_ui(container, ui_dict):

    ui_table = create_ui_table(json.loads(ui_dict))

    ui_row = BoxLayout(orientation="horizontal")

    # The final UI dict, for referring back to later, when a command requires a button from a slider for example
    ui_dict_rendered = {}

    for row in ui_table:
        for element in row:
            if element["type"] == "button":
                ui_dict_rendered[element["id"]] = Button(text=element["data"]["text"],
                                                         on_press=partial(execute_command, element["data"]["command"]))
                ui_row.add_widget(ui_dict_rendered[element["id"]])
            elif element["type"] == "slider":
                ui_dict_rendered[element["id"]] = Slider(min=element["data"]["min"], max=element["data"]["max"],
                                                         on_touch_up=partial(execute_command, element["data"]["command"]), step=1)
                ui_row.add_widget(ui_dict_rendered[element["id"]])

        container.add_widget(ui_row)
        ui_row = BoxLayout(orientation="horizontal")

    src.ui_dict = ui_dict_rendered

def create_ui_table(ui_dict):
    result = [[]]

    count = 0

    for element in ui_dict:
        if element["type"] == "html" and element["data"]["html"] == "<br>":
            result.append([])
            count += 1
        else:
            result[count].append(element)

    return result
