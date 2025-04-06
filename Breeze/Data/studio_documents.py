from mongoengine import *


class Palette(Document):
    # TODO: move to Studio db
    name = StringField(required=True, primary_key=True)

    white_text = StringField()
    black_text = StringField()

    primary = StringField()
    secondary = StringField()
    tertiary = StringField()
    surface = StringField()

    purple = StringField()
    red = StringField()
    orange = StringField()
    yellow = StringField()
    green = StringField()
    blue = StringField()
    cyan = StringField()

    meta = {
        'collection': 'Palettes',
        'db_alias': 'current_project',
    }

    def __repr__(self):
        return f"<Palette>: {self.name}"


class Status(Document):
    label = StringField(required=True, primary_key=True)
    color = StringField(required=True)
    order = IntField(required=True)

    meta = {
        'collection': 'Statuses',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Status>: {self.label}"
