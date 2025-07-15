import sys

import logging
from io import StringIO

import qdarkstyle
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QTextEdit


# class LogStream:
#     def __init__(self):
#         super().__init__()
#         self.logs: list[str] = []
#
#     def write(self, msg: str):
#         self.logs.append(msg)
#
#     def flush(self):
#         pass
#
#     @property
#     def output(self) -> str:
#         return "".join(self.logs)
#
#
# class LogHandler(logging.StreamHandler):
#     def __init__(self):
#         super().__init__()
#         self.logs: list[str] = []
#
#     def write(self, msg: str):
#         self.logs.append(msg)
#
#     @property
#     def output(self) -> str:
#         return "".join(self.logs)


class StepLogger:
    def __init__(self, name: str):
        # logger.setLevel(logging.DEBUG)
        stream = StringIO()
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s: %(message)s', datefmt='%H:%M:%S')

        handler = logging.StreamHandler()
        handler.setStream(stream)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)

        self.logger = logger
        self.stream = stream

    def info(self, msg: str):
        self.logger.info(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)

    @property
    def output(self) -> str:
        return self.stream.getvalue()


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
        logger = StepLogger(name = "test")
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')
        print(f"{logger.output = }")
        return

        # # create logger
        # logger = logging.getLogger("Turbine")
        # logger.setLevel(logging.DEBUG)
        #
        # # log_stream = LogStream()
        # # logging.basicConfig(stream=log_stream,
        # #                     level=logging.DEBUG,
        # #                     format='%(asctime)s - %(levelname)-8s: %(message)s',
        # #                     datefmt='%H:%M:%S')
        #
        # handler = logging.StreamHandler()
        # # # create console handler and set level to debug
        # # handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        # #
        # # # create formatter
        # # # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # # # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # # # formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s', datefmt='%I:%M:%S')
        # # # formatter = logging.Formatter(' [%(name)s] - %(levelname)-8s - %(message)s')
        # formatter = logging.Formatter('%(asctime)s - %(levelname)-8s: %(message)s', datefmt='%H:%M:%S')  # step logs
        # #
        # # # add formatter to ch
        # handler.setFormatter(formatter)
        # #
        # # # add ch to logger
        # # logger.addHandler(handler)
        #
        # # 'application' code
        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warning('warn message')
        # logger.error('error message')
        # logger.critical('critical message')
        #
        # print(f"{handler. = }")


def second_log():
    logger = StepLogger(name="test2")
    logger.debug('I am the second log')
    logger.info('I am the second log')
    logger.error('I am the second log')
    print(f"{logger.output = }")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    widget = Widget()
    widget.show()
    second_log()

    app.exec()
