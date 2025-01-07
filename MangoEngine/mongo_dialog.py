from MangoEngine.document_models import Asset, Stage
from Utils.chronometer import Chronometer


def text_to_input(text: str):
    s = text.replace("_", " ").replace("-", " ")
    s = s.split()
    if len(s) == 0:
        return text
    return s[0] + "".join(i.replace(i[0], i[0].upper()) for i in s[1:])


def create_asset(category: str, name : str, variant: str = None, **kwargs) -> Asset:
    kwargs = dict(name=name, category=category, variant=variant, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    asset = Asset(**kwargs)
    asset.save()
    print(f"Created: {asset}")
    return asset


def get_asset(category: str = None, name: str = None, variant: str = None, **kwargs) -> list[Asset]:
    chronometer = Chronometer()
    kwargs = dict(category=category, name=name, variant=variant, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    assets = list(Asset.objects(**kwargs))

    print(f"Found {len(assets)} Asset in {chronometer.tick()}:")
    for asset in assets:
        print("    -", asset.__repr__())
    return assets


def create_stage(asset: Asset, description: str, detail: str=None, **kwargs) -> Stage:
    kwargs = dict(asset=asset, description=description, detail=detail, **kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    stage = Stage(**kwargs)
    stage.save()
    print(f"Created: {stage}")
    return stage

