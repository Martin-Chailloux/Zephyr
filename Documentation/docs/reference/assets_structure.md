# Assets Structure (Reference)

Breeze uses a MongoEngine database to register and to store files.

An Asset contains multiple Stages that represents each step of its creation.
Each Stage generates multiple Components, they become the ingredients of other Stages.
Each Component contains multiple iterated Versions of a file.

## Classes

### `Version`
::: Breeze.Api.document_models.project_documents.Version

### `Component`
::: Breeze.Api.document_models.project_documents.Component

### `StageTemplate`
::: Breeze.Api.document_models.studio_documents.StageTemplate

### `Stage`
::: Breeze.Api.document_models.project_documents.Stage

### `Asset`
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
        category: str
        name: str
        variant: str
        stages: list[Stage]
        
        add_stage(stage: Stage)
        get_stage(name: str) Stage
    }
    
    class StageTemplate["StageTemplate (Document)"]{
        name: str
        label: str
        order: int
        color: str
        icon_name: str
        
        presets: list[str]
        processes: list[Process]
        recipe: dict[str, Any]
        software: Software
    }
    
    class Stage["Stage (Document)"]{
        stage_template: StageTemplate
        asset: Asset
        components: list[Component]
        work_component: Component
        status: Status
        user: User
        ingredients: dict[str, list[Version]]
        
        create_component() Component
        create_work_component() Component
        add_ingredient()
        replace_ingredient()
        _sort_ingredients()
    }
    
    class Component["Component (Document)"]{
        name: str
        label: str
        extension: str
        stage: Stage
        versions: list[Version]
        recommended_version: Version
        
        add_version()
        create_version(number: int) Version
        get_version(number: int) Version
        create_last_version() Version
        get_last_version() Optional[Version]
    }
    
    class Version["Version (Document)"]{
        component: Component
        number: int
        software: Software
        filepath: str
        creation_user: User
        last_user: User
        comment: str
        creation_time: datetime
        timestamp: datetime
        
        set_comment()
        increment() Version
        to_file() AbstractSoftwareFile
        open_interactive() AbstractSoftwareFile
        open_background() AbstractSoftwareFile
    }
```
