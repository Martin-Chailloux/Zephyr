import mongoengine

mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Api.breeze_app import BreezeApp
BreezeApp.set_project("JourDeVent")
BreezeApp.set_user("Martin")
mongoengine.connect(host="mongodb://localhost:27017", db=BreezeApp.project.name, alias="current_project")

from Api import data
from Api.document_models.studio_documents import StageTemplate
from Api.recipes.default_recipes import RecipesDefault


def set_recipe():
    print("set_recipe(): START ...")

    modeling: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.modeling)
    rigging: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.rigging)
    texturing: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.texturing)
    shading: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.shading)
    animation: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.animation)
    lighting: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.lighting)

    modeling.set_recipe(RecipesDefault.modeling.to_database())
    rigging.set_recipe(RecipesDefault.rigging.to_database())
    texturing.set_recipe(RecipesDefault.texturing.to_database())
    shading.set_recipe(RecipesDefault.shading.to_database())
    animation.set_recipe(RecipesDefault.animation.to_database())
    lighting.set_recipe(RecipesDefault.lighting.to_database())

    print("... set_recipe(): SUCCESS")

if __name__ == '__main__':
    set_recipe()