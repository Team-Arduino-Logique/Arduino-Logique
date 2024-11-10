from typing import Any

PERSO = 0
HORIZONTAL = 1
VERTICAL = 2
VERTICAL_END_HORIZONTAL = 3
AUTO = 0
DIRECT = 1
FREE = 0
USED = 1
INPUT = 0
OUTPUT = 1
NO = 0
YES = 1
LEFT = 0
RIGHT = 1

connexion_circuit: dict[str, list[Any]] = {
    "io": [],
    "wire" : [],
    "pwr" : [],
    "func" : []
}
