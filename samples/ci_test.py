"""
To demonstrate how to use this class, here is one way to use this tool.
"""

from ApiRepl import BaseWorker


class PersonWorker(BaseWorker):
    """ A fictional worker for a person api. """
    def api(self):
        """ Specalization for this api. """
        return {'TEST':'Success'}


def saveobj(item):
    return item

def throttle():
    """Simulate a kill condition."""
    return random.random() > 0.95

def test_specalization():
    worker = PersonWorker(type="person")
    for item in worker:
        if item is 0 or throttle():
            del worker
        saveobj(item)
