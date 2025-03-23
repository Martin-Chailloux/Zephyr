from dataclasses import dataclass

from Dialogs.palette_dialog import Palette

palette: Palette = Palette.objects.get(name="dev")


# TODO: define a color for disabled states

@dataclass
class StatusItem:
    label: str
    color: str


@dataclass
class StatusModel:
    wait = StatusItem(label="WAIT", color=palette.white_text)
    todo = StatusItem(label="TODO", color=palette.yellow)
    wip = StatusItem(label="WAIT", color=palette.orange)
    wfa = StatusItem(label="WFA", color=palette.purple)
    done = StatusItem(label="DONE", color=palette.green)
    error = StatusItem(label="ERROR", color=palette.red)
    omit = StatusItem(label="OMIT", color=palette.primary)


default_statuses = [
    StatusModel.todo,
    StatusModel.wip,
    StatusModel.wfa,
    StatusModel.done,
    StatusModel.wait,
    StatusModel.error,
    StatusModel.omit,
]