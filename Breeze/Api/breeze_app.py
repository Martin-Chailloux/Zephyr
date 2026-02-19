"""
A singleton that keeps track of the current Project, User and Palette.
It is meant to be freely modified.
"""
import gc
import subprocess
import sys
from datetime import timedelta

import mongoengine
import qdarkstyle
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

from Api.document_models.studio_documents import Project, User, Palette
from Utils.chronometer import Chronometer


class BreezeApp:
    project: Project = None
    user: User = None
    palette: Palette = None
    reloaded = Signal()

    @classmethod
    def set_project(cls, name: str):
        mongoengine.disconnect(alias="current_project")

        project = Project.objects.get(name=name)
        mongoengine.connect(host="mongodb://localhost:27017", db=project.name, alias="current_project")
        cls.project = project

    @classmethod
    def set_user(cls, pseudo: str):
        user = User.objects.get(pseudo=pseudo)
        cls.user = user
        cls.palette = user.palette
