from dataclasses import dataclass

import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")

mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")

@dataclass
class A:
    a: int
    b: bool
    c: str = None


if __name__ == '__main__':
    test = A()
    print(f"{A.a = }")
    print(f"{A.b = }")
    print(f"{A.c = }")