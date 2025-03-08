from Dialogs.palette_dialog import Palette

palette: Palette = Palette.objects.get(name="dev")


# TODO: define a color for disabled states

class Status:
    label: str
    color: str


# ------------------------

class WAIT(Status):
    label: str = "WAIT"
    color: str = palette.white_text


class TODO(Status):
    label: str = "TODO"
    color: str = palette.yellow


class WIP(Status):
    label: str = "WIP"
    color: str = palette.orange


class WFA(Status):
    label: str = "WFA"
    color: str = palette.purple


class DONE(Status):
    label: str = "DONE"
    color: str = palette.green


class ERROR(Status):
    label: str = "ERROR"
    color: str = palette.red


class OMIT(Status):
    label: str = "OMIT"
    color: str = palette.primary


default_statuses = [TODO, WIP, WFA, DONE, WAIT, ERROR, OMIT]