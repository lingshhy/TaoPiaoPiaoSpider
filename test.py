import time
import traceback
from taopiaopiaoSpider import taopiaopiaoSpider
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

# taopiaopiaoSpider(
#             "https://dianying.taobao.com/showDetail.htm?spm=a1z21.3046609.w2.4.IRhyJR&showId=199280&n_s=new&source=current")

for i in range(1, 101):
    try:
        start_time=time.localtime()
        print('第%d次测试于%s开始' %(i,time.strftime("%Y-%m-%d %H:%M:%S",start_time)))
        taopiaopiaoSpider(
            "https://dianying.taobao.com/showDetail.htm?spm=a1z21.3046609.w2.4.IRhyJR&showId=199280&n_s=new&source=current")
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试成功" % i, file=f)
        f.close()
    except NoSuchElementException as e1:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： NoSuchElementException" % i, file=f)
        print(e1, file=f)
        traceback.print_exc(file=f)
        f.close()
    except StaleElementReferenceException as e2:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： StaleElementReferenceException" % i, file=f)
        print(e2, file=f)
        traceback.print_exc(file=f)
        f.close()
    except TimeoutException as e3:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： TimeoutException" % i, file=f)
        print(e3, file=f)
        traceback.print_exc(file=f)
        f.close()
    except Exception as e4:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： 未知错误类型" % i, file=f)
        print(e4, file=f)
        traceback.print_exc(file=f)
        f.close()
    finally:
        end_time=time.localtime()
        print('第%d次测试于%s结束\n' %(i,time.strftime("%Y-%m-%d %H:%M:%S",end_time)))
        f = open("out.txt", "a")  # 打开文件
        print('第%d次测试于%s结束\n' %(i,time.strftime("%Y-%m-%d %H:%M:%S",end_time)),file=f)
        f.close()
        #相隔时间，程序100次后输出统计报告