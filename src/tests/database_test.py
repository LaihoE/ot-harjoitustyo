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
        db = Database(dbpath)
        if not os.path.isfile(dbpath):
            data_dict = {}
            data_dict["predictions"] = [0.46584928035736084]
            data_dict["player_names"] = ["Two pa cool"]
            data_dict["player_ids"] = [76561198112665670]
            data_dict["ticks"] = [1384]
            data_dict["file_names"] = ["match730_003416179073414595204_0172264905_181.dem"]
            df = pd.DataFrame.from_dict(data_dict)
            df.to_sql('testtable', con=db.engine, if_exists='append')

    def test_insert_successful(self):
        dbpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'database', 'database.db'))
        db = Database(dbpath)

        data_dict = {}
        data_dict["predictions"] = [0.46584928035736084]
        data_dict["player_names"] = ["Two pa cool"]
        data_dict["player_ids"] = [76561198112665670]
        data_dict["ticks"] = [1384]
        data_dict["file_names"] = ["match730_003416179073414595204_0172264905_181.dem"]
        df = pd.DataFrame.from_dict(data_dict)
        df.to_sql('testtable', con=db.engine, if_exists='append')

    def test_fetch_successful(self):
        """
        Seems like the setUp doesnt commit the changes? something is up, have to redo the insert here for it to work always.
        Maybe df.to_sql aint too great, will revisit next week
        """
        # insert
        dbpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db'))
        db = Database(dbpath)
        data_dict = {}
        data_dict["predictions"] = [0.46584928035736084]
        data_dict["player_names"] = ["Two pa cool"]
        data_dict["player_ids"] = [76561198112665670]
        data_dict["ticks"] = [1384]
        data_dict["file_names"] = ["match730_003416179073414595204_0172264905_181.dem"]
        df = pd.DataFrame.from_dict(data_dict)
        print(df.columns)
        df.to_sql('testtable', con=db.engine, if_exists='append')

        # Actual test
        data = db.find_data(table='testtable')
        row = data.iloc[0].tolist()
        print(row)
        # Each row has 6 values
        self.assertEqual(len(row), 5)
        # Tick is an integer
        self.assertEqual(type(int(row[-1])), int)
        # Steamid is correct
        self.assertEqual(len(str(row[2])), len('76561198978973136'))
        self.assertEqual(str(row[2])[:3], '765')
        # Probablity (confidence) is between 0 and 1
        self.assertEqual(0 < float(row[0]) < 1, True)
