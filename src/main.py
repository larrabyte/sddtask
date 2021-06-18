from player import Player
from game import Game

if __name__ == "__main__":
    p = Player()
    Game.add_entity(p)
    Game.run()
