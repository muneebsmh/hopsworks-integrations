@echo off
set "config_path=D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\tests\\test_conf.json"
set "script_path=D:\\Documents\\Office Documents\\Toptal\\TSGNC\\basketball-feature-tool\\tests\\UnitTest.py"

echo:
echo ========================================================================================
echo UNIT TESTS
echo RUNNING UnitTests
echo ========================================================================================
python -m pytest -v "%script_path%"

pause
