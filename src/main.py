import player
import level
import game

def start_game():
    gameObject = game.Game()
    mainPlayer = player.Player(gameObject)
    mainLevel = level.Level(gameObject, "level1")

    gameObject.add_entity(mainPlayer)
    gameObject.currentLevel = mainLevel

    # game.run() returns a boolean depending on whether
    # the player wishes to play the game again.
    while (rerunGame := gameObject.run()):
        gameObject = game.Game()
        mainPlayer = player.Player(gameObject)
        mainLevel = level.Level(gameObject, "level1")

        gameObject.add_entity(mainPlayer)
        gameObject.currentLevel = mainLevel

if __name__ == "__main__":
    start_game()
