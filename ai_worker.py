# ai_worker.py
from PySide6.QtCore import QRunnable, QObject, Signal
from typing import Optional
from ai_client import get_response

# Signals must inherit from QObject
class AISignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = Signal(str)      # Emits the successful reply text (str)
    error = Signal(Optional[str]) # Emits if the request fails (None is passed)

class AIWorker(QRunnable):
    """
    Worker for the API call, executing in a QThreadPool thread.
    """
    def __init__(self, prompt: str):
        super().__init__()
        self.prompt = prompt
        self.signals = AISignals()
        self.setAutoDelete(True) 

    def run(self):
        """
        The main method of the worker, executed by the QThreadPool.
        """
        reply = get_response(self.prompt)
        
        # Signals are automatically thread-safe (queued to the main thread).
        if reply is not None:
            self.signals.finished.emit(reply)
        else:
            # Emitting the error signal passes None or the error result back.
            self.signals.error.emit(reply)