import json
import logging
import pandas as pd
from sqlalchemy.sql import text
from pathlib import Path
import sys
import os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0,parent_dir)

from src.service import FeatureStoreService as fss, ComplexFeatureService as cfs
from src.database import DbTables

logger = logging.getLogger('logger')

class SimpleFeatureService:
    def __init__(self, config):
        self.conf = config
        with open(self.conf, "r") as jsonfile:
            data = json.load(jsonfile)

    def get_group(self, group_name: str, version: int):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fg = fss_obj.get_group(group_name, version)
            return fg

        except Exception as e:
            logger.error(e)

    def get_group_features(self, group_name: str, version: int, features):
        """

        :param group_name: Name of the feature group required to be fetched
        :param version: Version of the feature group required to be fetched
        :param features: Comma-separated list of features of the feature group required to be fetched
        :return: returns dataframe of required features
        """
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fg = fss_obj.get_group(group_name, version)
            query = fg.select(features)
            df = query.read()
            print(df.head())
            return df

        except Exception as e:
            logger.error(e)

    def build_group_from_db(self, group_name: str, version: int, description: str, table_name: str, primary_key: [],
                            partition_key: [], features: [], derived_features: []):
        """

        :param group_name: Name of the feature group to be built
        :param version: Version of the feature group to be built
        :param description: Short description of the feature group to be built
        :param table_name: Name of the table name which would be used to create the feature group
        :param primary_key: List of columns that would be designated as prime attributes in the feature group
        :param partition_key: List of columns that would be designated as partition key in the feature group
        :param features: List of table columns that would be used as features in the feature group
        :param derived_features: List of derived columns from the table that would be used as features in the feature group
        :return: returns nothing
        """
        try:
            dbtables_obj = DbTables.DbTables(self.conf)
            conn = dbtables_obj.get_db_conn()
            logger.info('Getting table details and data from the database')
            query = text('SELECT ' + ','.join(features + derived_features).strip(',') + ' FROM ' + table_name)
            df = dbtables_obj.run_query(conn, query)
            fss_obj = fss.FeatureStoreService(self.conf)
            fss_obj.build_group(group_name, version, description, primary_key, partition_key, features, df)

        except Exception as e:
            logger.error(e)

        finally:
            dbtables_obj.close_db_conn(conn)

    def build_group_from_view(self, group_name: str, group_version: int, description: str, view_name: str,
                              view_version: int, features: [],
                              primary_key: [], partition_key: []):
        try:
            logger.info('Getting details from the feature view')
            fss_obj = fss.FeatureStoreService(self.conf)
            fv = fss_obj.get_view(view_name, view_version)
            df = fv.query.read()
            df_filtered = df[[x.lower() for x in features]]
            fss_obj.build_group(group_name, group_version, description, primary_key, partition_key, df_filtered.columns.tolist(),
                                df_filtered)

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def build_group_from_file(self, group_name: str, group_version: int, description: str, file_path: str,
                              file_name: str, sep: str, index: str, header: str, quote_char: str, escape_char: str,
                              primary_key: [], partition_key: [], features: []):
        try:
            logger.info('Getting details from the file')
            fss_obj = fss.FeatureStoreService(self.conf)
            df = pd.read_csv(file_path + file_name, sep=sep, index_col=eval(index), header=header, quotechar=quote_char,
                             escapechar=escape_char)
            df_filtered = df[[x.lower() for x in features]]
            fss_obj.build_group(group_name, group_version, description, primary_key, partition_key, df_filtered.columns.tolist(),
                                df_filtered)

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def export_group_to_file(self, group_name: str, version: int, file_path: str, file_name: str):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fg = fss_obj.get_group(group_name, version)
            query = fg.select_all()
            df = query.read()

            out_file = file_name
            out_dir = Path(file_path)
            out_dir.mkdir(parents=True, exist_ok=True)
            df.to_csv(out_dir / out_file, sep='|', index=False, header=True, quotechar='"', escapechar="\"")

            return fg

        except Exception as e:
            logger.error(e)

    def drop_group(self, group_name: str, version: int):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fss_obj.drop_group(group_name, version)
        except Exception as e:
            logger.error(e)

    def get_view(self, view_name: str, version: int):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fv = fss_obj.get_view(view_name, version)
            return fv

        except Exception as e:
            logger.error(e)

    def get_view_features(self, view_name: str, version, features):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fv = fss_obj.get_view(view_name, version)
            df = fv.query.read()
            df_filtered = df[features]
            print(df_filtered.head())
            return df_filtered

        except Exception as e:
            logger.error(e)

    def build_view(self, view_name, view_version, description, view_json):
        try:
            cfs_obj = cfs.ComplexFeatureService(self.conf)

            if (view_name == 'view_name1'):
                ##TODO: Implement logic for view 1
                pass

            elif (view_name == 'view_name2'):
                ##TODO: Implement logic for view 2
                pass

            elif (view_name == 'view_name3'):
                ##TODO: Implement logic for view 3
                pass
            else:
                logger.error('Feature view function not found. Please implement the function in '
                             'ComplexFeatureService class.')
        except Exception as e:
            logger.error(e)

        finally:
            pass

    def export_view_to_file(self, view_name: str, version: int, file_path: str, file_name: str):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fv = fss_obj.get_view(view_name, version)

            df = fv.query.read()

            out_file = file_name
            out_dir = Path(file_path)
            out_dir.mkdir(parents=True, exist_ok=True)
            df.to_csv(out_dir / out_file, sep='|', index=False, header=True, quotechar='"', escapechar="\"")

            return fv

        except Exception as e:
            logger.error(e)

    def drop_view(self, view_name: str, version: int):
        try:
            fss_obj = fss.FeatureStoreService(self.conf)
            fss_obj.drop_view(view_name, version)
        except Exception as e:
            logger.error(e)
