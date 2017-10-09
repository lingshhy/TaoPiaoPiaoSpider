# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS()
driver.get(
    "https://dianying.taobao.com/showDetail.htm?spm=a1z21.6646385.city.4.vxOHMa&showId=199280&n_s=new&source=current&city=440100")
wait=WebDriverWait(driver, 5)

#xpath语句
xp_locations="//ul[@class='filter-select']/li[2]/div/a"  #所有影院标签
xp_more_locations="//ul[@class='filter-select']/li[2]/a"  #更多影院标签

#
# def getStaleElemByXpath(xp_string):
#     try:
#         print(xp_string)
#         print(type(xp_string))
#         print(type(xp_string.encode()))
#         print(type(xp_string.encode().decode('utf-8')))
#         return driver.find_element_by_xpath((By.XPATH, xp_string))
#     except StaleElementReferenceException:
#         print("Attempting to recover from StaleElementReferenceException ...")
#         return getStaleElemByXpath(xp_string)

# 统计影城数目并输出
wait.until(EC.presence_of_all_elements_located((By.XPATH, xp_locations)))
lens_locations = len(driver.find_elements_by_xpath(xp_locations))
print(lens_locations)

for index_loc in range(1, lens_locations + 1):  # 地点循环
    xp_location = "//ul[@class='filter-select']/li[2]/div/a[%d]" % index_loc  # 定位本轮影院

    #如果页面没有找到本轮影院按钮，点击更多影院加载
    if driver.find_element_by_xpath(xp_location).is_displayed():
        #你他妈是哪里都能出现啊，而且还专挑我没有排除异常的语句出现？
        #StaleElementReferenceException：Element is no longer attached to the DOM
        #这个没办法理解...
        pass
    else:
        driver.find_element_by_xpath(xp_more_locations).click()

    #尝试打印影院名称
    try:
        location=wait.until(EC.presence_of_element_located((By.XPATH, xp_location)))
        print('第%d个地点为：' % index_loc, location.text)
    except StaleElementReferenceException as e:
            driver.save_screenshot("codingpy1.png")
#StaleElementReferenceException：Element is no longer attached to the DOM

    #尝试选中影院
    driver.find_element_by_xpath(xp_location).click()  # 点击该影城
    xp_location_current = "//ul[@class='filter-select']/li[2]/div/a[%d][@class='current']" % index_loc
    wait.until(EC.presence_of_element_located((By.XPATH, xp_location_current)))  # 等到该影城被选中

    xp_dates = "//ul[@class='filter-select']/li[3]/div/a"
    lens_date = len(driver.find_elements_by_xpath(xp_dates))
    print('该影院总共有%d天放映' % lens_date)


    for index_date in range(1, lens_date + 1):  # 日期循环
        xp_date = "//ul[@class='filter-select']/li[3]/div/a[%d]" % index_date
        try:
            date=wait.until(EC.presence_of_element_located((By.XPATH, xp_date)))
            driver.find_element_by_xpath(xp_date).click()
            print('第%d天为：' % index_date, date.text)
        except StaleElementReferenceException as e:
            driver.save_screenshot("codingpy2.png")
#StaleElementReferenceException：Element is no longer attached to the DOM
        xp_date_current = "//ul[@class='filter-select']/li[3]/div/a[%d][@class='current']" % index_date
        wait.until(EC.presence_of_element_located((By.XPATH, xp_date_current)))  # 等到该日期被选中

        data_times = driver.find_elements_by_xpath("//tbody/tr")
        lens_time = len(data_times)
        print("该影院今天共有%d场放映" % lens_time)

#相比之前的语句分开写，应该避免了StaleElementReferenceException,即第二个语句时出现元素引用过久的错误，不过出现了TimeoutException
#有意思了，这个错误是在南京第24个发生，发生了两次，所以我在网页检查了下，这个错误是因为快到电影场次时间，停止售票，而带来的标签改换
#这个BUG还没有修正
#也就是说为了，健壮性考虑，不要使用纯索引去定位标签，而是要用UI特征
#stackoverflow的一段话：In general, your XPath expression is very fragile 
#- don't rely on the layout-oriented classes like yt-uix-button-size-small or yt-uix-expander-head. 
#Instead, for instance, rely on the button text which is "Filters".
#TMD还是有StaleElementReferenceException：Element is no longer attached to the DOM
#Element not found in the cache - perhaps the page has changed since it was looked up
#WebDriverException
        # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr")))
        #只单纯依靠判断"//tbody/tr/td"会出现今天没有场次的情况，而出现TimeoutException
        
        bs = BeautifulSoup(driver.page_source, "lxml")
        data_time_1=bs.select('table[class="hall-table"] > tbody > tr > td[class="hall-time"] > em')
        data_time_2=bs.select('table[class="hall-table"] > tbody > tr > td[class="hall-type"]')
        data_time_3=bs.select('table[class="hall-table"] > tbody > tr > td[class="hall-name"]')
        data_time_4=bs.select('table[class="hall-table"] > tbody > tr > td[class="hall-flow"] > div > label')
        data_time_5=bs.select('table[class="hall-table"] > tbody > tr > td[class="hall-price"] > em')
        for index,item in enumerate(data_time_1):
            print(index+1,item.get_text().strip(),
                data_time_2[index].get_text().strip(),data_time_3[index].get_text().strip(),
                data_time_4[index].get_text().strip(),data_time_5[index].get_text().strip())