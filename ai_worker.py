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
    # Emits the successful reply text (str)
    finished = Signal(str)      
    # Emits if the request fails (None is passed)
    error = Signal(Optional[str]) 

class AIWorker(QObject):
    """
    Worker for the API call, executing in a standard Python thread.
    
    NOTE: We switched from QRunnable to QObject managing a thread 
    to resolve potential conflicts between Qt's thread pool and 
    the 'requests' library's underlying I/O.
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
        self._thread.daemon = True # Allows application to exit even if thread is running
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
            # Emitting the error signal passes None or the error result back.
            self.signals.error.emit(reply)
            
# The ai_client.py remains unchanged.