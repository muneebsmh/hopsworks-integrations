import unittest
import sys
import os
import json

parent_dir = os.path.dirname(__file__)
sys.path.insert(0, parent_dir)
from src.database import DbTables
from src.service import FeatureStoreService

"""
UnitTest class: All the test cases are to be written here and this test class can be called using the following command:
pytest -v UnitTest.py
"""

class Tests(unittest.TestCase):
    config = 'D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\tests\\test_conf.json'

    def test_db_connectivity(self):
        db = DbTables.DbTables(self.config)
        conn = db.get_db_conn()
        query = 'select 1 as test_col'
        actual_df = DbTables.DbTables.run_query(self, conn, query)
        returned_value = actual_df.iloc[0, 0]
        expected_value = 1

        self.assertTrue(returned_value == expected_value)

    def test_hopsworks_connectivity(self):
        with open(self.config, "r") as jsonfile:
            test_data = json.load(jsonfile)
        fss = FeatureStoreService.FeatureStoreService(self.config)
        fs = fss.get_feature_store_connection()
        expected_value = test_data['hopsworks_project'] + '_featurestore'
        returned_value = fs.name

        self.assertTrue(returned_value == expected_value)

    def test_hopsworks_group_retrieval(self):
        with open(self.config, "r") as jsonfile:
            test_data = json.load(jsonfile)
        test_group_name = test_data['test_group_name']
        test_group_version = test_data['test_group_version']
        fss = FeatureStoreService.FeatureStoreService(self.config)
        fg = fss.get_group(test_group_name, test_group_version)

        expected_value = test_group_name
        returned_value = fg.name

        self.assertTrue(returned_value == expected_value)

    def test_hopsworks_view_retrieval(self):
        with open(self.config, "r") as jsonfile:
            test_data = json.load(jsonfile)
        test_view_name = test_data['test_view_name']
        test_view_version = test_data['test_view_version']
        fss = FeatureStoreService.FeatureStoreService(self.config)
        fv = fss.get_view(test_view_name, test_view_version)

        expected_value = test_view_name
        returned_value = fv.name

        self.assertTrue(returned_value == expected_value)
