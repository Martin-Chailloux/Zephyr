from Breeze.Data.breeze_documents import Asset, Stage, StageTemplate
from Breeze.Utils.chronometer import Chronometer


def text_to_conformed_text(text: str):
    """ Converts a string input into its camelCase equivalent """
    split_text = text.replace("_", " ").replace("-", " ").split()
    if len(split_text) == 0:
        return text
    return split_text[0] + "".join(s.replace(s[0], s[0].upper()) for s in split_text[1:])


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


def create_stage(asset: Asset, stage_template: StageTemplate, **kwargs) -> Stage:
    longname = "_".join(s for s in [asset.longname, stage_template.name])
    kwargs = dict(asset=asset, stage_template=stage_template, longname=longname, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    stage = Stage(**kwargs)
    stage.save()
    print(f"Created: {stage.__repr__()}")

    stage.append_to_asset()

    return stage

