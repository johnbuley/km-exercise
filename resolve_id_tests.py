import unittest
from resolve_id import *
from tokyo.dbm import *

class ResolveIDTest(unittest.TestCase):

    # Insert test key-value pair into database
    @classmethod
    def setUpClass(cls):
        db = open('people.db','w')
        if b'testid1' not in db:
            db[b'testid1'] = b'ntestid2'
        db.close()

    def setUp(self):
        self.db = open('people.db')

    def test_find_internal_id_fcn(self):
        self.assertEqual( 
            find_internal_id(b'++2mbves6uno87agf4uwhqdgmau=',self.db),
            3118062)

    def test_find_internal_id_fcn_dead_end(self):
        self.assertRaises(
            SystemExit,
            find_internal_id,
            b'testid1',
            self.db)

    def test_resolve_fcn(self):
        self.assertEqual(
            resolve(b'++2mbves6uno87agf4uwhqdgmau=',self.db),
            3118062)

    def test_resolve_fcn_dead_end(self):
        self.assertRaises(
            SystemExit,
            resolve,
            b'testid1',
            self.db)

    def tearDown(self):
        self.db.close()

    # Remove test key-value pair from database
    @classmethod
    def tearDownClass(cls):
        db = open('people.db','w')
        if b'testid1' in db:
            db.pop(b'testid1',None)
        db.close()

if __name__ == '__main__':
    unittest.main()
