from exceptions import ValueError

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.proxy import *
import json
import MySQLdb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

from base64 import b64encode

db_array =['union_db']

def db_connecting(db_name):
    return MySQLdb.connect("localhost", "root", "root", db_name, use_unicode=True, charset='utf8')


def get_login(cur,db_name):
    query ="select id, login, `password` from {0}.logins where source_id=1;".format(db_name)
    cur.execute(query)
    query=''
    try:
        return cur._rows[0]
    except:
        return None


def update_cookie_value(cur,db_name,login_cookie, login_id):
    query="update {0}.logins set cookie='{1}',date_cookie=NOW() where id={2};commit;".format(db_name, login_cookie, login_id)

    cur.execute(query)
    query=''


def main(db):
    db_connect = db_connecting(db)
    cur = db_connect.cursor()

    login_array = get_login(cur, db)
    cur.close()
    cur = db_connect.cursor()
    if login_array == None:
        exit()
    else:
        pass


    login_id = login_array[0]
    login_login = login_array[1]
    login_password = login_array[2]


    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.http", "77.246.159.237")
    fp.set_preference("network.proxy.http_port", int(65233))
    fp.set_preference("network.proxy.https", "77.246.159.237")
    fp.set_preference("network.proxy.https_port", int(65233))
    fp.set_preference("network.proxy.ssl", "77.246.159.237")
    fp.set_preference("network.proxy.ssl_port", int(65233))
    fp.set_preference("network.proxy.ftp", "77.246.159.237")
    fp.set_preference("network.proxy.ftp_port", int(65233))
    fp.set_preference("network.proxy.socks", "77.246.159.237")
    fp.set_preference("network.proxy.socks_port", int(65233))
    fp.set_preference("general.useragent.override",
                      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36 OPR/41.0.2353.56")



    fp.update_preferences()

    driver = webdriver.Firefox(firefox_profile=fp)

    time.sleep(1)

    alert = driver.switch_to_alert()

    alert.send_keys("restyva" + Keys.TAB + "funny123")
    #time.sleep(1)
    #driver.switch_to_alert().send_keys(Keys.RETURN)
    alert.accept()

    a = 1
    while a==1:
        try:
            driver.get("https://spb.hh.ru/account/login")
            a=2
        except ValueError:
            print ValueError.message
            time.sleep(3)


    time.sleep(3)


    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")

    username.send_keys(login_login)
    time.sleep(3)
    password.send_keys(login_password)

    driver.find_element_by_xpath('//input[@data-qa="account-login-submit"]').click()
    time.sleep(3)
    cookies_list = driver.get_cookies()
    cookies_dict = {}
    json_str = json.dumps(cookies_list)

    cur.close()
    cur = db_connect.cursor()

    update_cookie_value(cur, db, json_str, login_id)


    driver.quit()
for db in db_array:
    main(db)
print("well done")
