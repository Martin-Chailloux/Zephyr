import sys

import logging

import qdarkstyle
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QTextEdit


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.logging_demo()

    def _init_ui(self):
        # TODO: show lines number
        #  https://nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/
        layout = QVBoxLayout()
        self.setLayout(layout)

        subwidget = QTextEdit()
        layout.addWidget(subwidget)

        subwidget.setReadOnly(True)
        subwidget.append("huezotieahjm")
        subwidget.append("paoioeazuge")

        subwidget.setTextColor("red")
        subwidget.append("mmmmmmmmmm")
        subwidget.setTextColor("orange")
        subwidget.append("WARNING")

    def logging_demo(self):
        # create logger
        logger = logging.getLogger("Turbine")
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s', datefmt='%I:%M:%S')
        # formatter = logging.Formatter(' [%(name)s] - %(levelname)-8s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s: %(message)s', datefmt='%H:%M:%S')  # step logs

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # 'application' code
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    widget = Widget()
    widget.show()

    app.exec()
