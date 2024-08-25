@echo off
for %%i in (*.json) do D:\ProgramData\miniconda3\envs\rm\Scripts\labelme_json_to_dataset "%%i"
pause
