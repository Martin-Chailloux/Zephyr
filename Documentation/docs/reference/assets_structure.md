# Assets Structure

This is the base structure of documents used to register files in the database.


## Classes


::: Breeze.Api.document_models.project_documents.Version


::: Breeze.Api.document_models.project_documents.Component


::: Breeze.Api.document_models.project_documents.Stage


::: Breeze.Api.document_models.studio_documents.StageTemplate


::: Breeze.Api.document_models.project_documents.Asset


___


## Diagram

``` mermaid
classDiagram
    direction BT
    
    Asset --o Stage
    StageTemplate --o Stage
    Stage --o Component
    Component --o Version

    class Asset["Asset (Document)"]{
        + longname: str
        + category: str
        + name: str
        + variant: str
        + stages: list[Stage]
        
        + create() Asset
        + add_stage()
        + get_stage() Stage
    }
    
    class StageTemplate["StageTemplate (Document)"]{
        + name: str
        + label: str
        + order: int
        + color: str
        + icon_name: str
        + software: Software
        + presets: list[str]
        + processes: list[Process]
        + recipe: dict[str, Any]
        
        create() StageTemplate
        add_process()
        set_recipe()
        set_ingredient_slot()
    }
    
    class Stage["Stage (Document)"]{
        + longname: str
        + asset: Asset
        + stage_template: StageTemplate
        + components: list[Component]
        + work_component: Component
        + status: Status
        + user: User
        + ingredients: dict[str, list[Version]]
        
        + create() Stage
        + create_component() Component
        + create_work_component() Component
        + add_ingredient()
        + replace_ingredient()
        - _sort_ingredients()
    }
    
    class Component["Component (Document)"]{
        + longname: str
        + name: str
        + label: str
        + stage: Stage
        + extension: str
        + versions: list[Version]
        + recommended_version: Version
        
        + create() Component
        # to_folders() list[str]
        + add_version()
        + create_last_version() Version
        + create_version() Version
        + get_last_version() Optional[Version]
        + get_version() Version
    }
    
    class Version["Version (Document)"]{
        + longname: str
        + component: Component
        + number: int
        + software: Software
        + filepath: str
        + creation_user: User
        + last_user: User
        + comment: str
        + creation_time: datetime
        + timestamp: datetime
        
        + create() Version
        + set_comment()
        + increment() Version
        + open_folder()
        + copy_longname()
        + copy_filepath()
        + to_file() AbstractSoftwareFile
        + get_filter_keys()
    }
```
