
import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.hits = set()

    def choose(self):
        options = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if (r, c) not in self.tried
        ]

        if not options:
            return None

        # Prefer cells next to previous hits.
        nearby = set()

        for r, c in self.hits:
            for pos in (
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1),
            ):
                if (
                    0 <= pos[0] < self.size
                    and 0 <= pos[1] < self.size
                    and pos not in self.tried
                ):
                    nearby.add(pos)

        candidates = [pos for pos in options if pos in nearby]

        if not candidates:
            candidates = options

        pos = random.choice(candidates)
        self.tried.add(pos)
        return pos

    def record_result(self, pos, result):
        if result in ("hit", "sunk"):
            self.hits.add(pos)
