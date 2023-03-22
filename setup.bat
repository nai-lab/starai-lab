rem 現在のフォルダへ移動
cd %~dp0

py  -3.10 -m  venv  .stlit
call .stlit\Scripts\activate.bat
py  -m  pip  install  --upgrade  pip
call pip.bat