from typing import Optional

from Api.project_documents import Version
from Api.studio_documents import User
from Api.turbine import StepBase, ProcessBase


class AddSceneStep(StepBase):
    label = "Add Scene"
    tooltip = "adds a scene"

    def __init__(self, name: str):
        super().__init__()
        self.scene_name = name

    def _inner_run(self, **kwargs):
        self.add_step(AddMusicStep())


class AddMusicStep(StepBase):
    label = "Add Music"
    tooltip = "adds a music"

    def __init__(self):
        super().__init__()
        self.length: Optional[int] = None

    def run(self, length: int):
        super().run(length=length)

    def _inner_run(self, length: int):
        self.length = length
        print(f"{length = }")


class CreateMovie(ProcessBase):
    name: str = "create_movie"
    label: str = "Create Movie"
    tooltip: str = "demo process"

    def __init__(self, user: User, version: Version):
        super().__init__(user=user, version=version)
        print(f"CREATE MOVIE ...")

        # declare steps
        self.add_scene_steps: list[AddSceneStep] = []
        for name in ["Scene A", "Scene B"]:
            self.add_scene_steps.append(AddSceneStep(name=name))
        self.add_music_step = AddMusicStep()

        # add steps
        self.add_steps([
            *self.add_scene_steps,
            self.add_music_step,
        ])

    def _inner_run(self):
        # run steps
        for step in self.add_scene_steps:
            step.run()
        self.add_music_step.run(length=12)

