import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Breeze.Api import data
from Api.document_models.studio_documents import Software
mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")

def test():
    x = Software.from_extension(extension="blend")
    print(f"{x = }")

if __name__ == '__main__':
    test()