# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests
import time

from pyvirtualdisplay import Display  
display = Display(visible=0, size=(800,600))  
display.start()  

info_dict = json.load(open('./info','r'))

#import os
#os.system('killall chrome')
#os.system('killall chromedriver')

#driver = webdriver.Firefox()
driver = webdriver.Chrome("/home/alitest/chromedriver")
#driver.get("https://enterpriseportal.alipay.com/login.htm")
#driver.get("https://authzui.alipay.com/login/index.htm")
#driver.get("https://authgtj.alipay.com/login/enterprise.htm")
driver.get("https://auth.alipay.com/login/enterprise.htm?redirectType=parent&goto=")
login_windows = driver.current_window_handle
driver.implicitly_wait(10) 
myDynamicElement = driver.find_element_by_id("J-input-user")
element = WebDriverWait(driver, 10,1).until(
    EC.presence_of_element_located((By.ID, "J-input-user"))
)
pe = WebDriverWait(driver, 10,1).until(
    EC.presence_of_element_located((By.ID, "password_rsainput"))
)

login_btn = WebDriverWait(driver, 10,1).until(
    EC.presence_of_element_located((By.ID, "J-login-btn"))
)
if element and pe and login_btn:
    element.send_keys(info_dict["username"])  #参数为您的支付宝帐号
    pe.click()
    pe.send_keys(info_dict["password"])   #在此输入您的支付宝密码
    time.sleep(2)
    #login_btn.send_keys(Keys.ENTER)
    login_btn.click()
    time.sleep(2)
    driver.implicitly_wait(2)
    driver.switch_to.window(driver.current_window_handle)
    #trade_link = driver.find_element_by_link_text("卖出交易")
    #trade_link.click()
    #driver.get("https://mbillexprod.alipay.com/enterprise/productDispatcher.htm?productCode=ENT_TRADE_RECORD&functCode=000|201|102")
    driver.get("https://mbillexprod.alipay.com/enterprise/productDispatcher.htm?productCode=ENT_RECONCILE_CENTER&functCode=000|101|111")
    #get the session cookie  
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]  
    cookiestr = '; '.join(item for item in cookie)  
    ctoken = ""
    jsessionid = ""
    c = dict()
    for item in driver.get_cookies():
        c[item["name"]] = item["value"]
        if item["name"] == "ctoken":
            ctoken = item["value"]
        if item["name"] == "JSESSIONID" and jsessionid == "":
            jsessionid = item["value"]
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'331',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'mbillexprod.alipay.com',
        'Origin':'https://mbillexprod.alipay.com',
        'Referer':'https://mbillexprod.alipay.com/enterprise/fundAccountDetail.htm;jsessionid=' + jsessionid,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    ten_min_ago = time.time() - 60 * 30
    now = time.time()
    start = time.strftime('%Y-%m-%d+%H', time.localtime(ten_min_ago)) + '%3A'
    if time.localtime(ten_min_ago).tm_min < 10:
        start += '0' + str(time.localtime(ten_min_ago).tm_min)
    else:
        start += str(time.localtime(ten_min_ago).tm_min)
    end = time.strftime('%Y-%m-%d+%H', time.localtime(now)) + '%3A'
    if time.localtime(now).tm_min < 10:
        end += '0' + str(time.localtime(now).tm_min)
    else:
        end += str(time.localtime(now).tm_min)
    start += '%3A00'
    end += '%3A00'
    print start
    print end

    form_data = {
        'startTime': start,
        'endTime': end,
        'startAmount': '',
        'endAmount': '',
        'targetMainAccount': '',
        'goodsTitle': '',
        'sortType': '0',
        'sortTarget': 'gmtCreate',
        'pageSize': '20',
        'pageNum': '1',
        'billUserId': '2088521166926244',
        'status': 'ALL',
        'forceAync': '0',
        'searchType': '1',
        'fromTime': '00%3A00',
        'toTime': '00%3A00',
        'tradeFrom': 'ALL',
        'tradeType': '0',
        '_input_charset': 'utf-8',
        'ctoken': ctoken}
    #data_str = "startTime=" + start + "&endTime=" + end + "&startAmount=&endAmount=&targetMainAccount=&goodsTitle=&sortType=0&sortTarget=gmtCreate&pageSize=20&pageNum=1&billUserId=2088621608234792&status=ALL&forceAync=0&searchType=1&fromTime=" + start.split("+")[1] + "&toTime=" + end.split("+")[1] + "&tradeFrom=ALL&tradeType=0&_input_charset=utf-8&ctoken=" + ctoken
    #data_str = "startTime=2017-08-19+00%3A00&endTime=2017-08-20+00%3A00&startAmount=&endAmount=&targetMainAccount=&goodsTitle=&sortType=0&sortTarget=gmtCreate&pageSize=20&pageNum=1&billUserId=2088621608234792&status=ALL&forceAync=0&searchType=1&fromTime=00%3A00&toTime=00%3A00&tradeFrom=ALL&tradeType=0&_input_charset=utf-8&ctoken=" + ctoken
    data_str = "queryEntrance=1&billUserId=2088521166926244&showType=0&type=&precisionQueryKey=tradeNo&startDateInput=" + start + "&endDateInput=" + end + "&pageSize=200&pageNum=1&total=6&sortTarget=tradeTime&order=descend&sortType=0&_input_charset=utf-8&ctoken=" + ctoken;
    #data_str = "startDateInput=" + start + "&endDateInput=" + end + "&startAmount=&endAmount=&targetMainAccount=&activeTargetSearchItem=&orderNo=&tradeNo=&sortType=0&sortTarget=tradeTime&showType=0&searchType=0&pageSize=200&pageNum=1&billUserId=2088521166926244&forceAync=0&fromTime=" + start.split("+")[1] + "&toTime=" + end.split("+")[1] + "&type=&_input_charset=utf-8&ctoken=" + ctoken
    print "before post"
    print c
    print data_str
