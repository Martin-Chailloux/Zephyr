from Data.studio_documents import User


def create_user(pseudo: str, fullname: str, icon_path: str, password: str = None, mail: str=None, **kwargs) -> User:
    kwargs = dict(pseudo=pseudo, fullname=fullname, icon_path=icon_path, password=password, mail=mail, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    user = User(**kwargs)
    user.save()
    print(f"Created: {user.__repr__()}")
    return user
