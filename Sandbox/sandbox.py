import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Breeze.Api import data
from Api.document_models.studio_documents import Software
mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")
# from Gui.main_windows.turbine import TurbineGui
from Api.turbine.step import Step

def test():
    pass

if __name__ == '__main__':
    test()