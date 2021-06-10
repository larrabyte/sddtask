# Code Style Guidelines
These guidelines serve to help collaborators conform to a similar code style. Remember that common sense still triumphs these guidelines: if there exists a valid reason to break them, then do so.

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Imports](#imports)

## Naming Conventions
Variables names should be written using camelCase.
```py
# Correct: uses camel case.
longVariableName = 5
helloString = "hello, world!"

# Incorrect: uses an inconsistent mixture of styles.
LongVariableName = 5
e_String = "hello, world!"
```

Function names should be written using snake case.
```py
# Correct: function name uses snake case and arguments are written in camelCase.
def snakey_name_ssss(argOne: int, : argTwo, argThree: float) -> None:
    pass

# Incorrect: function and argument names are inconsistent.
def unsnakeyNameWOOPS(arg_one, arg2, argIII):
    pass
```

Constants should be written using uppercase, with spaces signified using underscores.
```py
# Correct: uses uppercase and underscores for spaces.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Incorrect: uses an inconsistent mixture of styles.
SCREENwidth = 640
ScReEnHeiGHt = 480
```

Class names should be written using Pascal Case.
```py
# Correct: uses the Pascal Case convention.
class EntitySystem:
    pass

# Incorrect: uses the camelCase convention.
class entitySystem:
    pass
```

## Imports
Import statements should be used for packages and modules only, not for individual classes or functions. Aliasing modules is strongly encouraged if potential naming conflicts are present. Seperate import statements should reside on seperate lines.
```py
# Correct: each import is separated and included as a *whole* module.
import typing as t
import pygame
import os

# Incorrect: specific sub-modules are imported into the global namespace.
from pygame import display
from json import loads
import os
```
