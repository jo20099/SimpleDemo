# coding=utf-8
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Base:
    def find_element(driver, by, value, timeout=5, poll=0.2):
        try:
            wait = WebDriverWait(driver, timeout, poll)
            el = wait.until(lambda x: x.find_element(by, value))
            if el:
                return el
            else:
                raise
        except Exception as errmsg:
            print("Cannot find element:", errmsg)
            return None


