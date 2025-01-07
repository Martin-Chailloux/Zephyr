from dataclasses import dataclass


@dataclass
class Status:
    TODO: str = "TODO"
    WIP: str = "WIP"
    WFA: str = "WFA"
    DONE: str = "DONE"
    ERROR: str = "ERROR"
    OMIT: str = "OMIT"