import unittest
import backend.routine_backend as backend
from logger import *


class TestBackendFunctions(unittest.TestCase):

    def setUp(self):
        # Create a fresh database and table before each test
        backend.connect()
        

    
    def tearDown(self):
        # Clean up after each test by dropping the table
        conn = backend.sqlite3.connect('routine.db')
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS routine")
        conn.commit()
        conn.close()

    def test_insert_and_view(self):
        # Test insert() and view() functions
        backend.insert('2-3-20', 200, 'done', 'done', 'yes', 300)
        rows = backend.view()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], '2-3-20')
        self.assertEqual(rows[0][2], 200)
        self.assertEqual(rows[0][3], 'done')
        self.assertEqual(rows[0][4], 'done')
        self.assertEqual(rows[0][5], 'yes')
        self.assertEqual(rows[0][6], 300)
        logging.info("Test 1 :-test_insert_and_view")

    def test_search(self):
        # Test search() function
        backend.insert('2-3-20', 200, 'done', 'done', 'yes', 300)
        backend.insert('3-3-20', 400, 'done', 'not done', 'yes', 500)
        backend.insert('4-3-20', 600, 'not done', 'not done', 'yes', 700)
        logging.info("Test 2 :-test_search")

        results = backend.search(earnings=400)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], '3-3-20')
        self.assertEqual(results[0][2], 400)
        self.assertEqual(results[0][3], 'done')
        self.assertEqual(results[0][4], 'not done')
        self.assertEqual(results[0][5], 'yes')
        self.assertEqual(results[0][6], 500)

    def test_delete(self):
        # Test delete() function
        backend.insert('2-3-20', 200, 'done', 'done', 'yes', 300)
        backend.insert('3-3-20', 400, 'done', 'not done', 'yes', 500)
        backend.insert('4-3-20', 600, 'not done', 'not done', 'yes', 700)
        logging.info("Test 3 :-test_delete")

        backend.delete(2)
        rows = backend.view()
        self.assertEqual(len(rows), 2)

        # The row with id=2 should have been deleted, so it shouldn't be in the list
        for row in rows:
            self.assertNotEqual(row[0], 2)

if __name__ == '__main__':
    unittest.main()
