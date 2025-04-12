from datetime import datetime
from typing import Self
from xmlrpc.client import SafeTransport

from mongoengine import *

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

    @classmethod
    def create(cls, asset: Asset, stage_template: StageTemplate, status: Status=None, **kwargs) -> Self:
        longname = "_".join(s for s in [asset.longname, stage_template.name])
        kwargs = dict(longname=longname, asset=asset, stage_template=stage_template, status=status, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        stage = cls(**kwargs)
        stage.save()
        print(f"Created: {stage.__repr__()}")

        stage.append_to_asset()

        return stage

    def append_to_asset(self):
        if self in self.asset.stages:
            print(f"WARNING: {self.__repr__()} is already a stage of {self.asset.__repr__()}. Cannot append.")
            return

        self.asset.stages.append(self)
        self.asset.save()


class Collection(Document):
    """
    Belongs to a Stage. Contains Versions. \n
    Work Component: contains the working versions of a Stage. \n
    Export Component: contains the versions of an exported item. \n
    Ingredient: Version of a component that is used inside a Stage.
    """
    longname: str = StringField(required=True, primary_key=True)

    label: str = StringField(required=True)
    stage: Stage = ReferenceField(document_type=Stage, required=True)

    versions: list['Version'] = SortedListField(ReferenceField(document_type='Version'), default=[])
    recommended_version: 'Version' = ReferenceField(document_type='Version')

    meta = {
        'collection': 'Collections',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Component>: {self.longname}"

    @classmethod
    def create(cls, label: str, stage: Stage, extension: str):
        # TODO
        pass


class Version(Document):
    """
    Belongs to a Component. Has an increment number and a filepath. \n
    Ingredient: Version that is used inside a Stage.
    """
    longname = StringField(required=True, primary_key=True)

    collection: Collection = ReferenceField(document_type=Collection, required=True)
    number: int = IntField(required=True)  # -1 is head
    extension: str = StringField(required=True)  # blend, kra, png, jpg, mov, etc.
    filepath: str = StringField()  # deduced from upper documents

    creation_user: User = ReferenceField(document_type='User')

    destinations: list[Stage] = SortedListField(ReferenceField(document_type=Stage, default=[]))

    # creation_time = DateTimeField(default=datetime.utcnow())
    # last_user = ReferenceField(document_type='User')
    # last_time = DateTimeField(default=datetime.utcnow())

    # comment = StringField(default="")
    # todo_list = ReferenceField(document_type='Task', default=[])
    # thumbnail_path = StringField()

    meta = {
        'collection': 'Versions',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Version>: {self.longname}"
