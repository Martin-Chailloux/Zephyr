import importlib
from typing import Self, Any

import mongoengine
from mongoengine import *

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Api.turbine.process import ProcessBase


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
    # NOTE: users should never be deleted, omit them instead
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
    extension: str = StringField(required=True)

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
    root_path: str = StringField(required=True)
    categories: list[str] = SortedListField(StringField(), default=["Character", "Decor", "Element", "Prop", "Shot"])
    users: list[User] = SortedListField(ReferenceField(document_type=User), default=[])

    meta = {
        'collection': 'Projects',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Project>: {self.name}"

    @classmethod
    def create(cls, name: str, db_name: str, root_path: str,
               categories: list[str], users: list[User],
               **kwargs):
        kwargs = dict(name=name, root_path=root_path, categories=categories, users=users, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        project = cls(**kwargs)
        project.save()
        print(f"Created: {project.__repr__()}")
        return project

    def add_category(self, category: str):
        self.categories.append(category)
        self.save()

    def add_user(self, user: User):
        # With a gui set_users() will probably make more sense and be enough
        self.users.append(user)
        self.save()

    def add_users(self, users: list[User]):
        self.users.extend(users)
        self.save()


class Process(Document):
    # TODO: cast stage templates in this (reciprocal field)
    #  Process.{set/add}_stage_templates(stage_template: list[StageTemplates])
    #  or StageTemplates.{set/add}_processes(processes: list[Process])

    longname: str = StringField(required=True, primary_key=True)
    label: str = StringField(required=True)
    tooltip: str = StringField(required=True)
    class_path: str = StringField(required=True)

    meta = {
        'collection': 'Processes',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Process>: {self.longname}"

    @classmethod
    def create(cls, longname: str, label: str, tooltip: str, class_path: str, **kwargs) -> Self:
        kwargs = dict(longname=longname, label=label, tooltip=tooltip, class_path=class_path, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        process = cls(**kwargs)
        process.save()
        print(f"Created: {process.__repr__()}")
        return process

    def to_class(self) -> 'ProcessBase'.__class__:
        path = self.class_path
        module_name, class_name = path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)


class StageTemplate(Document):
    """
    Generic infos about a stage, that are common to all its instances:
    name, label, description, color, icon
    """
    name: str = StringField(required=True, primary_key=True)
    label: str = StringField(required=True, unique=True)

    order: int = IntField(default=0)
    color: str = StringField(default="#ffffff")
    icon_name: str = StringField(default="fa5s.question")

    software: list[Software] = SortedListField(ReferenceField(document_type=Software), default=[])
    presets: list[str] = ListField(StringField(), default=[])  # TODO: an api to register presets would be easier to edit without using the ui

    processes: list[Process] = SortedListField(ReferenceField(document_type=Process, default=[]))
    recipe: list[dict[str, Any]] = ListField(DictField(), default=[])  # a list of Api.recipes.IngredientSlot.to_database()

    meta = {
        'collection': 'Stage templates',
        'db_alias': 'default',
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


# Delete rules
User.register_delete_rule(Project, 'users', mongoengine.PULL)

Palette.register_delete_rule(User, 'palette', mongoengine.DENY)
