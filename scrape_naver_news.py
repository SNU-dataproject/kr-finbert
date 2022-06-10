# 네이버기사에 +주가 +삼전 기간 2021.06.01 ~ 2022.02.07 설정해서 검색
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


result = []


def save_result():
    df = pd.DataFrame(result[:], columns=['date', 'title'])
    df.to_excel('./datasets/raw_naver_news.xlsx', index=False, encoding='cp949')


def get_info():
    driver = webdriver.Chrome('chromedriver')
    base_url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%2B%EC%A3%BC%EA%B0%80%20%2B%EC%82%BC%EC%A0%84&sort=1&photo=0&field=0&pd=3&ds=2017.06.01&de=2022.02.07&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from20170601to20220207,a:all'
    page_no = 0
    while 1:
        try:
            # url = base_url + f'&start={page_no}1'
            url = base_url + f'&start={page_no}1'
            driver.get(url)
            time.sleep(2)

            bxs = driver.find_element_by_xpath('//*[@id="main_pack"]/section[2]/div/div[2]/ul').find_elements_by_tag_name('li')
            print(f'--------- {page_no+1}페이지 크롤링 진행 중 ---------')
            for bx in bxs:
                date = bx.find_element_by_class_name('info_group').find_elements_by_tag_name('span')[-1].text.strip()
                title = bx.find_element_by_class_name('news_tit').get_attribute('title')
                result.append([date, title])
            page_no += 1
        except NoSuchElementException as e:
            print(e, "크롤링 마지막페이지까지 진행 완료")
            break
    driver.close()


def crawling():
    get_info()
    save_result()


if __name__ == "__main__":
    crawling()