from httprunner.api import HttpRunner

httprun = HttpRunner(save_tests=True)
# 传入文件绝对路径，再运行
httprun.run(r'C:\Users\jianyingfeng\PycharmProjects\Django\dev09_httprunner\testcases\projects_list_testcase.yml')
# 打印日志信息
print(httprun._summary)