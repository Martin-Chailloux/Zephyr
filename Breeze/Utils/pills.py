from dataclasses import dataclass
from typing import Optional

import qtawesome
from PySide6.QtGui import QIcon

from Utils.sub_widgets import IconLabel


@dataclass
class PillModel:
    name: str
    icon_name: str
    color: str

    def __repr__(self):
        return f"<Pill> {self.name}"

    @property
    def icon(self) -> QIcon:
        return qtawesome.icon(self.icon_name, color=self.color)


class AbstractPills:
    pills: list[PillModel] = []

    @classmethod
    def from_name(cls, name: str) -> Optional[PillModel]:
        for pill in cls.pills:
            if name == pill.name:
                return pill
        else:
            return None


class GenericPills(AbstractPills):
    minus = PillModel(name="minus", icon_name="fa.minus", color="lightgrey")
    true = PillModel(name="true", icon_name="fa.check", color="green")
    false = PillModel(name="false", icon_name="fa.close", color="tomato")

    pills = [minus, true, false]


class GenericPillIcon(IconLabel):
    def __init__(self, wh: int = 24):
        super().__init__(icon=GenericPills.minus.icon, wh=wh)

    def set_minus(self):
        self.set_icon(GenericPills.minus.icon)

    def set_true(self):
        self.set_icon(GenericPills.true.icon)

    def set_false(self):
        self.set_icon(GenericPills.false.icon)
