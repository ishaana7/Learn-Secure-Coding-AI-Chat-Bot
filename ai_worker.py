# ai_worker.py
import threading
from PySide6.QtCore import QObject, Signal
from typing import Optional
from ai_client import get_response

# Signals must inherit from QObject
class AISignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = Signal(str)      # Emits the successful reply text (str)
    
    # FIX: Define the error signal to accept one string argument
    error = Signal(str) 

class AIWorker(QObject):
    """
    Worker for the API call, executing in a standard Python thread.
    
    NOTE: We use QObject managing a standard Python thread (threading.Thread) 
    to avoid conflicts between Qt's thread pool and the 'requests' library's I/O.
    """
    def __init__(self, prompt: str, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.signals = AISignals()
        self._thread = None

    def run(self):
        """
        Starts the API call in a new dedicated Python thread.
        """
        # Create a standard Python thread to run the potentially problematic I/O
        self._thread = threading.Thread(target=self._execute_api_call)
        self._thread.daemon = True 
        self._thread.start()

    def _execute_api_call(self):
        """
        The actual work to be done in the background thread.
        """
        reply = get_response(self.prompt)
        
        # Signals are automatically thread-safe (queued to the main thread).
        if reply is not None:
            self.signals.finished.emit(reply)
        else:
            # FIX: Emit an empty string ("") instead of None to match the Signal(str) signature
            self.signals.error.emit("") 

# NOTE: The rest of the content from the original ai_worker.py 
# (which includes the get_response function) is assumed to be 
# in ai_client.py or elsewhere and doesn't need to be repeated here.