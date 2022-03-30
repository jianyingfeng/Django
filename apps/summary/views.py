from decimal import Decimal, ROUND_HALF_UP

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuites.models import Testsuites
from configures.models import Configures
from envs.models import Envs
from debugtalks.models import DebugTalks
from reports.models import Reports


class SummaryViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_summary(self, request, *args, **kwargs):
        user_boj = User.objects.get(id=request.user.id)
        total_count = 0
        success_count = 0
        for obj in Reports.objects.all():
            total_count += obj.count
            success_count += obj.success
        return Response(
            {
                'user':
                    {
                        'username': user_boj.username,
                        'role': '管理员' if user_boj.is_staff == 1 else '普通用户',
                        'date_joined': user_boj.date_joined,
                        'last_login': user_boj.last_login
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