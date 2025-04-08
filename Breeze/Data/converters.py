class BreezeText:
    def __init__(self, text: str):
        self.text = text

    def to_valid_name(self):
        split_text = self.text.replace("_", " ").replace("-", " ").split()
        if len(split_text) == 0:
            return self.text
        else:
            return split_text[0] + "".join(s.replace(s[0], s[0].upper()) for s in split_text[1:])
