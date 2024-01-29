# coding=utf-8
import os
import pytest
from common.comm import test_path, rep_path


if __name__ == '__main__':
  # 执行测试用例
  # pytest.main(['-s', '-v', f'{test_path}/test.py::TestAPPCase::test_setup', f'--alluredir={rep_path}'])
  # pytest.main(['-s', '-v', f'{test_path}/test.py::TestAPICase', f'--alluredir={rep_path}'])
  pytest.main(['-s', '-v', f'{test_path}/test.py', f'--alluredir={rep_path}'])
  # 生成测试报告
  os.system(f"allure serve {rep_path}")

