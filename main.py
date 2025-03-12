import json
import os
import warnings

import setproctitle
from fabric import Application
from fabric.utils import get_relative_path, exec_shell_command_async
import config.data as data



fonts_updated_file = f"{data.CACHE_DIR}/fonts_updated"
hyprconf = get_relative_path("config.json")


def load_config():
    with open(hyprconf, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    setproctitle.setproctitle(data.APP_NAME)

    if not os.path.isfile(data.CONFIG_FILE):
        exec_shell_command_async(f"python {get_relative_path('../config/config.py')}")

    config = load_config()

    assets = []
    if config["Basic"]["corners"]:
        from modules.corners import Corners

        corners = Corners()
        assets.append(corners)
    if config["Basic"]["bar"]:
        from modules.bar import Bar
        from modules.notch import Notch

        bar = Bar()
        assets.append(bar)
        notch = Notch()
        bar.notch = notch
        notch.bar = bar
        assets.append(notch)


    if config["Basic"]["widgets"]:
        if config["widgetstyle"] == "full":
            from modules.deskwidgets import Deskwidgetsfull

            widgets = Deskwidgetsfull()
            assets.append(widgets)
            pass
        elif config["widgetstyle"] == "basic":
            from modules.deskwidgets import Deskwidgetsbasic

            widgets = Deskwidgetsbasic()
            assets.append(widgets)
            pass
    if config["Basic"]["dock"]:
        from modules.dock import Dock

        dock = Dock()
        assets.append(dock)
    app = Application(f"{data.APP_NAME}", *assets)

    def set_css():
        app.set_stylesheet_from_file(
            get_relative_path("main.css"),
            exposed_functions={
                "overview_width": lambda: f"min-width: {data.CURRENT_WIDTH * 0.1 * 5 + 92}px;",
                "overview_height": lambda: f"min-height: {data.CURRENT_HEIGHT * 0.1 * 2 + 32 + 56}px;",
            },
        )

    app.set_css = set_css

    app.set_css()
    app.run()
