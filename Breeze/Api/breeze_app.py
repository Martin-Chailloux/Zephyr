"""
A singleton that keeps track of the current Project, User and Palette.
It is meant to be freely modified.
"""

from Api.document_models.studio_documents import Project, User, Palette


class BreezeApp:
    project: Project = None
    user: User = None
    palette: Palette = None

    @classmethod
    def set_project(cls, name: str):
        project = Project.objects.get(name=name)
        cls.project = project

    @classmethod
    def set_user(cls, pseudo: str):
        user = User.objects.get(pseudo=pseudo)
        cls.user = user
        cls.palette = user.palette
