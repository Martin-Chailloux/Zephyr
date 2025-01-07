import json
from typing import TypedDict, Unpack, Any
from dataclasses import dataclass

from PySide6.QtGui import QColor


class JsonDialog:
    file: str = "Gui/palette.json"

    def get_palette(self) -> dict[str, Any]:
        with open(self.file, "r") as file:
            palette = json.load(file)
        return palette

    def write(self, palette: dict):
        with open(self.file, "w") as file:
            file.write(json.dumps(palette, indent=4))


class Colors(TypedDict):
    text_white: Any
    text_black: Any
    background: Any
    light: Any
    medium: Any
    dark: Any
    purple: Any
    red: Any
    orange: Any
    yellow: Any
    green: Any
    blue: Any
    cyan: Any


class ZPalette:
    def __init__(self):
        self.json_dialog = JsonDialog()

    def get_color(self, name: str):
        palette = self.json_dialog.get_palette()
        color = palette[name]
        return QColor(color)

    @property
    def transparent(self): return QColor(0, 0, 0, 0)

    @property
    def text_white(self): return self.get_color("text_white")
    @property
    def text_black(self): return self.get_color("text_black")

    @property
    def background(self): return self.get_color("background")
    @property
    def light(self): return self.get_color("light")
    @property
    def medium(self): return self.get_color("medium")
    @property
    def dark(self): return self.get_color("dark")

    @property
    def purple(self): return self.get_color("purple")
    @property
    def red(self): return self.get_color("red")
    @property
    def orange(self): return self.get_color("orange")
    @property
    def yellow(self): return self.get_color("yellow")
    @property
    def green(self): return self.get_color("green")
    @property
    def blue(self): return self.get_color("blue")
    @property
    def cyan(self): return self.get_color("cyan")


class AbstractPalette:
    def __init__(self, **kwargs: Unpack[Colors]):
        self.palette = kwargs

    def apply(self):
        # TODO: bulletproof que y ait tous les noms
        dialog = JsonDialog()
        dialog.write(self.palette)


@dataclass
class GDefaultPalettes:
    dark = AbstractPalette(
        text_white = "#F9F9F9",
        text_black = "#2F2F32",

        background = "#303030",
        light = "#545454",
        medium = "#3D3D3D",
        dark = "#262626",

        purple = "#C8B8EA",
        red = "#FFC3C4",
        orange = "#FFD486",
        yellow = "#FFF2A0",
        green = "#C5FFAF",
        blue = "#6BB6FF",
        cyan = "#A5E5D9",
    )

# POUR APPLIQUER UNE PALETTE A L'APP
# x = GDefaultPalettes()
# x.dark.apply()

# POUR RECUPERER UNE COULEUR DEPUIS LA PALETTE
# x = GPalette()
# print(x.text_white)

