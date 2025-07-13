from pathlib import Path
import inspect

import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Api.project_documents import Job

mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")

jobs = Job.objects()
for job in jobs:
    print(f"{job = }")
    print(f"{job.steps = }")
    print(f"{job.steps.label = }")
