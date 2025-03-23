from Dialogs.palette_dialog import Palette

palette: Palette = Palette.objects.get(name="dev")


# TODO: define a color for disabled states

class StatusItem:
    label: str
    color: str


# ------------------------

class WAIT(StatusItem):
    label: str = "WAIT"
    color: str = palette.white_text


class TODO(StatusItem):
    label: str = "TODO"
    color: str = palette.yellow


class WIP(StatusItem):
    label: str = "WIP"
    color: str = palette.orange


class WFA(StatusItem):
    label: str = "WFA"
    color: str = palette.purple


class DONE(StatusItem):
    label: str = "DONE"
    color: str = palette.green


class ERROR(StatusItem):
    label: str = "ERROR"
    color: str = palette.red


class OMIT(StatusItem):
    label: str = "OMIT"
    color: str = palette.primary


default_statuses = [TODO, WIP, WFA, DONE, WAIT, ERROR, OMIT]