from .__genius import Connection as GeniusConnect
from .__spoti import Connection as SpotiConnect
from .__chatgpt import Connection as GPTConnect

__all__ = [
    GeniusConnect,
    SpotiConnect,
    GPTConnect
]