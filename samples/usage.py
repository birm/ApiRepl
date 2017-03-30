"""
To demonstrate how to use this class, here is one way to use this tool.
"""
import json
import urllib2
import random
import pymysql

from ApiRepl import BaseWorker

"""
Sample Schema:
Person:
- Name
- DOB
- Height
"""

class PersonWorker(BaseWorker):
    """ A fictional worker for a person api. """
    def api(self):
        """ Specalization for this api. """
        # get a list of names
        people = json.load(urllib2.urlopen("api.people.com/"))
        # toss out those out of range
        lookup = [p for p in people.keys() if
                  p > self.last and p <= self.maximum]
        if len(lookup) == 0:
            return 0
        who = sorted(lookup)[0]
        self.last = who
        person = json.load(urllib2.urlopen(
            "api.people.com/{item}".format(item=who)))
        return person


def saveobj(item):
    """Save each object from the worker."""
    # connect to database
    cursor = pymysql.connect(host='localhost', db='fetch').cursor()
    cursor.execute('insert into Person (Name, DOB, Height) values (%s %s %s)',
                   (item['Name'], item['DOB'], item['Height']))


def throttle():
    """Simulate a kill condition."""
    return random.random() > 0.95

if __name__ == "__main__":
    worker = PersonWorker(type="person")
    for item in worker:
        if item is 0 or throttle():
            del worker
        saveobj(item)
