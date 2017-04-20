import unittest
import os.path
from os import getenv
from datetime import datetime
from models.base_model import Base
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models.state import State
from models import *

"""
TODO: Need to fix removal of data from database after each test is run.

For now, skipping these tests. Make sure to edit `skipIf` call.
"""
@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class Test_DBStorage(unittest.TestCase):
    """
    Test the file storage class
    """
    @classmethod
    def setUpClass(cls):
        storage.reload()

    def setUp(self):
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': "0234",
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': 'wifi'}
        self.model = Amenity(**test_args)
        self.test_len = 0

    def test_all(self):
        output = storage.all('Amenity')
        self.assertEqual(len(output), self.test_len)

    def test_new(self):
        # note: we cannot assume order of test is order written
        self.test_len = len(storage.all())
        self.model.save()
        self.assertEqual(len(storage.all()), self.test_len + 1)
        a = Amenity(name="thing")
        a.save()
        self.assertEqual(len(storage.all()), self.test_len + 2)

        storage.delete(a)
        storage.delete(self.model)
        storage.save()

    def test_save(self):
        test_len = len(storage.all())
        a = Amenity(name="another")
        a.save()
        self.assertEqual(len(storage.all()), test_len + 1)
        b = State(name="california")
        self.assertNotEqual(len(storage.all()), test_len + 2)
        b.save()
        self.assertEqual(len(storage.all()), test_len + 2)

        storage.delete(a)
        storage.delete(b)
        storage.save()

    def test_reload(self):
        self.model.save()
        a = Amenity(name="different")
        a.save()
        for value in storage.all().values():
            self.assertIsInstance(value.created_at, datetime)

        storage.delete(self.model)
        storage.delete(a)
        storage.save()

    def test_get(self):
        self.model.save()
        a = storage.get("Amenity", "0234")
        self.assertIs(type(a), dict)
        b = storage.get(None, "0234")
        self.assertIs(None, b)

        storage.delete(self.model)
        storage.save()

    def test_count(self):
        a = storage.count(cls="Amenity")
        self.assertEqual(len(storage.all("Amenity")), a)
        b = storage.count(cls=None)
        self.assertEqual(len(storage.all()), b)


if __name__ == "__main__":
    unittest.main()
