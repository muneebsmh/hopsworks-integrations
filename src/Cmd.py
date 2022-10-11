import json
import logging
import argparse
from datetime import datetime
from src.service import SimpleFeatureService, ComplexFeatureService
from src.utils import process_logging
from pathlib import Path
import sys

def main(argv=sys.argv[1:]):
    try:
        """
            There are 12 run modes to call this application from the CLI.
            1) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_group --group_name gp_game_base --group_version 1
            2) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_group_features --group_name gp_box_score --group_version 1 --features adv_idx_uuid,box_type,mp
            3) python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_db --group_name gp_game_base
            4) python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_view --group_name test_group_from_view
            5) python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_file --group_name test_group_from_file
            6) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode export_group_to_file --group_name gp_game_base --group_version 1 --file_path "/path/to/export/folder/" --file_name gp_game_base_export.csv
            7) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode drop_group --group_name gp_game_base --group_version 1
            8) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_view --view_name t1vst2 --view_version 1
            9) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_view_features --view_name t1vst2 --view_version 1  --features uuid,box_type,mp
            10) python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/views.json" --run_mode build_view --view_name t1vst2
            11) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode export_view_to_file --view_name t1vst2 --view_version 1 --file_path "/path/to/export/folder/" --file_name t1vst2_view_export.csv
            12) python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode drop_view --view_name t1vst2 --view_version 1
    
            python.exe cmd.py --conf "config/conf.json" --build_conf "config/groups.json" --run_mode build_group --group_name gp_game_base
    
            Mandatory arguments: 
                --conf, --run_mode
            Optional arguments:
                build_conf, group_name, group_version, view_name, view_version, file_path, and file_name are optional and 
                will be used based on the operation type. For e.g. if you are running only get_group then you don't need 
                to specify build_conf argument, but you when you are running build_group, then you need to specify 
                build_conf argument but you don't need to specify group version in that. 
                See the examples below for clarification.
        """
        parser = argparse.ArgumentParser(description="Arguments for calling Feature Store API")

        parser.add_argument('-cn', '--conf',
                            type=str,
                            default='config/conf.json',
                            help='name of the configuration file',
                            required=True)

        parser.add_argument('-bc', '--build_conf',
                            type=str,
                            default='config/groups.json',
                            help='name of the preset file required to create a group or a view',
                            required=False)

        parser.add_argument('-r', '--run_mode',
                            type=str,
                            default='get_group',
                            help='type of operations: '
                                 '1) get_group'
                                 '2) get_group_features'
                                 '3) build_group_from_db'
                                 '4) build_group_from_view'
                                 '5) build_group_from_file'
                                 '6) export_group_to_file'
                                 '7) drop_group'
                                 '8) get_view'
                                 '9) get_view_features'
                                 '10) build_view'
                                 '11) export_view_to_file'
                                 '12) drop_view',
                            required=True)

        parser.add_argument('-gn', '--group_name',
                            type=str,
                            default='gp_game_base',
                            help='name of the required feature group',
                            required=False)

        parser.add_argument('-gv', '--group_version',
                            type=str,
                            default='1',
                            help='version of the feature group required to retrieve or create',
                            required=False)

        parser.add_argument('-vn', '--view_name',
                            type=str,
                            default='t1vst2',
                            help='name of the required feature view',
                            required=False)

        parser.add_argument('-vv', '--view_version',
                            type=str,
                            default='1',
                            help='version of the feature version required to retrieve or create',
                            required=False)

        parser.add_argument('-f', '--features',
                            type=str,
                            default='',
                            help='comma separated list of required group or view features',
                            required=False)

        parser.add_argument('-fp', '--file_path',
                            type=str,
                            default='files',
                            help='directory of the input/output files',
                            required=False)

        parser.add_argument('-fn', '--file_name',
                            type=str,
                            default='export.csv',
                            help='name of the input/output files',
                            required=False)

        args = parser.parse_args(argv)

        with open(args.conf, "r") as jsonfile:
            conf = json.load(jsonfile)

        today_datetime = datetime.now().strftime("%d%m%Y_%H%M%S")
        Path(conf['log_path']).mkdir(parents=True, exist_ok=True)
        process_logger = process_logging.process_logging()
        process_logger.process_log('logger', conf['log_path'] + '\\logs_' + today_datetime + '.txt')
        logger = logging.getLogger('logger')

        logger.info('The job has started')

        sfs = SimpleFeatureService.SimpleFeatureService(args.conf)
        cfs = ComplexFeatureService.ComplexFeatureService(args.conf)

        if args.run_mode == 'get_group':
            fg = sfs.get_group(args.group_name, args.group_version)
            return fg

        elif args.run_mode == 'get_group_features':
            df = sfs.get_group_features(args.group_name, args.group_version, list(args.features.split(',')))
            return df

        elif args.run_mode == 'build_group_from_db':
            with open(args.build_conf, "r") as jsonfile:
                groups_info = json.load(jsonfile)
                if args.group_name not in groups_info:
                    logger.error('Feature group key is not found in the groups json file')

                for group_name in groups_info:
                    if group_name == args.group_name:
                        group = groups_info[group_name]
                        sfs.build_group_from_db(group['hopsworks_group_name'],
                                                group['hopsworks_group_version'],
                                                group['description'],
                                                group['table_name'],
                                                group['primary_key'],
                                                group['partition_key'],
                                                group['features'],
                                                group['derived_features'])

        elif args.run_mode == 'build_group_from_view':
            with open(args.build_conf, "r") as jsonfile:
                groups_info = json.load(jsonfile)
                if args.group_name not in groups_info:
                    logger.error('Feature group key is not found in the groups json file')

                for group_name in groups_info:
                    if group_name == args.group_name:
                        group = groups_info[group_name]
                        sfs.build_group_from_view(group['hopsworks_group_name'],
                                                  group['hopsworks_group_version'],
                                                  group['description'],
                                                  group['hopsworks_view_name'],
                                                  group['hopsworks_view_version'],
                                                  group['features'],
                                                  group['primary_key'],
                                                  group['partition_key'])

        elif args.run_mode == 'build_group_from_file':
            with open(args.build_conf, "r") as jsonfile:
                groups_info = json.load(jsonfile)
                if args.group_name not in groups_info:
                    logger.error('Feature group key is not found in the groups json file')

                for group_name in groups_info:
                    if group_name == args.group_name:
                        group = groups_info[group_name]
                        sfs.build_group_from_file(group['hopsworks_group_name'],
                                                  group['hopsworks_group_version'],
                                                  group['description'],
                                                  group['file_path'],
                                                  group['file_name'],
                                                  group['sep'],
                                                  group['index_col'],
                                                  group['header_row'],
                                                  group['quote_char'],
                                                  group['escape_char'],
                                                  group['primary_key'],
                                                  group['partition_key'],
                                                  group['features'])

        elif args.run_mode == 'export_group_to_file':
            sfs.export_group_to_file(args.group_name, args.group_version, args.file_path, args.file_name)

        elif args.run_mode == 'drop_group':
            sfs.drop_group(args.group_name, args.group_version)

        elif args.run_mode == 'get_view':
            fv = sfs.get_view(args.view_name, args.view_version)
            return fv

        elif args.run_mode == 'get_view_features':
            df = sfs.get_view_features(args.view_name, args.view_version, list(args.features.split(',')))
            return df

        elif args.run_mode == 'build_view':
            with open(args.build_conf, "r") as jsonfile:
                views_info = json.load(jsonfile)
                if args.view_name not in views_info:
                    logger.error('Feature group key is not found in the groups json file')

                for view_name in views_info:
                    if view_name == args.view_name:
                        if (args.view_name in ['t1vst2', 'team', 'league']):
                            view = views_info[view_name]
                            a = view['hopsworks_view_name']
                            cfs.build_view(view['hopsworks_view_name'],
                                           view['hopsworks_view_version'],
                                           view['description'],
                                           view['features'])
                        else:
                            view = views_info[view_name]
                            a = view['hopsworks_view_name']
                            sfs.build_view(view['hopsworks_view_name'],
                                           view['hopsworks_view_version'],
                                           view['description'],
                                           view['features'])
        elif args.run_mode == 'export_view_to_file':
            sfs.export_view_to_file(args.view_name, args.view_version, args.file_path, args.file_name)

        elif args.run_mode == 'drop_view':
            sfs.drop_view(args.view_name, args.view_version)

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main(sys.argv[1:])