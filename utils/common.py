import os
import json
import yaml
import logging

from httprunner.task import HttpRunner
from rest_framework.response import Response
from datetime import datetime

from testcases.models import Testcases
from envs.models import Envs
from debugtalks.models import DebugTalks
from configures.models import Configures
from reports.models import Reports

# 定义一个日志器，参数名为settings.py中定义好的日志器名称
logger = logging.getLogger('mytest')


# 1、手动建一个projects_dir目录
# 2、在projects_dir目录下建一个以时间戳命名的目录（时间戳目录）
# 3、在时间戳目录下建一个以项目名称命名的目录（项目名称目录）（创建前要判断是否已经建过了，）
# 4、在项目名称目录下建debugtalk文件
# 5、在项目名称目录下建以接口名称命名的目录（接口名称目录）
# 6、建yaml文件
# 先组装config部分（需要判断config_id是否存在，分情况组装）
def generate_testcase_file(instance: Testcases, env: Envs, testcase_dir_path: str):
    # 创建以项目名称命名的目录（目录A）
    project_name = instance.interface.project.name
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    # 先判断目录A未被创建过
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = DebugTalks.objects.get(project__name=project_name)
        # 创建debugtalk.py文件，encoding='utf-8'防止中文乱码
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as file:
            file.write(debugtalk_obj.debugtalk)
    interfaces_name = instance.interface.name
    testcase_dir_path = os.path.join(testcase_dir_path, interfaces_name)
    testcase_list = []
    if not os.path.exists(testcase_dir_path):
        # 在目录A创建以接口名称命名的目录（目录B）
        os.makedirs(testcase_dir_path)
        # 获取config_id
        config_id = eval(instance.include).get('config')
        # 获取base_url
        base_url = env.base_url if env.base_url else ''
        # 组装config_dict
        if config_id:
            config_obj = Configures.objects.get(id=config_id)
            config_dict = json.loads(config_obj.request, encoding='utf-8')
            config_dict['config']['request']['base_url'] = base_url
        else:
            config_dict = {
                'config':
                {
                    'name': interfaces_name,
                    'request': {
                        'base_url': base_url
                    }
                }
            }
    testcase_list.append(config_dict)

    testcase_id_list = eval(instance.include).get('testcases')
    # 判断testcase_id_list不为空
    if testcase_id_list:
        # 组装前置用例的request信息
        for testcase_id in testcase_id_list:
            pre_testcase_request = json.loads(Testcases.objects.get(id=testcase_id).request, encoding='utf-8')
            testcase_list.append(pre_testcase_request)
    # 组装当前用例的request信息
    this_testcase_request = json.loads(instance.request, encoding='utf-8')
    testcase_list.append(this_testcase_request)
    # 生成yaml文件
    yam_file_path = os.path.join(testcase_dir_path, instance.name + '.yaml')
    with open(yam_file_path, 'w', encoding='utf-8') as f:
        # allow_unicode=True，防止写入中文时乱码
        yaml.dump(testcase_list, f, allow_unicode=True)


# 运行yaml文件
def run(instance: Testcases, testcase_dir_path: str):
    # 创建HttpRunner对象
    hrunner = HttpRunner()
    try:
        hrunner.run(testcase_dir_path)
    except Exception as e:
        logger.error(e)
        return Response({
            'msg': '用例执行失败'
        })
    report_id = create_report(hrunner, instance)
    return Response({
        'id': report_id
    })


# 生成报告
def create_report(runner: HttpRunner, instance: Testcases):
    """
    创建测试报告
    """
    report_name = instance.name

    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                # 字节类型在json.dumps()时会报错
                # 将字节类型转为str类型
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    # 将字节类型转为str类型
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    try:
        # 上面的for循环就是为了这一步不报错
        summary = json.dumps(runner.summary, ensure_ascii=False)
    except Exception as e:
        logging.error(e)
        return Response({'msg': '用例数据转化有误'}, status=400)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id
