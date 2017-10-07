from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.PhantomJS()
driver.get(
    "https://dianying.taobao.com/showDetail.htm?spm=a1z21.6646385.city.2.oLpxBI&showId=217389&n_s=new&city=310100")

lens_locations = len(driver.find_elements_by_xpath("//ul[@class='filter-select']/li[2]/div/a"))  # 统计影城数目
print(lens_locations)

for index_loc in range(1, lens_locations + 1):  # 地点循环
    if driver.find_element_by_xpath("//ul[@class='filter-select']/li[2]/a").is_displayed():
        driver.find_element_by_xpath("//ul[@class='filter-select']/li[2]/a").click()  # 点击更多按钮

    xp_location = "//ul[@class='filter-select']/li[2]/div/a[%d]" % index_loc  # 定位location的xpath语句
    print('第%d个地点为：' % index_loc, driver.find_element_by_xpath(xp_location).text)

    driver.find_element_by_xpath(xp_location).click()  # 点击该影城
    xp_location_current = "//ul[@class='filter-select']/li[2]/div/a[%d][@class='current']" % index_loc
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_location_current)))  # 等到该影城被选中

    xp_dates = "//ul[@class='filter-select']/li[3]/div/a"
    lens_date = len(driver.find_elements_by_xpath(xp_dates))
    print('该影院总共有%d天放映' % lens_date)

    for index_date in range(1, lens_date + 1):  # 日期循环
        xp_date = "//ul[@class='filter-select']/li[3]/div/a[%d]" % index_date
        print('第%d天为：' % index_date, driver.find_element_by_xpath(xp_date).text)
        driver.find_element_by_xpath(xp_date).click()

        xp_date_current = "//ul[@class='filter-select']/li[3]/div/a[%d][@class='current']" % index_date
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_date_current)))  # 等到该日期被选中

        data_times = driver.find_elements_by_xpath("//tbody/tr")
        lens_time = len(data_times)
        print("该影院今天共有%d场放映" % lens_time)
        for index_time in range(1, lens_time + 1):  # 时间循环
            data = []
            xp1 = "//tbody/tr[%d]/td[1]/em" % index_time
            xp2 = "//tbody/tr[%d]/td[2]" % index_time
            xp3 = "//tbody/tr[%d]/td[3]" % index_time
            xp4 = "//tbody/tr[%d]/td[4]/div/label" % index_time
            xp5 = "//tbody/tr[%d]/td[5]/em" % index_time
            xp6 = "//tbody/tr[%d]/td[6]/a" % index_time
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp1)))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp2)))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp3)))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp4)))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp5)))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp6)))
            data.append(driver.find_element_by_xpath(xp1).text)
            data.append(driver.find_element_by_xpath(xp2).text)
            data.append(driver.find_element_by_xpath(xp3).text)
            data.append(driver.find_element_by_xpath(xp4).text)
            data.append(driver.find_element_by_xpath(xp5).text)
            data.append(driver.find_element_by_xpath(xp6).text)
            print(data)
