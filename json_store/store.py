import tempfile
import os
import json
from threading import Lock
from functools import partial

class CannotSerialize(RuntimeError): pass

class JSONStore(object):

    lock = Lock()

    def __init__(self, name=None):
        self.dump = partial(json.dump, indent=2)

        if name:
            self.filename = name
        else:
            self.tempdir = tempfile.mkdtemp()
            self.filename = os.path.join(self.tempdir, "store.json")

    def raise_if_cannot_serialise(self, data):
        try:
            _ = json.dumps(data)
        except TypeError as err:
            if "serializable" in str(err):
                raise CannotSerialize("Cannot serialise data: {0}"
                                        .format(data))
            else:
                raise


    def append(self, data=None, **kwargs):
        previous_data = self.read()

        data = data if data else {}
        new_data = previous_data + [dict(data, **kwargs)]

        self.raise_if_cannot_serialise(new_data)

        with self.lock:
            with open(self.filename, 'w') as outfile:
                self.dump(new_data, outfile)

    def read(self):
        with self.lock:
            try:
                with open(self.filename) as infile:
                    return json.load(infile)
            except IOError:
                return []

    def __str__(self):
        return '<JSONStore fname:{0} contents:{1}>'.format(
            self.filename, self.read())
