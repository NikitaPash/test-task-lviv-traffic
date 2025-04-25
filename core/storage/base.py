from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def save(self, stops):
        """Saves data to a storage."""
        pass
