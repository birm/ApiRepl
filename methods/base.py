import json
import pymysql

class BaseWorker(Object):
    """
    Base tools to fetch and use objects from an
     API and process them gracefully with a generator.
    Defines a base api usage method; inhereting classes will
     likely have a different api() function.
    """

    def __init__(self, *args, **kwargs):
        """Handle general initialization for all classes."""
        self.type = type
        self.args = args
        self.kwarfs = kwargs
        cursor = pymysql.connect(host='localhost', db='fetch').cursor()
        self.cursor = cursor

        queue_query = "select * from queue where started is null\
        order by priority desc limit 1;"
        # keep those variables
        cursor.execute(queue_query)
        result = cursor.fetchone()
        self.maximum = result['min']
        self.minimum = result['max']
        self.state = result['state']
        queue_id = result['id']
        self.queue_id = queue_id

        started_query = "update queue set in_progress='Y' where\
        id=%s; self.queue_id;"
        cursor.execute(started_query, (queue_id,))
        self.count = 0
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

    # search the api for the next item
    def api(self):
        """
        Search the api for the next item.
        """
        self.last
        if True: # if there's more to go
            return {{"title": "Sample Record"}}
        else: # if done
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
            query = "insert into error (state, error, source)\
             values(%s, %s, %s);"
            self.cursor.execute(query, (self.state, str(err), self.queue_id))
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
        if False: # if we didn't finish
            # if we did not, add a new queue entry
            next_queue = "insert into queue (priority, state, min, max)\
            values(%s, %s, %s, %s);"
            self.cursor.execute(neq_queue, (self.priority, self.state,
                                            self.last, self.maximum))
