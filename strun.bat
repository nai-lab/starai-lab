set py_file=app.py

rem 現在のフォルダへ移動
cd %~dp0

rem 仮想環境で実行
call .stlit\Scripts\activate.bat & streamlit run %py_file%

deactivate
pause
