from Data.project_documents import Asset, Stage, StageTemplate
from Utils.chronometer import Chronometer


def text_to_conformed_text(text: str):
    """ Converts a string input into its camelCase equivalent """
    split_text = text.replace("_", " ").replace("-", " ").split()
    if len(split_text) == 0:
        return text
    return split_text[0] + "".join(s.replace(s[0], s[0].upper()) for s in split_text[1:])


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
