from dataclasses import dataclass
from pathlib import Path
import inspect

import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Api.project_documents import Job

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