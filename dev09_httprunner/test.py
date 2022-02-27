from httprunner.api import HttpRunner

httprun = HttpRunner()
# 传入文件绝对路径，再运行
# httprun.run(r'C:\Users\jianyingfeng\PycharmProjects\dev09\dev09_httprunner\api\login_api.yml')
# 打印日志信息
print(httprun._summary)