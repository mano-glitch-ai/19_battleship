
class Board:
    SIZE = 6

    def __init__(self):
        self.ships = set()
        self.shots = set()
        self.hits = set()
        self.ship_groups = []
        self.sunk_ships = set()

    def place_ship(self, cells):
        cells = set(cells)

        if not cells:
            raise ValueError("A ship must have at least one cell.")

        for r, c in cells:
            if not (0 <= r < self.SIZE and 0 <= c < self.SIZE):
                raise ValueError("Ship coordinates are outside the board.")

        if self.ships & cells:
            raise ValueError("Ships cannot overlap.")

        self.ships.update(cells)
        self.ship_groups.append(cells)

    def fire(self, pos):
        r, c = pos

        if not (0 <= r < self.SIZE and 0 <= c < self.SIZE):
            return "invalid"

        if pos in self.shots:
            return "repeat"

        self.shots.add(pos)

        if pos not in self.ships:
            return "miss"

        self.hits.add(pos)

        for index, ship in enumerate(self.ship_groups):
            if pos in ship and ship <= self.hits:
                self.sunk_ships.add(index)
                return "sunk"

        return "hit"

    def all_sunk(self):
        return bool(self.ship_groups) and all(
            ship <= self.hits for ship in self.ship_groups
        )

    def remaining_ship_cells(self):
        return len(self.ships - self.hits)
