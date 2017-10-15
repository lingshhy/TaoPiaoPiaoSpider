# -*- coding: utf-8 -*-
import time
import traceback
from taopiaopiaoSpider import taopiaopiaoSpider
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

num_success,num__nosuch,num_stale,num_time,num_others=0,0,0,0,0

for i in range(1, 101):
    try:
        start_time=time.localtime()
        print('第%d次测试于%s开始' %(i,time.strftime("%Y-%m-%d %H:%M:%S",start_time)))
        taopiaopiaoSpider(
            "https://dianying.taobao.com/showDetail.htm?spm=a1z21.6646273.w2.3.CayLtL&showId=217389&n_s=new&source=current")
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试成功" % i, file=f)
        num_success+=1
        f.close()
    except NoSuchElementException as e1:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： NoSuchElementException" % i, file=f)
        print(e1, file=f)
        traceback.print_exc(file=f)
        num__nosuch+=1
        f.close()
    except StaleElementReferenceException as e2:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： StaleElementReferenceException" % i, file=f)
        print(e2, file=f)
        traceback.print_exc(file=f)
        num_stale+=1
        f.close()
    except TimeoutException as e3:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： TimeoutException" % i, file=f)
        print(e3, file=f)
        traceback.print_exc(file=f)
        num_time+=1
        f.close()
    except Exception as e4:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： 未知错误类型" % i, file=f)
        print(e4, file=f)
        traceback.print_exc(file=f)
        num_others+=1
        f.close()
    finally:
        end_time=time.localtime()
        print('第%d次测试于%s结束\n' %(i,time.strftime("%Y-%m-%d %H:%M:%S",end_time)))
        f = open("out.txt", "a")  # 打开文件
        print('第%d次测试于%s结束\n' %(i,time.strftime("%Y-%m-%d %H:%M:%S",end_time)),file=f)
        f.close()
f = open("out.txt", "a")  # 打开文件
print('统计：共有%d次成功，\n\
        %d次 NoSuchElementException 错误，\n\
        %d次 StaleElementReferenceException 错误，\n\
        %d次 TimeoutException 错误，\n\
        %d次 其他 Exception 错误' %(num_success,num__nosuch,num_stale,num_time,num_others),file=f)
f.close()