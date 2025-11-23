# Recipes

To use external components in our working files, we use an ingredient-recipes system.

We cast expected ingredients in a [Stage](assets_structure.md#stage),
based on the recipe (1) from its [StageTemplate](assets_structure.md#stagetemplate).
These ingredients are the output [Components](assets_structure.md#component) of another Stage.
{ .annotate }

1. We can also cast ingredients that are not part of the recipe, if needed.

!!! Example
    In a `rigging` stage, we cast a geometry `geo` from the `modeling` and a material `shd` from the `shading`.


## Classes


### `Recipe`
::: Breeze.Api.recipes.recipe.Recipe

### `IngredientSlot`
::: Breeze.Api.recipes.ingredient_slot.IngredientSlot

### `ComponentFilterBase`
::: Breeze.Api.recipes.component_filters.ComponentFilterBase

### `ComponentFilterCategory(ComponentFilterBase)`
::: Breeze.Api.recipes.component_filters.ComponentFilterCategory

### `ComponentFilterStage(ComponentFilterBase)`
::: Breeze.Api.recipes.component_filters.ComponentFilterStage

### `ComponentFilterComponent(ComponentFilterBase)`
::: Breeze.Api.recipes.component_filters.ComponentFilterComponent


## Diagram

``` mermaid
classDiagram
    direction BT
    
    ComponentFilterBase --|> ComponentFilterCategory
    ComponentFilterBase --|> ComponentFilterStage
    ComponentFilterBase --|> ComponentFilterComponent
    ComponentFilterCategory --> ComponentFilters
    ComponentFilterStage --> ComponentFilters
    ComponentFilterComponent --> ComponentFilters
    
    ComponentFilters --> IngredientSlot
    IngredientSlot --o Recipe
    Recipe --> StageTemplate
    
    StageTemplate --* Stage
    IngredientSlot <..> Version
    Component --o Version
    Version --> Stage: Ingredient
    
    class ComponentFilterBase{
        items: list[str]
        blacklist: bool
        
        get_filtered_components(components: list[Component]) list[Component]
        filter_components(components: list[Component]) list[Component]
        to_database() dict[str, Any]
        @cls from_database(infos: dict[str, Any])
    }
    
    class ComponentFilterCategory{
        name
        filter_components()
    }
    class ComponentFilterStage{
        name
        filter_components()
    }
    class ComponentFilterComponent{
        name
        filter_components()
    }
    
    class ComponentFilters {
        Category: ComponentFilterCategory
        Stage: ComponentFilterStage
        Component: ComponentFilterComponent
        @cls from_name(name: str) Type[ComponentFilterBase]
    }
    <<enumeration>> ComponentFilters 
    
    class IngredientSlot {
        name: str
        is_multiple: bool
        filters: list[ComponentFilterBase]
        allowed_components: list[Components]
        _get_allowed_components() list[Component]
        to_database() dict[str, Any]
        @cls from_database(infos: dict[str, Any])
    }
    
    class Recipe {
        ingredient_slots: list[IngredientSlot]
        to_database() dict[str, Any]
        @cls from_database(infos: dict[str, Any])
    }
    
    class Stage {
        stage_template: StageTemplate
        ingredients: dict[str, list[Version]]
        
        add_ingredient(name: str, version: Version)
        replace_ingredient(name: str, old_version: Version, new_version: Version)
        _sort_ingredients()
    }
    class Component {
    }
    class Version {
        component: Component
    }
    
    class StageTemplate{
        recipe: dict[str, Any]
        set_recipe(recipe: dict[str, Any])
        set_ingredient_slot(slot_name: str, slot_infos: dict[str, Any], crash_if_exists: bool=True)
    }
    
```