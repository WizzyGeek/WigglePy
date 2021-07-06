"""The utils related to wiggling"""
from math import pi, cos
from time import sleep

from sys import stdout

# spaces.resize(std::round(width * ((-1 * (std::cos((PI * i) / (height / 2)))) + 1)), ' ');

class Wiggler:
    """A wiggler for wiggly lines.

    Attributes
    ==========
    height : int
        The amount of lines 1 wiggle takes. By default 40.
    width : int
        The width of the wiggle with respect to the x-axis,
        the maximum width (length) of wiggle is twice this value.
        By default 15.
    delay : float
        Amount milliseconds to delay each update, the actual speed of
        illusion of animation maybe limited by the display's refresh rate.
        By default 16.
    space : str
        The character to use as a white space. By defualt a space.
    """
    def __init__(self, height: int = 40, width: int = 15, delay: float = 16, space: str = " ") -> None:
        self.height = height
        self.width = width
        self.delay  = delay / 1000
        self.space = space

    def _get_spaces(self, itr: int = -1):
        height = self.height
        const = (2 * pi) / self.height
        nve_width = -1 * self.width
        space = self.space
        if itr > 0:
            for i in range(itr):
                i %= height
                yield space * round(nve_width * (cos(const * i) - 1))
        else:
            i = 0
            while True:
                yield space * round(nve_width * (cos(const * i) - 1))
                i = (i + 1) % height


    def wiggle(self, text: str, itr: int) -> None:
        """Prints a wave with given text.

        Arguments
        =========
        text : str
            The text which will be used in the wave
        itr : int
            amount of times to update the wave, if 0 or below
            then it will continue endlessly.
        """
        delay = self.delay
        for i in self._get_spaces(itr):
            sleep(delay)
            print(i, text, sep="", flush=True)

    def wiggleInfinitely(self, text: str) -> None:
        """Alias for wiggle() with infinite iterations"""
        delay = self.delay
        for i in self._get_spaces():
            sleep(delay)
            print(i, text, sep="", flush=True)

    def shm(self, text: str, itr: int = -1) -> None:
        """Simple Harmonic motion for give text

        Arguments
        =========
        text : str
            The text which will perform shm
        itr : int
            amount of times to update the shm, if 0 or below
            then it will continue endlessly.
        """
        delay = self.delay
        max_width = 2 * self.width
        write = stdout.write
        for i in self._get_spaces(itr):
            write(i + text + (" " * (max_width - len(i))) + "\r")
            sleep(delay)
