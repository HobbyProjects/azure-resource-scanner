import collections
from Common.Contracts import Queue

class QueueSimulator(Queue):

    def __init__(self, queue_name, config=None):
        self._queue_name = queue_name
        self._queue = collections.deque()
    
    def push(self, message):
        self._queue.append(message)
    
    def pop(self):
        return self._queue.popleft()

    def peek(self):
        return self._queue[0]
