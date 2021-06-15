import player
import game

if __name__ == "__main__":
    instance = game.Game()
    player = player.Player()
    instance.add_entity(player)
    instance.run()
