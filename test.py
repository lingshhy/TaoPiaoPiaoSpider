from taopiaopiaoSpider import taopiaopiaoSpider
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

# taopiaopiaoSpider(
#             "https://dianying.taobao.com/showDetail.htm?spm=a1z21.3046609.w2.4.IRhyJR&showId=199280&n_s=new&source=current")

for i in range(1, 101):
    try:
        taopiaopiaoSpider(
            "https://dianying.taobao.com/showDetail.htm?spm=a1z21.3046609.w2.4.IRhyJR&showId=199280&n_s=new&source=current")
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试成功" % i, file=f)
        f.close()
    except NoSuchElementException as e1:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： NoSuchElementException" % i, file=f)
        print(e1, file=f)
        f.close()
    except StaleElementReferenceException as e2:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： StaleElementReferenceException" % i, file=f)
        print(e2, file=f)
        f.close()
    except TimeoutException as e3:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： TimeoutException" % i, file=f)
        print(e3, file=f)
        f.close()
    except Exception as e4:
        f = open("out.txt", "a")  # 打开文件
        print("第%d次测试发生错误，错误原因： 未知错误类型" % i, file=f)
        print(e4, file=f)
        f.close()
    finally:
        print('一次测试结束')
        print('----------------------------------------------------------------------------------')