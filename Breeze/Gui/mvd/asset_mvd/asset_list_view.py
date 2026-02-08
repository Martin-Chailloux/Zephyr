from PySide6.QtCore import Signal, QItemSelectionModel

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import Asset, SubUser
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.asset_mvd.asset_list_item_delegate import AssetListItemDelegate
from Gui.mvd.asset_mvd.asset_list_model import AssetListModel, AssetItemRoles
from Gui.mvd.asset_mvd.asset_list_model import AssetItemMetrics


class AssetListView(AbstractListView):
    asset_selected = Signal()
    asset_data_modified = Signal()

    def __init__(self):
        super().__init__()
        self._set_model()
        self._set_delegate()

        self._connect_signals()

    def _set_model(self):
        self._model = AssetListModel()
        self.setModel(self._model)

    def _set_delegate(self):
        self._item_delegate = AssetListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def refresh(self):
        selected_indexes = self.selectionModel().selectedIndexes()
        self._model.refresh()

        if selected_indexes:
            index = self._model.index(selected_indexes[0].row(), 0)
            self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.Select)

    def set_assets(self, assets: list[Asset]):
        self.selectionModel().blockSignals(True)
        self._model.populate(assets=assets)
        self.selectionModel().blockSignals(False)

    @property
    def asset(self) -> Asset | None:
        selected_indexes = self.selectionModel().selectedIndexes()
        if not selected_indexes:
            return None

        selected_index = selected_indexes[0]
        selected_item = self._model.item(selected_index.row())
        if selected_item is None:
            return None

        current_asset: Asset = selected_item.data(AssetItemRoles.asset)
        return current_asset

    def select_asset(self, asset: Asset = None):
        if asset is None:
            self.selectionModel().clearSelection()
            return

        for row in range(self._model.rowCount()):
            index = self._model.index(row, 0)
            if asset == index.data(AssetItemRoles.asset):
                self.select_row(row)

    def _connect_signals(self):
        super()._connect_signals()
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        self.asset_selected.emit()

    def _set_hover_data(self, edit: bool=False):
        self._model.clear_hover_data()

        index = self._get_hovered_index()
        item = self._model.itemFromIndex(index)

        if index is None or item is None:
            return

        mouse_position = self._get_mouse_pos()
        x, y, w, h = self._get_viewport_rect()
        bookmark_x = x + AssetItemMetrics.height

        can_bookmark = bookmark_x > mouse_position.x()
        item.setData(can_bookmark, AssetItemRoles.can_bookmark)

    def mousePressEvent(self, event):
        index = self._get_hovered_index()
        if index.data(AssetItemRoles.can_bookmark):
            sub_user = SubUser.from_pseudo(pseudo=BreezeApp.user.pseudo)
            asset = index.data(AssetItemRoles.asset)
            is_bookmarked = asset in sub_user.bookmarks
            sub_user.set_bookmark(asset=asset, add=not is_bookmarked)
            self.update(index)
            self.asset_data_modified.emit()
        else:
            super().mousePressEvent(event)
