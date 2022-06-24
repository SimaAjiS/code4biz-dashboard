# code4biz-dashboard
- 2022/06/05
  - Create
- 2022/06/14
  - 追加 chromedriver win32 103.0.5060.24
  - chromeヘッドレスモードで取得エラーのため、ブラウザ起動モードをデフォルトへ 
- 2022/06/18
  - 出力グラフタイトル部に取得日時埋め込み
- 2022/06/19
  - Streamlit Cloudデプロイ時のヘッドレスモードエラー対応模索
- 2022/06/20
  - (https://www.free-ds.com/gcf-scraping/)
    - headless-chromiumの導入
    - Add headless-chromium 86.0.4240.111-amazonlinux-2017-03
    - (https://github.com/adieuadieu/serverless-chrome/releases)
    - Chromedriverの導入
    - Add chromedriver 86.0.4240.22 linux64
    - (https://chromedriver.storage.googleapis.com/index.html?path=86.0.4240.22/)
    - Add "Flask" to requirements.txt
    - Modify code
  - 100MB超でGitHubにプッシュできず
    - $ git reset --soft HEAD^
    - (https://qiita.com/kanaya/items/ad52f25da32cb5aa19e6)
    - Git LFSのインストール（Windows）
    - $ git lfs install
    - 下記は一度やっておけば，次からは省略できる．後は普通にコミット
      - $ git lfs track {LARGE_FILE}            # {LARGE_FILE} を登録 
      - $ git add .gitattributes                # 登録済みファイルリストをadd
    - Error！
      - selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable may have wrong permissions.
      - Please see https://chromedriver.chromium.org/home
      - パーミッションエラー
      - 持ち越し
- 2022/06/21
  - 下記を参考にテストアプリ
  - (https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563/21?page=2)
  - (https://github.com/Franky1/Streamlit-Selenium)
  - サンプルコードでのデプロイ成功確認！
- 2022/06/24
  - ヘッドレスモード再対応
  - Stremlit Cloudへのデプロイやっと完了！
  - 不要ファイルの整理とDevelopブランチをmainへマージ予定
  - seaborn文字化けあり（ローカルは問題なし）