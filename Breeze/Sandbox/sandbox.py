import mongoengine

mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")


from datetime import datetime, timedelta
from Data.breeze_app import BreezeApp


def sb_datetime():
    dt = datetime.now()
    print(f"{dt = }")
    print(f"{str(timedelta(seconds=1)) = }")
    print(f"{dt.microsecond = }")


if __name__ == '__main__':
    BreezeApp.set_project("dev")
    BreezeApp.set_user("Martin")

    print(f"{BreezeApp.project = }")
    print(f"{BreezeApp.palette = }")

