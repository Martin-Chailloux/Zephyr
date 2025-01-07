from mongoengine import *
from Manghost.data import Status

connect(host="mongodb+srv://MartinChailloux:adminGhost@learn.kqpry.mongodb.net/JourDeVent")


class Asset(Document):
    """
    Category & Name of an item
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

    # Required for the stage to do something, but should be added after the stage creation
    extension = StringField(default="-")  # when someone opens a soft and starts working

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

    @property
    def source(self) -> Stage | Product:
        if self.product is None:
            return self.stage
        elif self.stage is None:
            return self.product
        else:
            raise "Increments should have exactly one source."
