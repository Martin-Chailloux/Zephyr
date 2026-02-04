import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Api.breeze_app import BreezeApp
BreezeApp.set_project("JourDeVent")
BreezeApp.set_user("Martin")
mongoengine.connect(host="mongodb://localhost:27017", db=BreezeApp.project.name, alias="current_project")

from Api import data
from Api.document_models.studio_documents import StageTemplate
from Api.recipes.default_recipes import RecipesDefault
from Api.recipes.default_ouputs import OutputDefaults


def set_recipes():
    print("set_recipes(): START ...")

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

    print("... set_recipes(): SUCCESS")

def set_outputs():
    print("set_outputs(): START ...")

    modeling: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.modeling)
    rigging: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.rigging)
    texturing: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.texturing)
    shading: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.shading)
    animation: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.animation)
    lighting: StageTemplate = StageTemplate.objects.get(name=data.StageTemplates.lighting)

    modeling.set_outputs(OutputDefaults.modeling)
    rigging.set_outputs(OutputDefaults.rigging)
    texturing.set_outputs(OutputDefaults.texturing)
    shading.set_outputs(OutputDefaults.shading)
    animation.set_outputs(OutputDefaults.animation)
    lighting.set_outputs(OutputDefaults.lighting)

    print("... set_outputs(): SUCCESS")


if __name__ == '__main__':
    set_recipes()