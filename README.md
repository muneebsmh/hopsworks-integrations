# Hopsworks-Integration
This project has been built to be called using the CLI commands. This application provides the abstraction with the Hopsworks Feature Store and lets the user build and retrieve the required Hopsworks feature groups and feature view.

## Configurations:
There is a conf.json file in the project that lets the user store the necessary credentials like the database connection, and hopsworks credentials, and the json files that are used to build feature groups and views. This is a one time setting and is done while setting up the project on the local machine. Once set, there is no need to reset these values for each run.

## Runtime Arguments:
To make this application callable from the CLI commands, 12 execution modes have been introduced:
```
python.exe cmd.py --conf /path/to/config/conf.json --run_mode get_group --group_name gp_box_score --group_version 1
```
## Calling Modes:
This application has two execution modes:
1) It can either be called directly using the CLI commands, in that case you need to pull this Github repo and execute the **_cmd.py python_** file present in the src directory. **_To be able to run this command, make sure to switch the directory to src._**
2) It can also be called using import command by installing this library from the pypi and using it in your existing project.    

The details of both the calling modes are described below. The user can choose either one of them. 
## CLI Calling Mode:
### Explanation of the runtime arguments:

1) _--conf:_ This tells the path to the config file containing database and hopsworks credentials.
2) _--build_conf:_ This tells the path to the groups.json or views.json config file where you will define the source and destination and the schema of the feature group or view.
3) _--run_mode:_ This tells the application what type of operation to perform.
4) _--group_name:_ This is the required feature group name that is needed to be created or retrieved. 
5) _--group_version:_ This the required version of the feature group. 
6) _--view_name:_ This is the required feature view name that is needed to be created or retrieved.
7) _--view_version:_ This the required version of the feature view.
8) _--file_path:_ This is the directory path of the output files when you are exporting feature group or view to the .csv file.
9) _--file_name:_ This is the file name of the output files when you are exporting feature group or view to the .csv file. 

### Mandatory arguments: 
conf, run_mode
### Optional arguments: 
build_conf, group_name, group_version, view_name, view_version, file_path, and file_name are optional and will be used based on the operation type. For e.g. if you are running only get_group then you don't need to specify build_conf argument, but you when you are running build_group, then you need to specify build_conf argument but you don't need to specify group version in that. See the examples below for clarification.

### Example Runs:
```
1) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_group --group_name gp_game_base --group_version 1`
2) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_group_features --group_name gp_box_score --group_version 1 --features adv_idx_uuid,box_type,mp`
3) `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_db --group_name gp_game_base`
4) `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_view --group_name test_group_from_view`
5) `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_file --group_name test_group_from_file`
6) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode export_group_to_file --group_name gp_game_base --group_version 1 --file_path "/path/to/export/folder/" --file_name gp_game_base_export.csv`
7) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode drop_group --group_name gp_game_base --group_version 1`
8) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_view --view_name t1vst2 --view_version 1`
9) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_view_features --view_name t1vst2 --view_version 1  --features uuid,box_type,mp`
10) `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/views.json" --run_mode build_view --view_name t1vst2`
11) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode export_view_to_file --view_name t1vst2 --view_version 1 --file_path "/path/to/export/folder/" --file_name t1vst2_view_export.csv`
12) `python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode drop_view --view_name t1vst2 --view_version 1`
```

### Operation Types:

### get_group:  
This operation takes group name and group version as the command line arguments and returns the respective feature group handle.  
_example:_  
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_group --group_name gp_game_base --group_version 1
```  

### get_group_features:  
This operation takes group name and group version as the command line arguments and returns the respective feature dataframe.  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_group_features --group_name gp_box_score --group_version 1 --features adv_idx_uuid,box_type,mp
```  

### build_group_from_db:   
This operation builds a feature group from the DB table. To run this command, following are the steps:  
1. In the config directory, find or create the groups.json file or with any other name but it should be a json file and with a proper format as mentioned in the sample **groups.json** file.  
2. **groups.json** file contains the list of feature groups that can be created. Each feature group has its own key and the respective value tells the details like the name, version, primary key, partitions, and description of the hopsworks feature group to be made, the database table and required columns which will be used in creating that feature group. **Make sure to use the same name of the feature group in the CLI argument which is mentioned as the key in the groups.json file.**  
3. Once you have created or configured the json file for groups, you need to tell the path of this file as the command line argument using --build_conf argument while running the application.
4. Once done, you just need to open a command prompt or terminal and write the build_group_from_db command mentioning the correct path for conf.json, and groups.json files respectively. For e.g. assuming you have made the changes in the groups.json and conf.json file, and the json key name in the groups.json file is "gp_game_base", then your command should look like:  
    `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_db --group_name gp_game_base`  
__sample conf.json file path__ config/conf.json
__sample groups.json file path__ config/groups.json  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_db --group_name gp_game_base
```

### build_group_from_view:  
This operation builds a feature group from the feature view. Just like the build_group_from_db command, this command also takes required arguments from the **groups.json** file (or whichever file you have set). To run this command, following are the steps:  
1. In the config directory, find or create the groups.json file or with any other name but it should be a json file and with a proper format as mentioned in the sample **groups.json** file.  
2. **groups.json** file contains the list of feature groups that can be created. Each feature group has its own key and the respective value tells the details like the name, version, primary key, partitions, and description of the hopsworks feature group to be made, the feature view and version which will be used in creating that feature group. **Make sure to use the same name of the feature group in the CLI argument which is mentioned as the key in the groups.json file.**  
3. Once you have created or configured the json file for groups, you need to tell the path of this file as the command line argument using --build_conf argument while running the application.
4. Once both these configurations files are ready, you just need to open a command prompt or terminal and write the build_group_from_view command mentioning the correct path for conf.json, and groups.json files respectively. For e.g. assuming you have made the changes in the groups.json and conf.json file, and the json key name in the groups.json file is "test_group_from_view", then your command should look like:  
    `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_view --group_name test_group_from_view`  
__sample conf.json file path__ config/conf.json
__sample groups.json file path__ config/groups.json  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_view --group_name test_group_from_view
```

