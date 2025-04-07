from Data.studio_documents import Status, Palette


def create_status(label: str, color: str, order: int) -> Status:
    status = Status(label=label, color=color, order=order)
    status.save()
    return status
