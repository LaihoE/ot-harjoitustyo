import unittest
from anti_cheat import Model
import numpy as np
import os
from db import Database
import sqlalchemy
import sqlite3
import pandas as pd


class TestDb(unittest.TestCase):
    def setUp(self):
        dbpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'database', 'database.db'))
        self.db = Database(dbpath)
        if not os.path.isfile(dbpath):
            df = pd.DataFrame([['testdemo.dem',
                                'test', 76561198112665678, 4894, 0.76984928035736084]])
            df.to_sql('testtable', con=self.db.engine, if_exists='append')


    def test_insert_successful(self):
        dbpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'database', 'database.db'))
        db = Database(dbpath)
        df = pd.DataFrame([['match730_003416179073414595204_0172264905_181.dem',
                            'Two pa cool', 76561198112665670, 1384, 0.46584928035736084]])
        df.to_sql('testtable', con=db.engine, if_exists='append')


    def test_fetch_successful(self):
        """
        Seems like the setUp doesnt commit the changes? something is up, have to redo the insert here for it to work always.
        Maybe df.to_sql aint too great, will revisit next week
        """
        # insert
        df = pd.DataFrame([['match730_003416179073414595204_0172264905_181.dem',
                            'Two pa cool', 76561198112665670, 1384, 0.46584928035736084]])
        df.to_sql('testtable', con=self.db.engine, if_exists='append')

        # Actual test
        data = self.db.find_data(table='testtable')
        for row in data:
            # Each row has 6 values
            self.assertEqual(len(row), 6)
            # Tick is an integer
            self.assertEqual(type(row[-2]), int)
            # Steamid is correct
            self.assertEqual(len(str(row[3])), len('76561198978973136'))
            self.assertEqual(str(row[3])[:3], '765')
            # Probablity (confidence) is between 0 and 1
            self.assertEqual(0 < row[-1] < 1, True)

