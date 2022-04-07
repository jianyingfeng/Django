from rest_framework.pagination import PageNumberPagination as __PageNumberPagination


class PageNumberPagination(__PageNumberPagination):
    # 每页默认的数据条数
    page_size = 10
    # 页码的参数名称
    page_query_param = 'page'
    # 页码参数的描述
    page_query_description = '页码'
    # 每页展示的数据条数参数名称
    page_size_query_param = 'size'
    # 每页展示的数据条数参数描述
    page_size_query_description = '每页数据条数'
    # 每页最大展示条数
    max_page_size = 20
    # 无效页码提示
    invalid_page_message = '无效页码'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page_num'] = self.page.number
        response.data['total_pages'] = self.page.paginator.num_pages
        return response
