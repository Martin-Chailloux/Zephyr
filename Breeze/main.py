import sys
from datetime import timedelta

from Utils.chronometer import Chronometer
import mongoengine

import qdarkstyle

from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    print(f"Launching 'Breeze' ...")
    chrono = Chronometer()

    print("Connecting ...")
    mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")

    from Api.breeze_app import BreezeApp

    app = QApplication(sys.argv)
    BreezeApp.set_project("JourDeVent")
    BreezeApp.set_user("Martin")
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    mongoengine.connect(host="mongodb://localhost:27017", db=BreezeApp.project.name, alias="current_project")
    chrono.tick("... Connected in:")

    from Api import breeze_dialog
    breeze_dialog.Listener()
    from Gui.main_windows.main_tabs import BreezeMainWindow
    window = BreezeMainWindow()
    window.show()
    chrono.tick(f"... Finished launching 'Breeze' in:")
    print("-----------------")

    app.exec()

    runtime = chrono.tick()
    runtime = str(timedelta(seconds=runtime))
    hours = int(runtime.split(":")[0])
    minutes = int(runtime.split(":")[1])
    seconds = float(runtime.split(":")[2])
    msg = f"Run time: {hours}h, {minutes}m, {seconds:2.2f}s"
    print(msg)
