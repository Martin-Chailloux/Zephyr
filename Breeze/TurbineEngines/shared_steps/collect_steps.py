from typing import Optional

from Api.document_models.project_documents import Version, Component, Asset
from Api.turbine.step import TurbineStep


class GetTemplateSceneStep(TurbineStep):
    label = "Get template scene"

    def __init__(self, category: str, name: str, variant: str, stage_template: str, version_number: int=None):
        super().__init__()
        self._category = category
        self._name = name
        self._variant = variant
        self._stage_template = stage_template
        self._version_number = version_number

        # outputs
        self.version: Version

    def _inner_run(self):
        asset: Asset = Asset.objects(category=self._category, name=self._name, variant=self._variant)
        if not asset:
            raise ValueError(f"Asset not found with: {self._category = }, {self._name = }, {self._variant = }")
        asset = asset[0]
        stage = asset.get_stage(name=self._stage_template)
        self.logger.debug(f"{stage.get_work_component() = }")

        if self._version_number is not None:
            version = stage.get_work_component().get_version(number=self._version_number)
        else:
            version = stage.get_work_component().get_last_version()

        self.version = version
        self.logger.debug(f"{self.version = }")
