@echo off
set "config_path=D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\config\\conf.json"
set "group_build_conf=D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\config\\groups.json"
set "view_build_conf=D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\config\\views.json"
set "script_path=D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\cmd.py

echo:
echo ========================================================================================
echo FUNCTION 1:
echo RUNNING DROP_VIEW()
echo dropping already created view t1vst2 from hopsworks project
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "drop_view" --view_name "t1vst2" --view_version 1

echo:
echo:
echo ========================================================================================
echo FUNCTION 2:
echo RUNNING DROP_GROUP()
echo dropping already created group gp_game_base from hopsworks project
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "drop_group" --group_name "gp_game_base" --group_version 1


echo:
echo:
echo ========================================================================================
echo FUNCTION 3:
echo RUNNING BUILD_GROUP_FROM_DB()
echo creating feature group gp_game_base from db table adv_idx
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --build_conf "%group_build_conf%" --run_mode "build_group_from_db" --group_name "gp_game_base"


echo:
echo:
echo ========================================================================================
echo FUNCTION 4:
echo RUNNING BUILD_GROUP_FROM_FILE()
echo creating feature group test_group_from_file from csv file gp_box_export.csv
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --build_conf "%group_build_conf%" --run_mode "build_group_from_file" --group_name "test_group_from_file"


echo:
echo:
echo ========================================================================================
echo FUNCTION 5:
echo RUNNING GET_GROUP()
echo getting feature group gp_game_base from hopsworks project
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "get_group" --group_name "gp_game_base" --group_version 1


echo:
echo:
echo ========================================================================================
echo FUNCTION 6:
echo RUNNING GET_GROUP_FEATURES()
echo getting group features adv_idx_uuid,box_type,mp from feature group gp_box_score from hopsworks project
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "get_group_features" --group_name "gp_box_score" --group_version 1 --features adv_idx_uuid,box_type,mp


echo:
echo:
echo ========================================================================================
echo FUNCTION 7:
echo RUNNING BUILD_VIEW()
echo creating feature view t1vst2 from feature groups gp_game_base, gp_adv_stats, and gp_box_score
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --build_conf "%view_build_conf%" --run_mode "build_view" --view_name "t1vst2"


echo:
echo:
echo ========================================================================================
echo FUNCTION 8:
echo RUNNING GET_VIEW()
echo getting feature view t1vst2 from hopsworks project
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "get_view" --view_name "t1vst2" --view_version 1


echo:
echo:
echo ========================================================================================
echo FUNCTION 9:
echo RUNNING GET_VIEW_FEATURES()
echo getting view features season,league,team1,team2 from feature view t1vst2 from hopsworks project
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "get_view_features" --view_name "t1vst2" --view_version 1 --features season,league,team1,team2


echo:
echo:
echo ========================================================================================
echo FUNCTION 10:
echo RUNNING BUILD_GROUP_FROM_VIEW()
echo creating feature group test_group_from_view from feature view t1vst2
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --build_conf "%group_build_conf%" --run_mode "build_group_from_view" --group_name "test_group_from_view"


echo:
echo:
echo ========================================================================================
echo FUNCTION 11:
echo RUNNING EXPORT_GROUP_TO_FILE()
echo exporting feature group gp_game_base from hopsworks project to csv file
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "export_group_to_file" --group_name "gp_game_base" --group_version 1 --file_path "D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\files\\" --file_name "gp_game_base_export.csv"


echo:
echo:
echo ========================================================================================
echo FUNCTION 12:
echo RUNNING EXPORT_VIEW_TO_FILE()
echo exporting feature view t1vst2 from hopsworks project to csv file
echo ========================================================================================
python.exe "%script_path%" --conf "%config_path%" --run_mode "export_view_to_file" --view_name "t1vst2" --view_version 1 --file_path "D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\files\\" --file_name "t1vst2_view_export.csv"

pause
