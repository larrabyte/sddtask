import player
import level
import game

if __name__ == "__main__":
    game = game.Game()
    player = player.Player(game)
    level1 = game.resources.get_level("level1")

    game.add_entity(player)
    game.add_level(level1)
    game.run()
