from mongoengine import *

connect(host="mongodb+srv://MartinChailloux:adminGhost@learn.kqpry.mongodb.net/JourDeVent")


class Palette(Document):
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
        'collection': 'Palettes'
    }

    def __repr__(self):
        return f"<Palette>: {self.name}"


def create_palette(name: str,
                   white_text, black_text,
                   primary, secondary, tertiary, surface,
                   purple, red, orange, yellow, green, blue, cyan,
                   **kwargs):
    kwargs = dict(name=name,
                  white_text=white_text, black_text=black_text,
                  primary=primary, secondary=secondary, tertiary=tertiary, surface=surface,
                  purple=purple, red=red, orange=orange, yellow=yellow, green=green, blue=blue, cyan=cyan,
                  **kwargs)

    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    palette = Palette(**kwargs)
    palette.save()
    print(f"Created: {palette.__repr__()}")
    return palette
