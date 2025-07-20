from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

from Api.breeze_app import BreezeApp


class StepLogsPanel(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        color = BreezeApp.palette.black_text  # TODO: replace with a color from the real palette
        color = '#1c1c1c'
        self.setStyleSheet(f"background-color: {color}")

    def set_log(self, log: str):
        palette = BreezeApp.palette

        self.clear()
        lines = log.split('\n')
        for line in lines:
            if 'INFO' in line:
                self.setTextColor(palette.white_text)
            elif 'DEBUG' in line:
                self.setTextColor(palette.purple)
            elif 'WARNING' in line:
                self.setTextColor(palette.orange)
            elif 'ERROR' in line or 'CRITICAL' in line:
                self.setTextColor(palette.red)
            self.append(line)
