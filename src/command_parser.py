import requests
import src


def execute_command(cmd, *args):
    parsing_id = False
    current_id = ""
    #parsed_command = ""

    for char in cmd:
        if char == "]":
            parsing_id = False

            if type(src.ui_dict[current_id].value) == float:
                cmd = cmd.replace("[" + current_id + "]", str(src.ui_dict[current_id].value).split('.')[0])
            else:
                cmd = cmd.replace("[" + current_id + "]", str(src.ui_dict[current_id].value))

            current_id = ""

        if parsing_id:
            current_id += char

        if char == "[":
            parsing_id = True

    requests.post("http://{}:{}/command".format(src.bot_ip, src.bot_port), data={"command": cmd, "t": src.bot_token})
