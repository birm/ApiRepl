import json
import pymysql

class BaseWorker(object):
    """
    Base tools to fetch and use objects from an
     API and process them gracefully with a generator.
    Defines a base api usage method; inhereting classes will
     likely have a different api() function.
    """

    def __init__(self, *args, **kwargs):
        """Handle general initialization for all classes."""
        self.args = args
        self.kwargs = kwargs
        self.itemtype = kwargs.get('type', "undefined")
        host = self.kwargs.get('host', "localhost")
        db = self.kwargs.get('db', "apirepl")
        cursor = pymysql.connect(host=host, db=db).cursor(pymysql.cursors.DictCursor)
        self.cursor = cursor

        queue_query = "select * from queue where type = %s and started is null\
        order by priority desc limit 1;"
        # keep those variables
        cursor.execute(queue_query, (kwargs.get('type', "undefined"), ))
        result = cursor.fetchone()
        self.maximum = result['min']
        self.minimum = result['max']
        self.apitype = result['type']
        queue_id = result['id']
        self.queue_id = queue_id

        started_query = "update queue set started=now() where\
        id=%s; self.queue_id;"
        cursor.execute(started_query, (queue_id,))
        self.count = 0
        self.finished = False
        self.last = self.minimum

    def __iter__(self):
        """
        Return the iterator/generator object.
        """
        return self

    def __next__(self):
        """
        Get the next item in the generator.
        """
        return self.next()


    def api(self):
        """
        Search the api for the next item.
        """
        self.last
        if self.count<=1: # if there's more to go
            return {{"title": "Sample Record"}}
        else: # if done
            self.finished = True
            return 0

    def next(self):
        """
        Get the next item in the generator.
        """
        try:
            item = self.api()
            yield item
            if not item:
                raise StopIteration
        except StopIteration:
            pass
        except Exception as err:
            query = "insert into error (type, error, source)\
             values(%s, %s, %s);"
            self.cursor.execute(query, (self.apitype, str(err), self.queue_id))
            raise err
        self.count += 1

    def __del__(self):
        """
        Handle queue and log before deletion.
        """
        query = "insert into fetchlog (recordsadded)\
         values(%s);"
        self.cursor.execute(query, (self.count,))
        done_queue = "update queue set finished = now() where id = %s;"
        self.cursor.execute(done_queue, (self.queue_id,))
        if not self.finished:  # if we didn't finish
            # if we did not, add a new queue entry
            next_queue = "insert into queue (priority, type, min, max)\
            values(%s, %s, %s, %s);"
            self.cursor.execute(next_queue, (self.priority,
                                             self.apitype,
                                             self.last,  self.maximum))
