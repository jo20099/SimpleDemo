import fileinput
import os
import yaml
import pytest

base_path = os.path.dirname(os.path.dirname(__file__))  # 项目根目录

comm_path = os.path.join(base_path, 'common')
conf_file_path = os.path.join(base_path, 'conf', 'conf.yml')
rep_path = os.path.join(base_path, 'report')
test_path = os.path.join(base_path, 'testcase')

def get_conf():
    # 打开yaml文件
    with open(conf_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
        file.close()
        return yaml_data

conf = get_conf()

desired_caps = {
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:appPackage": conf['app']['package_name'],
  "appium:appActivity": conf['app']['appActivity'],
  "appium:platformVersion": conf['device']['os_version'],
  "appium:deviceName": conf['device']['device_name'],
  "appium:noReset": True
}