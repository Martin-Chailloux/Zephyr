from typing import Self

from mongoengine import *


class Palette(Document):
    name = StringField(required=True, primary_key=True)

    white_text = StringField(required=True)
    black_text = StringField(required=True)

    primary = StringField(required=True)
    secondary = StringField(required=True)
    tertiary = StringField(required=True)
    surface = StringField(required=True)

    purple = StringField(required=True)
    red = StringField(required=True)
    orange = StringField(required=True)
    yellow = StringField(required=True)
    green = StringField(required=True)
    blue = StringField(required=True)
    cyan = StringField(required=True)

    meta = {
        'collection': 'Palettes',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Palette>: {self.name}"

    @classmethod
    def create(cls, name: str,
                       white_text: str, black_text: str,
                       primary: str, secondary: str, tertiary: str, surface: str,
                       purple: str, red: str, orange: str, yellow: str, green: str, blue: str, cyan: str,
                       **kwargs):
        kwargs = dict(name=name,
                      white_text=white_text, black_text=black_text,
                      primary=primary, secondary=secondary, tertiary=tertiary, surface=surface,
                      purple=purple, red=red, orange=orange, yellow=yellow, green=green, blue=blue, cyan=cyan,
                      **kwargs)

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        palette = cls(**kwargs)
        palette.save()
        print(f"Created: {palette.__repr__()}")
        return palette


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

    @classmethod
    def create(cls, label: str, color: str, order: int, **kwargs) -> Self:
        kwargs = dict(label=label, color=color, order=order, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        status = cls(**kwargs)
        status.save()
        print(f"Created: {status.__repr__()}")
        return status


class User(Document):
    pseudo = StringField(required=True, primary_key=True)
    fullname = StringField(required=True)
    password = StringField(default="zephyr")
    icon_path = StringField(required=True)

    palette = ReferenceField(document_type=Palette, default=Palette.objects.get(name="dev"))
    mail = StringField()


    meta = {
        'collection': 'Users',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<User>: {self.pseudo}"

    @classmethod
    def create(cls, pseudo: str, fullname: str, icon_path: str, password: str = None, mail: str = None,
                    **kwargs) -> Self:
        kwargs = dict(pseudo=pseudo, fullname=fullname, icon_path=icon_path, password=password, mail=mail, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        user = cls(**kwargs)
        user.save()
        print(f"Created: {user.__repr__()}")
        return user

    def set_palette(self, palette: Palette):
        self.palette = palette
        self.save()


class Project(Document):
    name = StringField(required=True, primary_key=True)
    db_name = StringField(required=True, unique=True)
    categories = SortedListField(StringField(), default=["Character", "Decor", "Element", "Prop", "Shot"])
    users = SortedListField(ReferenceField(document_type=User), default=[])

    meta = {
        'collection': 'Projects',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Project>: '{self.name}'"

    def add_category(self, new_categories: str | list[str]):
        if type(new_categories) is str:
            new_categories = [new_categories]

        categories = list(self.categories)
        categories.extend(new_categories)

        self.categories = categories
        self.save()

    @classmethod
    def create(cls, name: str = None, db_name: str=None,
               categories: list[str] = None, users: list[User] = None,
               **kwargs):
        kwargs = dict(name=name, db_name=db_name, categories=categories, users=users, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        project = cls(**kwargs)
        project.save()
        print(f"Created: {project.__repr__()}")
        return project

    def add_users(self, users: list[User]):
        self.users.extend(users)
        self.save()