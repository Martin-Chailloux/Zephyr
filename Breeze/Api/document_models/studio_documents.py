from typing import Self, Any, Optional

import mongoengine
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

    def __str__(self):
        return self.__repr__()

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
        print(f"Created: {palette}")
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

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, label: str, color: str, order: int, **kwargs) -> Self:
        kwargs = dict(label=label, color=color, order=order, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        status = cls(**kwargs)
        status.save()
        print(f"Created: {status}")
        return status


class User(Document):
    # NOTE: users should never be deleted, omit them instead

    pseudo: str = StringField(required=True, primary_key=True)
    first_name: str = StringField(required=True)
    last_name: str = StringField(required=True)
    full_name: str = StringField(required=True)

    order: int = IntField(default=0)

    # TODO: move to SubUser
    palette: Palette = ReferenceField(document_type=Palette, default=Palette.objects.get(name="dev"))

    meta = {
        'collection': 'Users',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<User>: {self.pseudo}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, pseudo: str, first_name: str, last_name:str, **kwargs) -> Self:
        full_name = f"{first_name} + {last_name}"
        kwargs = dict(pseudo=pseudo, first_name=first_name, last_name=last_name, full_name=full_name, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        user = cls(**kwargs)
        user.save()
        print(f"Created: {user}")
        return user

    @classmethod
    def from_pseudo(cls, pseudo: str) -> Optional[Self]:
        for user in User.objects():
            if user.pseudo == pseudo:
                return user
        else:
            return None

    @property
    def icon_path(self) -> str:
        # TODO: root_path somewhere else
        # TODO: tool to import a profile picture and keep the size to 64x64 (too heavy creates lags)
        path = f"C:/Users/marti/OneDrive/Documents/__work/_dev/Zephyr/Resources/Icons/Users/{self.pseudo}"
        return path


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

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, label: str, icon_path: str, exe_path: str, **kwargs) -> Self:
        kwargs = dict(label=label, icon_path=icon_path, exe_path=exe_path, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        software = cls(**kwargs)
        software.save()
        print(f"Created: {software}")
        return software

    @classmethod
    def from_extension(cls, extension: str) -> Optional[Self]:
        for soft in Software.objects():
            if soft.extension == extension:
                return soft
        else:
            return None


class Project(Document):
    name: str = StringField(primary_key=True)
    root_path: str = StringField(required=True)
    categories: list[str] = SortedListField(StringField(), default=["Character", "Decor", "Element", "Prop", "Shot"])
    users: list[User] = SortedListField(ReferenceField(document_type=User), default=[])

    meta = {
        'collection': 'Projects',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Project>: {self.name}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, name: str, root_path: str, categories: list[str] = None, users: list[User] = None,
               **kwargs):
        kwargs = dict(name=name, root_path=root_path, categories=categories, users=users, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        project = cls(**kwargs)
        project.save()
        print(f"Created: {project}")
        return project

    @classmethod
    def create_from_project(cls, source: 'Project', name: str, root_path: str) -> 'Project':
        project = cls.create(name=name, root_path=root_path, categories=source.categories, users=source.users)
        return project

    def add_category(self, category: str):
        self.categories.append(category)
        self.save()

    def add_user(self, user: User):
        self.users.append(user)
        self.save()

    def add_users(self, users: list[User]):
        self.users.extend(users)
        self.save()


class Process(Document):
    """
    The database document that registers an Engine
    """

    longname: str = StringField(required=True, primary_key=True)
    class_path: str = StringField(required=True)
    label: str = StringField(required=True)
    tooltip: str = StringField(required=True)

    # NOTE: label and tooltip are there to be displayed in delegates

    meta = {
        'collection': 'Processes',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Process>: {self.longname}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create(cls, longname: str, class_path: str, label: str, tooltip: str, **kwargs) -> Self:
        kwargs = dict(longname=longname, class_path=class_path, label=label, tooltip=tooltip, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        process = cls(**kwargs)
        process.save()
        print(f"Created: {process}")
        return process


class StageTemplate(Document):
    """
    Model for a Stage, with expected ingredients and associated processes.

    Examples: `modeling`, `rigging`, `shading`, `animation`, `lighting`, etc...
    """
    name: str = StringField(required=True, primary_key=True)
    label: str = StringField(required=True, unique=True)

    order: int = IntField(default=0)
    color: str = StringField(default="#ffffff")
    icon_name: str = StringField(default="fa5s.question")

    # used when creating a new empty Version
    available_software: list[Software] = SortedListField(ReferenceField(document_type=Software), default=[])

    presets: list[str] = ListField(StringField(), default=[])  # TODO: an api to register presets would be easier to edit without using the ui

    processes: list[Process] = SortedListField(ReferenceField(document_type=Process, default=[]))
    recipe: dict[str, Any] = DictField()  # dict[name, infos], contains IngredientSlots

    # TODO: this cannot scale with multiple different and dynamic outputs
    outputs: list[str] = SortedListField(StringField(), default=[])  # list of exported component names

    meta = {
        'collection': 'Stage templates',
        'db_alias': 'default',
    }

    def __repr__(self):
        return f"<Stage template>: {self.name}"

    def __str__(self):
        return self.__repr__()

    # NOTE: GUI does not exist yet
    @classmethod
    def create(cls, name: str, label: str, color: str = None, icon_name: str = None, **kwargs) -> Self:
        kwargs = dict(name=name, label=label, color=color, icon_name=icon_name, **kwargs)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        stage_template = cls(**kwargs)
        stage_template.save()
        print(f"Created: {stage_template}")
        return stage_template

    def add_process(self, process: Process):
        self.processes.append(process)
        self.save()

    def set_recipe(self, recipe: dict[str, Any]):
        previous_recipe = self.recipe
        self.recipe = recipe
        self.save()
        print(f"{self}'s recipe was set from {previous_recipe} to {recipe}")

    def set_outputs(self, outputs: list[str]):
        previous_outputs = self.outputs
        self.outputs = outputs
        self.save()
        print(f"{self}'s outputs was set from {previous_outputs} to {outputs}")

    def set_ingredient_slot(self, slot_name: str, slot_infos: dict[str, Any], crash_if_exists: bool=True):
        slot_exists = slot_name in self.recipe.keys()

        if slot_exists and crash_if_exists:
            raise ValueError(f"{self}'s recipe already has an ingredient slot with name {slot_name}")
        self.recipe[slot_name] = slot_infos

        if slot_exists:
            print(f"Ingredient {slot_name} was overridden in {self}'s recipe: from {self.recipe[slot_name]} to {slot_infos}")
        else:
            print(f"Ingredient {slot_name} was added to {self}'s recipe: {slot_infos}")


# ------------------------
# Delete rules
# ------------------------
# TODO: cascade deletions in unconnected project databases

User.register_delete_rule(Project, 'users', mongoengine.PULL)

Palette.register_delete_rule(User, 'palette', mongoengine.DENY)
