"""Message, to be passed around and logged into a journal..."""

from abc import\
    ABC, abstractmethod
import time
from . import utils, Level

class Message(ABC):
    """Base Message"""

    def __init__(self, *msgs, **kwargs):
        """Initialize Me"""
        self._value = '\n'.join(msgs)
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def level(self):
        """..."""
        pass

    @property
    @abstractmethod
    def label(self):
        """..."""
        pass

    @property
    def labelstamp(self):
        """Enclose a string in a box."""
        return "<{}>".format(self.label)

    @property
    def value(self):
        """..."""
        return self._value

    def formatted(self, caller=None):
        """Message value formatted according to a class 'caller'
        """
        if not caller:
            return "@{} {} {}"\
                .format(
                    utils.timestamp(),
                    self.labelstamp,
                    self.value)
        return "{}@{} {} {}\n"\
            .format(
                caller.__name__,
                utils.timestamp(),
                self.labelstamp,
                self.value)


class Funda(Message):
    """A single unit of fundamental understanding."""
    level = Level.STUDY
    label = "FUNDA"


class Info(Message):
    """General Info, can be anything."""
    level = Level.INFO
    label = "INFO"

class ProgressInfo(Info):
    """Info about progress"""
    label = "Progress"
