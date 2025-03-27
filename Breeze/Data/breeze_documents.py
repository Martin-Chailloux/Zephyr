from datetime import datetime
from mongoengine import *


class Project(Document):
    #TODO: The database matches a single project : no need to have a project document model
    #  -> Replace with a json that saves the project's settings
    #  -> Same for users: they are related to a project
    # There should be a database that contains every project, with related users, etc
    name = StringField(required=True, unique=True)
    categories = SortedListField(StringField(), default = ["Characters", "Decors", "Elements", "Props", "Shots"])
    users = SortedListField(StringField(), default = ["Martin", "Kim", "Elise", "Chloé", "Hugo", "Camille"])

    meta = {
        'collection': 'Projects'
    }

    def __repr__(self):
        return f"<Project>: name ='{self.name}'"

    def add_category(self, new_categories: str | list[str]):
        if type(new_categories) is str:
            new_categories = [new_categories]

        categories = list(self.categories)
        categories.extend(new_categories)

        self.categories = categories
        self.save()


class Asset(Document):
    """
    Category + Name + Variant. Contains stages.
    """
    longname = StringField(required=True, primary_key=True)

    category = StringField(required=True)
    name = StringField(required=True)
    variant = StringField(default="-")

    stages = ListField(ReferenceField(document_type='Stage'), default=[])

    meta = {
        'collection': 'Assets'
    }

    def __repr__(self):
        return f"<Asset>: {self.longname}]"


class StageTemplate(Document):
    """
    Template for a Stage. \n
    Infos: name, label, description, color, icon
    """
    name = StringField(required=True, primary_key=True)
    label = StringField(required=True, unique=True)
    tooltip = StringField(default="")

    color = StringField(default="#ffffff")
    icon_name = StringField(default="fa5s.question")

    presets = ListField(StringField(), default=[])

    meta = {
        'collection': 'Stage templates'
    }

    def __repr__(self):
        return f"<Stage template>: {self.name}"


class Stage(Document):
    """
    Belongs to an Asset. Working step in its utilisation.
    (ex: modeling, rigging, animation, lighting, etc.) \n
    Is based on a StageTemplate. \n
    Contains a Work Component, and Exports Components.
    """
    longname = StringField(required=True, primary_key=True)
    asset = ReferenceField(document_type=Asset)
    stage_template = ReferenceField(document_type=StageTemplate)

    components = ListField(ReferenceField(document_type='Component', default=[]))  # TODO: migration ?
    ingredients = ListField(ReferenceField(document_type='Versions'), default=[]) # TODO: migration ?

    meta = {
        'collection': 'Stages'
    }

    def __repr__(self):
        return f"<Stage>: {self.longname}'"

    def append_to_asset(self):
        if self in self.asset.stages:
            print(f"WARNING: {self.__repr__()} is already a stage of {self.asset.__repr__()}. Cannot append.")
            return

        self.asset.stages.append(self)
        self.asset.save()


class Component(Document):
    """
    Belongs to a Stage. Contains Versions. \n
    Work Component: contains the working versions of a Stage. \n
    Export Component: contains the versions of an exported item. \n
    Ingredient: Version of a component that is used inside a Stage.
    """
    longname = StringField(required=True, primary_key=True)

    name = StringField(required=True)
    label = StringField(required=True)
    description = StringField(required=True)
    extension = StringField(required=True)

    stage = ReferenceField(document_type=Stage, required=True)
    versions = ListField(ReferenceField(document_type='Version'), default=[])
    head_version = ReferenceField(document_type='Version')

    destinations = ListField(ReferenceField(document_type=Stage, default=[]))

    meta = {
        'collection': 'Components'
    }

    def __repr__(self):
        return f"<Component>: {self.longname}"


class Version(Document):
    """
    Belongs to a Component. Has an increment number and a filepath. \n
    Ingredient: Version that is used inside a Stage.
    """
    longname = StringField(required=True, primary_key=True)

    source = ReferenceField(document_type=Component, required=True)

    number = IntField(required=True)
    filepath = IntField(required=True)

    creation_time = DateTimeField(default=datetime.utcnow())
    # creation_user = ReferenceField(document_type='User')
    last_time = DateTimeField(default=datetime.utcnow())
    # last_user = ReferenceField(document_type='User')

    comment = StringField(default="")
    thumbnail_path = StringField()
    # todo_list = ReferenceField(document_type='Task', default=[])

    meta = {
        'collection': 'Versions'
    }

    def __repr__(self):
        return f"<Version>: {self.longname}"
