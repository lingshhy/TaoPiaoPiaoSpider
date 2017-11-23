# -*- coding: utf-8 -*-
import hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
import time

from mysql import TppDB


# 数据库操作
db = TppDB()
table_name = ""

# 当前爬虫结果
start = False
end = False
data_cnt = 0

# 获取结果
def get_res():
    if start == True and end == False:
        return "正在爬取数据...\n目前爬取%d条数据" % (data_cnt)
    elif start == False and end == True:
        return "爬取数据完成!!!\n成功爬取%d条数据" % (data_cnt)
    else:
        return ""

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


# 返回页面中是否显示该标签
# 标签xpath： xp_string % index
def bool_stale_element_by_xpath(driver, xp_string, index):
    try:
        return driver.find_element_by_xpath(xp_string % index).is_displayed()
    except StaleElementReferenceException:
        print("Attempting to recover from StaleElementReferenceException.bool ..............................")
        time.sleep(1)
        bool_stale_element_by_xpath(driver, xp_string, index)
    except TimeoutException:
        print("Attempting to recover from TimeoutException.bool ...................................................")
        bool_stale_element_by_xpath(driver, xp_string, index)


# 返回页面中该标签的文本
# 标签xpath： xp_string % index
def get_stale_text_by_xpath(driver, wait, xp_string, index, text_type):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xp_string % index)))
        if text_type == 'location':
            return driver.find_element_by_xpath(xp_string % index).text
        elif text_type == 'date':
            return driver.find_element_by_xpath(xp_string % index).text
    except StaleElementReferenceException:
        print("Attempting to recover from StaleElementReferenceException.text ....................................")
        time.sleep(1)
        get_stale_text_by_xpath(driver, wait, xp_string, index, text_type)
    except TimeoutException:
        print("Attempting to recover from click on TimeoutException.text ........................................")
        get_stale_text_by_xpath(driver, wait, xp_string, index, text_type)
    else:
        pass


# 点击该标签
# 标签xpath： xp_string % index
# 完成标签xpath： xp_string_current % index
# 参数click_type:
#   'wait': 等待完成标签加载
#   'nowait': 不等待
def click_stale_element_by_xpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion=0):
    try:
        if click_type == 'wait':
            driver.find_element_by_xpath(xp_string % index).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xp_string_current % index)))
        elif click_type == 'nowait':
            print("Attempting to click the more locations .....................................................")
            driver.find_element_by_xpath(xp_string).click()
    except StaleElementReferenceException:
        print("Attempting to recover from click on StaleElementReferenceException ............... %ds" % num_recursion)
        time.sleep(1)
        num_recursion += 1
        click_stale_element_by_xpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion)
    except TimeoutException:
        print("Attempting to recover from click on TimeoutException ................................................")
        click_stale_element_by_xpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion)
    except ElementNotVisibleException:
        driver.save_screenshot('click.png')
        print("Attempting to recover from click on ElementNotVisibleException ....................................")
        time.sleep(1)
        click_stale_element_by_xpath(driver, wait, xp_string, xp_string_current, index, click_type, num_recursion)
    else:
        pass


# 点击日期
# 日期标签： xp_date % index
def date_click(driver, wait, index, location):
    #  获取日期，打印
    date = get_stale_text_by_xpath(driver, wait, xp_date, index, text_type='date')
    print('第%d天为：' % index, date)

    click_stale_element_by_xpath(driver, wait, xp_date, xp_date_current, index, click_type='wait')

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
        s = [location, date, item.get_text().strip(), screening_type[index].get_text().strip(),
             screening_name[index].get_text().strip(), screening_flow[index].get_text().strip(),
             float(screening_price[index].get_text().strip())]
        global data_cnt
        data_cnt += 1
        db.save_datas(table_name, results=s)


# 点击影院
# index： 影院索引
def location_click(driver, wait, index):
    # 如果页面没有找到本轮影院按钮，点击更多影院加载
    # 可能会出现ElementNotVisibleException
    if not bool_stale_element_by_xpath(driver, xp_location, index):
        click_stale_element_by_xpath(driver, wait, xp_more_locations, xp_string_current=None, index=index,
                                     click_type='nowait')

    # 获取第index个影院的名字，打印影院名称
    location = get_stale_text_by_xpath(driver, wait, xp_location, index, text_type='location')
    print('第%d个地点为：' % index, location)
    click_stale_element_by_xpath(driver, wait, xp_location, xp_location_current, index, click_type='wait')
    lens_date = len(driver.find_elements_by_xpath(xp_dates))
    print('该影院总共有%d天放映' % lens_date)

    for index_date in range(1, lens_date + 1):  # 日期循环
        date_click(driver, wait, index_date, location)


# 获取当前正在上映的所有电影列表，并更新数据库
def get_current_movies():
    movie_page = "https://dianying.taobao.com/showList.htm?n_s=new"  # 查看正在上映电影页面
    driver = webdriver.PhantomJS()
    driver.get(movie_page)
    wait = WebDriverWait(driver, 5)

    db.connect()
    db.create_table_movies_list()

    movies_xpath = "//div[4]/div[1]/div[2]/div[1]/div"  # 正在上映电影标签
    lens_movies = len(driver.find_elements_by_xpath(movies_xpath))

    movie_list = []
    moiv_href_xpath = "/html/body/div[4]/div[1]/div[2]/div[1]/div[%d]/a[1]"  # 电影链接标签
    movie_name_xpath = "//div[4]/div[1]/div[2]/div[1]/div[%d]/a[1]/div[3]/span[1]"  # 电影名标签
    for index_movie in range(1, lens_movies + 1):
        movie_href = driver.find_element_by_xpath(moiv_href_xpath % (index_movie)).get_attribute("href")
        movie_name = driver.find_element_by_xpath(movie_name_xpath % (index_movie)).text
        m = hashlib.md5()
        m.update(movie_name.encode("utf-8"))
        table_name = "movie" + m.hexdigest()  # 数据表名为:movie+散列值
        db.update_movies_list(movie_name, table_name, movie_href)
        movie_list.append([movie_name, movie_href])

    db.commit()
    db.close()

    driver.close()
    return movie_list


# 爬取电影数据
# movie_name： 电影名
# url： 电影的具体链接
def taopiaopiao_spider(movie_name):
    global start
    global end
    global data_cnt
    start = True
    end = False
    data_cnt = 0

    db.connect()
    db.create_table_movies_list()

    res = db.get_table_href(movie_name)  # 获取数据表名
    global table_name
    table_name = res[0]
    url = res[1]

    db.create_movie_table(movie_name, table_name)
    db.commit()

    driver = webdriver.PhantomJS()
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    wait.until(EC.presence_of_all_elements_located((By.XPATH, xp_locations)))
    lens_locations = len(driver.find_elements_by_xpath(xp_locations))
    print("当前有%d个电影院上映该电影" % lens_locations)

    for index_loc in range(1, lens_locations + 1):  # 地点循环
        location_click(driver, wait, index_loc)
        print('已插入一个电影院的数据')
    driver.close()

    start = False
    end = True

    db.commit()
    db.close()

# 查找数据库中电影列表
def get_movie_table_name():
    db.connect()
    db.create_table_movies_list()
    res = db.get_movie_table_name()

    db.commit()
    db.close()
    return res

# 查找电影名对应的表名
def get_table(movie_name):
    db.connect()
    db.create_table_movies_list()
    res = db.get_table_href(movie_name)

    db.commit()
    db.close()
    return res[0]

# 查找数据
def get_data(movie_name):
    db.connect()
    table = db.get_table_href(movie_name)[0]
    return db.get_data(table)
