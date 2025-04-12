from PySide6.QtWidgets import QApplication

from Data.studio_documents import Project, User, Palette


def set_project(name: str):
    project = Project.objects.get(name=name)
    QApplication.instance().project = project

def get_project() -> Project:
    project = QApplication.instance().project
    return project

def set_user(pseudo: str):
    user = User.objects.get(pseudo=pseudo)
    QApplication.instance().user = user

def get_user() -> User:
    user = QApplication.instance().user
    return user

def get_palette() -> Palette:
    palette = QApplication.instance().user.palette
    return palette