### build_group_from_file:   
This operation builds a feature group from the .csv file. Just like the build_group_from_db command, this command also takes required arguments from the **groups.json** file(or whichever file you have set). To run this command, following are the steps:  
1. In the config directory, find or create the groups.json file or with any other name but it should be a json file and with a proper format as mentioned in the sample **groups.json** file.  
2. **groups.json** file contains the list of feature groups that can be created. Each feature group has its own key and the respective value tells the details like the name, version, primary key, partitions, and description of the hopsworks feature group to be made, the feature view and version which will be used in creating that feature group. **Make sure to use the same name of the feature group in the CLI argument which is mentioned as the key in the groups.json file.**  
3. Once you have created or configured the json file for groups, you need to tell the path of this file as the command line argument using --build_conf argument while running the application.  
4. Once both these configurations files are ready, you just need to open a command prompt or terminal and write the build_group_from_view command mentioning the correct path for conf.json, and groups.json files respectively. For e.g. assuming you have made the changes in the groups.json and conf.json file, and the json key name in the groups.json file is "test_group_from_file", then your command should look like:  
    `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_file --group_name test_group_from_file`  
__sample conf.json file path__ config/conf.json
__sample groups.json file path__ config/groups.json  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/groups.json" --run_mode build_group_from_file --group_name test_group_from_file
```

### export_group_to_file:  
This operation takes group name, group version, destination directory, and file name as the command line arguments and outputs the feature group in the form of .csv file to the described destination directory.  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode export_group_to_file --group_name gp_game_base --group_version 1 --file_path "/path/to/export/folder/" --file_name gp_game_base_export.csv
```  

### drop_group:  
This operation takes group name and group version as the command line arguments and deletes the feature group from the hopsworks project.  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode drop_group --group_name gp_game_base --group_version 1
```  

### get_view:  
This operation takes view name and view version as the command line arguments and returns the respective feature view handle.  
_example:_  
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_view --view_name t1vst2 --view_version 1
```  

### get_view_features:  
This operation takes view name and view version as the command line arguments and returns the respective feature dataframe.  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode get_view_features --view_name t1vst2 --view_version 1 --features adv_idx_uuid,box_type,mp
```  

### build_view:   
This operation builds a feature view from the mentioned feature groups. To run this command, following are the steps:  
1. In the config directory, find or create the views.json file or with any other name but it should be a json file and with a proper format as mentioned in the sample **views.json** file.  
2. **views.json** file contains the list of feature views that can be created. Each feature views has its own key and the respective value tells the details like the name, version, description of the hopsworks feature view to be made, source feature groups and their required features, filters, and the joining criteria which will be used in creating that feature view. **Make sure to use the same name of the feature view in the CLI argument which is mentioned as the key in the views.json file.**  
3. Once you have created or configured the json file for views, you need to tell the path of this file as the command line argument using --build_conf argument while running the application.
4. Once done, you just need to open a command prompt or terminal and write the build_view command mentioning the correct path for conf.json, and views.json files respectively. For e.g. assuming you have made the changes in the views.json and conf.json file, and the json key name in the views.json file is "t1vst2", then your command should look like:  
    `python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/views.json" --run_mode build_view --view_name t1vst2`  
__sample conf.json file path__ config/conf.json
__sample views.json file path__ config/views.json  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --build_conf "/path/to/config/views.json" --run_mode build_view --view_name t1vst2
```

### export_view_to_file:  
This operation takes view name, view version, destination directory, and file name as the command line arguments and outputs the feature view in the form of .csv file to the described destination directory.  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode export_view_to_file --view_name t1vst2 --view_version 1 --file_path "/path/to/export/folder/" --file_name t1vst2_export.csv
```  

### drop_view:  
This operation takes view name and view version as the command line arguments and deletes the feature view from the hopsworks project.  
_example:_    
```
python.exe cmd.py --conf "/path/to/config/conf.json" --run_mode drop_view --view_name t1vst2 --view_version 1
```  

## Library Calling Mode:
The run modes, and functions are the same as described in the **_CLI Calling Mode_**. The only difference is that, in this mode you can install this project as a library in your existing python project and use like any other libraries.  
The steps to install and use this as a standalone library are:
1) Create an empty python project or open up your existing python project in which you want to use any of the 12 functions written in this project.
2) Install this library using `pip install -i https://test.pypi.org/simple/ Hopsworks-Integration-Test-Syed-Muneeb-Hussain`
3) This command will install all the required dependencies in your project.
4) Once the installation is done, the library can be used by: 
```
import src.Cmd as s

# For operations which return something like get_group, get_view, get_group_features, get_view_features
arguments = []
df = s.main(arguments)


# For operations which do not return anything like build_group_from_db, drop_group, etc.
arguments = []
df = s.main(arguments)

# arguments is a list, which is composed of all the arguments that you write in the CLI calling mode.
# For e.g.: 
# To get group features in CLI, you will write: 
# python.exe cmd.py --conf /path/to/config/conf.json --run_mode get_group_features --group_name gp_box_score --group_version 1 --features adv_idx_uuid,box_type,mp
# To get group features in Library Mode, you will write:
# import src.Cmd as s
# arguments = ["--conf","/path/to/config/conf.json","--run_mode","get_group_features","--group_name","gp_box_score","--group_version","1","--features","adv_idx_uuid,box_type,mp"]
# df = s.main(arguments)
```