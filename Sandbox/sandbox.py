import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Breeze.Api import data
mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")

def test():
    print(f"{data.Categories.prop = }")
    print(f"{data.Components.all() = }")


if __name__ == '__main__':
    test()