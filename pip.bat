rem 現在のフォルダへ移動
cd %~dp0

call .stlit\Scripts\activate.bat
py  -m  pip install -r requirements.txt
