# 必要なライブラリをインポートする
import streamlit as st
import streamlit.components.v1 as stc

from PIL import Image

# lessonファイルをインポートする
import chat_debugger


def main():

    # タブに表示されるページ名の変更
    st.set_page_config(page_title="STAR AI Lab")
    # Streamlit入門 – テーマの変更, ページの設定 | 楽しみながら理解するAI・機械学習入門
    # https://data-analytics.fun/2022/07/10/streamlit-theme-page-settings/

    img = Image.open('./assets/image/logo_01.png')
    # st.image(img, caption='', use_column_width=True)
    st.sidebar.image(img)

    # レッスン名の一覧
    chapters = [
                "開発者ツール",
                "検証者ツール",
    ]

    chapter_name = st.sidebar.selectbox("章を選択してください",(chapters))

    activitys = []

    if chapters.index(chapter_name) == 0:
        activitys = [
                    "チャットCSVデバッガ",
        ]

        activity_name = st.sidebar.selectbox("アクティビティを選択してください",(activitys))

        if activitys.index(activity_name) == 0:
            chat_debugger.view_lesson()

    if chapters.index(chapter_name) == 1:
        activitys = [
                    "ツールは存在しません",
        ]

        activity_name = st.sidebar.selectbox("アクティビティを選択してください",(activitys))

        if activitys.index(activity_name) == 0:
            pass

# デプロイ時に必要になるmain関数
if __name__ == "__main__":
    main()
