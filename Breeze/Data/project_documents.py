from datetime import datetime
from typing import Self
from xmlrpc.client import SafeTransport

from mongoengine import *

from Data import app_dialog
from Data.studio_documents import Status, User, Software


class Asset(Document):
    """
    An element from the film. Contains stages.
    category > name > variant
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

    @classmethod
    def create(cls, category: str, name : str, variant: str = None, **kwargs) -> Self:
        v = variant or "-"  # pre-compute the longname using the default variant value if it is None
        longname = "_".join(s for s in [category, name, v])
        kwargs = dict(name=name, category=category, variant=variant, longname=longname, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        asset = cls(**kwargs)
        asset.save()
        print(f"Created: {asset.__repr__()}")
        return asset

    def add_stage(self, stage: 'Stage'):
        if stage in self.stages:
            raise ValueError(f"{stage.__repr__()} is already a stage of {self.__repr__()}")
        self.stages.append(stage)
        self.save()


class StageTemplate(Document):
    """
    Infos about a specific kind of stage: \n
    name, label, description, color, icon
    """
    name: str = StringField(required=True, primary_key=True)
    label: str = StringField(required=True, unique=True)

    color: str = StringField(default="#ffffff")
    icon_name: str = StringField(default="fa5s.question")

    software: list[Software] = SortedListField(ReferenceField(document_type=Software), default=[])
    presets: list[str] = ListField(StringField(), default=[])  # TODO: a db to register presets would be easier to edit

    meta = {
        'collection': 'Stage templates',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Stage template>: {self.name}"

    # NOTE: no GUI for now
    @classmethod
    def create(cls, name: str, label: str, color: str = None, icon_name: str = None, **kwargs) -> Self:
        kwargs = dict(name=name, label=label, color=color, icon_name=icon_name, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        stage_template = cls(**kwargs)
        stage_template.save()
        print(f"Created: {stage_template.__repr__()}")
        return stage_template


class Stage(Document):
    """
    Step in the creation of an asset, based on a StageTemplate
    (ex: modeling, rigging, animation, lighting, etc.) \n
    Contains a Collection 'Work', and export Collections.
    """
    longname: str = StringField(required=True, primary_key=True)
    asset: Asset = ReferenceField(document_type=Asset)
    stage_template: StageTemplate = ReferenceField(document_type=StageTemplate)

    collections: list['Collection'] = ListField(ReferenceField(document_type='Collection', default=[]))
    ingredients: list['Version'] = ListField(ReferenceField(document_type='Version'), default=[])
    status: Status = ReferenceField(document_type=Status, default=Status.objects.get(label='WAIT'))
    user: User = ReferenceField(document_type=User, default=User.objects.get(pseudo="Martin"))

    meta = {
        'collection': 'Stages',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Stage>: {self.longname}'"

    def add_collection(self, collection: 'Collection'):
        if collection in self.collections:
            raise ValueError(f"{collection.__repr__()} is already a collection of {self.__repr__()}")
        self.collections.append(collection)
        self.save()

    def create_collection(self, name: str, label: str) -> 'Collection':
        collection = Collection.create(name=name, label=label, stage=self)
        self.add_collection(collection)
        return collection

    def create_work_collection(self) -> 'Collection':
        collection = self.create_collection(name="work", label="Work")
        return collection

    @classmethod
    def create(cls, asset: Asset, stage_template: StageTemplate, status: Status=None, **kwargs) -> Self:
        longname = "_".join(s for s in [asset.longname, stage_template.name])
        kwargs = dict(longname=longname, asset=asset, stage_template=stage_template, status=status, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        stage = cls(**kwargs)
        stage.save()
        print(f"Created: {stage.__repr__()}")

        asset.add_stage(stage=stage)
        stage.create_work_collection()

        return stage


class Collection(Document):
    """
    Belongs to a Stage. Contains Versions. \n
    Work Component: contains the working versions of a Stage. \n
    Export Component: contains the versions of an exported item. \n
    Ingredient: Version of a component that is used inside a Stage.
    """
    longname: str = StringField(required=True, primary_key=True)

    name: str = StringField(required=True, unique_with='stage')  # unique_with seems to not be working as intended
    label: str = StringField(required=True)
    stage: Stage = ReferenceField(document_type=Stage, required=True)

    versions: list['Version'] = SortedListField(ReferenceField(document_type='Version'), default=[])
    recommended_version: 'Version' = ReferenceField(document_type='Version')

    meta = {
        'collection': 'Collections',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Collection>: {self.longname}"

    @classmethod
    def create(cls, name: str, label: str, stage: Stage, **kwargs):
        longname = "_".join(s for s in [stage.longname, name])
        kwargs = dict(longname=longname, name=name, label=label, stage=stage, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        existing_collection = Collection.objects(longname=longname)
        if existing_collection:
            raise FileExistsError(f"{existing_collection[0].__repr__()}")

        collection = cls(**kwargs)
        collection.save()
        print(f"Created: {collection.__repr__()}")

        return collection

    def add_version(self, version: 'Version'):
        if version in self.versions:
            raise ValueError(f"{version.__repr__()} is already a version of {self.__repr__()}")
        self.versions.append(version)
        self.save()

    def create_last_version(self, extension: str) -> 'Version':
        versions: list[Version] = self.versions
        if not versions:
            number = 1
        else:
            versions = sorted(versions, key=lambda v: v.number, reverse=True)
            number: int = versions[0].number + 1

        version = Version.create(collection=self, number=number, extension=extension)
        return version


class Version(Document):
    """
    Belongs to a Component. Has an increment number and a filepath. \n
    Ingredient: Version that is used inside a Stage.
    """
    longname = StringField(required=True, primary_key=True)

    collection: Collection = ReferenceField(document_type=Collection, required=True)
    number: int = IntField(required=True)  # -1 is head
    extension: str = StringField(required=True)  # blend, kra, png, jpg, mov, etc.

    # deduced from upper documents
    label: str = StringField(required=True)  # TODO: sert à rine on le compute dans le delegate directement
    filepath: str = StringField(required=True)

    creation_user: User = ReferenceField(document_type='User', required=True)
    last_user: User = ReferenceField(document_type='User', required=True)

    destinations: list[Stage] = SortedListField(ReferenceField(document_type=Stage, default=[]))

    # TODO: set delete_rules
    # TODO: test timestamp related methods
    # TODO: compute_filepath and create Path architecture
    # TODO: work / publish ?
    # creation_timestamp = DateTimeField(default=datetime.utcnow())
    # last_timestamp = DateTimeField(default=datetime.utcnow())

    # comment = StringField(default="")
    # todo_list = ReferenceField(document_type='Task', default=[])
    # thumbnail_path = StringField()

    meta = {
        'collection': 'Versions',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Version>: {self.longname}"

    @classmethod
    def create(cls, collection: Collection, number: int, extension: str, **kwargs):
        longname = f"{collection.longname}_{number:03d}.{extension}"

        filepath = ""  # TODO
        label = f"{collection.name}_{number}.{extension}"
        creation_user = app_dialog.get_user()
        last_user = creation_user

        kwargs = dict(longname=longname, collection=collection, number=number, extension=extension,
                      filepath=filepath, label=label,
                      creation_user=creation_user, last_user=last_user,
                      **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        existing_version = Version.objects(longname=longname)
        if existing_version:
            raise FileExistsError(f"{existing_version[0].__repr__()}")

        version = cls(**kwargs)
        version.save()
        print(f"Created: {version.__repr__()}")
        collection.add_version(version)
        return version
