import subprocess
import tkinter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Self, Optional

import mongoengine
from mongoengine import *

from Api.breeze_app import BreezeApp
from Api.document_models.studio_documents import Status, User, Software, Process, StageTemplate
from abstract_io import AbstractSoftwareFile
from blender_file import BlenderFile


class Asset(Document):
    """
    An element from the film. Contains stages.
    category ⮞ name ⮞ variant
    """
    longname: str = StringField(required=True, primary_key=True)

    category: str = StringField(required=True)
    name: str = StringField(required=True)
    variant: str = StringField(default="-")

    stages: list['Stage'] = ListField(ReferenceField(document_type='Stage'), default=[])

    meta = {
        'collection': 'Assets',
        'db_alias': 'current_project'
    }

    def __repr__(self):
        return f"<Asset>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, category: str, name : str, variant: str = None, **kwargs) -> Self:
        v = variant or "-"  # pre-compute the longname using the default variant value if it is None
        longname = "_".join(s for s in [category, name, v])
        kwargs = dict(name=name, category=category, variant=variant, longname=longname, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        asset = cls(**kwargs)
        asset.save()
        print(f"Created: {asset}")
        return asset

    def add_stage(self, stage: 'Stage'):
        if stage in self.stages:
            raise ValueError(f"{stage} is already a stage of {self}")
        self.stages.append(stage)
        self.save()


class Stage(Document):
    """
    Step in the creation of an asset, based on a StageTemplate
    (ex: modeling, rigging, animation, lighting, etc.) \n
    Contains a single Component 'Work', and multiple export Components.
    """
    longname: str = StringField(required=True, primary_key=True)
    asset: Asset = ReferenceField(document_type=Asset)
    stage_template: StageTemplate = ReferenceField(document_type=StageTemplate)

    components: list['Component'] = ListField(ReferenceField(document_type='Component'), default=[])
    work_component: 'Component' = ReferenceField(document_type='Component')

    status: Status = ReferenceField(document_type=Status, default=Status.objects.get(label='WAIT'))
    # TODO: User unknown, with a question mark icon
    #  it should appear first in lists, add User.order to have some special users at -1
    user: User = ReferenceField(document_type=User, default=User.objects.get(pseudo="Martin"))

    ingredients: dict[str, list['Version']] = DictField()  # {name: list[Versions]}

    meta = {
        'collection': 'Stages',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Stage>: {self.longname}'"

    def __str__(self):
        return self.__repr__()

    def create_component(self, name: str, label: str, crash_if_exists: bool = True) -> 'Component':
        component = Component.objects(name=name, label=label, stage=self)
        if len(component) == 1:
            if crash_if_exists:
                raise ValueError(f"{component} is already a component of {self}")
            else:
                return component[0]

        component = Component.create(name=name, label=label, stage=self)
        self.components.append(component)
        self.save()
        return component

    @classmethod
    def create(cls, asset: Asset, stage_template: StageTemplate, status: Status=None, **kwargs) -> Self:
        longname = "_".join(s for s in [asset.longname, stage_template.name])
        kwargs = dict(longname=longname, asset=asset, stage_template=stage_template, status=status, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        stage = cls(**kwargs)

        stage.update(work_component=stage.create_component(name="work", label="Work"))

        asset.add_stage(stage=stage)

        print(f"Created: {stage}")

        return stage

    def add_ingredient(self, name: str, version: 'Version'):
        if name not in self.ingredients.keys():
            self.ingredients[name] = []
        self.ingredients[name].append(version)
        self.save()
        self.sort_ingredients()
        print(f"{version} was added to the '{name}' ingredients of {self}")

    def replace_ingredient(self, name: str, old_version: 'Version', new_version: 'Version'):
        if name not in self.ingredients.keys():
            raise ValueError(f"Existing ingredients with name {name} not found in {self}")

        versions = self.ingredients[name]
        if old_version not in versions:
            raise ValueError(f"Did not find {old_version} in the ingredients {name} of {self}")
        versions.remove(old_version)
        versions.append(new_version)

        self.ingredients[name] = versions
        self.save()
        self.sort_ingredients()
        print(f"{new_version} replaced {old_version} in the '{name}' ingredients of {self}")

    def sort_ingredients(self):
        sorted_ingredients: dict[str, list[Version]] = {}

        # sort names
        names = [name for name in self.ingredients.keys()]
        names.sort()
        if 'extra' in names:
            names.remove('extra')
            names.append('extra')

        # sort versions
        for name in names:
            versions = self.ingredients[name]
            versions = sorted(versions, key=lambda version: (
                version.component.stage.stage_template.name,
                version.longname,
                version.number,
            ))
            sorted_ingredients[name] = versions

        # update
        self.ingredients = sorted_ingredients
        self.save()


class Component(Document):
    """
    Belongs to a Stage. Contains Versions. \n
    Work Component: contains the working versions of a Stage. \n
    Export Component: contains the versions of an exported item. \n
    Ingredient: Version of a component that is used inside a Stage.
    """
    longname: str = StringField(required=True, primary_key=True)  # category_name_variant_stage_component

    name: str = StringField(required=True, unique_with='stage')  # unique_with seems to not be working as intended
    label: str = StringField(required=True)
    stage: Stage = ReferenceField(document_type=Stage, required=True)

    versions: list['Version'] = SortedListField(ReferenceField(document_type='Version'), default=[])
    recommended_version: 'Version' = ReferenceField(document_type='Version', default=None)

    meta = {
        'collection': 'Components',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Component>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, name: str, label: str, stage: Stage, **kwargs):
        longname = "_".join(s for s in [stage.longname, name])
        kwargs = dict(longname=longname, name=name, label=label, stage=stage, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        existing_component = Component.objects(longname=longname)
        if existing_component:
            raise FileExistsError(f"{existing_component[0]}")

        component = cls(**kwargs)
        component.save()
        print(f"Created: {component}")

        return component

    def add_version(self, version: 'Version'):
        if version in self.versions:
            raise ValueError(f"{version} is already a version of {self}")
        self.versions.append(version)
        self.save()

    def create_last_version(self, software: Software) -> 'Version':
        versions: list[Version] = self.versions
        if not versions:
            number = 1
        else:
            versions = sorted(versions, key=lambda v: v.number, reverse=True)
            number: int = versions[0].number
            number += 1

        version = Version.create(component=self, number=number, software=software)
        return version

    def create_version(self, number: int, software: Software):
        version = Version.create(component=self, number=number, software=software)
        return version

    def get_last_version(self) -> Optional['Version']:
        versions: list[Version] = self.versions
        if not versions:
            return None
        else:
            versions = sorted(versions, key=lambda v: v.number, reverse=True)
            return versions[0]

    def get_version(self, number: int) -> Optional['Version']:
        versions = [v for v in self.versions if v.number == number]
        if not versions:
            return None
        elif len(versions) > 1:  # this should not be possible
            raise ValueError(f"Found more than 1 version with number {number}: {versions}")
        else:
            return versions[0]


class Version(Document):
    """
    Belongs to a Component. Has an increment number and a filepath. \n
    Ingredient: Version that is used inside a Stage.
    """
    longname = StringField(required=True, primary_key=True)

    component: Component = ReferenceField(document_type=Component, required=True)
    number: int = IntField(required=True)  # -1 is head
    software: Software = ReferenceField(document_type=Software, required=True)

    # deduced from upper documents
    filepath: str = StringField(required=True)

    creation_user: User = ReferenceField(document_type=User, required=True)
    last_user: User = ReferenceField(document_type=User, required=True)

    destinations: list[Stage] = SortedListField(ReferenceField(document_type=Stage, default=[]))

    # user editable
    comment: str = StringField(default="")

    creation_time = DateTimeField(default=datetime.now)
    timestamp = DateTimeField(default=datetime.now)

    # todo_list = ReferenceField(document_type='Task', default=[])
    # thumbnail_path = StringField()

    meta = {
        'collection': 'Versions',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Version>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, component: Component, number: int, software: Software, **kwargs):
        extension = software.extension

        longname = f"{component.longname}_{number:03d}.{extension}"
        existing_version = Version.objects(longname=longname)
        if existing_version:
            raise InvalidDocumentError(f"Version already exists: {existing_version[0]}")

        creation_user = BreezeApp.user
        last_user = creation_user

        # get filepath
        subfolders = component.longname.split("_")
        filepath = Path(BreezeApp.project.root_path).joinpath(*subfolders).joinpath(longname)

        # create dirs
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        # create document
        kwargs = dict(longname=longname, component=component, number=number, software=software,
                      creation_user=creation_user, last_user=last_user, filepath=str(filepath),
                      **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        version = cls(**kwargs)
        version.save()

        # add to component
        component.add_version(version)

        print(f"Created: {version}")
        return version

    def open_folder(self):
        print(f"Opening in explorer ... '{self.filepath}'")
        subprocess.Popen(f'explorer /select,{self.filepath}')

    def copy_filepath(self):
        """source: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard"""

        print(f"Copying to clipboard ... '{self.filepath}'")
        r = tkinter.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.filepath)
        r.update()  # now it stays on the clipboard after the window is closed
        r.destroy()

    def to_file(self) -> AbstractSoftwareFile:
        if self.software.label == 'Blender':
            return BlenderFile(filepath=self.filepath)
        else:
            raise NotImplementedError(f"File instance for: {self.software}")

    def get_filter_keys(self) -> str:
        """ returns a string of keys used with search bars to filter a list of versions """
        # TODO: it does not work with users
        #  convert date to something that makes sense to write (actual format: 2025-07-13 19:03:53.368000)
        keys = [
            f"{self.number:03d}",
            self.creation_user.pseudo,
            self.creation_user.fullname,
            self.last_user.pseudo,
            self.last_user.fullname,
            self.software.extension,
            str(self.timestamp),
        ]
        result = " ".join(s for s in keys)
        return result


@dataclass
class JobContext:
    user: User
    component: Component
    version: Optional[Version]
    creation_time: datetime = field(default_factory=datetime.now)  # creation_time = datatime.now() would only update on first import

    def set_component(self, component: Component):
        self.component = component

    def set_version(self, version: Version = None):
        self.version = version

    def update_creation_time(self):
        self.creation_time = datetime.now()


class Job(Document):
    longname: str = StringField(required=True, primary_key=True) # name + date
    user: User = ReferenceField(document_type=User, required=True)
    creation_time = DateTimeField(default=datetime.now)
    source_process: Process = ReferenceField(document_type=Process, required=True)
    source_version: Version = ReferenceField(document_type=Version, required=True)
    steps: dict = DictField(required=True)
    inputs: list[dict] = ListField(DictField(), default=[])

    meta = {
        'collection': 'Jobs',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Job>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, source_process: Process, context: JobContext, steps: dict[str, any], inputs: list[dict[str, any]], **kwargs) -> Self:
        longname = " ".join(s for s in [source_process.longname, context.version.longname, context.user.pseudo, str(context.creation_time)])
        kwargs = dict(longname=longname, creation_time=context.creation_time, user=context.user,
                      source_process=source_process, source_version=context.version,
                      steps=steps, inputs=inputs, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        process = cls(**kwargs)
        process.save()
        print(f"Created: {process}")

        return process


# ------------------------
# Delete rules
# ------------------------

# Asset
Stage.register_delete_rule(Asset, 'stages', mongoengine.PULL)

# StageTemplate
Software.register_delete_rule(StageTemplate, 'software', mongoengine.DENY)

# Stage
Asset.register_delete_rule(Stage, 'asset', mongoengine.CASCADE)
StageTemplate.register_delete_rule(Stage, 'stage_template', mongoengine.DENY)
Component.register_delete_rule(Stage, 'components', mongoengine.PULL)
Component.register_delete_rule(Stage, 'work_component', mongoengine.DENY)
Version.register_delete_rule(Stage, 'ingredients', mongoengine.DENY)
Status.register_delete_rule(Stage, 'status', mongoengine.DENY)
User.register_delete_rule(Stage, 'user', mongoengine.DENY)

# Component
Stage.register_delete_rule(Component, 'stage', mongoengine.CASCADE)
Version.register_delete_rule(Component, 'versions', mongoengine.PULL)
Version.register_delete_rule(Component, 'recommended_version', mongoengine.NULLIFY)

# Version
Component.register_delete_rule(Version, 'component', mongoengine.CASCADE)
Software.register_delete_rule(Version, 'software', mongoengine.DENY)
User.register_delete_rule(Version, 'creation_user', mongoengine.DENY)
User.register_delete_rule(Version, 'last_user', mongoengine.DENY)
Stage.register_delete_rule(Version, 'destinations', mongoengine.PULL)

# Job
User.register_delete_rule(Job, 'user', mongoengine.DENY)
Process.register_delete_rule(Job, 'source_process', mongoengine.CASCADE)
Version.register_delete_rule(Job, 'source_version', mongoengine.CASCADE)
