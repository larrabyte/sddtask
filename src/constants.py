# World/level constants.
WORLD_TILE_SIZE = 32 # World tile size in game units.
WORLD_TILE_SHIFT = 5 # Bit shift required to turn units into tiles.
WORLD_GRAVITY = -20 * WORLD_TILE_SIZE # Gravity in world units.
WORLD_BACKGROUND_COLOUR = (0, 0, 0) # World background colour (when no tile is present).

# Player-related constants.
PLAYER_FRICTION_COEFFICIENT = 0.9 # Player friction coefficient.
PLAYER_MOVEMENT_SPEED = 16 # Movement speed of the player.
PLAYER_HEALTH_MAX = 100 # Maximum player health.
PLAYER_VELOCITY_MAX = 800 # Cap player velocity
PLAYER_JUMPING_SPEED = 200 # Jumping force.
PLAYER_JETPACK_SPEED = 1250 # Jetpack acceleration.
PLAYER_JETPACK_MAX = 300 # Max jetpack fuel.
PLAYER_JETPACK_FUEL_USE = 60 # Fuel consumed per second.
PLAYER_JETPACK_FUEL_REGEN = 120 # Fuel regeneration per second.
PLAYER_DETECT_RANGE = 32 * WORLD_TILE_SIZE # Detection range of the player to the enemies.
SCREEN_SCALE = 2 # Screen scaling factor.

PROJECTILE_SPEED = 180 # Speed of enemy projeciles.
PROJECTILE_FIRE_RATE = 0.03 # Enemy fire rate.