#   r = requests.post('https://mbillexprod.alipay.com/enterprise/sellTransQuery.json', headers=headers, cookies=c, data=data_str)
    r = requests.post('https://mbillexprod.alipay.com/enterprise/fundAccountDetail.json', headers=headers, cookies=c, data=data_str, verify=False)

    deny = r.text.find('deny')
    fuck = 1
    while (deny != -1):
        print 'deny by server', fuck
        fuck = fuck+1
        if fuck == 4:
            break
        time.sleep(10)
        r = requests.post('https://mbillexprod.alipay.com/enterprise/fundAccountDetail.json', headers=headers, cookies=c, data=data_str, verify=False)
        deny = r.text.find('deny')


    print(r.text)
    print "after post"
    output = open(info_dict["output"], 'a')
    output.write(start + "============>" + end)
    output.write('\n')
    output.write(r.text)
    output.write('\n')
    output.close()

#post data to squloan
    squList = json.loads(r.text)

    if squList['result']['detail']:
        for squ in squList['result']['detail']:
            if squ['accountType'] == '转账' :
                if float(squ['tradeAmount']) > 0 :

                    tradeTime = squ['tradeTime']
                    tradeNo = squ['tradeNo']
                    transMemo = squ['transMemo']
                    tradeAmount = squ['tradeAmount']
                    otherAccountEmail = squ['otherAccountEmail']
                    otherAccountFullname = squ['otherAccountFullname']
                    
                    payload = {'tradeTime': tradeTime, 'tradeNo': tradeNo, 'transMemo' : transMemo,'tradeAmount': tradeAmount, 'otherAccountEmail':otherAccountEmail, 'otherAccountFullname':otherAccountFullname}
                    r = requests.get('http://xxxxxxxxxxxx', params=payload)
                    
                    #print tradeNo
                    #print tradeAmount
                    logInfo = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + '   ' + str(r.url) + '   ' + str(r.status_code) + '   ' + str(r.raise_for_status()) + '\n'
                    output = open(info_dict["httplog"], 'a')
                    output.write(logInfo)
                    output.close()
##end post

    driver.close()
    driver.quit()
    display.stop()
#    sys.exit(0)

    import os
    os.system('killall chrome')
    os.system('killall chromedriver')
    os.system('killall Xvfb')

