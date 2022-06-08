from selenium import webdriver
import pandas as pd
import time

result = ['']


def save_result():
    df = pd.DataFrame(result[1:], columns=['title', 'press', 'date', 'link'])
    df.to_excel('./datasets/naver_finance_news.xlsx', index=False, encoding='cp949')


def extract_article_info(c):
    tmp = c.find_element_by_class_name('title')
    title = tmp.text.strip()
    press = c.find_element_by_class_name('info').text.strip()
    date = c.find_element_by_class_name('date').text.strip()[:10]
    link = tmp.find_element_by_tag_name('a').get_attribute('href')

    if title in result[-1] or title == '':
        return

    result.append([title, press, date, link])


def get_info(lastPage):
    driver = webdriver.Chrome('chromedriver')
    for i in range(lastPage):
        url = f'https://finance.naver.com/item/news_news.naver?code=005930&page={i + 1}&sm=title_entity_id.basic&clusterId='
        driver.get(url)
        time.sleep(3)

        print(f'--------- {i+1}페이지 크롤링 진행 중 ---------')
        contents = driver.find_elements_by_xpath('/html/body/div/table[1]/tbody/tr')
        for con in contents:
            extract_article_info(con)


def get_last_page():
    base_url = 'https://finance.naver.com/item/news_news.naver?code=005930&page=1&sm=title_entity_id.basic&clusterId='
    driver = webdriver.Chrome('chromedriver')
    driver.get(base_url)
    time.sleep(3)

    driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr/td[12]/a').click()
    time.sleep(2)

    last_page_string = driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr')\
        .find_elements_by_tag_name('td')[-1].text.strip()
    last_page = int(last_page_string.replace(',', ''))
    driver.close()
    return last_page


def crawling():
    last_page = get_last_page()
    get_info(last_page)
    save_result()