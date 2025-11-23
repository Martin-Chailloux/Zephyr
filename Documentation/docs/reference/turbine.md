# Turbine (Reference)

Turbine is used to build, update, export and review scenes.
A series of Steps are assembled into an Engine, then they are executed after each other.

An Engine is always run from a Version.
The existing Engines are stored in its Stage's StageTemplate.

### Relation with Components
A Build Engine will use and import the ingredient-Components that are cast in the Version's Stage.
An Export Engine will create new out-Components for the Version's Stage.

### Inputs
Using the Engine's Gui, a user can define a set of specific inputs before executing the steps.

!!! Example
    Unsetting `don't overwrite` in an Export Engine will allow existing out-Components to be replaced.

___

## Classes

### `TurbineStep`
::: Breeze.Api.turbine.step.TurbineStep

### `TurbineGui`
::: Breeze.Gui.main_windows.turbine.TurbineGui

### `TurbineEngine`
::: Breeze.Api.turbine.engine.TurbineEngine

### `Process`
::: Breeze.Api.document_models.studio_documents.Process

### `Job`
::: Breeze.Api.document_models.project_documents.Job


___

## Diagram

``` mermaid
classDiagram
    direction BT
    
    TurbineStep --|> TurbineEngine
    TurbineGui --o TurbineEngine
    TurbineGui --> TurbineInputs
    TurbineEngine <..> Process
    
    TurbineEngine --> Job
    TurbineInputs --> Job
    JobContext --> Job

    class TurbineGui{
        context: Jobcontext
        widgets: list[TurbineWidgetBase]
        
        _init_ui()
        _connect_signals()
        _init_state()
        inputs()
    }
     
    class TurbineInputs{
        use_last_version: bool
        version_number: int
        dont_overwrite: bool
        ...
    }
    
    class JobContext{
        user: User
        component: Component
        version: Version
        creation_time: datetime
    }
      
    class Job ["Job (Document)"] {
        source_process: Process
        steps: dict[str, any]
        inputs: dict[str, Any]
        user: User
        creation_time: datetime
        source_process: Process
        source_version: Version
    }
    
    
    class Process ["Process (Document)"] {
        class_path: str
    }

```
