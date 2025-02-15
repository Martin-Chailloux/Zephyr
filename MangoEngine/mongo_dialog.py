from MangoEngine.document_models import Asset, Stage, StageTemplate
from Utils.chronometer import Chronometer


def text_to_input(text: str):
    s = text.replace("_", " ").replace("-", " ")
    s = s.split()
    if len(s) == 0:
        return text
    return s[0] + "".join(i.replace(i[0], i[0].upper()) for i in s[1:])


def create_asset(category: str, name : str, variant: str = None, **kwargs) -> Asset:
    v = variant or "-"
    longname = "_".join(s for s in [category, name, v])
    kwargs = dict(name=name, category=category, variant=variant, longname=longname, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    asset = Asset(**kwargs)
    asset.save()
    print(f"Created: {asset.__repr__()}")
    return asset


def get_asset(category: str = None, name: str = None, variant: str = None, unique=False, **kwargs) -> list[Asset] | Asset:
    chronometer = Chronometer()
    kwargs = dict(category=category, name=name, variant=variant, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if unique:
        asset = Asset.objects.get(**kwargs)
        print(f"Found 1 unique Asset in {chronometer.tick()}:")
        print("    -", asset.__repr__())
        return asset

    else:
        assets = list(Asset.objects(**kwargs))
        print(f"Found {len(assets)} Asset in {chronometer.tick()}:")
        for asset in assets:
            print("    -", asset.__repr__())
        return assets


# NOTE: currently no gui to create stages
def create_stage_template(name: str, label: str, description: str,
                          color: str = None, icon_name: str = None, **kwargs) -> StageTemplate:
    kwargs = dict(name=name, label=label, description=description,
                  color=color, icon_name=icon_name, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    stage_template = StageTemplate(**kwargs)
    stage_template.save()
    print(f"Created: {stage_template.__repr__()}")
    return stage_template


def create_stage(stage_template: StageTemplate, asset: Asset, **kwargs) -> Stage:
    # TODO: MIGRATION: longname = {asset.longname}_{stage_template.name}
    longname = "_".join(s for s in [stage_template.name, asset.longname])
    kwargs = dict(stage_template=stage_template, asset=asset, longname=longname, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    stage = Stage(**kwargs)
    stage.save()
    print(f"Created: {stage.__repr__()}")

    stage.append_to_asset()

    return stage

