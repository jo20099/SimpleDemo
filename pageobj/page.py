# coding=utf-8

from appium import webdriver
from selenium.webdriver.common.by import By
from common.base import Base
from common.comm import get_conf

conf = get_conf()
class AppCase:
    def app_login(self, account, pwd, nickname):
        Base.find_element(self.driver, By.XPATH, "//*[@text='同意']").click()
        Base.find_element(self.driver, By.XPATH, "//*[@text='登录']").click()

        Base.find_element(self.driver, By.XPATH, "//*[@text='QQ号登录']").click()

        e_account = Base.find_element(self.driver, By.XPATH, "//*[@content-desc='请输入QQ号码或手机号或QID或邮箱']")
        assert e_account
        e_account.click()
        e_account.clear()
        e_account.send_keys(account)

        e_pwd = Base.find_element(self.driver, By.XPATH, "//*[@content-desc='密码 安全']")
        assert e_pwd
        e_pwd.click()
        e_pwd.clear()
        e_pwd.send_keys(pwd)

        # 同意用户协议
        Base.find_element(self.driver, By.ID, "com.tencent.mobileqq:id/s8a").click()
        # 点击登录按钮
        Base.find_element(self.driver, By.ID, "com.tencent.mobileqq:id/s80").click()
        # 验证登录成功，用户账号名称正确
        e_name = Base.find_element(self.driver, By.ID, "%s:id/ymj" % conf['app']['package_name'])
        assert e_name
        if e_name:
            assert e_name.text == nickname

    def app_logout(self):
        el = Base.find_element(self.driver, By.XPATH, "//*[@content-desc='账户及设置']")
        assert el  # 注销登录前，确认当前为已登录状态
        el.click()
        Base.find_element(self.driver, By.XPATH, "//*[@content-desc='设置']").click()
        Base.find_element(self.driver, By.XPATH, "//*[@text='账号管理']").click()

        Base.find_element(self.driver, By.XPATH, "//*[@text='退出']").click()
        Base.find_element(self.driver, By.XPATH, "//*[@text='退出登录']").click()
        Base.find_element(self.driver, By.XPATH, "//*[@text='确定退出']").click()
        # 验证退出登录完成
        el = Base.find_element(self.driver, By.XPATH, "//*[@text='添加账号']")
        assert el

