import hopsworks
import json
import hsfs.constructor.query
import logging

logger = logging.getLogger('logger')


class FeatureStoreService:
    def __init__(self, config):
        self.conf = config
        with open(self.conf, "r") as jsonfile:
            data = json.load(jsonfile)

        self.hopsworks_host = data['hopsworks_host']
        self.hopsworks_port = data['hopsworks_port']
        self.hopsworks_project = data['hopsworks_project']
        self.hopsworks_api_key_value = data['hopsworks_api_key_value']

    def get_feature_store_connection(self):
        try:
            logger.info('Trying to establish a connection with the hopsworks project')
            connection = hopsworks.login(host=self.hopsworks_host,
                                         port=self.hopsworks_port,
                                         project=self.hopsworks_project,
                                         api_key_value=self.hopsworks_api_key_value)
            fs = connection.get_feature_store()
            logger.info('Connection successfully established with the hopsworks project')
            return fs

        except Exception as e:
            logger.error('Connection failed to establish. ' + e)

        finally:
            pass

    def close_feature_store_connection(self, fs):
        try:
            hopsworks.Connection.close(fs)
            logger.info('Connection closed with the hopsworks project')
        except Exception as e:
            logger.error(e)

        finally:
            pass

    def get_group(self, group_name: str, version: int):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to retrieve a feature group')
            fg = fs.get_feature_group(group_name, version)
            logger.info('Feature group has been successfully retrieved')
            return fg

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def build_group(self, group_name: str, version: int, description: str, primary_key: [str], partition_key: [str],
                    features: [hsfs.feature.Feature], df):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to build a feature group')
            fg = fs.get_or_create_feature_group(
                name=group_name,
                version=version,
                description=description,
                primary_key=primary_key,
                partition_key=partition_key
            )
            fg.insert(df)
            logger.info('Feature group has been successfully built')

        except Exception as e:
            logger.error(e)
            pass

        finally:
            pass

    def drop_group(self, group_name: str, version: int):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to delete a feature group')
            fg = fs.get_feature_group(group_name, version)
            fg.delete()
            logger.info('Feature group has been successfully deleted')

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def get_view(self, view_name: str, version: int):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to retrieve a feature view')
            fv = fs.get_feature_view(view_name, version)
            logger.info('Feature view has been successfully retrieved')
            return fv

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def build_view(self, view_name: str, view_version: int, description: str, trans_functions: [],
                   query: hsfs.constructor.query.Query):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to build a feature view')
            logger.info('Retrieving the respective feature group')

            fs.create_feature_view(
                name=view_name,
                version=view_version,
                description=description,
                ## TODO: insert the correct labels below
                labels=["box_type"],
                query=query
            )
            logger.info('Feature view has been successfully created')

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def drop_view(self, view_name: str, version: int):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to delete a feature view')
            fv = fs.get_feature_view(view_name, version)
            fv.delete()
            logger.info('Feature view has been successfully deleted')

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def do_drop_group(self, group_name: str, version: int):
        try:
            fs = self.get_feature_store_connection()
            logger.info('Trying to hard delete a feature group')
            logger.info('Feature group has been successfully hard deleted')

        except Exception as e:
            logger.error(e)

        finally:
            pass
