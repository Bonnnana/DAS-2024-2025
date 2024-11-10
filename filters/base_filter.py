"""FILTER BASE """

from abc import ABC, abstractmethod


class Filter(ABC):
    @abstractmethod
    def process(self, data):
        pass
