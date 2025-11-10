# Turbine

## Diagram

``` mermaid
classDiagram
    direction BT

    StepLogger --* TurbineStep
    TurbineStep --|> StepGroup
    TurbineStep --|> TurbineEngine
    
    TurbineEngine <--> Process
    TurbineEngine --> Job
    TurbineInputs --> Job
    JobContext --> Job
    
    TurbineWidgetBase --* TurbineGui
    TurbineGui --o TurbineEngine
    TurbineGui --> TurbineInputs

    PillModel --* AbstractPills
    AbstractPills --|> StepPills
    StepPills --o StepPill
    StepPill --* TurbineStep
    
    class PillModel{
        + name
        + icon_name
        + color
        + icon()
    }
    
    class AbstractPills{
        + pills
        + from_name()
    }
    
    class StepPills["StepPills (AbstractPills)"]{
        + idle: PillModel
        + not_needed: PillModel
        + running: PillModel
        + warning: PillModel
        + error: PillModel
        + success: PillModel
    }
    
    class StepPill{
        + pill: PillModel
        
        + from_name()
        + set_idle()
        + set_running()
        + set_warning()
        + set_error()
        + set_success()
    }
    
    class StepLogger{
        + stream: StringIO
        + formatter: logging.Formatter
        + handler: logging.StreamHandler
        + logger: logging.Logger
        
        + info()
        + debug()
        + warning()
        + error()
        + critical()
    }
    
    class TurbineWidgetBase{
        + name: str
        + label: str
        
        - _init_ui()
        + set_enabled()
        + export_infos()
        + import_inputs()
    }
        
    class TurbineGui{
        + context: Jobcontext
        + widgets: list[TurbineWidgetBase]
        + layout: QVBoxLayout
        
        - _init_ui()
        - _connect_signals()
        - _init_state()
        + add_checkbox()
        + add_combobox()
        + inputs()
        + to_database() 
    }

    class TurbineStep{
        + label: str
        + sub_label: str
        + tooltip: str
        + sub_label: str
        + Pill: StepPill
        + logger: StepLogger
        + steps: list[TurbineStep]
        
        + set_sub_label()
        + get_log()
        + pill() PillModel
        + add_step() StepBase
        + add_group() StepGroup
        + run()
        - _inner_run()
        + set_success()
        + set failed()
        + to_dict()
        + from_dict()
    }
    
    class StepGroup["StepGroup(TurbineStep)"] {
        + label: str
        + sub_label: str
    }

    class TurbineEngine["TurbineEngine (TurbineStep)"]{
        + name: str
        + label: str
        + tooltip: str
        + Gui: Type[TurbineGui]
        
        + from_database() TurbineGui
        + get_related_process() Process
        + register()
        + update_contet()
        + set_gui()
        + on_sub_step_updated()
        + get_class_path() str
        + create_job() Job
        + update_job()
    }

    class TurbineInputs{
        + use_last_version
        + version_number
        etc.
    }
    
    class JobContext{
        + user: User
        + component: Component
        + version: Version
        + creation_time: datetime
        
        + set_component()
        + set_version()
        + update_creation_time()
    }
    
    class Process ["Process (Document)"] {
        + longname: str
        + class_path: str
        + label: str
        + tooltip: str
        
        + create() Process
    }
    
    class Job ["Job (Document)"] {
        + longname: str
        + user: User
        + creation_time: datetime
        + source_process: Process
        + source_version: Version
        + steps: dict[str, any]
        + inputs: dict[str, Any]
        
        + create() Job
    }

```

## Classes

::: Breeze.Utils.pills.PillModel

::: Breeze.Utils.pills.AbstractPills

::: Breeze.Api.turbine.utils.StepPills

::: Breeze.Api.turbine.utils.StepPill

::: Breeze.Api.turbine.logger.StepLogger

::: Breeze.Api.turbine.inputs_widgets.TurbineWidgetBase

::: Breeze.Gui.main_windows.turbine.TurbineGui

::: Breeze.Api.turbine.step.TurbineStep

::: Breeze.Api.turbine.step.StepGroup

::: Breeze.Api.turbine.engine.TurbineEngine

::: Breeze.Api.turbine.utils.TurbineInputs

::: Breeze.Api.turbine.utils.JobContext

::: Breeze.Api.document_models.studio_documents.Process

::: Breeze.Api.document_models.project_documents.Job
