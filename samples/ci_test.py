"""
To demonstrate how to use this class, here is one way to use this tool.
"""

from ApiRepl import BaseWorker
import random

class PersonWorker(BaseWorker):
    """ A fictional worker for a person api. """
    def __init__(self, *args, **kwargs):
        BaseWorker.__init__(self, *args, **kwargs)

    def api(self):
        """ Specalization for this api. """
        self.finished=True
        return {'TEST':'Success'}


def saveobj(item):
    return item

def throttle():
    """Simulate a kill condition."""
    return random.random() > 0.95

def test_specalization():
    worker = PersonWorker(type="undefined")
    for item in worker:
        if item is 0 or throttle():
            break
        saveobj(item)
    del worker
