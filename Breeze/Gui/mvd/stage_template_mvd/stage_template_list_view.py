from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListView

from Api.document_models.project_documents import Asset
from Api.document_models.studio_documents import StageTemplate
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.stage_template_mvd.stage_template_list_item_delegate import StageTemplateListItemDelegate
from Gui.mvd.stage_template_mvd.stage_template_list_model import StageTemplateListModel, \
    StageTemplateItemRoles


class StageTemplateListView(AbstractListView):
    stage_selected = Signal()
    stage_data_modified = Signal()

    def __init__(self):
        super().__init__()
        self._model = StageTemplateListModel()
        self.setModel(self._model)

        self._item_delegate = StageTemplateListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.setSelectionMode(QListView.SelectionMode.MultiSelection)

        self._init_state()

    def refresh(self):
        selected_indexes = self.selectionModel().selectedIndexes()
        self._model.refresh()
        if selected_indexes:
            index = self._model.index(selected_indexes[0].row(), 0)
            self.select_row(row=index.row())
        self.viewport().update()

    def set_asset(self, asset: Asset=None):
        self.selectionModel().blockSignals(True)
        self._model.populate(stage_templates=StageTemplate.objects())
        self.selectionModel().blockSignals(False)

        if asset is None:
            return
        else:
            # TODO: show infos about already used stage templates for the selected asset
            pass

    @property
    def selected_stage_templates(self) -> list[StageTemplate]:
        selected_indexes = self.selectionModel().selectedIndexes()

        stage_templates = []
        for index in selected_indexes:
            item = self._model.item(index.row())
            stage_template = item.data(StageTemplateItemRoles.stage_template)
            stage_templates.append(stage_template)

        return stage_templates

    @property
    def stage_templates(self) -> list[StageTemplate]:
        return self._model.stage_templates

    def set_preset(self, preset: str):
        print(f"SET PRESET: {preset = }")
        for item in self._model.items:
            stage_template: StageTemplate = item.data(StageTemplateItemRoles.stage_template)
            self.select_row(row=item.row(), is_selected=preset in stage_template.presets)

    def save_preset(self, preset: str):
        selected_items = self.selected_items
        for item in self._model.items:
            stage_template: StageTemplate = item.data(StageTemplateItemRoles.stage_template)
            if item in selected_items:
                if preset not in stage_template.presets:
                    stage_template.presets.append(preset)
            else:
                if preset in stage_template.presets:
                    stage_template.presets.remove(preset)
            stage_template.save()


    def _init_state(self):
        # by default show stage templates without asset-related infos
        self.set_asset(asset=None)
