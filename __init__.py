"""
2D Shape Engine in Python based by pygame
"""
# cython: language_level=3

__author__ = "NotEasy"
__version__ = "1.0.0"

from .call import Call
from .script import Script, ControlScript
from .fileobject import FileObject
from .image import Image
from .color import Color
from .texture import ImageTexture, SolidColorTexture, get_texture
from .vector import Vector
import shape._aliases as colors
from .app import App
from .collision import Collision
from .errorlistener import ErrorListener
from .event import EventListener, EventManager
from .audio import Audio, AudioManager
from .font import Font
from .input import mouse, keyboard
from .model import Model, get_square_model
from .object import Object, TextObject, Direction
from .math import get_x_center, get_y_center, get_distance
from .scene import Scene, SceneManager
from .soundeffect import SoundEffect
from .soundtrack import SoundTrack

app: App

keyboard: keyboard.KeyBoard
mouse: mouse.Mouse

margin: int

print(f"ShapeEngine v{__version__} by {__author__}")
