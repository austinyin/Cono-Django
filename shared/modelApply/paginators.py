from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

class DjangoPaginator(Paginator):
    def _check_object_list_is_ordered(self):
        """
        Warn if self.object_list is unordered (typically a QuerySet).
        Pagination may yield inconsistent results with an unordered
        """
        pass
class StandardResultSetPagination(PageNumberPagination):
    django_paginator_class = Paginator

    #默认每页显示的条数
    page_size = 10
    #url 中传入的显示数据条数的参数
    page_size_query_param = 'page_size'

    # 最大每页显示条数