### 必要な標準ライブラリをインポートする
import copy
import chardet  # 文字コードの判定
import os
import math     # nanの判定（math.isnan）
import json
import io
import zipfile

### 必要な外部ライブラリをインポートする
import streamlit as st
import streamlit.components.v1 as stc
import numpy as np
import pandas as pd


### 自作のモジュールをインポートする
import func_html_lab


def st_display_table(df: pd.DataFrame):
    """
    Streamlitでデータフレームを表示する関数
    
    Parameters
    ----------
    df : pd.DataFrame
        対象のデータフレーム

    Returns
    -------
    なし
    """

    # データフレームを表示
    st.subheader('データの確認')
    st.table(df)

    # 参考：Streamlitでdataframeを表示させる | ITブログ
    # https://kajiblo.com/streamlit-dataframe/


def view_lesson():

    ### 各種フラグなどを初期化するセクション ###
    if 'init_flg' not in st.session_state:

        st.session_state['init_flg'] = True         # 初期化(済)フラグをオンに設定
        st.session_state['list_csv'] = {}           # csvのリスト
        st.session_state['check_flg'] = False       # csv初期検査の実行済フラグ
        st.session_state['count_page'] = 0          # 表示しているページ数        
        # st.session_state['error_flg'] = False       # csv初期検査のエラーフラグ

    if st.session_state['check_flg'] == False:

        # ファイルアップローダー
        uploaded_files = st.file_uploader('CSVファイルをドラッグ＆ドロップしてください', accept_multiple_files=True, type=['csv'])

        # アップロードの有無を確認
        if uploaded_files:

            error_flg = False

            for uploaded_file in uploaded_files:

                # 文字コードの判定
                stringio = uploaded_file.getvalue()
                enc = chardet.detect(stringio)['encoding']
                # print(enc)

                # データフレームの読み込み
                df = pd.read_csv(uploaded_file, encoding=enc) 
                df.index = np.arange(1, len(df)+1)

                # データフレームをリストに変換
                list_csv = df.to_numpy().tolist()

                if uploaded_file.name in st.session_state['list_csv']:
                    # キーが存在する場合、追加する名前に連番を追加する
                    i = 1
                    while f"{uploaded_file.name}_{i}" in st.session_state['list_csv']:
                        i += 1
                    new_key = f"{uploaded_file.name}_{i}"
                    st.session_state['list_csv'][new_key] = list_csv
                else:
                    # キーが存在しない場合、そのまま追加する
                    st.session_state['list_csv'][uploaded_file.name] = list_csv

                try:
                    for idx, line in enumerate(list_csv):

                        # style列のチェック
                        styles = ['left', 'right']
                        if line[0] not in styles:
                            st.warning(f'{uploaded_file.name}{idx+1} 行目の style 列に不正な値が設定されています（left,rightのみ許可）')
                            error_flg = True

                        # character列のチェック
                        if not isinstance(line[1], str):
                            st.warning(f'{uploaded_file.name}{idx+1} 行目の character 列が入力されていません ※必須入力')
                            error_flg = True

                        # name列のチェック
                        if not isinstance(line[4], str):
                            st.warning(f'{uploaded_file.name}{idx+1} 行目の name 列が入力されていません ※必須入力')
                            error_flg = True

                        # text列のチェック
                        if not isinstance(line[5], str):
                            st.warning(f'{uploaded_file.name}{idx+1} 行目の text 列が入力されていません ※必須入力')
                            error_flg = True

                        # content列のチェック
                        if line[2] != line[2] or line[2] in ["image", "video"]:
                            # 正常な処理
                            pass
                        else:
                            # エラー処理
                            st.warning(f'{uploaded_file.name}{idx+1} 行目の content 列に不正な値が設定されています（未入力,image,videoのみ許可）')
                            error_flg = True

                        # text列のチェック
                        if isinstance(line[5], str):                        
                            for text in line[5]:
                                # print(f'{text} = {ord(text)}')
                                if ord(text) == 10:
                                    st.warning(f'{uploaded_file.name}{idx+1} 行目の text 列に改行が含まれています')
                                    error_flg = True

                except Exception as e:

                    print(f'エラー : {e}')
                    error_flg = True


                if error_flg == True:
                    st.error(f'CSVデータにエラーが見つかりました。修正して再アップロードしてください。')

                    # テーブルの表示
                    st_display_table(df)

            if error_flg == False:
                st.success(f'CSVデータが正常に読み込めました。ボタンを押してプレビュー画面に進んでください。')
                st.session_state['check_flg'] = True

                if st.button('チャットのプレビュー'):
                    pass

    else:

        # print(st.session_state['list_csv'])

        title = st.selectbox("プレビューするCSVファイルを選択してください", st.session_state['list_csv'].keys())
        list_csv = st.session_state['list_csv'][title]

        page = st.slider('表示するページを指定してください（スライダーにフォーカスを当てた後は、カーソルキーで移動できます）', min_value=1, max_value=len(list_csv))
        idx = page -1

        text_html = func_html_lab.make_html_balloon(str(list_csv[idx][1]), func_html_lab.trans_html_tag(str(list_csv[idx][5])))
        stc.html(text_html, height=200)
        st.write(f'【話者】 {list_csv[idx][4]}')

        st.radio('【選択肢】', [list_csv[idx][6], list_csv[idx][7], list_csv[idx][8]])

        st.write('')
        st.write('【csvファイル詳細】')
        st.write(list_csv[idx])


        # for idx, line in enumerate(list_csv):
        #     pass

        st.sidebar.caption('機能')
        col = st.sidebar.columns([7,3])

        if col[0].button('別なCSVを読込みなおす'):
            del st.session_state['init_flg']    # セッションステートの削除
            st.sidebar.info('デバッガを初期化しました。《再読込》ボタンをクリックしてください。')
            uploaded_file = None
            col[1].button('再読込')

        # export_file_name = st.sidebar.text_input('JSONファイル名', placeholder='例： it01-01-c1 、 it01-01-c2 など')
        export_button = st.sidebar.button('CSVファイルをJSON形式に変換する')

        if export_button:
            # if not export_file_name:
            #     st.sidebar.warning('JSONファイル')
            json_list = {}

            for file_name, file in st.session_state['list_csv'].items():

                dict_json = {}
                dict_json['scene'] = file_name.split(".")[0]
                dict_json['datas'] = []

                num_id = 0

                for idx, line in enumerate(file):
                    num_id += 1

                    dict_temp = {'id': num_id}

                    keys = ['style', 'character', 'content', 'content_path', 'name', 'text', 'res1', 'res2', 'res3', 'next1', 'next2', 'next3']
                    dict_temp.update({keys[i]: str(line[i]) for i in range(len(keys))})

                    keys_to_check = ['content', 'content_path', 'name', 'text']

                    for key in keys_to_check:
                        if dict_temp[key] == 'nan':
                            dict_temp[key] = ''


                    keys_to_check = ['res1', 'res2', 'res3']

                    for key in keys_to_check:
                        if dict_temp.get(key) == 'nan':
                            del dict_temp[key]


                    keys_to_check = ['next1', 'next2', 'next3']

                    for key in keys_to_check:
                        if dict_temp.get(key) == 'nan':
                            del dict_temp[key]
                        else:
                            dict_temp[key] = str(int(float(dict_temp[key])) + num_id)

                    dict_json['datas'].append(dict_temp)

                # json_path = './temp/' + str(export_file_name) + '.json'
                # json_file = open(json_path, mode='w', encoding='utf-8')
                # json.dump(dict_json, json_file, indent=4, ensure_ascii=False)
                # json_file.close()

                json_string = json.dumps(dict_json, indent=4, ensure_ascii=False)
                json_list[file_name] = json_string

                print('json_string\n\n')
                print(json_string)


            if len(json_list) == 1:
                st.sidebar.download_button(
                    label="JSONファイルをダウンロードする",
                    file_name=file_name.split(".")[0] + '.json',
                    mime="application/json",
                    data=json_string,
                )
            else:
                # ファイルをBytesIOに追加
                zip_bytes_io = io.BytesIO()
                with zipfile.ZipFile(zip_bytes_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
                    for file_name, json_string in json_list.items():
                        zip_file.writestr(file_name.split(".")[0] + '.json', json_string)

                # ダウンロードボタン
                st.sidebar.download_button(
                    label="ZIPファイルをダウンロードする",
                    file_name="json_files.zip",
                    mime="application/zip",
                    data=zip_bytes_io.getvalue(),
                )