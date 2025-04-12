from typing import Self

from mongoengine import *


class Palette(Document):
    name: str = StringField(required=True, primary_key=True)

    white_text: str = StringField(required=True)
    black_text: str = StringField(required=True)

    primary: str = StringField(required=True)
    secondary: str = StringField(required=True)
    tertiary: str = StringField(required=True)
    surface: str = StringField(required=True)

    purple: str = StringField(required=True)
    red: str = StringField(required=True)
    orange: str = StringField(required=True)
    yellow: str = StringField(required=True)
    green: str = StringField(required=True)
    blue: str = StringField(required=True)
    cyan: str = StringField(required=True)

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
    label: str = StringField(required=True, primary_key=True)
    color: str = StringField(required=True)
    order: int = IntField(required=True)

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
    pseudo: str = StringField(required=True, primary_key=True)
    fullname: str = StringField(required=True)
    password: str = StringField(default="zephyr")
    icon_path: str = StringField(required=True)

    palette: Palette = ReferenceField(document_type=Palette, default=Palette.objects.get(name="dev"))
    mail: str = StringField()  # Not used yet

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


class Software(Document):
    label: str = StringField(required=True, primary_key=True)
    icon_path: str = StringField(required=True)

    exe_path: str = StringField(required=True)

    meta = {
        'collection': 'Software',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Software>: {self.label}"

    @classmethod
    def create(cls, label: str, icon_path: str, exe_path: str, **kwargs) -> Self:
        kwargs = dict(label=label, icon_path=icon_path, exe_path=exe_path, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        software = cls(**kwargs)
        software.save()
        print(f"Created: {software.__repr__()}")
        return software


class Project(Document):
    name: str = StringField(required=True, primary_key=True)
    db_name: str = StringField(required=True, unique=True)
    categories: list[str] = SortedListField(StringField(), default=["Character", "Decor", "Element", "Prop", "Shot"])
    users: list[User] = SortedListField(ReferenceField(document_type=User), default=[])

    meta = {
        'collection': 'Projects',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Project>: '{self.name}'"

    def add_category(self, category: str):
        self.categories.append(category)
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

    def add_user(self, user: User):
        # With a gui set_users() will probably make more sense and be enough
        self.users.append(user)
        self.save()

    def add_users(self, users: list[User]):
        self.users.extend(users)
        self.save()
