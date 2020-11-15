from selenium.webdriver import Chrome, ChromeOptions
import pandas as pd

import os
import time
import sys
import logging

logging.basicConfig(level=logging.INFO)


### main処理
def main():
    """
    マイナビサイトの各ページをクローリングし会社情報を取得。
    取得したデータはcsv形式で保存
    """
    
    # driverを起動
    driver=set_driver(False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(2)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    
    try:
        search_keyword = sys.argv[1] # コマンドライン引数に指定されたものを検索キーワードに指定
    except IndexError:
        print('Usage: mynavi_sample.py SEARCH_KEYWORD', file=sys.stderr)
        exit(1)
        
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    
    Company_job_information = []
    i = 1
    while True:
        try:
            logging.info(f'現在{i}ページ目の情報を取得中')
            cassetteRecruit = driver.find_elements_by_class_name("cassetteRecruit") # 各ページの会社情報取得
            for Recruit in cassetteRecruit:
                company_name = [Recruit.find_element_by_class_name('cassetteRecruit__name').text]
                company_details = Recruit.find_elements_by_class_name('tableCondition__body')
                company_details = [detail.text for detail in company_details]
                company_url = Recruit.find_element_by_class_name('cassetteRecruit__copy')
                company_url = [company_url.find_element_by_tag_name('a').get_attribute('href')]
                Company_job_information.append(company_name + company_details + company_url)
            url = driver.find_element_by_class_name('iconFont--arrowLeft').get_attribute('href')
            driver.get(url)
            i += 1
        except:
            break
    
    # csvデータとして出力する
    df = pd.DataFrame(Company_job_information)
    df.to_csv('to_csv_out.csv')






### Chromeを起動する関数
def set_driver(headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # ChromeのWebDriverオブジェクトを作成する。環境変数内にpathが存在しているため、executable_pathの指定はいらない
    return Chrome(options=options) 




### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
