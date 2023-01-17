from abc import ABC, abstractmethod
from typing import List


class AfterCommit(ABC):
    @abstractmethod
    def after_commit(self):
        pass


class Resettable(ABC):
    @abstractmethod
    def reset(self):
        pass


class BeforeCommit(ABC):
    @abstractmethod
    def before_commit(self):
        pass


class SidedEffectUtils(AfterCommit, BeforeCommit, Resettable):
    def __init__(self, sided_effected_items: List):
        self.__sided_effected_items = sided_effected_items

    def after_commit(self):
        for item in self.__sided_effected_items:
            if isinstance(item, AfterCommit):
                item.after_commit()

    def before_commit(self):
        for item in self.__sided_effected_items:
            if isinstance(item, BeforeCommit):
                item.before_commit()

    def reset(self):
        for item in reversed(self.__sided_effected_items):
            if isinstance(item, Resettable):
                item.reset()
