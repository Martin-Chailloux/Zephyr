from Data.gui_documents import Palette


def create_palette(name: str,
                   white_text, black_text,
                   primary, secondary, tertiary, surface,
                   purple, red, orange, yellow, green, blue, cyan,
                   **kwargs):
    kwargs = dict(name=name,
                  white_text=white_text, black_text=black_text,
                  primary=primary, secondary=secondary, tertiary=tertiary, surface=surface,
                  purple=purple, red=red, orange=orange, yellow=yellow, green=green, blue=blue, cyan=cyan,
                  **kwargs)

    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    palette = Palette(**kwargs)
    palette.save()
    print(f"Created: {palette.__repr__()}")
    return palette
