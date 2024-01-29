# coding=utf-8
import os
import pytest
import allure
from pageobj.page import AppCase
from common.comm import get_conf, desired_caps
from appium import webdriver
import requests
import json

conf = get_conf()

driver = webdriver.Remote(conf['appium']['server'], desired_caps)

@allure.feature("Android APP testcase")
class TestAPPCase:
    # 测试执行前启动准备
    @allure.story("setup before test")
    def test_setup(self):
        # 启动app前清除应用数据，确保初始状态一致
        driver.terminate_app(conf['app']['package_name'])
        os.system("adb shell pm clear %s " % conf['app']['package_name'])
        driver.activate_app(conf['app']['package_name'])

    # 测试QQ账号登录功能
    # 入参：account, pwd, nickname
    # 两组测试数据（一组正确，一组错误），分别对应success、fail测试结果，在conf.yml中配置
    @pytest.mark.parametrize('account, pwd, nickname', \
                             [conf['app']['wrong_case'].split(', '), \
                              (conf['app']['account'], \
                               conf['app']['passwd'], \
                               conf['app']['nick_name'])])

    @allure.story("app login test")
    def test_app_login(self, account, pwd, nickname):
        self.driver = driver
        self.test_setup()
        AppCase.app_login(self, account, pwd, nickname)

    # 测试QQ账号登出功能
    @allure.story("app logout test")
    def test_app_logout(self):
        self.driver = driver
        AppCase.app_logout(self)

    @allure.story("tear down and finish test")
    def test_teardown(self):
        # 关闭应用，结束测试
        driver.terminate_app(conf['app']['package_name'])
        driver.quit()


@allure.feature("API testcase")
class TestAPICase:
    # 根据用户id查询用户接口
    # 入参：id
    # 两组测试数据（一组正确，一组错误），分别对应success、fail测试结果，在conf.yml中配置
    @allure.story("query user")
    @pytest.mark.parametrize('id', \
                             [conf['api_test']['query_api']['param']['id'], \
                              conf['api_test']['query_api']['param']['failed_id']])
    def test_api_query(self, id):
        test_conf = conf['api_test']['query_api']
        url = test_conf['host'] + test_conf['path']
        payload = {}
        headers = conf['api_test']['headers']

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        assert response.status_code == 200
        found = 0
        for usr in json.loads(response.text):
            for key in usr:
                if usr[key] == id:
                    found = 1
                    break
        assert found  # 返回的查询列表中，有正确的用户id

    # 根据post_id提交一个新comment
    # 入参：post_id
    # 两组测试数据（一组post_id存在，一组post_id不存在），分别对应success、fail测试结果
    @allure.story("commit new comment")
    @pytest.mark.parametrize('post_id', [0, 1])
    def test_api_write(self, post_id):
        test_conf = conf['api_test']['create_comments_api']
        url = test_conf['host'] + test_conf['path_query']
        payload = {}
        headers = conf['api_test']['headers']

        # 查询现有post列表第一个id
        response = requests.request("GET", url, headers=headers, data=payload)

        assert response.status_code == 200

        if 'id' in json.loads(response.text)[0] and post_id:
            post_id = json.loads(response.text)[0]['id']
        assert post_id

        url = test_conf['host'] + test_conf['path_post'].replace('%s', str(post_id)) + str(conf['api_test']['token'])
        payload = {"name": test_conf['param']['name'],
                   "email": test_conf['param']['email'],
                   "body": test_conf['param']['body']
                   }
        response = requests.post(url, headers=headers, data=payload)
        assert response.status_code in [200, 201]  # 重复提交
        if 'body' in response.json():
            assert response.json()["body"] == test_conf['param']['body']  # 评论内容查询结果和提交的一致