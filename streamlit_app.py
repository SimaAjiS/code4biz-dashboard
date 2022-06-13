import json
from time import sleep

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


sns.set(style='dark', font='Meiryo')


@st.cache
def scraping_progress_data(my_mail, my_pass, run_mode):
    service = Service(ChromeDriverManager().install())

    if run_mode == 'ブラウザ起動モード':
        # ブラウザ起動モード
        driver = webdriver.Chrome(service=service)
        # driver = webdriver.Chrome('chromedriver.exe')
    elif run_mode == 'ヘッドレスモード':
        # ヘッドレスモード
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, chrome_options=options)
        # driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

    url = 'https://school.code4biz.jp/login'
    driver.get(url)
    sleep(0.5)

    # ログインページ処理
    form = driver.find_element(by=By.CSS_SELECTOR, value='#new_member_session')
    login_mail = form.find_element(by=By.NAME, value='member[email]')
    login_passwd = form.find_element(by=By.NAME, value='member[password]')

    login_mail.clear()
    login_passwd.clear()

    login_mail.send_keys(my_mail)
    login_passwd.send_keys(my_pass)

    sleep(0.5)
    # ログインボタンを押す
    btn = form.find_element(by=By.TAG_NAME, value='button')
    btn.click()

    # ライブラリページ一覧ページへ
    courses = driver.find_elements(by=By.CLASS_NAME, value='product')

    # 学習コースリンクのリスト作成
    course_links = []
    for course in courses:
        course_link = course.find_elements(by=By.TAG_NAME, value='a')[0].get_attribute('href')
        course_links.append(course_link)

    data = []
    data_text = []
    for course_link in course_links:
        driver.get(course_link)
        sleep(0.5)

        # コースタイトルの取得
        _course_name = driver.find_element(by=By.TAG_NAME, value='h1').text
        # course_name = _course_name.split('×')[-1].replace('コース', '')
        course_name = _course_name.split('×')[-1]

        # 進捗度の取得
        progress = driver.find_element(by=By.CLASS_NAME, value='panel__heading').text

        # 文字列分割を行い、データ用意
        lesson_done = int(progress.split(' ')[0])
        lesson_total = int(progress.split(' ')[2])
        if lesson_total != 0:
            lesson_comp_rate = round(lesson_done / lesson_total * 100, 1)
        else:
            lesson_comp_rate = round(0, 1)

        # 判定式の用意
        if lesson_comp_rate == 0:
            status = 'Unstudied'
        elif lesson_comp_rate == 100:
            status = 'Complete'
        else:
            status = 'Studying'

        datum = {
            'Course name': course_name,
            'Done lessons': lesson_done,
            'Total lessons': lesson_total,
            'Progress[%]': lesson_comp_rate,
            'Status': status
        }
        data.append(datum)

        datum_text = {
            'コース名': _course_name,
            '進捗度': progress
        }
        data_text.append(datum_text)
        log_text = f'{_course_name}...Done'
        print(log_text)
    driver.quit()

    # データフレームの準備
    df = pd.DataFrame(data)
    df_text = pd.DataFrame(data_text)
    return df, df_text


# 出力レポート（バープロット）
def create_barplot_progress(df):
    fig, ax = plt.subplots()
    # plt.figure(figsize=(6, 5))
    sns.barplot(data=df, y=df['Course name'], x=df['Progress[%]'], palette='deep', hue=df['Status'], ax=ax)
    plt.grid()
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1.0))
    plt.savefig('progress_bar.png', bbox_inches='tight')
    return fig, ax


# 進捗指標の配置
def place_metrics(df):
    col1, col2, col3, col4, col5 = st.columns(5)
    for index, row in df.iterrows():
        finished_ratio = row['Progress[%]']
        remain_ratio = finished_ratio - 100
        match index % 5:
            case 0:
                with col1:
                    st.metric(label=row['Course name'],
                              value=f'{finished_ratio :.1f} %',
                              delta=f'{remain_ratio :.1f} %')
            case 1:
                with col2:
                    st.metric(label=row['Course name'],
                              value=f'{finished_ratio :.1f} %',
                              delta=f'{remain_ratio :.1f} %')
            case 2:
                with col3:
                    st.metric(label=row['Course name'],
                              value=f'{finished_ratio :.1f} %',
                              delta=f'{remain_ratio :.1f} %')
            case 3:
                with col4:
                    st.metric(label=row['Course name'],
                              value=f'{finished_ratio :.1f} %',
                              delta=f'{remain_ratio :.1f} %')
            case 4:
                with col5:
                    st.metric(label=row['Course name'],
                              value=f'{finished_ratio :.1f} %',
                              delta=f'{remain_ratio :.1f} %')


def main():
    st.set_page_config(layout="wide")  # ワイドモードで表示
    st.title('code4biz 学習進捗ダッシュボード')
    st.sidebar.write('オプション')

    st.write('1. code4bizログイン用認証ファイルをJSON形式で各自のローカル環境に保存します')
    code = '''
    {"my_mail": "ABC@123",
    "my_pass": "DEF456"}
    '''
    st.sidebar.write('JSON記載例')
    st.sidebar.code(code, language='json')

    st.write('2. ローカルに保存した認証用JSONファイルを下記へ読み込ませます')
    uploaded_file = st.file_uploader('', type=['json'])
    if uploaded_file is not None:
        auth_info = json.load(uploaded_file)
        my_mail, my_pass = auth_info.values()

        st.write('3. データ取得ボタンを押すと、進捗データのスクレイピングを開始します')
        run_mode = st.sidebar.selectbox('ブラウザ起動モードを選択する', ('ブラウザ起動モード', 'ヘッドレスモード'))
        scraping = st.empty()
        if scraping.button('データ取得'):
            scraping.write('データ取得中...')
            # 関数
            df, df_text = scraping_progress_data(my_mail, my_pass, run_mode)
            scraping.success('データ取得が完了しました')

            # 各コース毎の進捗度一覧を表とグラフで可視化
            col_left, col_right = st.columns(2)
            with col_left:
                fig, ax = create_barplot_progress(df)
                st.write('4. 各コース毎の進捗度一覧')
                st.pyplot(fig)

                with open("progress_bar.png", "rb") as f:
                    st.download_button(
                        label="Download image",
                        data=f,
                        file_name="progress_bar.png",
                        mime="image/png"
                    )
            with col_right:
                st.dataframe(df_text)

            st.write('5. 各コース毎の進捗度指標')
            place_metrics(df)


if __name__ == '__main__':
    main()
