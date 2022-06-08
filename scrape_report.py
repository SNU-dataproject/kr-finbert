from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd

result = []
final_result = []


def save_result():
    df = pd.DataFrame(final_result[:], columns=['date', 'title'])
    df.to_excel('./datasets/report.xlsx', index=False, encoding='cp949')


def preprocess(row):
    row = re.sub('ㅁ', "", row)
    row = re.sub(r"^\s+", "", row, flags=re.UNICODE)
    row = re.sub(r"\n", ",", row)
    return row


def get_info_from_each_page(driver):
    tr_elements = driver.find_element_by_xpath('//*[@id="grid1_body_tbody"]').find_elements_by_tag_name('tr')
    for tr in tr_elements:
        td = tr.find_elements_by_tag_name('td')
        date = td[0].text.strip()

        summary = td[2].text.strip()
        cleaned_summary = preprocess(summary)
        result.append([date, cleaned_summary])


def get_info(driver, last_page):
    i, flag = 2, 0
    k = 1
    while True:
        driver.find_element_by_xpath('//*[@id="cntsPaging01"]/ul').find_elements_by_tag_name('li')[i].click()
        time.sleep(3)
        if i == last_page:
            break
        if i == 4 and not flag:
            i, flag = 2, 1
            driver.find_element_by_xpath('//*[@id="cntsPaging01"]/ul').find_elements_by_tag_name('li')[i].click()
        print(f"--------- {k}페이지 크롤링 진행 중 ---------")
        get_info_from_each_page(driver)
        i += 1
        k += 1


def get_last_page(driver):
    # input_box에 삼성전자 입력 후 엔터
    input_box = driver.find_element_by_xpath('//*[@id="INPUT_SN2"]')
    input_box.send_keys('삼성전자')
    input_box.send_keys(Keys.RETURN)

    # 삼성전자 클릭
    driver.switch_to.frame('iframe1')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="P_isinList_0_P_group87"]').click()
    driver.switch_to.default_content()

    # 조회기간 start에 2021년6월1일 입력 후 엔터
    select_box_start = driver.find_element_by_xpath('//*[@id="sd1_inputCalendar1_input"]')
    select_box_start.click()
    select_box_start.clear()
    select_box_start.send_keys('20210601')
    select_box_start.send_keys(Keys.TAB)

    # 조회 클릭 -> 페이지 불러오는 데 시간 걸리므로 3초 정도 sleep
    submit_button = driver.find_element_by_xpath('//*[@id="group10"]')
    submit_button.click()
    time.sleep(3)

    # paging에서 >> 버튼 눌러서 마지막 페이지 번호 가져오기
    driver.find_element_by_xpath('//*[@id="cntsPaging01"]/ul').find_elements_by_tag_name('li')[-1].click()
    time.sleep(2)
    last_page = int(driver.find_element_by_xpath('//*[@id="cntsPaging01"]/ul').find_elements_by_tag_name('li')[-3].text.strip())
    driver.find_element_by_xpath('//*[@id="cntsPaging01"]/ul').find_elements_by_tag_name('li')[0].click()
    time.sleep(2)
    return last_page


def set_driver(url):
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    time.sleep(3)
    return driver


def crawling():
    url = 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01019V.xml&menuNo=16#'

    driver = set_driver(url)
    last_page = get_last_page(driver)
    get_info(driver, last_page)
    driver.close()
    
    for idx, i in enumerate(result):
        if i == ['', '']:
            continue
        final_result.append(i)
        print(idx, i)

    save_result()