import time

class Chronometer:
    def __init__(self):
        self.previous = time.time()

    def tick(self, text: str = None) -> float:
        now = time.time()
        delta = now - self.previous

        if text is not None:
            print(f"{text} {delta:3.2f} seconds")

        self.previous = time.time()
        return delta
