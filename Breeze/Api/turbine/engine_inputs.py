from dataclasses import dataclass


@dataclass
class EngineInputsBase:
    use_last_version: bool = True
    version_number: int = None
    dont_overwrite: bool = False


@dataclass
class EngineInputsBuild(EngineInputsBase):
    create_new_version: bool = False
