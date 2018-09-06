from abc import ABC, abstractmethod


class Queue(ABC):

    @abstractmethod
    def push(self, message):
        raise NotImplementedError("Should have implemented push")

    @abstractmethod
    def pop(self):
        raise NotImplementedError("Should have implemented pop")

    @abstractmethod
    def peek(self):
        raise NotImplementedError("Should have implemented peek")
