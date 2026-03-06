from typing import Optional

from Api.document_models.studio_documents import Project
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.project_mvd.project_list_item_delegate import ProjectListItemDelegate
from Gui.mvd.project_mvd.project_list_model import ProjectListModel, ProjectItemRoles


class ProjectListView(AbstractListView):
    def __init__(self, single_click: bool=True):
        super().__init__()
        self.single_click = single_click  # hack to swap projects 1 by 1 in project settings
        self._model = ProjectListModel()
        self.setModel(self._model)

        self._item_delegate = ProjectListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    @property
    def projects(self) -> list[Project]:
        return self._model.projects

    def set_projects(self, projects: list[Project] = None):
        if projects is None:
            projects = Project.objects()
        self._model.populate(projects=projects)

    def get_project(self) -> Optional[Project]:
        index = self.get_selected_index()
        if index is None:
            return None
        project: Project = index.data(ProjectItemRoles.project)
        return project
