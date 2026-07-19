from dispatcher_service import DispatcherService
import multiprocess as mq

## implementazione di DispatcherService
class dispatcherImpl(DispatcherService): # dispatcherImpl implementa DispatcherService (il mio servizio)

    def __init__(self, queue=mq.Queue(5)):
        self.queue = queue

    def sendCmd(self, value):
        self.queue.put(value)
    
    def getCmd(self):
        value_to_get = self.queue.get()
        return value_to_get
