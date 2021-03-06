from decimal import Decimal, ROUND_HALF_UP

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuites.models import Testsuites
from configures.models import Configures
from envs.models import Envs
from debugtalks.models import DebugTalks
from reports.models import Reports


class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        total_count = 0
        success_count = 0
        for obj in Reports.objects.all():
            total_count += obj.count
            success_count += obj.success
        return Response(
            {
                'user':
                    {
                        'username': user.username,
                        'role': '管理员' if user.is_staff == 1 else '普通用户',
                        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
                        'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else ''
                    },
                'statistics':
                    {
                        'projects_count': Projects.objects.all().count(),
                        'interfaces_count': Interfaces.objects.all().count(),
                        'testcases_count': Testcases.objects.all().count(),
                        'testsuits_count': Testsuites.objects.all().count(),
                        'configures_count': Configures.objects.all().count(),
                        'envs_count': Envs.objects.all().count(),
                        'debug_talks_count': DebugTalks.objects.all().count(),
                        'reports_count': Reports.objects.all().count(),
                        'success_rate': Decimal((success_count/total_count)*100).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP),
                        'fail_rate': 100 - Decimal((success_count/total_count)*100).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
                    }
            }
        )