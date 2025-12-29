import subprocess
from datetime import datetime
from pathlib import Path
from typing import Self, Optional, Any

import mongoengine
from mongoengine import *

from Api import data, utils
from Api.breeze_app import BreezeApp
from Api.document_models.studio_documents import Status, User, Software, Process, StageTemplate
from software_base import AbstractSoftwareFile
from Blender.blender_file import BlenderFile


class Asset(Document):
    """
    An element from a project. It is made of a category, a name and variant.
    For every combination of _category + name_, there is always a default variant `-` .

    Examples: `character_Gabin_-`, `set_Playground_broken`, `element_tree_B`, `element_tree_C`,
    `sequence_sq0020_sh0180`, `library_lightrigs_master`, `sandbox_vfx_boom`
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
        longname = "_".join(s for s in [category, name, variant or "-"])
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

    def get_stage(self, name: str) -> 'Stage':
        stage = [stage for stage in self.stages if stage.stage_template.name == name]
        if not stage:
            raise ValueError(f"Stage '{name}' not found in the stages of {self}: {self.stages = }")
        return stage[0]


class Stage(Document):
    """
    A step during the creation of an Asset.
    Uses Components as ingredients, and exports other Components.
    It always has a `work` Component that contains work software files.
    """
    longname: str = StringField(required=True, primary_key=True)
    asset: Asset = ReferenceField(document_type=Asset)
    stage_template: StageTemplate = ReferenceField(document_type=StageTemplate)

    components: list['Component'] = ListField(ReferenceField(document_type='Component'), default=[])

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

    @classmethod
    def create(cls, asset: Asset, stage_template: StageTemplate, status: Status=None, **kwargs) -> Self:
        longname = "_".join(s for s in [asset.longname, stage_template.name])
        kwargs = dict(longname=longname, asset=asset, stage_template=stage_template, status=status, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        stage = cls(**kwargs)
        stage.save()
        print(f"Created: {stage}")

        asset.add_stage(stage=stage)

        return stage

    def create_component(self, name: str, label: str, extension: str, crash_if_exists: bool = True) -> 'Component':
        component = Component.objects(name=name, label=label, extension=extension, stage=self)
        if len(component) == 1:
            if crash_if_exists:
                raise ValueError(f"{component} is already a component of {self}")
            else:
                return component[0]

        component = Component.create(name=name, label=label, stage=self, extension=extension)
        self.components.append(component)
        self.save()
        return component

    def create_work_component(self, extension: str) -> 'Component':
        work_component = self.create_component(name=data.Components.work, label=data.Components.work.title(), extension=extension)
        return work_component

    def get_work_components(self) -> list['Component']:
        work_components = [c for c in self.components if c.name == 'work']
        return work_components

    def get_work_component(self, extension: str=None) -> Optional['Component']:
        work_components = self.get_work_components()
        match len(work_components):
            case 0:
                return None
            case 1:
                return work_components[0]
            case _:
                if extension is None:  # get last used work component
                    work_components = sorted(work_components, key=lambda c: c.get_last_version().timestamp)
                    return work_components[0]
                else:  # get component with matching extension
                    for component in work_components:
                        if component.extension == extension:
                            return component
                    else:
                        return None

    def add_ingredient(self, name: str, version: 'Version'):
        if name not in self.ingredients.keys():
            self.ingredients[name] = []
        self.ingredients[name].append(version)
        self.save()
        self._sort_ingredients()
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
        self._sort_ingredients()
        print(f"{new_version} replaced {old_version} in the '{name}' ingredients of {self}")

    def _sort_ingredients(self):
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
    An independent building component of the project.
    It contains multiple Versions.
    It is exported from a Stage and becomes the ingredient of another Stage.

    Examples: `geo`, `rig`, `anim`, etc...
    """
    longname: str = StringField(required=True, primary_key=True)  # category_name_variant_stage_component

    name: str = StringField(required=True)
    label: str = StringField(required=True)
    extension: str = StringField()

    stage: Stage = ReferenceField(document_type=Stage, required=True)

    versions: list['Version'] = SortedListField(ReferenceField(document_type='Version'), default=[])
    recommended_version: 'Version' = ReferenceField(document_type='Version', default=None)

    # TODO: destinations: list[Stage], reciprocal with Stage.components

    meta = {
        'collection': 'Components',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Component>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, name: str, label: str, stage: Stage, extension: str, **kwargs):
        longname = "_".join(s for s in [stage.longname, name, extension])
        kwargs = dict(longname=longname, name=name, label=label, stage=stage, extension=extension, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        existing_component = Component.objects(longname=longname)
        if existing_component:
            raise FileExistsError(f"{existing_component[0]}")

        component = cls(**kwargs)
        component.save()
        print(f"Created: {component}")

        return component

    def to_folders(self) -> list[str]:
        """ returns a folder's hierarchy based on its fields """
        folders = self.longname.split("_")  # [character, baby, -, modeling, work, blend]
        del folders[-1]  # [character, baby, -, modeling, work]
        folders[-1] = f"{folders[-1]}_{self.extension}"  # [character, baby, -, modeling, work_blend]
        return folders

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

    def create_version(self, number: int, software: Software) -> 'Version':
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

    def get_software(self) -> Optional[Software]:
        software = Software.from_extension(extension=self.extension)
        return software


class Version(Document):
    """
    An iteration of a file.
    """
    longname = StringField(required=True, primary_key=True)

    component: Component = ReferenceField(document_type=Component, required=True)
    number: int = IntField(required=True)  # -1 is head

    # TODO: remove and replace with Component.get_software() -> Optional[Software], that uses Component.extension
    software: Software = ReferenceField(document_type=Software, required=True)  # strange to have in exports

    # deduced from upper documents
    filepath: str = StringField(required=True)

    creation_user: User = ReferenceField(document_type=User, required=True)
    last_user: User = ReferenceField(document_type=User, required=True)

    # user editable
    comment: str = StringField(default="")

    creation_time = DateTimeField(default=datetime.now)
    timestamp = DateTimeField(default=datetime.now)
    destinations: list[Stage] = SortedListField(ReferenceField(document_type=Stage, default=[]))

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
        longname = f"{component.longname}_{number:03d}"
        existing_version = Version.objects(longname=longname)
        if existing_version:
            raise InvalidDocumentError(f"Version already exists: {existing_version[0]}")

        creation_user = BreezeApp.user
        last_user = creation_user

        # get filepath
        root = BreezeApp.project.root_path
        filename = f"{longname}.{component.extension}"
        filepath = Path(root).joinpath(*component.to_folders()).joinpath(filename)

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

    def set_comment(self, text: str):
        old_comment = self.comment
        self.update(comment=text)
        print(f"{self}'s comment changed from '{old_comment}' to '{text}'")

    def increment(self, comment: str = "") -> Self:
        print(f"Incrementing {self} ... ")
        new_version = self.component.create_last_version(software=self.software)
        new_version.update(comment=comment)
        return new_version

    def open_folder(self):
        print(f"Opening in explorer ... '{self.filepath}'")
        subprocess.Popen(f'explorer /select,{self.filepath}')

    def copy_longname(self):
        utils.copy_to_clipboard(text=self.longname)

    def copy_filepath(self):
        utils.copy_to_clipboard(text=self.filepath)

    def to_file(self) -> AbstractSoftwareFile:
        software = self.component.get_software()
        match software.extension:
            case data.Extensions.blend:
                return BlenderFile(filepath=self.filepath)
            case _:
                raise NotImplementedError(f"File instance for: {software}")

    def open_interactive(self)-> AbstractSoftwareFile:
        file = self.to_file()
        file.open_interactive()
        print(f"Opening an interactive {self.software.label} file: {self.filepath}")
        return file

    def open_background(self)-> AbstractSoftwareFile:
        file = self.to_file()
        file.open()
        print(f"Opening a background {self.software.label} file: {self.filepath}")
        return file

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
            self.component.extension or '-',
            str(self.timestamp),
        ]
        result = " ".join(s for s in keys)
        return result


class Job(Document):
    """ An Engine's instance """
    longname: str = StringField(required=True, primary_key=True) # name + date
    user: User = ReferenceField(document_type=User, required=True)
    creation_time = DateTimeField(default=datetime.now)
    source_process: Process = ReferenceField(document_type=Process, required=True)
    source_version: Version = ReferenceField(document_type=Version, required=True)
    steps: dict[str, any] = DictField(required=True)
    inputs: dict[str, Any] = DictField()  # dict[name: widget_infos]

    meta = {
        'collection': 'Jobs',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Job>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, source_process: Process, steps: dict[str, any], inputs: dict[str, any],
               user: User, version: Version, creation_time: datetime,
               **kwargs) -> Self:
        longname = " ".join(s for s in [source_process.longname, version.longname, user.pseudo, str(creation_time)])
        kwargs = dict(longname=longname, creation_time=creation_time, user=user,
                      source_process=source_process, source_version=version,
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
Component.register_delete_rule(Stage, 'work_component', mongoengine.NULLIFY)
Version.register_delete_rule(Stage, 'ingredients', mongoengine.DENY)  # might not be working, because there Versions are dict values
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
