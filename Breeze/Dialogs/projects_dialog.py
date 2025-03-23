from Breeze.Data.breeze_documents import Project


def create_project(name: str, categories: list[str] = None, users: list[str] = None, **kwargs) -> Project:
    kwargs = dict(name=name, categories=categories, users=users, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    project = Project(**kwargs)
    project.save()
    print(f"Created: {project}")
    return project

def get_project(name: str) -> Project:
    return Project.objects.get(name=name)