
from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI(Board.SIZE)
        self._setup()

    def _setup(self):
        # Player fleet: three separate ships.
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.player.place_ship({(3, 0), (4, 0)})
        self.player.place_ship({(5, 5)})

        # Enemy fleet: three separate ships.
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})
        self.enemy.place_ship({(0, 4), (0, 5)})
        self.enemy.place_ship({(4, 0), (4, 1)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Enter q to quit.")
        print("Enemy ship cells remaining:",
              self.enemy.remaining_ship_cells())
        print("Your ship cells remaining:",
              self.player.remaining_ship_cells())

    @staticmethod
    def show_result(shooter, result):
        if result == "hit":
            print(f"{shooter} HIT!")
        elif result == "miss":
            print(f"{shooter} MISS!")
        elif result == "sunk":
            print(f"{shooter} SUNK a ship!")
        elif result == "repeat":
            print(f"{shooter} already fired there.")
        elif result == "invalid":
            print(f"{shooter} shot was outside the board.")

    def run(self):
        print("Battleship vs AI")

        while True:
            self.show()
            raw = input("> ").strip().lower()

            if raw == "q":
                print("Game quit.")
                return

            try:
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError

                r, c = map(int, parts)
                pos = (r - 1, c - 1)

            except ValueError:
                print("Invalid input. Enter row,col (e.g. 2,3) or q.")
                continue

            if not (
                0 <= pos[0] < Board.SIZE
                and 0 <= pos[1] < Board.SIZE
            ):
                print("Outside board. Use coordinates from 1 to 6.")
                continue

            # Player fires at the enemy board.
            result = self.enemy.fire(pos)

            if result == "repeat":
                print("Already fired there.")
                continue

            self.show_result("You", result)

            if self.enemy.all_sunk():
                print("You sank the entire enemy fleet. You win!")
                return

            # AI chooses an internal zero-based tuple.
            ai_pos = self.ai.choose()

            if ai_pos is None:
                print("AI has no untried cells remaining.")
                continue

            # AI fires through the player's board.
            ai_result = self.player.fire(ai_pos)
            self.ai.record_result(ai_pos, ai_result)

            # Display coordinates as 1-based row,col.
            print(
                f"AI fired at {ai_pos[0] + 1},{ai_pos[1] + 1}"
            )
            self.show_result("AI", ai_result)

            if self.player.all_sunk():
                print("Your entire fleet was sunk. AI wins!")
                return
