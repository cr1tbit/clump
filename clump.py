import dearpygui.dearpygui as dpg
import json
import subprocess


# Target proces:
# 1.Parse settings
# 2.get PC's status
# 3.prepare dict with commands
# 4.create button for each command

def create_list_from_json(monitors: list[str]):
    commands_list = {}
    with open('config.json', 'r') as file:
        json_content = (json.load(file))
        return dict((k, v.format(*monitors)) for k, v in json_content.items())

def get_monitors():
    command = "xrandr |awk '/connected/{print $1,$2}' | grep -v disconnected"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f"Error: {error}")
    else:
        return [o.split(" ")[0] for o in output.decode().split("\n") if o != ""]
        

def button_callback(sender, app_data, user_data):
    print(f"Execute \"{user_data}\" ")
    process = subprocess.Popen(user_data, stdout=subprocess.PIPE, shell=True)


app_config = {
    "start_height": 400,
    "start_width": 1000
}

monitors = get_monitors();
print(monitors)

commands = create_list_from_json(monitors)
print(json.dumps(commands, indent=4))

dpg.create_context()

with dpg.font_registry():
    font = dpg.add_font("/usr/share/fonts/liberation/LiberationMono-Regular.ttf",
                         30, tag="ttf-font")
    dpg.bind_font(font)
    font_smol = dpg.add_font("/usr/share/fonts/liberation/LiberationMono-Regular.ttf",
                             15, tag="ttf-font-smol")

with dpg.window(tag="Primary Window"):
    # prepare button theme
    with dpg.theme(tag="monitor_button"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (2, 85, 68, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 20)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 15, 15)

    dpg.add_text("CLUMP - cringe linux universal management panel")
    dpg.add_separator()
    
    with dpg.group(horizontal=True):
        dpg.add_text("Monitors:")
        for monitor in monitors:
            dpg.add_text(monitor)

    dpg.add_separator()

    with dpg.group(horizontal=True):
        for name, command in commands.items():
            dpg.add_button(label=name, callback=button_callback, user_data=command)
            dpg.bind_item_theme(dpg.last_item(), "monitor_button")

            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(command, wrap=app_config["start_width"]*0.7,
                             )

    dpg.add_separator()
    dpg.add_slider_float(label="lmao", default_value=0.273, max_value=1)
            

viewport = dpg.create_viewport(
    title='clump', width=app_config["start_width"], 
    height=app_config["start_height"], x_pos=1000, y_pos=1000)

dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()