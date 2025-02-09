from mongoengine import *
from MangoEngine.data import Status


# TODO: Est-ce que c'est pertinant sur le long terme de le mettre ici ?
# TODO: Tester à l'ouverture du soft quand y aura un truc qui ressemble à un soft
connect(host="mongodb+srv://MartinChailloux:adminGhost@learn.kqpry.mongodb.net/JourDeVent")


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
    name = StringField(required=True, primary_key=True)
    label = StringField(required=True, unique=True)
    description = StringField(default="")

    color = StringField(default="#ffffff")
    icon_name = StringField(default="fa5s.question")

    presets = ListField(StringField(), default=[])

    meta = {
        'collection': 'Stage templates'
    }

    def __repr__(self):
        return f"<Stage template>: {self.name}"


class Stage(Document):
    longname = StringField(required=True, primary_key=True)
    stage_template = ReferenceField(document_type=StageTemplate)
    asset = ReferenceField(document_type=Asset)

    meta = {
        'collection': 'Stages'
    }

    def __repr__(self):
        return f"<Stage>: {self.longname}'"

    def append_to_asset(self):
        self.asset.stages.append(self)
        self.asset.save()


# ======================================================
# NOTE: below is theory, it can change a lot in practice
# ======================================================

class Component(Document):
    """
    Base class for Stages and Products
    """
    asset = ReferenceField(Asset, reverse_delete_rule=CASCADE, required=True)

    description = StringField(required=True)
    detail = StringField(default="-")

    current_status = StringField(
        choices=[Status.TODO, Status.WIP, Status.WFA, Status.DONE, Status.ERROR, Status.OMIT],
        default=Status.TODO
    )

    meta = {
        'collection': 'Components',
        'allow_inheritance': True
    }

    def __repr__(self):
        return (f"Stage: asset='{self.asset}'"
                f"\ndescription='{self.description}', detail='{self.detail}', ext='{self.extension}")

    @property
    def longname(self) -> str:
        return f"{self.asset.longname}_{self.description}_{self.detail}_{self.extension}"

    @classmethod
    def from_longname(cls, longname: str, filepath: str):
        keys = longname.split("_")
        if len(keys) != 6:
            raise "Incorrect number of keys in longname."
        asset = Asset.objects(category=keys[0], name=keys[1], variant=keys[2])
        return cls(asset=asset,
                   description=keys[3], detail=keys[4], extension=keys[5],
                   filepath=filepath)


class StageOld(Component):
    """
    A Component that creates Products
    """
    components = ListField(ReferenceField(document_type=Component, reverse_delete_rule=PULL), default=[])
    products = ListField(ReferenceField(document_type='Product'), default=[])


class Product(Component):
    """
    A Component created from a Stage
    """
    stage = ReferenceField(document_type=StageOld, required=True)

Stage.register_delete_rule(Product, 'products', PULL)


class Increment(Document):
    """
    Numbered iteration of a Stage
    """
    stage: StageOld = ReferenceField(document_type=StageOld, reverse_delete_rule=CASCADE, default=None)
    product: Product = ReferenceField(document_type=Product, reverse_delete_rule=CASCADE, default=None)

    count = IntField(min=0, required=True)
    filepath = StringField(required=True)
    extension = StringField(required=True)

    @property
    def source(self) -> StageOld | Product:
        if self.product is None:
            return self.stage
        elif self.stage is None:
            return self.product
        else:
            raise "Increments should have exactly one source."
