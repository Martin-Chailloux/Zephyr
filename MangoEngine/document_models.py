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
        return f"Project: name ='{self.name}'"

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
    category = StringField(required=True)
    name = StringField(required=True)
    variant = StringField(default="-")

    meta = {
        'collection': 'Assets'
    }

    def __repr__(self):
        return f"Asset: category='{self.category}', name='{self.name}', variant='{self.variant}'"

    @property
    def longname(self) -> str:
        return f"{self.category}_{self.name}_{self.variant}"

    @classmethod
    def from_longname(cls, longname: str):
        keys = longname.split("_")
        if len(keys) != 3:
            raise "Incorrect number of keys in longname."
        return cls(category=keys[0], name=keys[1], variant=keys[2])


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


class Stage(Component):
    """
    A Component that creates Products
    """
    components = ListField(ReferenceField(document_type=Component, reverse_delete_rule=PULL), default=[])
    products = ListField(ReferenceField(document_type='Product'), default=[])


class Product(Component):
    """
    A Component created from a Stage
    """
    stage = ReferenceField(document_type=Stage, required=True)

Stage.register_delete_rule(Product, 'products', PULL)


class Increment(Document):
    """
    Numbered iteration of a Stage
    """
    stage: Stage = ReferenceField(document_type=Stage, reverse_delete_rule=CASCADE, default=None)
    product: Product = ReferenceField(document_type=Product, reverse_delete_rule=CASCADE, default=None)

    count = IntField(min=0, required=True)
    filepath = StringField(required=True)
    extension = StringField(required=True)

    @property
    def source(self) -> Stage | Product:
        if self.product is None:
            return self.stage
        elif self.stage is None:
            return self.product
        else:
            raise "Increments should have exactly one source."
