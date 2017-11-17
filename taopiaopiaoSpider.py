# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
import time
import pymysql
from pipeline import saveDatas

#连接数据库
db = pymysql.connect("localhost","testuser","test123","TaoPiaoPiaoDB", use_unicode=True, charset="utf8")
cursor = db.cursor()


# xpath语句
xp_more_locations = "//ul[@class='filter-select']/li[2]/a"  # 更多影院标签
xp_locations = "//ul[@class='filter-select']/li[2]/div/a"  # 所有影院标签
xp_location = "//ul[@class='filter-select']/li[2]/div/a[%d]"  # 定位影院
xp_location_current = "//ul[@class='filter-select']/li[2]/div/a[%d][@class='current']"  # 当前选中影城
xp_dates = "//ul[@class='filter-select']/li[3]/div/a"  # 所有日期标签
xp_date = "//ul[@class='filter-select']/li[3]/div/a[%d]"  # 定位日期
xp_date_current = "//ul[@class='filter-select']/li[3]/div/a[%d][@class='current']"  # 当前选中日期
xp_screenings = "//tbody/tr"  # 所有场次标签
xp_screening_time = 'table[class="hall-table"] > tbody > tr > td[class="hall-time"] > em'  # 该场次上映时间
xp_screening_type = 'table[class="hall-table"] > tbody > tr > td[class="hall-type"]'  # 该场次上映语言
xp_screening_name = 'table[class="hall-table"] > tbody > tr > td[class="hall-name"]'  # 该场次上映放映厅
xp_screening_flow = 'table[class="hall-table"] > tbody > tr > td[class="hall-flow"] > div > label'  # 该场次上映座位情况
xp_screening_price = 'table[class="hall-table"] > tbody > tr > td[class="hall-price"] > em'  # 该场次上映价格

def BoolStaleElemByXpath(driver, xp_string, index):
    try:
        return driver.find_element_by_xpath(xp_location % index).is_displayed()
    except StaleElementReferenceException:
        print("Attempting to recover from StaleElementReferenceException.bool ..............................")
        time.sleep(1)
        BoolStaleElemByXpath(driver, xp_string, index)
    except TimeoutException:
        print("Attempting to recover from TimeoutException.bool ...................................................")
        BoolStaleElemByXpath(driver, xp_string, index)

def getStaleTextByXpath(driver, wait, xp_string ,index, text_type):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xp_string % index)))
        if(text_type=='location'):
            return driver.find_element_by_xpath(xp_string % index).text
        elif(text_type=='date'):
            return driver.find_element_by_xpath(xp_string % index).text
    except StaleElementReferenceException:
        print("Attempting to recover from StaleElementReferenceException.text ....................................")
        time.sleep(1)
        getStaleTextByXpath(driver, wait, xp_string ,index, text_type)
    except TimeoutException:
        print("Attempting to recover from click on TimeoutException.text ........................................")
        getStaleTextByXpath(driver, wait, xp_string ,index, text_type)
    else:
        pass

def clickStaleElemByXpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion=0):
    try:
        if(click_type=='wait'):
            driver.find_element_by_xpath(xp_string % index).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xp_string_current % index)))
        elif(click_type=='nowait'):
            print("Attempting to click the more locations .....................................................")
            driver.find_element_by_xpath(xp_string).click()
#解决了！！！
    except StaleElementReferenceException:
        print("Attempting to recover from click on StaleElementReferenceException ............... %ds" %num_recursion)
        time.sleep(1)
        num_recursion+=1
        clickStaleElemByXpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion)
#测试过程中发现能解决TimeoutException
    except TimeoutException:
        print("Attempting to recover from click on TimeoutException ................................................")
        clickStaleElemByXpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion)
    except ElementNotVisibleException:
        driver.save_screenshot('click.png')
        print("Attempting to recover from click on ElementNotVisibleException ....................................")
        time.sleep(1)
        clickStaleElemByXpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion)
    else:
        pass

def date_click(driver, wait, index, location):

    #  打印日期
    date=getStaleTextByXpath(driver, wait, xp_date, index, text_type='date')
    print('第%d天为：' % index, date)

    clickStaleElemByXpath(driver, wait, xp_date, xp_date_current, index, click_type='wait')

    screenings = driver.find_elements_by_xpath("//tbody/tr")
    lens_screenings = len(screenings)
    print("该影院今天共有%d场放映" % lens_screenings)

    bs = BeautifulSoup(driver.page_source, "html.parser")
    screening_time = bs.select(xp_screening_time)
    screening_type = bs.select(xp_screening_type)
    screening_name = bs.select(xp_screening_name)
    screening_flow = bs.select(xp_screening_flow)
    screening_price = bs.select(xp_screening_price)
    for index, item in enumerate(screening_time):
        s=[location, date, item.get_text().strip(),
           screening_type[index].get_text().strip(),
           screening_name[index].get_text().strip(),
           screening_flow[index].get_text().strip(),
           float(screening_price[index].get_text().strip())]
        # print(index + 1, s)
        saveDatas(db, cursor, results=s)

def location_click(driver, wait, index):
    # 如果页面没有找到本轮影院按钮，点击更多影院加载

#这里应该是最后一个BUG
    if(not BoolStaleElemByXpath(driver, xp_location, index)):
#可能会出现ElementNotVisibleException
        clickStaleElemByXpath(driver, wait, xp_more_locations, xp_string_current=None, index=index, click_type='nowait')

    # 打印影院名称
    location=getStaleTextByXpath(driver, wait, xp_location, index, text_type='location')
    print('第%d个地点为：' % index, location)
    clickStaleElemByXpath(driver, wait, xp_location, xp_location_current, index, click_type='wait')
    lens_date = len(driver.find_elements_by_xpath(xp_dates))
    print('该影院总共有%d天放映' % lens_date)

    for index_date in range(1, lens_date + 1):  # 日期循环
        date_click(driver, wait, index_date, location)


def taopiaopiaoSpider(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    wait.until(EC.presence_of_all_elements_located((By.XPATH, xp_locations)))
    lens_locations = len(driver.find_elements_by_xpath(xp_locations))
    print(lens_locations)

    for index_loc in range(1, lens_locations + 1):  # 地点循环
        location_click(driver, wait, index_loc)
        print('已插入一个电影院的数据')
    driver.close()

taopiaopiaoSpider(
            "https://dianying.taobao.com/showDetail.htm?spm=a1z21.3046609.w2.4.l62kmd&showId=168600&n_s=new&source=current")

# 相比之前的语句分开写，应该避免了StaleElementReferenceException,即第二个语句时出现元素引用过久的错误，不过出现了TimeoutException
# 有意思了，这个错误是在南京第24个发生，发生了两次，所以我在网页检查了下，这个错误是因为快到电影场次时间，停止售票，而带来的标签改换
# 这个BUG还没有修正

# WebDriverException

